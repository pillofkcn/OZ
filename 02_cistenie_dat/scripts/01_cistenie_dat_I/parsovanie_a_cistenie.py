# ==========================================================
# CV1 - Uloha 05: Parsovanie a zakladne cistenie Apache logu
# ==========================================================
#
# CIEL:
#   Surovy log webserveru ma cca 257000 riadkov, vacsina je "smetie"
#   (obrazky, chybove odpovede, technicke pozadie). Z tohto skriptu
#   vyjde tabulka, ktora obsahuje len skutocne navstevy stranok
#   pouzivatelom. To pouzijeme v dalsich ulohach (sedenia, vzory).
#
# TEORIA pre laika:
#   - WUM = Web Usage Mining = hladanie vzorov v spravani pouzivatelov
#     na webe (napr. "ak otvoril A, casto otvori aj B").
#   - Apache log = textovy subor, kam si webserver zapisuje kazdy
#     request (kto, kedy, co chcel, ci to dostal).
#   - Jeden riadok logu vyzera takto:
#       193.87.12.30 - - [19/Feb/2020:06:25:50 +0100] "GET / HTTP/1.1" 200 20925 "-" "Mozilla/5.0"
#     Po lavej strane je IP (adresa pocitaca), v zatvorkach datum,
#     v uvodzovkach metoda + adresa stranky, potom kod odpovede atd.
#   - Niektore polia (Cookie, user, Bytes) podla zadania zahadzujeme,
#     nie su uzitocne pre nase ulohy.
#
# CO ROBIME (v skratke):
#   1) Kazdy riadok rozlozime na stlpce (regex = sablona na hladanie textu).
#   2) Vyhodime POST/HEAD requesty (nie su to navstevy stranok).
#   3) Vyhodime chybove kody (4xx, 5xx) - user stranku nevidel.
#   4) Vyhodime obrazky, CSS, JS - to nie su stranky, len ich vyzdoba.
#   5) Ulozime cistu tabulku do CSV.
#
# VSTUP:  in/Log_jeden_den.log  - surovy log za jeden den
# VYSTUP: out/05_cleaned_log.csv - tabulka so stlpcami
#         IP, DateTime, RequestMethod, URL, StatusCode, Referrer, Agent
#
# POUZITE KNIZNICE:
#   - re      : praca s regularnymi vyrazmi (sablony na hladanie textu)
#   - pandas  : tabulkove data + jednoduche filtrovanie a export do CSV

import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))  # umoznuje spustenie skriptu odkialkolvek (nielen z jeho priecinka)

import re
import pandas as pd

# === KROK 1: Sablona na rozlozenie jedneho riadku logu ===
#
# Regex = sablona, kde () = "toto si zapamataj" (zachytena skupina).
# Casti, ktore nepotrebujeme (Cookie, user), len preskocime.
# Cislovanie skupin zlava: 1=IP, 2=DateTime, 3=Method, 4=URL,
# 5=Status, 6=Bytes (zahodime), 7=Referrer, 8=Agent.
pattern = re.compile(
    r'^(\S+)\s+\S+\s+\S+\s+'           # IP + preskocime Cookie a user (su tam "-")
    r'\[([^\]]+)\]\s+'                 # datum v hranatych zatvorkach
    r'"(\S+)\s+(\S+)\s*\S*"\s+'        # metoda (GET/POST...) + URL + verzia HTTP
    r'(\d{3})\s+'                      # kod odpovede (3 cifry, napr. 200, 404)
    r'(\S+)\s+'                        # pocet bajtov - chytime ale neulozime
    r'"([^"]*)"\s+'                    # Referrer = z akej stranky user prisiel
    r'"([^"]*)"'                       # Agent = nazov prehliadaca/bota
)

