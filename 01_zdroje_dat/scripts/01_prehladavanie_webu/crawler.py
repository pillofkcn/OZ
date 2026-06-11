# ==========================================================
# CV1 - Uloha 01: Prehladavanie webu (web scraping)
# ==========================================================
#
# CIEL: Stiahnut text z 5 webovych clankov a ulozit kazdy do samostatneho
# .txt suboru. Toto je prvy krok WUM (Web Usage Mining) - vyrobime si surovy
# textovy material, ktory v dalsich ulohach budeme cistit a analyzovat.
#
# TEORIA (pre laika):
#   - Webova stranka = HTML kod (text s "tagmi" ako <p>, <div>, <a>).
#   - "Scraping" = stiahnut HTML a vytahnut z neho iba citatelny text bez tagov.
#   - HTML parser = nastroj, ktory chape strukturu HTML a vie z nej vybrat
#     iba slova, nie znacky. My pouzivame BeautifulSoup.
#
# VSTUP:  zoznam 5 URL (zadane priamo v kode nizsie).
# VYSTUP: out/articles/article_1.txt .. article_5.txt (kodovanie UTF-8,
#         jeden subor = jeden clanok, bez HTML tagov, bez prazdnych riadkov).
#
# POUZITE KNIZNICE:
#   - requests       - stiahne webovu stranku (posle poziadavku, vrati odpoved).
#   - BeautifulSoup  - rozparsuje HTML a da nam iba text bez znaciek.
#   - sys, os        - prepnut konzolu na UTF-8 a vytvorit vystupny priecinok.
#
# ALGORITMUS: pre kazdu URL stiahni stranku, vytiahni cisty text, vyhod
# prazdne riadky, zapis do article_<i>.txt.
# ==========================================================

import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))  # umoznuje spustenie skriptu odkialkolvek (nielen z jeho priecinka)

import sys
import os
import requests
from bs4 import BeautifulSoup

# Windows konzola standardne nevie pisat slovenske znaky => prepneme ju na UTF-8,
# inak by print() so slovami s diakritikou spadol.
sys.stdout.reconfigure(encoding="utf-8")

# === KROK 1: Zoznam URL adries ===
# 5 clankov z fakultnej vyvesky UKF FPVAI. Pocet 5 = poziadavka zo zadania.
urls = [
    "https://www.fpvai.ukf.sk/sk/fakulta/uradna-vyveska/hlavne-spravy/2003-prihlaste-sa-na-erasmus-mobilitu-v-ar-2026-2027",
    "https://www.fpvai.ukf.sk/sk/fakulta/uradna-vyveska/hlavne-spravy/2001-novym-rektorom-ukf-sa-stal-prof-petrovic-dekan-fpvai",
    "https://www.fpvai.ukf.sk/sk/fakulta/uradna-vyveska/hlavne-spravy/2002-informatici-testovali-bezpecnost-routera-ako-profesionalni-analytici",
    "https://www.fpvai.ukf.sk/sk/fakulta/uradna-vyveska/hlavne-spravy/1997-gamejam-nitra-2026-ked-24-hodin-staci-na-vznik-hier-s-buducnostou",
    "https://www.fpvai.ukf.sk/sk/fakulta/uradna-vyveska/hlavne-spravy/1996-studenti-katedry-informatiky-ukf-vyvijali-hru-v-spolupraci-s-powerplaystudio",
]

# Pripravime priecinok na vystupne subory; exist_ok=True = ak uz existuje, neplac.
os.makedirs("out/articles", exist_ok=True)

# enumerate(urls, 1) = prejdeme URL po jednej a cislujeme od 1 (kvoli nazvu suboru).
for i, url in enumerate(urls, 1):
    # === KROK 2: Stiahnutie HTML stranky ===
    r = requests.get(url)  # posle poziadavku na server a vrati odpoved (r.text = HTML)

    # === KROK 3: Vytiahnutie cisteho textu z HTML ===
    # BeautifulSoup chape HTML ako strom znaciek; get_text() z neho vyberie
    # iba textovy obsah a zahodi vsetky tagy (<p>, <div>, <a> a pod.).
    soup = BeautifulSoup(r.text, "html.parser")  # rozparsuje HTML na strom
    raw_text = soup.get_text()                   # vyberie iba text, tagy vyhodi

    # === KROK 4: Vycistenie prazdnych riadkov ===
    # HTML ma vela odsadenia a prazdnych riadkov. Postup:
    #   - splitlines()  = rozdeli text na zoznam riadkov,
    #   - strip()       = orezeme medzery na zaciatku/konci riadku,
    #   - if l.strip()  = riadky tvorene iba medzerami preskocime.
    lines = [l.strip() for l in raw_text.splitlines() if l.strip()]
    text = "\n".join(lines)  # spojime neprazdne riadky spat do jedneho textu

    # === KROK 5: Zapis do suboru ===
    # encoding="utf-8" je nutne kvoli slovenskej diakritike (Windows by inak spadol).
    with open(f"out/articles/article_{i}.txt", "w", encoding="utf-8") as f:
        f.write(text)
    print(f"Ulozene: out/articles/article_{i}.txt")  # vypise progress po kazdom clanku

# Na konci zhrnieme, kolko clankov sme spracovali.
print(f"\nCelkovo: {len(urls)} clankov")
