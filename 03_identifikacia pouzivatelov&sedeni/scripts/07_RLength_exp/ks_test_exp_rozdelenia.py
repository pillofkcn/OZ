# ==========================================================
# CV2 - Uloha 07: Ma premenna Length exponencialne rozdelenie?
# ==========================================================
#
# CIEL:
#   V predoslej ulohe sme pre kazdy klik pouzivatela vypocitali Length =
#   pribilizny cas straveny na stranke (sekundy), ako rozdiel casu medzi
#   tymto a nasledujucim klikom toho isteho pouzivatela. Teraz overujeme,
#   ci tieto casy maju "exponencialne rozdelenie" - taky tvar krivky, kde
#   je vela kratkych hodnot a malo dlhych (typicke pre cakacie casy).
#
# PRECO TO TESTUJEME:
#   Ak Length ma exponencialne rozdelenie, mozeme hranicny cas sedenia
#   (STT) odhadnut kvantilovou funkciou STT = -ln(1-q) * priemer.
#   Ak nema, pouzijeme kvartilovy odhad Q3 + 1.5*IQR.
#
# TEORIA - co je exponencialne rozdelenie:
#   Rozdelenie, kde je vela kratkych hodnot a malo velmi dlhych (ma "dlhy chvost").
#   Riadi sa jednym cislom "lambda" (frekvencia). Plati:
#     - priemer hodnot = 1/lambda
#     - median (prostredna hodnota) = ln(2)/lambda, cca 0.693 * priemer
#     - standardna odchylka = priemer (hodnoty su velmi rozhadzane)
#   Dosledok: ak je priemer vyrazne vacsi ako median, je to znak dlheho chvosta,
#   co exponencialnemu rozdeleniu sedi. Priklad: priemer 150 s, median ~104 s
#   (= 0.693 * 150) by exponencialnemu rozdeleniu zodpovedalo.
#
# TEORIA - co je KS test (Kolmogorov-Smirnov):
#   Statisticky test, ktory porovna ci nase data vyzeraju ako dana krivka.
#   Vyhodi dve cisla:
#     - KS statistika: najvacsi rozdiel medzi nasimi datami a teoriou
#       (cislo medzi 0 a 1; cim mensie, tym lepsia zhoda).
#     - p-hodnota: pravdepodobnost, ze by sme nahodou dostali taky velky
#       rozdiel, keby data naozaj boli z tej krivky.
#   Pravidlo: ak p-hodnota < 0.05, tak data NIE SU z danej krivky.
#
# VSTUP:
#   in/03_length.csv - tabulka z predoslej ulohy so stlpcom Length.
#                                Niektore riadky maju Length prazdne (NaN) -
#                                tam, kde uzivatel uz dalej neklikol.
# VYSTUP:
#   stdout                  - pocet hodnot, priemer, median, std,
#                             vysledok KS testu a slovny zaver.
#   out/07_rlength_exp.png  - graf: histogram Length + teoreticka exp. krivka.
#
# POUZITE KNIZNICE:
#   pandas             - praca s tabulkami (nacitanie CSV, filtrovanie).
#   matplotlib.pyplot  - kreslenie grafu.
#   scipy.stats        - statisticke nastroje (KS test, exp. rozdelenie).
#
# ALGORITMUS:
#   Nacitaj Length, spocitaj zakladne statistiky, spusti KS test proti
#   exponencialnemu rozdeleniu, nakresli histogram s krivkou, uloz PNG.
# ==========================================================

import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))  # umoznuje spustenie skriptu odkialkolvek (nielen z jeho priecinka)

import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import kstest   # test, ci data vyzeraju ako dana krivka
from scipy.stats import expon    # objekt exponencialneho rozdelenia; expon.pdf(x,...) = teoreticka krivka (hustota pravdepodobnosti)

# === KROK 1: Nacitanie dat ===
df = pd.read_csv("in/03_length.csv")  # nacitame tabulku zo vstupu
# dropna() = odstrani vsetky prazdne (NaN) hodnoty zo stlpca. Length chyba pri
# poslednom kliku usera (nema dalsi klik); do testu chceme len realne casy.
length_data = df["Length"].dropna()