# === KROK 2: Precitame log riadok po riadku a kazdy rozlozime ===
#
# Citame po riadkoch (nie cely subor naraz) - log moze byt velky
# a takto sa nezaplni pamat. errors="replace" = ked narazime na
# pokazeny znak, nahradime ho otaznikom miesto padu skriptu.
rows = []
with open("in/Log_jeden_den.log", encoding="utf-8", errors="replace") as f:
    for line in f:
        m = pattern.match(line)        # skusime na zaciatok riadku priklepnut sablonu
        if m:                          # ak sedi, vytiahneme hodnoty zo skupin
            rows.append({
                "IP": m.group(1),                 # adresa pocitaca, z ktoreho prisla navsteva
                "DateTime": m.group(2),           # datum a cas ako text (rozparzujeme neskor)
                "RequestMethod": m.group(3),      # GET/POST/HEAD - filtrujeme v kroku 3
                "URL": m.group(4),                # adresa stranky/zdroja
                "StatusCode": int(m.group(5)),    # prevedieme na cislo, lebo budeme porovnavat rozsahy
                "Referrer": m.group(7),           # preskocime skupinu 6 (Bytes) - zadanie ich kaze zmazat
                "Agent": m.group(8),              # text identifikujuci prehliadac alebo bota
            })

df = pd.DataFrame(rows)                # zo zoznamu slovnikov sprasime tabulku (DataFrame)
print(f"Parsed: {len(df)} riadkov")

# === KROK 3: Necham len GET requesty ===
#
# HTTP metoda hovori, co user chcel:
#   GET    = "daj mi tuto stranku" - TOTO je navsteva
#   POST   = "tu mas data" (odoslany formular) - nie je to otvorenie stranky
#   HEAD   = "len mi povedz, ci stranka existuje" - technicke, nie clovek
# Pre nas (vzory navstev) ma zmysel iba GET.
df = df[df["RequestMethod"] == "GET"]  # nechame len riadky kde metoda je GET
print(f"Po odstraneni POST/HEAD: {len(df)}")

# === KROK 4: Necham len uspesne odpovede (kody 200-399) ===
#
# Kod odpovede hovori, ako request dopadol:
#   2xx (200-299) = vsetko OK, stranka sa zobrazila
#   3xx (300-399) = presmerovanie, user nakoniec dostal odpoved
#   4xx (400-499) = chyba na strane usera (napr. 404 = stranka neexistuje)
#   5xx (500-599) = chyba na strane servera (server padol)
# Stranku user "videl" len pri 2xx a 3xx, ostatne zahodime.
df = df[df["StatusCode"].between(200, 399)]   # between zahrna oba konce (200 aj 399)
print(f"Po odstraneni 1xx/4xx/5xx: {len(df)}")

# === KROK 5: Vyhodime obrazky, CSS, JS a podobne stahovanie ===
#
# Ked user otvori jednu stranku, prehliadac automaticky stiahne
# aj 10-100 dalsich suborov (obrazky, styly, fonty). V logu su to
# samostatne GET requesty, ale user ich vedome "nenavstivil".
# Pre nas su to len smeti - vyhodime ich podla pripony v URL.
#
# Sablona dole hovori: "URL koncia na .jpg, .png, .css, .js..."
# (?:\?|$) = za priponou musi byt bud otaznik (parametre URL)
# alebo koniec URL - inak by sme nechtiac matchli aj veci ako
# "/clanok.cssicky/index" (nahodne pismena).
unwanted_ext = re.compile(
    r'\.(?:bmp|jpe?g|png|gif|css|flv|ico|swf|rss|xml|cur|js|json|svg|woff2?|eot|ttf|otf)(?:\?|$)',
    re.IGNORECASE
)
# str.contains pre kazdy riadok zisti, ci v URL je pripona zo zoznamu.
# Vlnovka ~ obrati True/False - nechame len tie, kde pripona NIE je.
df = df[~df["URL"].str.contains(unwanted_ext)]
print(f"Po odstraneni statickych suborov: {len(df)}")

# === KROK 6: Zoradime riadky a ulozime do CSV ===
#
# Po filtroch mame "diery" v cislovani riadkov (0, 2, 5, 8...).
# reset_index ich precisluje pekne od nuly.
df = df.reset_index(drop=True)
print(f"\nFinal: {len(df)} riadkov")     # zadanie ocakava cca 56500, dostavame ~57650 (ok)
# index=False = neukladaj cisla riadkov ako zvlastny stlpec
df.to_csv("out/05_cleaned_log.csv", index=False)
