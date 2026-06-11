# ==========================================================
# PROJEKT - Uloha 01: Cistenie zaznamov (parsovanie + filtre)
# ==========================================================
#
# CIEL:
#   Prvy krok celej analyzy. Zo suroveho textoveho logu (zaznam co sa dialo na webe)
#   spravime peknu tabulku v CSV. Tato tabulka pojde do dalsich skriptov, ktore z nej
#   odvodia napr. pouzivatelov, ich sedenia a co kde klikali.
#
# TEORIA (vysvetlene polopate):
#   - Web server (Apache) si zapisuje kazdy klik na stranku do textoveho suboru
#     zvaneho "log". Jeden riadok = jedno otvorenie nejakej adresy.
#   - Riadok ma fixny format: IP adresa pocitaca, datum, metoda (GET = pozriet stranku,
#     POST = poslat formular), adresa stranky, kod odpovede (200 = OK, 404 = nenajdene),
#     odkial pouzivatel prisiel (Referrer) a co za prehliadac pouziva (Agent).
#   - Z logu nepotrebujeme uplne vsetko. Hlavne nas zaujimaju realne navstevy stranok
#     ludmi. Preto zahodime:
#       1) ine metody ako GET (POST je odoslanie formulara, nie navsteva)
#       2) chybove kody (4xx = chyba klienta, 5xx = chyba servera => stranka sa
#          v skutocnosti nezobrazila)
#       3) staticke subory (obrazky, CSS styly, JavaScript) - tie sa stahuju
#          automaticky spolu so strankou, pouzivatel na ne nekliknul
#
# VSTUP:
#   in/wm2020projekt_studeny.log
#     - velky textovy subor (cca 910-tisic riadkov, stovky MB)
#     - kazdy riadok = jeden poziadavkový zapis web servera
#
# VYSTUP:
#   out/01_cleaned_log.csv
#     - tabulka so 7 stlpcami: IP, DateTime, RequestMethod, URL, StatusCode, Referrer, Agent
#     - DateTime ostava ako text (na cislo sa prevedie az v dalsom kroku)
#     - po cisteni zostane cca 211-tisic riadkov
#
# POUZITE KNIZNICE:
#   - re: praca s regularnymi vyrazmi (vzory na hladanie v texte). Apache log ma
#         kuskoch s medzerami v uvodzovkach, takze obycajny split podla medzery
#         by ho rozbil. Regex to zvladne spravne.
#   - pandas: praca s tabulkami a ulozenie do CSV.
#
# ALGORITMUS (v 1 vete):
#   Cita log po riadkoch, kazdy rozparsuje regexom na 8 casti, zahodi nezelane
#   zaznamy a zvysok ulozi do CSV.
# ==========================================================

import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))  # umoznuje spustenie skriptu odkialkolvek (nielen z jeho priecinka)

import re                # vzory na hladanie a rozparsovanie textu
import pandas as pd      # tabulky a zapis CSV


# === KROK 1: Vzor (regex) na rozparsovanie jedneho riadku logu ===
#
# Riadok v logu vyzera takto (priklad):
#   193.87.12.30 - - [17/Dec/2017:06:28:17 +0100] "GET / HTTP/1.1" 200 12345 "-" "Mozilla/..."
#
# Vzor nizsie ma 8 zatvoriek (...) = 8 casti, ktore z riadku vytiahneme.
# Casti, ktore nepotrebujeme (dve pomlcky za IP), len preskocime.
pattern = re.compile(
    r'^(\S+)\s+\S+\s+\S+\s+'           # 1. IP adresa (prva nemedzerova cast)
    r'\[([^\]]+)\]\s+'                 # 2. datum a cas v hranatych zatvorkach
    r'"(\S+)\s+(\S+)\s*\S*"\s+'        # 3. metoda (GET/POST), 4. adresa stranky
    r'(\d{3})\s+'                      # 5. kod odpovede (presne 3 cislice, napr. 200)
    r'(\S+)\s+'                        # 6. pocet bajtov (nepouzivame, len preskocime)
    r'"([^"]*)"\s+'                    # 7. Referrer = odkial pouzivatel prisiel
    r'"([^"]*)"'                       # 8. Agent = jeho prehliadac
)


