# ==========================================================
# PROJEKT - Uloha 00: Vystrihnutie prideleneho tyzdna z velkeho logu
# ==========================================================
#
# CIEL:
#   Z velkeho zaznamu navstev na webe (Apache log, asi 12 GB, obdobie
#   2017-2020) vyberieme len riadky pre nas tyzden (17.-23.12.2017)
#   a ulozime ich do mensieho suboru (~216 MB), s ktorym sa uz da
#   normalne pracovat.
#
# TEORIA (laickou recou):
#   - Apache log = textovy subor, kazdy riadok je jedna navsteva stranky.
#   - Datum v riadku vyzera takto: [17/Dec/2017:06:25:47 +0200].
#   - Aby sme vybrali nas tyzden, staci v kazdom riadku hladat
#     retazec ako "17/Dec/2017" - ked tam je, riadok patri nam.
#   - 12 GB sa nezmesti do pamate, takze subor citame "po riadku"
#     (stream): jeden riadok prectieme, rozhodneme, zahodime. Pamat
#     teda nepotrebuje 12 GB, staci jeden riadok naraz.
#
# VSTUP:
#   ../../materials/wm2020projekt.log   (~12 GB, povodny log za 2017-2020)
#
# VYSTUP:
#   ../01_cistenie_zaznamov/in/wm2020projekt_studeny.log   (~216 MB)
#   ../02_robot_ips/in/wm2020projekt_studeny.log           (~216 MB, kopia)
#   Dva ciele preto, lebo dve nasledujuce ulohy (cistenie a robot detekcia)
#   maju kazda svoj vlastny in/ priecinok a chceme byt standalone.
#
# POUZITE KNIZNICE:
#   - os     : vytvori cielovy priecinok ak neexistuje
#   - shutil : skopiruje hotovy subor do druheho ciela (rychle, robi to OS)
#   Pandas tu schvalne nepouzivame - nacital by cely subor do pamate.
#
# ALGORITMUS:
#   Citaj log po riadku, ak riadok obsahuje datum z nasho tyzdna, zapis ho;
#   na konci skopiruj vystup aj do druheho priecinka.
# ==========================================================

import os         # praca s priecinkami (vytvorenie ciela)
import shutil     # kopirovanie hotoveho suboru

os.chdir(os.path.dirname(os.path.abspath(__file__)))  # umoznuje spustenie skriptu odkialkolvek (nielen z jeho priecinka)

# === KROK 1: Cesty k vstupu a vystupom ===

src = "../../materials/wm2020projekt.log"  # povodny velky log (12 GB)

# Dva ciele - kazda nasledujuca uloha ma svoj vlastny in/ priecinok,
# tak aby sa dala spustit samostatne bez ohladu na ostatne.
out_paths = [
    "../01_cistenie_zaznamov/in/wm2020projekt_studeny.log",  # cistenie poli
    "../02_robot_ips/in/wm2020projekt_studeny.log",          # detekcia robotov
]

# === KROK 2: Datumy nasho tyzdna ===

# Sedem retazcov - presne tak, ako vyzera datum v logu (DD/Dec/2017).
# Pre kazdy riadok stacit pozriet, ci obsahuje jeden z nich = patri do tyzdna.
dni = ("17/Dec/2017", "18/Dec/2017", "19/Dec/2017", "20/Dec/2017",
       "21/Dec/2017", "22/Dec/2017", "23/Dec/2017")

# === KROK 3: Priprava cieloveho priecinka ===

# Ak by priecinok '../01_cistenie_zaznamov/in/' neexistoval, open() by spadol.
# makedirs s exist_ok=True priecinok vytvori, a ak uz je, nic sa nestane.
first_out = out_paths[0]
os.makedirs(os.path.dirname(first_out), exist_ok=True)

# === KROK 4: Citanie po riadku a vyber tyzdna ===

count = 0       # kolko riadkov sme zapisali (patria do nasho tyzdna)
total = 0       # kolko riadkov sme celkovo precitali (pre informaciu uzivatelovi)

# Otvorime vstupny subor na citanie a vystupny na zapis sucasne.
# errors="replace" = ak v logu narazime na pokazeny znak, nahradime ho,
#                    aby skript kvoli jednemu zlemu bajtu nepadol.
with open(src, encoding="utf-8", errors="replace") as fin, \
     open(first_out, "w", encoding="utf-8") as fout:
    for line in fin:
        total += 1

        # Kazdych 10 milionov riadkov vypiseme, kde sme - aby pouzivatel
        # videl, ze skript bezi a netreba ho ukoncit.
        if total % 10_000_000 == 0:
            print(f"  ... {total:,} citanych, {count:,} ulozenych")

        # Pozrieme sa, ci v riadku je niektory zo siedmich datumov.
        # Ak najdeme jeden, riadok patri nam - zapiseme ho a koncime kontrolu
        # (dalsie datumy uz testovat netreba, jeden riadok = jeden den).
        for d in dni:
            if d in line:
                fout.write(line)   # zapis bez uprav, riadok ma uz vlastny koniec
                count += 1
                break

# === KROK 5: Vypis vysledkov ===

# Format {:,} oddeli tisicky ciarkou, aby sa cislo dalo lahsie precitat.
print(f"\nCelkom precitanych: {total:,}")
print(f"Ulozenych pre tyzden: {count:,}")
print(f"-> {first_out}")

# === KROK 6: Kopia do druheho ciela ===

# Vysledok je ten isty subor, len ho potrebuju dve nasledujuce ulohy.
# shutil.copy spravi presnu kopiu - rychlejsie ako citat a zapisovat
# znova v Pythone, lebo to robi priamo operacny system.
shutil.copy(first_out, out_paths[1])
print(f"-> {out_paths[1]}")
