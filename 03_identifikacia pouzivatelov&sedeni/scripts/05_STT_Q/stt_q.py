# ==========================================================
# CV2 - Uloha 05: Identifikacia sedeni metodou STT_Q
# ==========================================================
#
# CIEL: Rozdelit kliky kazdeho pouzivatela na samostatne sedenia (suvisle navstevy).
#       Sedenie skoncime, ked je pauza medzi dvoma klikmi privelka. Hranicu pauzy
#       urcime z kvartilov (STT_Q = robustny odhad nezavisly na extremnych pauzach).
#
# TEORIA (jednoducho):
#   - STT = Session Timeout Threshold (hranica casu necinnosti, po ktorej
#     povazujeme sedenie za ukoncene).
#   - STT_Q = variant odhadnuty z kvartilov (preto _Q).
#   - Length = cas medzi tymto a predoslym klikom toho isteho pouzivatela.
#   - Q1 = hodnota, pod ktorou lezi 25 % vsetkych pauz (kratke pauzy).
#   - Q3 = hodnota, pod ktorou lezi 75 % vsetkych pauz.
#   - IQR = Q3 - Q1 = sirka "stredneho 50 %" pauz (typicky rozsah).
#   - STT_Q = Q3 + 1.5 * IQR = hranica, nad ktorou je pauza neprirodzene dlha.
#     Ked je pauza vacsia, povieme ze pouzivatel uz odisiel a vratil sa neskor
#     => zaciname mu nove sedenie.
#   - PRECO kvartily a nie priemer: jedna par-dnova pauza vie potiahnut priemer
#     hore a vysledok je nezmyselny. Kvartily extremne hodnoty ignoruju.
#
# VSTUP:  in/03_length.csv  - log z ulohy 03, uz ma vypocitany stlpec Length
# VYSTUP: out/05_stt_q.csv  - ten isty log + novy stlpec SESSION_ID
#
# POUZITE KNIZNICE:
#   pandas - praca s tabulkou v pamati (rychle operacie nad celymi stlpcami).
#
# ALGORITMUS:
#   Spocitam Q1, Q3, IQR z Length, urcim prah STT_Q, oznacim zaciatky sedeni
#   (prvy klik usera alebo prilis dlha pauza) a postupne im pridelim cisla 1, 2, 3...
# ==========================================================

import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))  # umoznuje spustenie skriptu odkialkolvek (nielen z jeho priecinka)

import pandas as pd

# === KROK 1: Nacitanie logu ===
# Nacitame log, ktory uz ma stlpec Length z predchadzajucej ulohy.
df = pd.read_csv("in/03_length.csv")

# === KROK 2: Vypocet prahu STT_Q ===
q1 = df["Length"].quantile(0.25)   # 25 % pauz je kratsich ako q1
q3 = df["Length"].quantile(0.75)   # 75 % pauz je kratsich ako q3
iqr = q3 - q1                      # typicka sirka pauz (stredne 50 %)
stt_q = q3 + 1.5 * iqr             # nad touto hranicou je pauza "privelka" = koniec sedenia

print(f"Q1: {q1:.2f}, Q3: {q3:.2f}, IQR: {iqr:.2f}")
print(f"STT_Q (Q3 + 1.5*IQR): {stt_q:.2f} sekund")

# === KROK 3: Oznacenie zaciatkov sedeni ===
# Riadok zacina nove sedenie, ak:
#   a) Length je prazdne (NaN) = je to prvy klik pouzivatela, nema predchodcu.
#   b) Length je vacsie alebo rovne prahu = medzi klikmi bola privelka pauza.
df["NEW_SESSION"] = (df["Length"].isna()) | (df["Length"] >= stt_q)

# === KROK 4: Priradenie cisla sedenia ===
# cumsum() na stlpci True/False scita postupne True ako 1 a False ako 0.
# Cislo sa zvysi prave tam, kde zacina nove sedenie. Vsetky kliky v jednom
# sedeni tak dostanu rovnake cislo.
# Priklad:  NEW_SESSION:  T F F T F F T
#           SESSION_ID:   1 1 1 2 2 2 3
df["SESSION_ID"] = df["NEW_SESSION"].cumsum()

# Pomocny stlpec uz nepotrebujeme, do vystupu nepatri.
df = df.drop(columns=["NEW_SESSION"])

# === KROK 5: Ulozenie vystupu ===
# index=False = nepridame umely cislovaci stlpec navyse.
df.to_csv("out/05_stt_q.csv", index=False)

# Kontrolny vypis: prvych 20 riadkov a celkove pocty.
print(df[["USER_ID", "UNIXTIME", "Length", "SESSION_ID"]].head(20))
print(f"\nPocet zaznamov: {len(df)}")
# nunique() = pocet roznych hodnot SESSION_ID = pocet sedeni. Zadanie ocakava cca 7500.
print(f"Pocet sedeni: {df['SESSION_ID'].nunique()}")
