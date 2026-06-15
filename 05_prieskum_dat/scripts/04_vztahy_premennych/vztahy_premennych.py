# ==========================================================
# CV5 - Uloha 04: Vztahy medzi premennymi
# ==========================================================
#
# CIEL:
#   Zistit, ci dvojice premennych v logoch banky spolu suvisia
#   (napr. ci sa pocas krizy citaju ine kategorie obsahu).
#   Nestaci povedat "suvisia" - chceme aj cislo o sile vztahu.
#
# TEORIA (od nuly):
#
#   1) CO ZNAMENA "VZTAH MEDZI PREMENNYMI"
#   Dve premenne spolu suvisia, ked hodnota jednej nieco prezradi o druhej.
#   Priklad: ak sa pocas krizy citali ine kategorie ako po krize, potom
#   "obdobie" a "kategoria" suvisia. Ak je rozlozenie kategorii rovnake bez
#   ohladu na obdobie, nesuvisia.
#
#   2) KONTINGENCNA TABULKA (crosstab)
#   Zaklad pre dve TEXTOVE premenne: tabulka, kde riadky = hodnoty prvej,
#   stlpce = hodnoty druhej a v bunke je POCET, kolkokrat dana kombinacia
#   nastala. Z nej sa da vycitat, ci su niektore kombinacie castejsie, nez
#   by sme cakali pri nahode.
#
#   3) CHI-KVADRAT TEST (chi2)
#   Spocita, ako velmi sa SKUTOCNE pocty v tabulke lisia od poctov, ktore by
#   sme cakali, KEBY premenne vobec nesuviseli (boli nezavisle). Velky rozdiel
#   = velke chi2 = premenne zrejme suvisia.
#
#   4) p-HODNOTA (vysvetlena od nuly)
#   Test vrati p-hodnotu = pravdepodobnost, ze by sme videli TAKY (alebo este
#   vacsi) rozdiel CISTE NAHODOU, keby v skutocnosti ziadny vztah nebol.
#     - mala p (typicky < 0.05) = nahoda je nepravdepodobna -> vztah asi existuje,
#     - velka p = pokojne to mohla byt nahoda -> vztah nevieme potvrdit.
#   POZOR (dolezite pri tomto datasete): p-hodnota silno zavisi od poctu
#   riadkov. Pri ~2 milionoch zaznamov vyjde p takmer vzdy ~0 a "vsetko je
#   signifikantne" - aj uplne triviálny vztah. Preto sama p-hodnota tu
#   nestaci a potrebujeme mieru SILY vztahu (bod 5).
#
#   5) CRAMEROVO V (sila vztahu, 0 az 1)
#   Samotne chi2 rastie s velkostou vzorky, takze sa neda porovnavat medzi
#   tabulkami. Cramerovo V chi2 "znormuje" (vydeli najvyssou moznou hodnotou),
#   takze vyjde cislo 0-1 nezavisle od poctu riadkov:
#     0 = ziadny vztah, ~0.1 slaby, ~0.3 stredny, ~0.5+ silny.
#   Toto je cislo, ktoremu pri velkych datach veris viac nez p-hodnote.
#
#   6) ANOVA (Analysis Of Variance = analyza rozptylu)
#   Pouzije sa, ked jedna premenna je CISLO (cas) a druha KATEGORIA (typ
#   stranky). Otazka: maju jednotlive kategorie rozne PRIEMERNE casy, alebo
#   su rozdiely len nahodny sum? ANOVA porovna rozdiely priemerov MEDZI
#   skupinami s rozptylom VNUTRI skupin a vrati F-statistiku a p-hodnotu.
#   F = (rozptyl priemerov MEDZI skupinami) / (rozptyl VNUTRI skupin):
#   velke F = skupiny sa vyrazne lisia, male F = su podobne.
#   Pozn.: ANOVA predpoklada zhruba normalne rozdelenie; cas na stranke je
#   skoseny, takze vysledok beriem orientacne.
#
# VSTUP:
#   in/logs5.csv - POSKYTNUTY bankovy dataset (zo studie v materials/),
#                  oddelovac ';', cca 2 mil. riadkov. Nie je to vystup cv1-4,
#                  ale length/frame/anonIP/unixTime zodpovedaju premennym z cv1-4.
#   Klucove stlpce:
#     category (text)  - typ obsahu stranky (DV - co pouzivatel cital)
#     crisis   (0/1)   - 1 ak pristup spada do obdobia krizy
#     year     (cislo) - rok pristupu
#     internal (0/1/2) - odkial pristup prisiel: 0 = zvonku (mimo banky),
#                        1 = z vnutornej siete banky, 2 = z IT firmy spravujucej web
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
os.chdir(os.path.dirname(os.path.abspath(__file__)))  # nastavi pracovny priecinok na ten, kde lezi tento skript - vdaka tomu cesty "in/..." funguju aj ked skript spustis odinakial

