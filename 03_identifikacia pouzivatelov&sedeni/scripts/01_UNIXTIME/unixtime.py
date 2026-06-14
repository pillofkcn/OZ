# ==========================================================
# CV2 - Uloha 01: Vytvorenie premennej UNIXTIME
# ==========================================================
#
# CIEL:
#   Z ocisteneho logu z cv1 spravime numericky cas pristupu.
#   Kazdy riadok dostane jedno cislo = pocet sekund od 1.1.1970.
#   S takym cislom sa lahko pocita (rozdiely casu, triedenie).
#
# TEORIA (jednoducho):
#   - Apache log ma cas v tvare "19/Feb/2020:06:25:49 +0100".
#     To je text, nie cislo - pocitac s nim nevie priamo ratat.
#   - UNIX timestamp je trik: zoberieme zaciatok roku 1970 a
#     spocitame, kolko sekund od neho ubehlo do nasho casu.
#     Vysledok je jedno velke cislo (napr. 1582089949).
#   - Ked mame dve takeho cisla, ich rozdiel = pocet sekund
#     medzi tymito dvomi pristupmi. To pouzijeme dalej:
#       * uloha 02 (Length): cas stravený na stranke = rozdiel
#         dvoch po sebe iducich pristupov toho isteho cloveka.
#       * uloha 03 (Session = jedna navsteva webu od prichodu
#         po odchod): novu navstevu zacneme, ked je medzera
#         medzi klikmi vacsia ako napr. 30 minut.
#
# VSTUP:
#   in/04_cleaned_log.csv  - log z cv1 (~20666 riadkov), ma stlpec
#                          "DateTime" s textovym casom.
# VYSTUP:
#   out/01_unixtime.csv - to iste + novy stlpec UNIXTIME.
#
# POUZITE KNIZNICE:
#   - pandas:   praca s tabulkami (citanie/zapis CSV, stlpce).
#   - datetime: standardna kniznica Pythonu na pracu s datumom;
#               zo zadania pouzivame datetime(...).timestamp().
#
# ALGORITMUS:
#   Pre kazdy riadok rozoberieme text na rok/mesiac/den/hod/min/sek,
#   postavime z toho datum a zavolame .timestamp() = cislo sekund.
# ==========================================================

import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))  # umoznuje spustenie skriptu odkialkolvek (nielen z jeho priecinka)

import pandas as pd      # praca s tabulkou (CSV, stlpce)
import datetime          # praca s datumom (zo zadania)

# === KROK 1: Nacitanie logu ===
df = pd.read_csv("in/04_cleaned_log.csv")   # nacitame ocisteny log z cv1 do tabulky

# Prevod 3-pismenovej skratky mesiaca na cislo.
# Apache log pise mesiac vzdy anglickou skratkou ("Feb"),
# datetime ale potrebuje cislo (2). Slovnik to spravi rychlo.
months = {
    "Jan": 1, "Feb": 2, "Mar": 3, "Apr": 4, "May": 5, "Jun": 6,
    "Jul": 7, "Aug": 8, "Sep": 9, "Oct": 10, "Nov": 11, "Dec": 12,
}


# === KROK 2: Funkcia na prevod textu na cislo sekund ===
def to_unixtime(dt_str):
    """Z textu '19/Feb/2020:06:25:49 +0100' spravi cislo 1582089949.0.
    Cislo = pocet sekund od 1.1.1970."""
    # Text rozdelime podla ":" -> ["19/Feb/2020", "06", "25", "49 +0100"].
    # Apache pouziva ":" medzi datumom a casom aj medzi hodinami/minutami/sekundami.
    parts = dt_str.split(":")
    date_part = parts[0]       # "19/Feb/2020" - samotny datum
    hour = int(parts[1])       # hodina ako cislo
    minute = int(parts[2])     # minuta ako cislo
    # Posledna cast "49 +0100" - za medzerou je casove pasmo, to zahodime.
    second = int(parts[3].split(" ")[0])

    # Datum rozdelime podla "/" -> ["19", "Feb", "2020"].
    day, month_str, year = date_part.split("/")

    # Postavime datum (mesiac dostaneme cez slovnik) a zavolame
    # .timestamp() = pocet sekund od 1.1.1970.
    return datetime.datetime(int(year), months[month_str], int(day), hour, minute, second).timestamp()


# === KROK 3: Pridanie noveho stlpca UNIXTIME ===
# Funkciu pustime na kazdy riadok stlpca "DateTime".
# Vysledky ulozime ako novy stlpec UNIXTIME.
df["UNIXTIME"] = df["DateTime"].apply(to_unixtime)

# === KROK 4: Ulozenie vysledku ===
# index=False = nezapisujeme cisla riadkov 0,1,2..., chceme len data.
df.to_csv("out/01_unixtime.csv", index=False)

# Rychla kontrola - vypiseme prvych 10 dvojic povodny datum + nove cislo,
# aby sme videli ze prevod sedi.
print(df[["DateTime", "UNIXTIME"]].head(10))
# Pocet riadkov - ma sediet s cv1 (~20666).
print(f"\nPocet zaznamov: {len(df)}")
