# ==========================================================
# CV1 - Uloha 06: Cistenie dat II - Hlbsie cistenie logu
# ==========================================================
#
# CIEL: Druhe kolo cistenia zaznamov z webovej stranky (Apache log).
#       Prve kolo (uloha 05) zahodilo obrazky, CSS a chybove stavy.
#       Tu pokracujeme: vyhodime robotov, duplicitne kliky, interne
#       URL a presmerovania. Cielom je dostat sa na ~31500 riadkov,
#       ktore reprezentuju skutocne navstevy ludi.
#
# TEORIA (jednoducho):
#   - WUM = Web Usage Mining = hladanie vzorcov v spravani navstevnikov.
#   - Aby vysledky neboli skreslene, treba zahodit "neludske" pristupy:
#       * Robot/bot = automat (napr. Google), ktory chodi po stranke sam.
#         Pozname ho podla "User-Agent" retazca, kde sa sam priznava
#         (obsahuje slovo "bot", "crawler", "spider"...).
#       * robots.txt = subor, ktory citaju len roboty (hovori im, kam
#         smu/nesmu). Clovek ho v prehliadaci nikdy neotvori.
#       * Duplikat = ten isty klik zapisany dvakrat (napr. dvojklik,
#         alebo refresh F5 v tej istej sekunde).
#       * Interne URL (obrazok v galerii, PDF, RSS feed, /component/)
#         = nie su to "stranky", ktore by clovek vedome navstevoval.
#       * HTTP stav 2xx = stranka sa naozaj zobrazila. 3xx = presmerovanie
#         (clovek tam nebol, server ho posiela inam). 4xx/5xx = chyba.
#
# POZN. k detekcii robotov (podla Munka):
#   Munk uvadza 4 metody detekcie robotov: (1) podla User-Agent retazca,
#   (2) podla zoznamu znamych IP, (3) podla pristupu k robots.txt, (4) podla
#   pristupu k skrytemu odkazu (nezviditelnenemu linku, ktory clovek v
#   prehliadaci nevidi). My pouzivame UA + robots.txt - najspolahlivejsie
#   pre nas log; IP zoznam by sme potrebovali externy, skryty odkaz by sa
#   musel na webe predtym nasadit.
#
# VSTUP : in/01_cleaned_log.csv   (~57000 riadkov, vystup z ulohy 05)
# VYSTUP: out/02_cleaned_log.csv  (~31500 riadkov, vstup pre cv2)
#
# POUZITE KNIZNICE:
#   - pandas: praca s tabulkou (filtre, mazanie duplikatov, ukladanie CSV).
#   - re: regularne vyrazy = vzory na hladanie textu (napr. "obsahuje bot").
#
# ALGORITMUS: postupne aplikujeme 5 filtrov a vysledok ulozime do CSV.

import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))  # umoznuje spustenie skriptu odkialkolvek (nielen z jeho priecinka)

import re
import pandas as pd

# === KROK 0: Nacitanie vstupu ===
df = pd.read_csv("in/01_cleaned_log.csv")  # nacitame log z prveho kola cistenia
print(f"Nacitane: {len(df)} riadkov")      # kontrola, ci sme nacitali ocakavany pocet

# === KROK 1: Vyhodenie robotov podla User-Agent ===
# Vzor hlada klucove slova typicke pre roboty. Robot sa nimi sam priznava
# v hlavicke "User-Agent" (napr. "Googlebot/2.1"). re.IGNORECASE = nezalezi
# na velkych/malych pismenach (bot = Bot = BOT).
bot_pattern = re.compile(
    r'bot|crawl|spider|slurp|archiver|curl|wget|libwww|perl|ltx71|facebook',
    re.IGNORECASE
)
# Ponechame riadky, kde Agent NEOBSAHUJE ziadne slovo robota.
# Znak ~ otaca pravdivost (z "obsahuje" sa stane "neobsahuje").
# na=False = ak je Agent prazdny, neberieme ho ako zhodu.
df = df[~df["Agent"].str.contains(bot_pattern, na=False)]
print(f"Po odstraneni botov: {len(df)}")

# === KROK 2: Vyhodenie pristupov k robots.txt ===
# Tento subor citaju iba roboty. Aj keby sa nejaky robot zamaskoval v kroku 1,
# tu ho chytime podla URL. V regexe znamena bodka "lubovolny znak", preto
# pisem \. aby som hladal naozaj bodku.
df = df[~df["URL"].str.contains(r'robots\.txt', case=False, na=False)]
print(f"Po odstraneni robots.txt: {len(df)}")

# === KROK 3: Vyhodenie duplicitnych klikov ===
# Ak ma viacero riadkov rovnake IP, cas aj URL, je to skoro iste dvojklik
# alebo refresh. Pre analyzu nas zaujima len jeden taky klik.
# subset = ktore stlpce porovnavame; prvy vyskyt ostane, dalsie sa zmazu.
df = df.drop_duplicates(subset=["IP", "DateTime", "URL"])
print(f"Po odstraneni duplicit: {len(df)}")

# === KROK 4: Vyhodenie nepotrebnych URL ===
# Zaujimaju nas len skutocne stranky, ktore clovek navstivil.
# Nahlad obrazka v galerii (Joomla "image?view=image") nie je navsteva stranky.
df = df[~df["URL"].str.contains(r'image\?view=image', case=False, na=False)]
# PDF stahovanie nie je preklikanie na stranku (\. = doslovna bodka).
df = df[~df["URL"].str.contains(r'\.pdf', case=False, na=False)]
# /component/ = interne cesty Joomla CMS (prihlasovanie, handlery), nie obsah.
df = df[~df["URL"].str.contains(r'/component/', case=False, na=False)]
# RSS/Atom feedy si stahuju citacky na pozadi, clovek ich v prehliadaci necita.
df = df[~df["URL"].str.contains(r'format=feed|/feed', case=False, na=False)]
print(f"Po odstraneni obrazkov/PDF/komponentov/feedov: {len(df)}")

# === KROK 5: Ponechat len uspesne zobrazenia (HTTP 2xx) ===
# 2xx = stranka sa naozaj zobrazila. 3xx (presmerovanie) by sa nam zapocitalo
# dvakrat (raz presmerovanie, raz cielova stranka). 4xx/5xx = chyba, nezobrazilo sa.
df = df[df["StatusCode"].between(200, 299)]
print(f"Po odstraneni presmerovani: {len(df)}")

# === KROK 6: Ulozenie vysledku ===
# Po filtroch maju riadky "diery" v cislovani (1, 5, 8...). Precislujeme od nuly.
df = df.reset_index(drop=True)
print(f"\nFinal: {len(df)} riadkov")  # malo by byt cca 31500
# index=False = neukladame cislovanie riadkov ako stlpec (inak by pribudol "Unnamed: 0").
df.to_csv("out/02_cleaned_log.csv", index=False)
