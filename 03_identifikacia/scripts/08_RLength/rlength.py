# ==========================================================
# CV2 - Uloha 08: Rozdelenie klikov na sedenia metodou RLength
# ==========================================================
#
# CIEL:
#   Vezmeme log klikov (uz vycisteny a doplneny o cas straveny
#   na stranke) a rozdelime ho na "sedenia" - skupiny klikov,
#   o ktorych predpokladame, ze ich urobil ten isty clovek
#   pocas jednej navstevy webu.
#
# AKO TO ROBIME (jednoducho):
#   Niektore stranky clovek len rychlo preklikne (hlada cestu,
#   to su "navigacne"), na inych zostane dlhsie a cita obsah.
#   Predpokladame, ze 40% stranok su navigacne (rychle kliky).
#   Vyrobime casovy prah: ak na stranke clovek stravil viac
#   nez prah, povazujeme to za koniec sedenia a dalsi klik
#   uz patri do novej navstevy.
#
# VZOREC NA PRAH (preco vyzera ako vyzera):
#   Predpokladame, ze casy na strankach sa spravaju ako
#   "exponencialne rozdelenie" (typicke pre cakacie casy -
#   napr. cas medzi prichodom dvoch autobusov).
#   Vzorec: prah = -ln(1 - p) * priemerny_cas,
#   kde p = 0.4 (40% navigacnych).
#   ln je "prirodzeny logaritmus" (logaritmus so zakladom e).
#   Vyjde nam prah asi 75 sekund.
#
# ODKIAL VZOREC POCHADZA (teoria):
#   Vzorec vychadza z kvantilovej funkcie exponencialneho
#   rozdelenia: ak chceme casovy prah pod ktorym lezi p%
#   najkratsich casov, dostaneme -ln(1-p)/lambda.
#   A lambda = 1/priemer (maximalny vierohodny odhad),
#   takze prah = -ln(1-p) * priemer.
#
# VSTUP:
#   in/cleaned_log4_length.csv - log klikov, kazdy riadok uz
#   ma stlpec Length = pocet sekund stravenych na stranke.
#   Posledny klik kazdeho cloveka ma Length prazdne (NaN),
#   lebo nevieme, kedy realne odisiel.
#
# VYSTUP:
#   out/cleaned_log4_rlength.csv - to iste + novy stlpec
#   SESSION_ID (cislo sedenia: 1, 2, 3, ...).
#
# POUZITE KNIZNICE:
#   pandas - praca s tabulkou (CSV)
#   numpy  - matematicke funkcie (logaritmus)
#
# OCAKAVANY VYSLEDOK: cca 8000 sedeni.
# ==========================================================

import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))  # umoznuje spustenie skriptu odkialkolvek (nielen z jeho priecinka)

import pandas as pd                  # praca s tabulkou (CSV log)
import numpy as np                   # potrebujeme logaritmus (np.log)

# === KROK 1: Nacitanie logu ===
df = pd.read_csv("in/cleaned_log4_length.csv")  # tabulka klikov so stlpcom Length

# === KROK 2: Vypocet casoveho prahu ===
# Prah = -ln(1 - 0.4) * priemerny cas na stranke.
# Vyssie p (40%) urcuje, kolko najkratsich casov povazujeme za "len preklikol".
p = 0.4                              # 40% stranok povazujeme za rychle navigacne kliky
mean_length = df["Length"].mean()    # priemerny cas na stranke (prazdne hodnoty sa preskakuju)
rlength = -np.log(1 - p) * mean_length  # vysledny prah v sekundach (asi 75 s)

print(f"Priemer Length: {mean_length:.2f}")
print(f"RLength = -ln(1 - {p}) * {mean_length:.2f} = {rlength:.2f} sekund")

# === KROK 3: Oznacenie zaciatkov sedeni ===
# Klik je zaciatok noveho sedenia v dvoch pripadoch:
#   1) Length je prazdne (NaN) - prvy klik cloveka alebo prerusenie.
#   2) Length je vacsie alebo rovne prahu - na predoslej stranke
#      bol clovek prilis dlho, takze ho povazujeme za odisleho.
df["NEW_SESSION"] = (df["Length"].isna()) | (df["Length"] >= rlength)

# === KROK 4: Cislovanie sedeni ===
# Trik: ked spocitavame True/False zhora nadol (True = 1, False = 0),
# kazde dalsie True zvysi sucet o 1. Tak vsetky kliky v tom istom
# sedeni dostanu rovnake cislo a nove sedenie dostane vyssie cislo.
# Priklad: NEW_SESSION = [T, F, F, T, F, T] -> SESSION_ID = [1, 1, 1, 2, 2, 3]
df["SESSION_ID"] = df["NEW_SESSION"].cumsum()

df = df.drop(columns=["NEW_SESSION"])  # pomocny stlpec uz nepotrebujeme

# === KROK 5: Ulozenie vysledku ===
df.to_csv("out/cleaned_log4_rlength.csv", index=False)  # index=False = neukladaj cisla riadkov

# Kontrolny vypis: ukazka prvych 20 riadkov a celkove pocty.
print(df[["USER_ID", "UNIXTIME", "Length", "SESSION_ID"]].head(20))
print(f"\nPocet zaznamov: {len(df)}")
print(f"Pocet sedeni: {df['SESSION_ID'].nunique()}")
