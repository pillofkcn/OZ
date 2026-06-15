# =============================================================================
# CV2 - Uloha 03: Premenna Length (kolko sekund user stravil na stranke)
# =============================================================================
#
# CIEL:
#   Pre kazdy klik v logu vypocitat, ako dlho user pozeral danu stranku.
#   Toto je medzikrok v spracovani web logov - vysledok bude pouzity dalej
#   pri delení klikov na sedenia (jedna navsteva = sled klikov po sebe).
#
# TEORIA (pre laika):
#   Apache server pri kazdom kliku zapise CAS, kedy user prisiel na stranku.
#   Ale uz nevie, kedy z nej odisiel. Preto cas "citania" odhadujeme takto:
#   zoberieme cas dalsieho kliku toho isteho usera a odcitame od neho cas
#   tohto kliku. Vysledok v sekundach = ako dlho user na stranke zostal.
#
#   Pripady, ked Length nedava zmysel a dame mu prazdnu hodnotu (NaN):
#     1) Je to PRVY klik usera - nemame od coho odcitat.
#     2) Medzera medzi klikmi je vacsia ako 60 minut (3600 sekund) -
#        vtedy user uz pravdepodobne davno odisiel a tu stranku necital.
#        Hranicu 60 minut urcuje zadanie (zauzivany odhad v literature).
#
#   Pozn.: 60 min STT (session timeout threshold = hranica pre koniec sedenia)
#   je podla ZADANIA. Prednaska (P8) hovori, ze STT by sa malo odhadnut z dat
#   (kvantilova funkcia ak Length ma exp. rozdelenie, alebo kvartilovy odhad
#   Q3+1.5*IQR). Robime to neskor v cv3 (STT_Q) a v projekte (RLength).
#
#   Ocakavany priemer Length podla zadania je okolo 150 sekund.
#
# VSTUP:
#   in/02_users.csv  - log z predoslej ulohy, uz s prirad. USER_ID.
#
# VYSTUP:
#   out/03_length.csv - to iste + novy stlpec Length (v sekundach).
#
# POUZITE KNIZNICE:
#   pandas - praca s tabulkou (citanie CSV, zoskupenie po userovi, vypocty).
#
# ALGORITMUS (jedna veta):
#   Pre kazdeho usera zoberieme cas predoslého kliku, odcitame od aktualneho,
#   a ak je rozdiel vacsi ako hodina, nahradime ho prazdnou hodnotou.
# =============================================================================

import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))  # umoznuje spustenie skriptu odkialkolvek (nielen z jeho priecinka)

import pandas as pd

# === KROK 1: Nacitanie logu ===
df = pd.read_csv("in/02_users.csv")  # nacitame log z predoslej ulohy (uz obsahuje USER_ID)

# === KROK 2: Cas predosleho kliku toho isteho usera ===
#
# Chceme: pre kazdy riadok pridat stlpec "cas predchadzajuceho kliku rovnakeho usera".
#   groupby("USER_ID") = rozdel tabulku na skupiny podla usera,
#   shift(1)           = v kazdej skupine posun hodnoty o 1 riadok nadol (cize do
#                        riadku vlozi cas z PREDOSLEHO riadku toho isteho usera).
# Priklad: casy klikov usera [100, 160, 230] -> PREV_UNIXTIME = [NaN, 100, 160].
# Prvy klik usera nema nad sebou predchodcu -> ostane prazdne (NaN).
df["PREV_UNIXTIME"] = df.groupby("USER_ID")["UNIXTIME"].shift(1)

# === KROK 3: Vypocet Length ako rozdielu casov ===
#
# Length = teraz - predtym (v sekundach). Priklad: klik v case 160, predosly v 100
# -> Length = 160 - 100 = 60 s na predoslej stranke. Ak je predtym prazdne (prvy
# klik usera), vysledok je tiez prazdny - to nam vyhovuje.
df["Length"] = df["UNIXTIME"] - df["PREV_UNIXTIME"]

# === KROK 4: Vyhodime prilis velke medzery (>= 1 hodina) ===
#
# Ak je medzi dvoma klikmi 60 minut a viac, predpokladame, ze user medzitym
# odisiel - cas na predoslej stranke nepocitame, dame tam prazdnu hodnotu.
df.loc[df["Length"] >= 3600, "Length"] = None

# pomocny stlpec uz nepotrebujeme, ostane len finalny Length
df = df.drop(columns=["PREV_UNIXTIME"])

# === KROK 5: Ulozenie vystupu ===
df.to_csv("out/03_length.csv", index=False)  # index=False = neukladame poradove cisla riadkov

# === Kontrolny vypis pre rychle overenie ===
print(df[["USER_ID", "UNIXTIME", "Length"]].head(20))  # prvych 20 riadkov - vidno NaN pri prvych klikoch userov
print(f"\nPocet zaznamov: {len(df)}")
print(f"Priemerna hodnota Length: {df['Length'].mean():.2f}")  # ocakavame okolo 150 sekund podla zadania
