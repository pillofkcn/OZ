# ==========================================================
# PROJEKT - Uloha 04: Vyber obdobia + premenna UNIXTIME
# ==========================================================
#
# CIEL: Z velkeho logu (zaznam o tom, kto a kedy navstivil stranku)
# nechame len nas pridelenych 7 dni (17.-23.12.2017) a ku kazdemu
# riadku dopiseme cas v sekundach od roku 1970. Vdaka tomu sa daju
# v dalsich ulohach lahko pocitat rozdiely medzi navstevami.
#
# TEORIA (pre laika):
#   - Apache log = textovy subor, kazdy riadok = jedna navsteva stranky.
#     V nom je datum v tvare "17/Dec/2017:06:25:47 +0100".
#   - UNIXTIME = jedno cislo (sekundy od 1.1.1970). Pohodlne, lebo
#     rozdiel dvoch cisiel = pocet sekund medzi udalostami.
#   - Kedze nas zaujima len jeden tyzden, ostatne dni vyhodime.
#
# VSTUP:  in/03_cleaned_log.csv  - log po odstraneni robotov (uloha 03)
# VYSTUP: out/04_obdobie.csv     - len nas tyzden + novy stlpec UNIXTIME
#
# POUZITE KNIZNICE:
#   - pandas:   praca s tabulkou (nacitanie CSV, filtrovanie riadkov)
#   - datetime: prepocet kalendarneho casu na sekundy od roku 1970
#
# ALGORITMUS: nacitaj CSV -> nechaj len 7 dni -> ku kazdemu riadku
# prepocitaj datum na sekundy -> uloz vysledok.
# ==========================================================

import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))  # umoznuje spustenie skriptu odkialkolvek (nielen z jeho priecinka)

import pandas as pd
import datetime

# === KROK 1: Nacitanie logu ===
df = pd.read_csv("in/03_cleaned_log.csv", low_memory=False)  # nacitame log; low_memory=False = pandas si prejde cely stlpec a urci typ spravne
print(f"Nacitane: {len(df):,} riadkov")

# === KROK 2: Filter na nas tyzden 17.-23.12.2017 ===
# Datum v logu zacina napr. "17/Dec/2017:...". Pre kazdy zo 7 dni
# spravime kontrolu, ci riadok zacina danym datumom. Operator | znamena
# "alebo" - staci, aby sedel jeden den, a riadok si necham.
mask = (
    df["DateTime"].str.startswith("17/Dec/2017") |  # pondelok
    df["DateTime"].str.startswith("18/Dec/2017") |  # utorok
    df["DateTime"].str.startswith("19/Dec/2017") |  # streda
    df["DateTime"].str.startswith("20/Dec/2017") |  # stvrtok
    df["DateTime"].str.startswith("21/Dec/2017") |  # piatok
    df["DateTime"].str.startswith("22/Dec/2017") |  # sobota
    df["DateTime"].str.startswith("23/Dec/2017")    # nedela
)
df = df[mask].reset_index(drop=True)  # nechame len vyhovujuce riadky a precislujeme ich od 0
print(f"Po filtrovani na 17.-23.12.2017: {len(df):,} riadkov")

# === KROK 3: Pomocna tabulka mesiacov a funkcia na prepocet casu ===
# V logu je mesiac napisany ako "Dec", ale Python pri praci s datumom
# potrebuje cislo 12. Slovnik nam to rychlo prelozi.
months = {
    "Jan": 1, "Feb": 2, "Mar": 3, "Apr": 4, "May": 5, "Jun": 6,
    "Jul": 7, "Aug": 8, "Sep": 9, "Oct": 10, "Nov": 11, "Dec": 12,
}


def to_unixtime(dt_str):
    """Z textoveho datumu "17/Dec/2017:06:25:47 +0100" vyrobime
    jedno cislo - sekundy od 1.1.1970. Vdaka tomu sa s casom
    da pocitat ako s normalnym cislom (odcitavanie, porovnanie)."""
    # Text rozsekneme podla dvojbodky. Vznikne nam: datum, hodina,
    # minuta a posledny kus "47 +0100" (sekundy + casove pasmo).
    parts = dt_str.split(":")
    date_part = parts[0]                       # napr. "17/Dec/2017"
    hour = int(parts[1])                       # hodina ako cislo
    minute = int(parts[2])                     # minuta ako cislo
    second = int(parts[3].split(" ")[0])       # zo "47 +0100" si zoberieme len "47"

    # Datum este rozdelime na den, mesiac a rok podla lomitka.
    day, month_str, year = date_part.split("/")

    # Z jednotlivych casti zlozime datum a zavolame .timestamp(),
    # ktora vrati sekundy od 1.1.1970 (to je nas UNIXTIME).
    return datetime.datetime(
        int(year), months[month_str], int(day), hour, minute, second
    ).timestamp()


# === KROK 4: Pridanie stlpca UNIXTIME ===
# .apply znamena: zober kazdy riadok stlpca DateTime a presun ho cez
# nasu funkciu to_unixtime. Vysledne cisla ulozime ako novy stlpec.
df["UNIXTIME"] = df["DateTime"].apply(to_unixtime)

# === KROK 5: Ulozenie vysledku ===
df.to_csv("out/04_obdobie.csv", index=False)  # index=False = neukladame cislovanie riadkov ako stlpec
print(f"Ulozene -> out/04_obdobie.csv")
print(df[["DateTime", "UNIXTIME"]].head(5))  # kratky pohlad na vysledok pre kontrolu
