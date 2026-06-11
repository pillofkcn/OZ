# ==========================================================
# CV2 - Uloha 09: Identifikacia sedeni metodou h-ref
# ==========================================================
#
# CIEL:
#   Rozdelit kliky kazdeho pouzivatela na "sedenia" (sedenie = jedna
#   suvisla navsteva webu). Metoda h-ref = heuristika podla referreru,
#   teda podla toho, odkial pouzivatel na stranku prisiel.
#
# TEORIA (jednoducho):
#   POZN. K ZJEDNODUSENIU vs PREDNASKA P8:
#     Plna h-ref (z prednasky) by sledovala aj prerusenie navigacneho
#     retazca - nove sedenie by zacalo aj vtedy, ked Referrer
#     NEZODPOVEDA URL predoslej navstivenej stranky pouzivatela.
#     My implementujeme zjednodusenu variantu: nove sedenie len ked
#     Referrer je prazdny (= externy vstup).
#     Tiez: h-ref metoda VYZADUJE, aby log obsahoval stlpec Referrer
#     (tzv. Extended Log File / ELF). Bez Referrera by sme h-ref
#     nemohli pouzit, museli by sme prejst na cisto casovu metodu STT.
#
#   Sedenie = skupina po sebe iducich klikov toho isteho pouzivatela,
#   ktore patria spolu (jedna navsteva). Ked pouzivatel odide a vrati
#   sa neskor, je to uz nove sedenie.
#
#   Ako poznat, ze sa zacalo nove sedenie? Pouzijeme 3 pravidla
#   (staci splnit jedno):
#     1) Je to prvy klik daneho pouzivatela v logu (Length nemame).
#     2) Od posledneho kliku presiel velky cas (viac ako priemer).
#        - "Length" je cas medzi tymto a predoslym klikom (sekundy).
#        - Ked Length presiahne priemer, predpokladame, ze pouzivatel
#          medzitym odisiel a vratil sa.
#     3) Pouzivatel prisiel z vonku (Referrer = "-").
#        - Referrer hovori, z akej stranky pouzivatel klikol sem.
#        - Ked je "-", pouzivatel napisal URL rucne, kliknul na zalozku
#          alebo prisiel z externej stranky (google a pod.) - to je
#          jasny zaciatok novej navstevy.
#
# VSTUP:
#   in/cleaned_log4_length.csv  - log z predchadzajucej ulohy, uz ma
#                                  vypocitany Length a USER_ID.
#
# VYSTUP:
#   out/cleaned_log4_href.csv   - povodny log + novy stlpec SESSION_ID
#                                  (cislo sedenia, ku ktoremu klik patri).
#
# POUZITE KNIZNICE:
#   pandas - praca s tabulkami (citanie CSV, filtre, vypocty cez stlpce).
#
# ALGORITMUS:
#   Pre kazdy klik si oznacime, ci zacina nove sedenie (True/False).
#   Potom tieto True hodnoty postupne scitavame - kazdy True zvysi
#   cislo sedenia o 1. Tak dostaneme SESSION_ID.
#
# OCAKAVANY VYSLEDOK: cca 7200 sedeni (tolerancia v jednotkach %).
# ==========================================================

import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))  # umoznuje spustenie skriptu odkialkolvek (nielen z jeho priecinka)

import pandas as pd  # pandas = knihovna na pracu s tabulkami

# === KROK 1: Nacitanie logu ===
df = pd.read_csv("in/cleaned_log4_length.csv")  # nacitame log z predoslej ulohy

# === KROK 2: Vypocet casoveho prahu ===
# Prah = priemerny cas, ktory pouzivatelia travili na stranke.
# Ked Length presiahne tento priemer, povazujeme to za odchod.
mean_length = df["Length"].mean()  # priemer Length v sekundach (priemer automaticky preskoci prazdne hodnoty)
print(f"Casove okno (priemer Length): {mean_length:.2f} sekund")  # vypis pre kontrolu

# === KROK 3: Oznacenie zaciatku noveho sedenia ===
# Pre kazdy klik si urcime True/False - ci tu zacina nove sedenie.
# Staci, aby platilo jedno z troch pravidiel (operator | = "alebo").
# Zatvorky okolo podmienok su povinne, inak pandas hodi chybu.
df["NEW_SESSION"] = (
    (df["Length"].isna())               # 1) prvy klik pouzivatela (nemame predoslu navstevu)
    | (df["Length"] >= mean_length)     # 2) od minuleho kliku presiel velky cas
    | (df["Referrer"] == "-")           # 3) pouzivatel prisiel zvonku (prazdny referrer)
)

# === KROK 4: Priradenie SESSION_ID ===
# Postupne scitavame True/False hodnoty (True = 1, False = 0).
# Priklad: [True, False, False, True, False] -> [1, 1, 1, 2, 2]
# Kliky s rovnakym cislom patria do toho isteho sedenia.
df["SESSION_ID"] = df["NEW_SESSION"].cumsum()  # postupny sucet -> unikatne cislo sedenia
df = df.drop(columns=["NEW_SESSION"])  # pomocny stlpec uz nepotrebujeme

# === KROK 5: Ulozenie vysledku ===
df.to_csv("out/cleaned_log4_href.csv", index=False)  # index=False = nepise cisla riadkov ako prvy stlpec

# === Kontrolne vypisy ===
# Prvych 20 riadkov - vizualna kontrola, ze sedenia stupaju spravne.
print(df[["USER_ID", "UNIXTIME", "Length", "Referrer", "SESSION_ID"]].head(20))
print(f"\nPocet zaznamov: {len(df)}")  # pocet vsetkych klikov v logu
print(f"Pocet sedeni: {df['SESSION_ID'].nunique()}")  # pocet unikatnych sedeni (porovnaj s ~7200)