# === KROK 2: Vzor na pripony statickych suborov ===
#
# Ked otvorime webovu stranku, prehliadac sam od seba stiahne aj jej obrazky, CSS
# styly, ikony a pisma. Tieto stiahnutia su v logu, ale pouzivatel na ne nekliknul.
# Pre analyzu spravania ich potrebujeme vyhodit, inak by skreslovali, kde ludia chodili.
#
# Tento vzor zachyti URL koncace na typicke staticke pripony (.jpg, .css, .js, ...).
unwanted_ext = re.compile(
    r'\.(?:bmp|jpe?g|png|gif|css|flv|ico|swf|rss|xml|cur|js|json|svg|woff2?|eot|ttf|otf)(?:\?|$)',
    re.IGNORECASE     # aby bolo jedno ci je pripona malymi alebo velkymi pismenami
)


# === KROK 3: Citanie logu po riadkoch a filtrovanie ===
#
# Cely subor naraz nenacitavame (mal by stovky MB). Citame ho po riadkoch, co je
# pamatovo setrne (v pamati drzime vzdy len jeden riadok).
rows = []        # sem si odkladame zaznamy, ktore presli filtrami
total = 0        # pocitadlo precitanych riadkov (kvoli statistike)

# encoding="utf-8" lebo adresy mozu mat diakritiku.
# errors="replace" = ked sa narazi na poskodeny znak, nahradi sa otaznikom
# (radsej preskocime kus textu nez aby skript spadol).
with open("in/wm2020projekt_studeny.log", encoding="utf-8", errors="replace") as f:
    for line in f:
        total += 1

        # Kazdych 100-tisic riadkov vypiseme stav, aby bolo vidno ze skript bezi.
        if total % 100000 == 0:
            print(f"  ... spracovanych {total:,} riadkov, ponechane {len(rows):,}")

        # Skusime na riadok aplikovat vzor. Ak sa nepodari (atypicky/poskodeny riadok),
        # vrati None a riadok preskocime.
        m = pattern.match(line)
        if not m:
            continue

        # Vytiahneme len to, co potrebujeme na filtre. Ostatne az pri zapise.
        method = m.group(3)              # napr. "GET" alebo "POST"
        url = m.group(4)                 # napr. "/index.html"
        status = int(m.group(5))         # kod odpovede ako cislo, aby sme mohli porovnavat

        # --- Filter 1: nechavame len GET ---
        # GET = pouzivatel si zobrazil stranku.
        # POST = poslal formular (data), HEAD/OPTIONS/PUT/DELETE = technicke operacie.
        # Pre analyzu spravania nas zaujimaju len skutocne navstevy = GET.
        if method != "GET":
            continue

        # --- Filter 2: nechavame len uspesne odpovede (kody 200-399) ---
        # 2xx = stranka sa uspesne zobrazila.
        # 3xx = presmerovanie (typicky tiez OK, pouzivatel sa dostal kam chcel).
        # 4xx = chyba klienta (404 = stranka neexistuje) - pouzivatel nic neuvidel.
        # 5xx = chyba servera - tiez nic neuvidel.
        if not (200 <= status <= 399):
            continue

        # --- Filter 3: zahadzujeme staticke subory (obrazky, CSS, JS...) ---
        # Ak adresa konci na priponu zo zoznamu, nie je to klik pouzivatela,
        # ale automaticke nacitanie prehliadacom.
        if unwanted_ext.search(url):
            continue

        # === KROK 4: Riadok presiel vsetkymi 3 filtrami - ulozime ho ===
        #
        # Vytvorime slovnik so 7 polickami = 7 buducich stlpcov tabulky.
        rows.append({
            "IP": m.group(1),                # IP adresa pocitaca pouzivatela
            "DateTime": m.group(2),          # datum a cas (zatial ako text)
            "RequestMethod": method,         # vzdy "GET" (po filtri vyssie)
            "URL": url,                      # adresa zobrazenej stranky
            "StatusCode": status,            # kod odpovede (200-399)
            "Referrer": m.group(7),          # odkial pouzivatel prisiel (alebo "-")
            "Agent": m.group(8),             # nazov prehliadaca
        })

# Vypis kolko sme precitali a kolko ostalo. {:,} prida oddelovac tisicov.
print(f"\nCelkom precitanych: {total:,}")
print(f"Po parsovani + cisteni: {len(rows):,}")


# === KROK 5: Prevod zoznamu slovnikov na tabulku a ulozenie do CSV ===
#
# Z kazdeho slovnika sa stane jeden riadok tabulky, kluce slovnika su nazvy stlpcov.
df = pd.DataFrame(rows)

# index=False = nepridavaj na zaciatok cisla riadkov (0, 1, 2, ...), nepotrebujeme ich.
df.to_csv("out/01_cleaned_log.csv", index=False)
print(f"Ulozene -> out/01_cleaned_log.csv")
