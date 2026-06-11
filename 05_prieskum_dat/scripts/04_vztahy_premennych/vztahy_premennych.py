# ==========================================================
# CV4 - Uloha 04: Vztahy medzi premennymi
# ==========================================================
#
# CIEL:
#   Zistit, ci dvojice premennych v logoch banky spolu suvisia
#   (napr. ci sa pocas krizy citaju ine kategorie obsahu).
#   Nestaci povedat "suvisia" - chceme aj cislo o sile vztahu.
#
# TEORIA (jednoducho):
#   - chi2 test (chi-kvadrat): porovna, ci sa hodnoty jednej premennej
#     spravaju rovnako pri vsetkych hodnotach druhej premennej.
#     Vystup: p-hodnota. Ak je p < 0.05, premenne spolu suvisia.
#   - Cramerovo V: cislo od 0 do 1, ktore hovori, AKO SILNE spolu suvisia.
#     Samotne chi2 cislo rastie s velkostou vzorky (pri 2 milionoch
#     riadkov vyjde obrovske aj pri slabom vztahu), preto ho normujeme.
#   - ANOVA (Analysis Of Variance, analyza rozptylu): statisticky test,
#     ktory porovna priemery medzi viacerymi skupinami. Otazka: maju
#     vsetky skupiny rovnaky priemer, alebo sa aspon jedna lisi?
#     Pouzivame ju, ked jedna premenna je cislo (cas) a druha kategoria
#     (typ stranky). Otazka znie: maju jednotlive kategorie rozne
#     priemerne casy?
#
# VSTUP:
#   in/logs5.csv - cisteny dataset z cv1 (oddelovac ';', cca 2 mil. riadkov)
#   Klucove stlpce:
#     category (text)  - typ obsahu stranky (DV - co pouzivatel cital)
#     crisis   (0/1)   - 1 ak pristup spada do obdobia krizy
#     year     (cislo) - rok pristupu
#     internal (0/1)   - 1 ak pouzivatel prisiel z internej linky
#     length   (cislo) - cas straveny na stranke v sekundach
#
# VYSTUP:
#   stdout - 4 bloky s vysledkami (chi2/F, p-hodnota, sila vztahu).
#
# POUZITE KNIZNICE:
#   pandas - praca s tabulkou; crosstab vyrobi tabulku frekvencii
#   numpy  - matematika (odmocnina pre Cramerovo V)
#   scipy.stats - hotove statisticke testy (chi2, ANOVA)
#
# ALGORITMUS:
#   Nacitaj data -> pre kazdu dvojicu sprav crosstab + chi2 + Cramerovo V;
#   pre cas vs kategoria sprav ANOVA; vsetko vypis.
# ==========================================================

import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))  # umoznuje spustenie skriptu odkialkolvek (nielen z jeho priecinka)

import pandas as pd
import numpy as np
from scipy.stats import chi2_contingency, f_oneway

# === KROK 1: Nacitanie dat ===
# Potrebujeme celu tabulku v pamati, lebo testy pocitaju nad vsetkym.
print("Nacitavam dataset...")
df = pd.read_csv("in/logs5.csv", sep=";", quotechar='"', low_memory=False)
# sep=";" lebo cv1 ulozil data s bodkociarkou (URL casto obsahuju ciarku);
# quotechar='"' aby URL v uvodzovkach ostali ako jedno pole;
# low_memory=False aby pandas presne urcil typ kazdeho stlpca naraz.


def cramers_v(chi2, n, r, c):
    """Cramerovo V - sila vztahu medzi dvoma kategorickymi premennymi.

    Vrati cislo od 0 do 1:
      0 = ziadny vztah, 1 = perfektny vztah.

    Preco to ratame: samotna chi2 hodnota sa neda porovnavat medzi
    roznymi tabulkami - rastie s poctom riadkov v datach. Cramerovo V
    chi2 vydeli najvyssou moznou hodnotou, aby vysiel pekny ukazovatel.

    Parametre:
      chi2 - vystup chi2 testu
      n    - kolko riadkov dat sme spolu zratali
      r, c - kolko riadkov a stlpcov ma tabulka frekvencii
    """
    return np.sqrt(chi2 / (n * (min(r, c) - 1)))