# === KROK 2: Zakladne statistiky ===
# Vypiseme cisla, ktore napovedaju ci data mozu byt exponencialne:
# pri exp. rozdeleni byva priemer ~ standardna odchylka a median ~ 0.69 * priemer.
print(f"Pocet hodnot Length: {len(length_data)}")
print(f"Priemer: {length_data.mean():.2f}")     # priemerny cas na stranke
print(f"Median: {length_data.median():.2f}")    # prostredna hodnota (polovica je mensia)
print(f"Std: {length_data.std():.2f}")          # ako velmi sa hodnoty rozhadzuju okolo priemeru

# === KROK 3: KS test (zhoda s exponencialnym rozdelenim) ===
# Co testujeme:
#   H0 (zaciatocny predpoklad): data SU z exponencialneho rozdelenia.
#   H1 (opak):                  data NIE SU z exponencialneho rozdelenia.
# Ak p-hodnota < 0.05, H0 zamietame -> data nie su exponencialne.
#
# Parametre kstest:
#   "expon"           - chceme porovnat s exponencialnym rozdelenim.
#   args=(0, mean)    - prvy 0 znamena, ze rozdelenie zacina v nule
#                       (Length nemoze byt zaporna);
#                       druhy parameter je "scale" = priemer dat
#                       (odhad parametra lambda zo samotnych dat).
#                       Pozn.: scale je 1/lambda (cize priemer); lambda
#                       samotnu by sme dostali ako 1/priemer.
ks_stat, p_value = kstest(length_data, "expon", args=(0, length_data.mean()))
print(f"\nKolmogorov-Smirnov test:")
print(f"KS statistika: {ks_stat:.4f}")          # najvacsi rozdiel medzi datami a krivkou
print(f"P-hodnota: {p_value:.6f}")              # ak < 0.05 -> zamietame H0

# Slovny zaver podla hranice 0.05 (bezna konvencia v statistike).
if p_value < 0.05:
    print("Zamietame H0 - data NEMAJU exponencialne rozdelenie (p < 0.05)")
else:
    print("Nezamietame H0 - data MAJU exponencialne rozdelenie (p >= 0.05)")

# === KROK 4: Priprava grafu ===
# Test povie len ano/nie; graf navyse vizualne ukaze, ako sa data podobaju krivke.
# subplots() = jeden graf; figsize = sirka a vyska v palcoch.
fig, ax = plt.subplots(figsize=(8, 5))

# === KROK 5: Histogram dat + teoreticka krivka ===
# Histogram ukaze, ako su nase Length rozhadzane (kolko hodnot kde pada).
# bins=50      - data rozdelime na 50 stlpcov.
# density=True - prepocita stlpce tak, aby plocha pod histogramom bola 1
#                (rovnako ako pod teoretickou krivkou, aby sa dali porovnat).
ax.hist(length_data, bins=50, density=True, alpha=0.7, label="Length data")
# Teoreticka krivka exponencialneho rozdelenia s nasim priemerom.
# Ak data sediu, histogram a krivka by sa mali prekryvat.
x = range(0, int(length_data.max()))
ax.plot(x, expon.pdf(x, 0, length_data.mean()), "r-", label="Exp. rozdelenie")
ax.set_title("Histogram Length vs Exponencialne rozdelenie")
ax.set_xlabel("Cas na stranke (s)")
ax.set_ylabel("Hustota")
ax.legend()
ax.set_xlim(0, 1000)  # zobrazime len do 1000 s; vyssie hodnoty su velmi zriedkave

plt.tight_layout()  # automaticky upravi okraje, aby sa popisky neprekryvali

# === KROK 6: Ulozenie grafu ===
# dpi=150 = dostatocna ostrost pre tlac aj prezentaciu.
plt.savefig("out/07_rlength_exp.png", dpi=150)
plt.show()  # zobrazi okno s grafom (uzitocne pri lokalnom behu)
print("\nGraf ulozeny do out/07_rlength_exp.png")