import pandas as pd
import numpy as np
from scipy.stats import chi2_contingency, f_oneway

# === KROK 1: Nacitanie dat ===
# Celu tabulku potrebujeme v pamati, lebo testy pocitaju nad vsetkymi riadkami.
print("Nacitavam dataset...")
# sep=";" = stlpce su oddelene bodkociarkou; quotechar='"' = pole s ciarkou
# vnutri (napr. URL) drzia uvodzovky ako jednu hodnotu; low_memory=False =
# pandas precita cely subor naraz a spravne urci typ kazdeho stlpca.
df = pd.read_csv("in/logs5.csv", sep=";", quotechar='"', low_memory=False)


def cramers_v(chi2, n, r, c):
    """Cramerovo V - sila vztahu medzi dvoma kategorickymi premennymi (0 az 1).

    0 = ziadny vztah, 1 = perfektny vztah.

    Preco to ratame: samotna chi2 hodnota sa neda porovnavat medzi roznymi
    tabulkami - rastie s poctom riadkov. V ju "znormuje" na pekny ukazovatel.

    Parametre: chi2 = vystup chi2 testu, n = pocet vsetkych pozorovani,
               r, c = pocet riadkov a stlpcov tabulky frekvencii.
    """
    # Vzorec: V = odmocnina( chi2 / (n * (min(r,c) - 1)) ).
    # Preco delime: n*(min(r,c)-1) je najvacsie chi2, ake pri danej velkosti
    # vzorky a tabulky moze vyjst. Podielom teda chi2 prepocitame na rozsah 0..1
    # (0 = ziadny vztah, 1 = maximalny), nezavisle od poctu riadkov.
    # np.sqrt() = druha odmocnina. Priklad: chi2=500, n=100000, min(r,c)=2 ->
    #   V = sqrt(500 / (100000*1)) = sqrt(0.005) = 0.07 (velmi slaby vztah).
    return np.sqrt(chi2 / (n * (min(r, c) - 1)))


def interpretuj_v(v):
    # Preklad cisla V na slovne hodnotenie sily vztahu (hranice su konvencia).
    if v < 0.1: return "velmi slaba"   # prakticky ziadny vztah
    if v < 0.3: return "slaba"         # vztah existuje, ale maly
    if v < 0.5: return "stredna"       # vidno jasny trend
    return "silna"                      # premenne spolu silno suvisia


def chi2_test(df, col1, col2):
    """Chi2 test nezavislosti pre dvojicu kategorickych stlpcov.

    Postup:
      1) crosstab = kontingencna tabulka: riadky = hodnoty col1, stlpce = col2,
         bunka = pocet, kolkokrat ta kombinacia nastala.
      2) chi2 test = lisia sa skutocne pocty od pripadu "premenne nesuvisia"?
      3) Cramerovo V = ako silny ten vztah je (lebo chi2 pri velkych datach klame).
    """
    tabulka = pd.crosstab(df[col1], df[col2])      # kontingencna tabulka poctov dvojic
    chi2, p, dof, _ = chi2_contingency(tabulka)    # test vrati: chi2, p-hodnotu, stupne volnosti, (ocakavane pocty - tie nepotrebujeme, preto "_")
    n = tabulka.sum().sum()                        # sucet vsetkych buniek = pocet vsetkych pozorovani
    cv = cramers_v(chi2, n, *tabulka.shape)        # *tabulka.shape = rozbali dvojicu (pocet_riadkov, pocet_stlpcov) na argumenty r, c
    return chi2, p, dof, cv, tabulka


