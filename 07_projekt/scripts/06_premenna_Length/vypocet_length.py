# ==========================================================
# PROJEKT - Uloha 06: Premenna Length (cas straveny na stranke)
# ==========================================================
#
# CIEL: Pre kazdy klik v logu vypocitat, ako dlho pouzivatel
# pravdepodobne stravil na predoslej stranke. Vysledok pouzije
# uloha 07 na rozdelenie klikov na sedenia (suvisle navstevy).
#
# TEORIA (jednoducho):
# Server log je len zoznam poziadaviek (kliknuti). NEVIE, kedy
# pouzivatel stranku zatvoril. Cas na stranke preto ODHADUJEME:
# ked pouzivatel klikol o 12:00 a dalsi klik mal o 12:01, tak
# na prvej stranke bol asi 60 sekund (rozdiel casov).
# Pri prvom kliku pouzivatela nemame predoslu stranku -> Length
# zostane prazdne. Ak je medzera medzi klikmi velmi velka
# (60 minut a viac), pouzivatel sa pravdepodobne medzitym uplne
# odpojil, takze cas na stranke je nezmyselny -> tiez prazdne.
# Tych 60 minut je tzv. STT (Session Timeout Threshold) =
# hranicna doba necinnosti, po ktorej povazujeme navstevu za
# ukoncenu (v zadani je 60 min, klasicke WUM pouziva 30 min).
#
# VSTUP: in/05_users.csv - log s priradenym USER_ID
#                          (pouzivatel = (IP, prehliadac)),
#                          uz zoradeny od najstarsieho kliku.
# VYSTUP: out/06_length.csv - to iste + novy stlpec Length
#                             (cas v sekundach, alebo prazdne).
#
# POUZITE KNIZNICE:
#   pandas - praca s tabulkou (citanie CSV, vypocty po stlpcoch).
#
# ALGORITMUS: Pre kazdy riadok zoberieme cas predosleho kliku
# toho isteho pouzivatela, odcitame, a velke medzery vymazeme.
# ==========================================================

import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))  # umoznuje spustenie skriptu odkialkolvek (nielen z jeho priecinka)

import pandas as pd

# === KROK 1: Nacitanie tabulky z ulohy 05 ===
# Potrebujeme tabulku, kde uz existuje stlpec USER_ID (kto klikol).
# Riadky su uz zoradene podla casu v ramci kazdeho pouzivatela.
df = pd.read_csv("in/05_users.csv", low_memory=False)  # low_memory=False = pandas si data prejde celé a urci typy spravne
print(f"Nacitane: {len(df):,} riadkov")

# === KROK 2: Cas predosleho kliku toho isteho pouzivatela ===
# Pre kazdy klik chceme vediet, kedy ten isty pouzivatel klikol
# tesne predtym. Tabulku si v hlave rozdelime po pouzivateloch
# a v kazdej skupine posunieme casy o jeden riadok nizsie.
# Prvy klik pouzivatela nema predchodcu -> ostane prazdne (NaN).
df["PREV_UNIXTIME"] = df.groupby("USER_ID")["UNIXTIME"].shift(1)

# === KROK 3: Vypocet Length = rozdiel casov v sekundach ===
# UNIXTIME je cas v sekundach, takze rozdiel je tiez v sekundach.
# Ked je predosly cas prazdny (prvy klik pouzivatela), rozdiel
# automaticky vyjde tiez prazdny.
df["Length"] = df["UNIXTIME"] - df["PREV_UNIXTIME"]

# === KROK 4: Pri prilis velkej medzere Length zmazeme ===
# Ak su dva kliky od seba aspon 60 minut (3600 sekund),
# pouzivatel medzitym pravdepodobne odisiel a vratil sa neskor.
# Cas "na stranke" by bol nerealne dlhy, tak ho vymazeme.
df.loc[df["Length"] >= 3600, "Length"] = None  # None pandas v cislach ulozi ako prazdne (NaN)

# === KROK 5: Zahodime pomocny stlpec ===
# PREV_UNIXTIME nam sluzil len na vypocet, do vystupu ho netreba.
df = df.drop(columns=["PREV_UNIXTIME"])

# === KROK 6: Ulozenie vysledku ===
df.to_csv("out/06_length.csv", index=False)  # index=False = nezapisuj cislovanie riadkov ako extra stlpec

# Rychla kontrola: priemer a median dlzky pobytu na stranke.
# mean/median v pandas prazdne hodnoty automaticky preskakuju.
print(f"\nPriemer Length: {df['Length'].mean():.2f}s")
print(f"Median Length: {df['Length'].median():.2f}s")
print(f"Ulozene -> out/06_length.csv")
