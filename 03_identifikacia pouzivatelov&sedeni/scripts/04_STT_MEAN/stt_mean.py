# ==========================================================
# CV2 - Uloha 04: Identifikacia sedeni metodou STT_MEAN
# ==========================================================
#
# CIEL: Zo zoznamu kliknuti (log) chceme zistit, kde konci jedno "sedenie"
# (sedenie = sused suvislych klikov jedneho pouzivatela v jednej navsteve)
# a kde zacina dalsie. Bez sedeni sa neda robit dalsia analyza spravania.
#
# TEORIA — co je STT_MEAN (jednoducho):
#   Pre kazdy klik mame "Length" = kolko sekund pouzivatel zostal na danej
#   stranke (z ulohy 03). Spocitame priemer tychto casov cez cely log.
#   Ked nejaky klik trval VYRAZNE dlho (viac ako priemer), predpokladame,
#   ze pouzivatel medzitym odisiel (napr. zatvoril prehliadac) — povazujeme
#   to za koniec sedenia a dalsi klik bude uz nove sedenie.
#
# POZN.: Munk v prednaske 8 hovori, ze odhad pomocou priemeru NIE JE vhodny,
# ak Length nema exponencialne rozdelenie (exponencialne = vacsina hodnot mala,
# zopar velmi velkych). Robime to napriek tomu, lebo metoda STT_MEAN je presne
# to co zadanie cvika predpisuje. Robustnejsie metody (STT_Q = Q3 + 1.5*IQR,
# RLength z exp. rozdelenia) pouzivame v dalsich ulohach cv3 a v projekte.
#
#   Pravidlo "tu zacina nove sedenie":
#     - Length je prazdny (NaN) = neznamy cas, typicky prvy klik pouzivatela
#       -> nove sedenie (kazdy pouzivatel zacina novym sedenim)
#     - Length >= priemer = pouzivatel sa zdrzal dlho -> nove sedenie
#     - Length < priemer = kratky cas -> pokracovanie toho isteho sedenia
#
# VSTUP:  in/03_length.csv  - vycisteny log s USER_ID, UNIXTIME, Length
# VYSTUP: out/04_stt_mean.csv - to iste + novy stlpec SESSION_ID
#
# POUZITE KNIZNICE:
#   pandas - praca s tabulkovymi datami (citanie CSV, priemer, kumulativny sucet)
#
# ALGORITMUS (jedna veta):
#   Pre kazdy riadok urcime, ci je to zaciatok noveho sedenia (True/False),
#   a tieto True hodnoty postupne scitavame -> dostaneme cislo sedenia.
# ==========================================================

import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))  # umoznuje spustenie skriptu odkialkolvek (nielen z jeho priecinka)

import pandas as pd  # pandas = praca s tabulkami v Pythone

# === KROK 1: Nacitanie vycisteneho logu ===
df = pd.read_csv("in/03_length.csv")  # nacitame CSV z predoslej ulohy do tabulky

# === KROK 2: Vypocet priemerneho casu na stranke (prah STT_MEAN) ===
# Prah = priemer (mean) vsetkych Length = sucet vsetkych casov / ich pocet.
# pandas automaticky preskakuje prazdne (NaN) hodnoty, takze neznamy cas vysledok
# neskresli. Priklad: ak je priemerny Length 150 s, kazdy klik s Length >= 150 s
# budeme povazovat za koniec sedenia.
stt_mean = df["Length"].mean()  # priemerny cas v sekundach = nas prah pre delenie sedeni
print(f"STT_MEAN (priemerne casove okno): {stt_mean:.2f} sekund")

# === KROK 3: Oznacenie riadkov, kde zacina nove sedenie ===
# Pre kazdy riadok chceme True/False odpoved na otazku "zacina tu nove sedenie?".
# True dame, ak:
#   - Length je prazdny (prvy klik pouzivatela, nemame predchadzajuci cas), ALEBO
#   - Length je rovny alebo vacsi nez priemer (pouzivatel sa zdrzal dlho).
# isna() = vrati True tam, kde je hodnota prazdna (NaN). Znak "|" je "alebo" pre
# cely stlpec naraz (stlpec je objekt pandas, bezne slovo "or" by tu vyvolalo chybu).
df["NEW_SESSION"] = (df["Length"].isna()) | (df["Length"] >= stt_mean)

# === KROK 4: Priradenie cisla sedenia (SESSION_ID) ===
# Postup: True sa berie ako 1, False ako 0. Ked tieto cisla postupne scitavame
# zhora dole (cumsum = kumulativny sucet), dostaneme rastuce cisla sedeni:
#   napr. [True, False, False, True, False] -> [1, 1, 1, 2, 2]
# Cize prvy riadok dostane 1, vsetky dalsie riadky v tom istom sedeni tiez 1,
# a hned ako narazime na novy zaciatok, cislo sa zvysi.
df["SESSION_ID"] = df["NEW_SESSION"].cumsum()

# Pomocny stlpec True/False uz nepotrebujeme vo vystupnom subore.
df = df.drop(columns=["NEW_SESSION"])

# === KROK 5: Ulozenie vysledku a kontrolny vypis ===
# index=False = nezapisujeme cislovanie riadkov, aby CSV obsahovalo iba nase data.
df.to_csv("out/04_stt_mean.csv", index=False)

# Kontrolny vypis prvych 20 riadkov - vidno, ako SESSION_ID rastie na hraniciach sedeni.
print(df[["USER_ID", "UNIXTIME", "Length", "SESSION_ID"]].head(20))

# Sumarne cisla - kolko klikov a kolko sedeni sme nasli celkovo.
# nunique() = pocet roznych hodnot v stlpci = pocet sedeni.
print(f"\nPocet zaznamov: {len(df)}")
print(f"Pocet sedeni: {df['SESSION_ID'].nunique()}")