# === TESTY ===
# Spustime 4 testy: 3x chi2 (kategoria vs kategoria) + 1x ANOVA (cas vs kategoria).
# Dvojice su vybrane tak, aby pokryli vsetky skupiny premennych zo zadania.

# === TEST 1: kategoria vs kriza ===
# Otazka: citaju ludia pocas krizy ine kategorie ako mimo nej?
print(f"\n=== TEST 1: kategoria vs kriza ===")
chi2_1, p_1, dof_1, cv_1, tab_1 = chi2_test(df, "category", "crisis")  # funkcia vrati 5 hodnot naraz
# Citaj V, nie p: pri ~2 mil. riadkov je p skoro vzdy ~0. V (0-1) = realna sila vztahu.
print(f"chi2={chi2_1:.2f}, p={p_1:.6f}, V={cv_1:.4f} ({interpretuj_v(cv_1)})")

# === TEST 2: kategoria vs internal ===
# Otazka: pozeraju ludia z roznych miest (zvonku / vnutorna siet banky / IT firma)
# rozne kategorie obsahu? (internal ma tri hodnoty 0/1/2.)
print(f"\n=== TEST 2: kategoria vs internal ===")
chi2_2, p_2, dof_2, cv_2, _ = chi2_test(df, "category", "internal")  # posledny vystup (tabulka) tu nepotrebujeme -> "_"
print(f"chi2={chi2_2:.2f}, p={p_2:.6f}, V={cv_2:.4f} ({interpretuj_v(cv_2)})")

# === TEST 3: ANOVA - cas na stranke vs kategoria ===
# Tu je jedna premenna CISLO (cas) a druha KATEGORIA -> nie chi2, ale ANOVA.
# Otazka: maju rozne kategorie rozny priemerny cas na stranke?
print(f"\n=== TEST 3: ANOVA - cas vs kategoria ===")

# Do casovej analyzy pustime len realne casy (length > 0). Nuly su roboti a
# zaporne hodnoty (-1, -2) su konce sedeni - nie su to skutocne casy citania.
df_clean = df[df["length"] > 0]

# ANOVA chce pre kazdu kategoriu SAMOSTATNE pole jej casov.
# Riadok nizsie je list-comprehension = skrateny zapis na vytvorenie zoznamu:
#   [ vyraz  for k in zoznam ]  znamena "pre kazde k zo zoznamu vytvor vyraz".
# Tu pre kazdu kategoriu k vyberieme jej riadky a z nich stlpec length;
# .values = prerobi ten stlpec na obycajne pole cisel. Vysledok = zoznam poli,
# jedno pole casov na kazdu kategoriu.
skupiny = [df_clean[df_clean["category"] == k]["length"].values
           for k in df_clean["category"].unique()]

# f_oneway = ANOVA test, porovna priemery skupin. *skupiny = "rozbali" zoznam
# poli na samostatne argumenty (kazda kategoria ide do funkcie ako vlastny vstup).
# Vrati F-statistiku a p-hodnotu (F = rozptyl medzi skupinami / rozptyl vnutri skupin).
f_stat, p_anova = f_oneway(*skupiny)
print(f"F={f_stat:.2f}, p={p_anova:.6f}")

# === TEST 4: kategoria vs rok ===
# Otazka: menia sa typy citaneho obsahu medzi rokmi (vyvoj zaujmu v case)?
print(f"\n=== TEST 4: kategoria vs rok ===")
chi2_4, p_4, dof_4, cv_4, _ = chi2_test(df, "category", "year")
print(f"chi2={chi2_4:.2f}, p={p_4:.6f}, V={cv_4:.4f} ({interpretuj_v(cv_4)})")
