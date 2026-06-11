# ==========================================================
# PROJEKT - Uloha 02: Najdenie IP adries robotov
# ==========================================================
#
# CIEL:
#   Z logu webu najdeme IP adresy, ktore patria robotom (automatickym
#   programom, co prechadzaju web — napr. Google bot). Robotov potom
#   dalej v pipeline odfiltrujeme, aby nam neskreslovali spravanie
#   skutocnych ludi.
#
# TEORIA (jednoducho):
#   Kazdy slusny robot si na zaciatku stiahne subor /robots.txt — to je
#   taky "navod" pre robotov, kde im stranka povie co smu a co nesmu
#   prechadzat. Bezny clovek v prehliadaci tento subor nikdy nestahuje
#   (prehliadac to nerobi). Takze plati jednoduche pravidlo:
#       kto si stiahol /robots.txt = skoro urcite robot.
#   Toto je nasa heuristika (= jednoducha rozhodovacia pomocka).
#
# VSTUP:  in/wm2020projekt_studeny.log
#         (Apache log = textovy subor, kde kazdy riadok = jedna poziadavka
#          na server. Obsahuje IP, datum, URL, prehliadac atd.)
# VYSTUP: out/02_robot_ips.csv
#         (jeden stlpec "IP" — IP adresy, ktore si stiahli robots.txt.
#          Duplikaty ponechavame — dalsi krok pipeline si urobi unikat.)
#
# POUZITE KNIZNICE:
#   - re     : praca s regularnymi vyrazmi (vzory, podla ktorych rozparsujeme
#              riadok logu na jednotlive casti — IP, URL, datum...).
#   - pandas : tabulkove data; pouzivame ho len na ulozenie vysledku do CSV.
#
# ALGORITMUS:
#   Pre kazdy riadok logu sa pozrieme, ci v nom je slovo "robots.txt".
#   Ak hej, riadne ho rozparsujeme a overime, ze "robots.txt" je naozaj
#   v URL (a nie nahodou v nazve prehliadaca). Ak hej, ulozime IP.

import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))  # umoznuje spustenie skriptu odkialkolvek (nielen z jeho priecinka)

import re
import pandas as pd

# === KROK 1: Vzor (regex) na rozparsovanie riadku logu ===
#
# Apache log ma na kazdom riadku tieto casti, oddelene medzerami:
#   IP - - [Datum] "Metoda URL HTTP/Verzia" StatusKod Bajty "Referer" "Prehliadac"
# Regex nizsie zachyti tieto casti do ocislovanych skupin (group 1, 2, ...).
# \S+ znamena "jedno alebo viac neprazdnych znakov bez medzery".
pattern = re.compile(
    r'^(\S+)\s+\S+\s+\S+\s+'             # skupina 1: IP adresa (na zaciatku riadku)
    r'\[([^\]]+)\]\s+'                   # skupina 2: datum a cas v hranatych zatvorkach
    r'"(\S+)\s+(\S+)\s*\S*"\s+'          # skupina 3: metoda (GET/POST), skupina 4: URL
    r'(\d{3})\s+'                        # skupina 5: status kod (napr. 200, 404)
    r'(\S+)\s+'                          # skupina 6: pocet poslanych bajtov
    r'"([^"]*)"\s+'                      # skupina 7: referer (z akej stranky pouzivatel prisiel)
    r'"([^"]*)"'                         # skupina 8: nazov prehliadaca / robota
)

# === KROK 2: Citanie logu po riadkoch ===
#
# Log moze byt velky (stovky MB), tak ho nenacitavame naraz do pamate,
# ale citame ho po jednom riadku. To zaberie len trochu pamate.
rows = []       # sem si budeme ukladat najdene IP adresy robotov
total = 0       # pocitadlo riadkov — len aby sme videli ze to bezi

# encoding="utf-8", errors="replace":
#   logy mavaju obcas pokazene znaky (zly kod URL); "replace" zabezpeci,
#   ze sa to nepokazi — pokazeny znak sa len nahradi otaznikom.
with open("in/wm2020projekt_studeny.log", encoding="utf-8", errors="replace") as f:
    for line in f:                           # citame jeden riadok logu za druhym
        total += 1
        if total % 100000 == 0:              # kazdych 100 tisic riadkov vypiseme pokrok
            print(f"  ... spracovanych {total:,}")

        # === KROK 3: Rychla predkontrola ===
        #
        # Vacsina riadkov NIE JE pristup na robots.txt. Najprv teda lacno
        # zistime, ci tam to slovo vobec niekde je. Az ked je, pustime drahy
        # regex. .lower() = prevedieme na male pismena (niektori boti pisu
        # Robots.txt s velkym R).
        if "robots.txt" not in line.lower():
            continue                          # nie je tam -> dalsi riadok

        # === KROK 4: Rozparsovanie riadku a vytiahnutie IP ===
        m = pattern.match(line)
        if m:                                 # ak sa riadok zhoduje so vzorom
            url = m.group(4)                  # vytiahneme URL (4. skupina vzoru)

            # Overenie: slovo "robots.txt" sa mohlo v riadku objavit aj inde
            # nez v URL — napriklad v nazve prehliadaca ("robots.txt-checker").
            # Tu sa preto este raz uistime, ze je naozaj v URL = naozaj si
            # ten subor stiahol.
            if "robots.txt" in url.lower():
                rows.append({"IP": m.group(1)})  # ulozime IP adresu (1. skupina vzoru)

# === KROK 5: Ulozenie do CSV ===
#
# Z listu slovnikov spravime tabulku — pandas vytvori stlpec "IP".
# Duplikaty v tabulke necheme odstranovat — kazdy riadok = jeden pristup
# na robots.txt, a dalsi krok pipeline si sam najde unikatne IP.
df = pd.DataFrame(rows)
print(f"\nZaznamy s robots.txt: {len(df)}")            # spolu vratane duplikatov
print(f"Unikatnych IP: {df['IP'].nunique()}")          # kolko roznych IP adries to bolo

# index=False = v CSV nepiseme cisla riadkov (0, 1, 2...), len cisty stlpec IP.
df.to_csv("out/02_robot_ips.csv", index=False)
print(f"Ulozene -> out/02_robot_ips.csv")
