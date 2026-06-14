# ==========================================================
# CV2 - Uloha 06: Identifikacia sedeni metodou SLength
# ==========================================================
#
# CIEL: Rozdelit kliky pouzivatelov do sedeni (sessions).
#   Sedenie = suvisla aktivita jedneho cloveka na webe.
#   Toto je zakladna jednotka, z ktorej dalej hladame vzory spravania.
#
# TEORIA (jednoducho):
#   Metoda SLength (Session Length = dlzka sedenia) hovori:
#   "ked CELKOVY cas od zaciatku sedenia (sucet casov na vsetkych jeho strankach)
#   prekroci 10 minut, otvorime nove sedenie.
#   (POZN.: NIE je to o jednom kliku - to by bola STT metoda - ale o SUCTE casov
#   v ramci jedneho sedenia.)"
#   Cize ratame, kolko casu uz uplynulo od zaciatku aktualneho sedenia.
#   Akonahle prekrocime 10 minut (600 sekund), zacneme rataT nove sedenie.
#   Existuju aj ine metody (RLength, STT_MEAN, STT_Q), ktore robia podobne,
#   ale s inymi pravidlami (napr. cas MEDZI dvoma klikmi, nie celkovy cas).
#
# VSTUP:
#   in/03_length.csv - log z predoslej ulohy.
#     Obsahuje stlpec Length = cas v sekundach, ktory pouzivatel stravil
#     na predoslej stranke (rozdiel casu medzi dvoma klikmi).
#     Prvy klik kazdeho pouzivatela ma Length prazdne (NaN) - lebo
#     pred nim ziadny iny klik toho cloveka nebol.
#
# VYSTUP:
#   out/06_slength.csv - ten isty log + novy stlpec SESSION_ID
#     (cislo 1, 2, 3, ... ktore hovori, do ktoreho sedenia klik patri).
#     Pocet sedeni ma vyjst priblizne 6700 (tolerancia ~5%).
#
# POUZITE KNIZNICE:
#   pandas - praca s tabulkou dat (nacitanie CSV, prechadzanie riadkov, ulozenie).
#
# ALGORITMUS (jednou vetou):
#   Postupne scitavame cas stravany v sedeni; ked prekroci 10 minut alebo
#   sa zacne novy pouzivatel, otvorime nove sedenie.
# ==========================================================

import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))  # umoznuje spustenie skriptu odkialkolvek (nielen z jeho priecinka)

import pandas as pd  # pandas = kniznica na pracu s tabulkami (Excel-style data)

# === KROK 1: Nacitanie logu ===
df = pd.read_csv("in/03_length.csv")  # nacitame tabulku klikov z predoslej ulohy

slength = 600  # limit sedenia = 10 minut = 600 sekund (zo zadania)
print(f"SLength (casove okno): {slength} sekund (10 minut)")

# === KROK 2: Priradenie SESSION_ID kazdemu kliku ===
#
# Ideme po jednom kliku za druhym a pocitame cas od zaciatku sedenia.
# Tri situacie, kedy sa rozhodujeme:
#   1) Prazdny Length => zacal novy pouzivatel => zacneme nove sedenie.
#   2) Po pripoctani by sme prekrocili 10 minut => zacneme nove sedenie.
#   3) Inak => pokracujeme v rovnakom sedeni, len pripocitame cas.

session_id = 0         # cislo aktualneho sedenia (zacina od 0, prve sedenie bude 1)
session_ids = []       # zoznam, kam pre kazdy riadok pridame jeho cislo sedenia
cumulative_time = 0    # kolko sekund sme uz nazbierali v aktualnom sedeni

# Tabulka je uz zoradena podla pouzivatela a casu, takze kliky toho isteho
# cloveka idu pekne za sebou v chronologickom poradi.
for i, row in df.iterrows():
    if pd.isna(row["Length"]):
        # Prazdna hodnota = prvy klik noveho pouzivatela => zacina nove sedenie.
        session_id += 1        # zvysime cislo sedenia o 1
        cumulative_time = 0    # nova nadoba na cas zacina na nule
    elif cumulative_time + row["Length"] >= slength:
        # Ak by sme pripocitanim presli cez 10 minut, zacneme nove sedenie.
        # Cas tohto kliku rovno zaratame do noveho sedenia (aby sa nestratil).
        session_id += 1                         # zvysime cislo sedenia o 1
        cumulative_time = row["Length"]         # cas tohto kliku je prvy v novom sedeni
    else:
        # Sedenie pokracuje - este sme nepresli limit, len pripocitame cas.
        cumulative_time += row["Length"]  # pridame cas tohto kliku do sedenia

    session_ids.append(session_id)  # zapiseme, do ktoreho sedenia tento klik patri

# Pridame do tabulky novy stlpec s cislami sedeni (poradie sedi s poradim riadkov).
df["SESSION_ID"] = session_ids

# === KROK 3: Ulozenie vystupu ===
df.to_csv("out/06_slength.csv", index=False)  # ulozime; index=False = bez cislovacieho stlpca navyse

# === Diagnostika ===
print(df[["USER_ID", "UNIXTIME", "Length", "SESSION_ID"]].head(20))  # ukazka prvych 20 riadkov na vizualnu kontrolu
print(f"\nPocet zaznamov: {len(df)}")  # pocet klikov - musi byt rovnaky ako vo vstupe
print(f"Pocet sedeni: {df['SESSION_ID'].nunique()}")  # kolko roznych sedeni sme nasli; ocakavame ~6700