def interpretuj_v(v):
    # Prelozime cislo Cramerovho V na slovne hodnotenie sily vztahu.
    if v < 0.1: return "velmi slaba"   # takmer ziadny vztah
    if v < 0.3: return "slaba"         # vztah je, ale maly
    if v < 0.5: return "stredna"       # vidno jasny trend
    return "silna"                      # premenne spolu silno suvisia


def chi2_test(df, col1, col2):
    """Spusti chi2 test pre dvojicu kategorickych stlpcov.

    Postup:
      1) Vyrobime tabulku, kde riadky = hodnoty col1, stlpce = hodnoty col2,
         a v bunkach je pocet, kolkokrat dana kombinacia nastala.
      2) chi2 test povie, ci sa hodnoty col1 spravaju rovnako pre vsetky
         hodnoty col2 (ak nie, premenne spolu suvisia).
      3) Spocitame Cramerovo V, aby sme vedeli, ako silny ten vztah je.
    """
    tabulka = pd.crosstab(df[col1], df[col2])      # tabulka s poctami dvojic
    chi2, p, dof, _ = chi2_contingency(tabulka)    # samotny test
    n = tabulka.sum().sum()                        # spolu vsetkych pozorovani
    cv = cramers_v(chi2, n, *tabulka.shape)        # sila vztahu (0-1)
    return chi2, p, dof, cv, tabulka


# === TESTY ===
# Sputame 4 testy: 3x chi2 (kategoria vs kategoria) + 1x ANOVA (cas vs kategoria).
# Vyber je taky, aby sme pokryli vsetky skupiny premennych zo zadania.

# === TEST 1: kategoria vs kriza ===
# Otazka: Citaju ludia pocas krizy ine kategorie obsahu ako mimo nej?
print(f"\n=== TEST 1: kategoria vs kriza ===")
chi2_1, p_1, dof_1, cv_1, tab_1 = chi2_test(df, "category", "crisis")
# Vypis: chi2 (velke cislo), p (moze byt velmi male), V (sila 0-1).
print(f"chi2={chi2_1:.2f}, p={p_1:.6f}, V={cv_1:.4f} ({interpretuj_v(cv_1)})")

# === TEST 2: kategoria vs internal ===
# Otazka: Pozeraju ludia ine kategorie, ked prisli z internej linky
# (preklik v banke) oproti tym, co prisli z vonku (Google, priamy vstup)?
print(f"\n=== TEST 2: kategoria vs internal ===")
chi2_2, p_2, dof_2, cv_2, _ = chi2_test(df, "category", "internal")  # tabulku tu uz nepotrebujeme
print(f"chi2={chi2_2:.2f}, p={p_2:.6f}, V={cv_2:.4f} ({interpretuj_v(cv_2)})")

# === TEST 3: ANOVA - cas na stranke vs kategoria ===
# Otazka: Travia pouzivatelia rozne dlhy cas na roznych typoch stranok?
# ANOVA porovna priemerny cas v kazdej kategorii a povie, ci sa lisia.
print(f"\n=== TEST 3: ANOVA - cas vs kategoria ===")

# Necheme nuly a zaporne casy:
#   length == 0 znamena, ze sme cas nevedeli zistit (posledny klik usera).
#   Tieto pripady by stiahli priemery dole.
df_clean = df[df["length"] > 0]

# Pre kazdu kategoriu si vytiahneme pole casov - ANOVA potrebuje samostatne
# pole pre kazdu skupinu, ktoru porovnavame.
skupiny = [df_clean[df_clean["category"] == k]["length"].values
           for k in df_clean["category"].unique()]

# *skupiny = posleme f_oneway kazdu kategoriu ako samostatny argument.
f_stat, p_anova = f_oneway(*skupiny)
print(f"F={f_stat:.2f}, p={p_anova:.6f}")

# === TEST 4: kategoria vs rok ===
# Otazka: Menia sa typy citaneho obsahu medzi rokmi?
# Ak ano, vidime vyvoj zaujmu pouzivatelov v case.
print(f"\n=== TEST 4: kategoria vs rok ===")
chi2_4, p_4, dof_4, cv_4, _ = chi2_test(df, "category", "year")
print(f"chi2={chi2_4:.2f}, p={p_4:.6f}, V={cv_4:.4f} ({interpretuj_v(cv_4)})")
