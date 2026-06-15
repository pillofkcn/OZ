# ==========================================================
# CV6 - Uloha 04: Statisticka analyza vysledkov
# ==========================================================
#
# CIEL:
#   Mame 4 rocne obdobia (O1=2009, O2=2010, O3=2011, O4=2012)
#   a pre kazde z nich sme v predoslych ulohach nasli "asociacne
#   pravidla" = pravidla typu "ked pouzivatel navstivi stranku A,
#   casto navstivi aj B". Tu chceme zistit: spravali sa pouzivatelia
#   v tychto 4 rokoch rovnako, alebo sa to medzi rokmi rozne lisi?
#
# TEORIA (jednoducho):
#
#   VYCHODISKO: tabulka ~450 pravidiel (riadky) x 4 roky (stlpce), v bunkach 0/1
#   (1 = pravidlo sa v danom roku objavilo, inak 0). To je vystup ulohy 03.
#
#   1) PRECO SPECIALNY TEST (a nie obycajny chi-kvadrat)
#   Tie iste pravidla meriame opakovane v 4 rokoch. Stlpce teda nie su nezavisle
#   skupiny, ale STALE TIE ISTE pravidla, len odmerane 4-krat. Na taketo "parove"
#   data 0/1 sa hodi Cochranov Q test (chi-kvadrat by tu nesedel - ten chce
#   nezavisle skupiny).
#
#   2) COCHRANOV Q TEST - hovori CI su rozdiely
#   Otazka: objavuje sa pravidlo rovnako casto vo vsetkych 4 rokoch, alebo niektory
#   rok vybocuje? Test scita jednotky v kazdom roku a pozrie sa, ako velmi sa tie
#   sucty lisia - cim vacsi rozdiel, tym vacsie cislo Q. Z Q sa odvodi p-hodnota
#   (= sanca, ze by taky rozdiel vznikol cistou nahodou, keby v skutocnosti nebol):
#     - p < 0.05  -> rozdiely medzi rokmi su skutocne,
#     - p >= 0.05 -> rozdiel moze byt len nahoda.
#
#   3) KENDALLOV KOEFICIENT W - hovori KOLKO
#   Cochran povie len ANO/NIE. Kendallovo W je cislo 0 az 1 a meria zhodu medzi
#   rokmi: 0 = roky sa spravaju uplne inak, 1 = roky maju takmer rovnake pravidla.
#   Pri datach 0/1 sa da vyratat priamo z Q:
#     W = Q / (n * (k - 1)),  n = pocet pravidiel, k = pocet rokov.
#     (menovatel n*(k-1) je najvacsie mozne Q, preto podiel vyjde pekne 0..1.)
#   Priklad: Q=120, n=100, k=4 -> W = 120 / (100*3) = 0.4 (stredna zhoda).
#   Spolu: Cochran povie "ci sa lisia", Kendall "ako velmi sa (ne)lisia".
#
# VSTUP:
#   in/matica_pravidiel.csv  - 450 pravidiel, stlpce O1..O4 (0/1)
#                              a stlpec pocet_obdobi (v kolkych
#                              rokoch sa pravidlo vyskytlo).
#
# VYSTUP:
#   stdout          - vysledky oboch testov + strucne zhrnutie (pocty/rok, distribucia, zaver)
#   out/analyza.png - dva grafy vedla seba (pocty po rokoch + stabilita pravidiel),
#                     vizualizacia pre rychly prehlad ("zosumarizovanie" zo zadania).
#
# POUZITE KNIZNICE:
#   - pandas: praca s tabulkou (citanie CSV, scitavanie stlpcov)
#   - matplotlib: kreslenie stlpcovych grafov
#   - statsmodels: hotova implementacia Cochranovho Q testu
#
# ALGORITMUS:
#   Nacitaj tabulku -> spusti Cochranov Q test -> vypocitaj Kendallovo W ->
#   vypis strucne zhrnutie -> nakresli 2 grafy.
# ==========================================================

import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))  # nastavi pracovny priecinok na ten, kde lezi tento skript - vdaka tomu cesty "in/..." a "out/..." funguju aj ked skript spustis odinakial

import pandas as pd                                          # praca s tabulkou
import matplotlib.pyplot as plt                              # kreslenie grafov
from statsmodels.stats.contingency_tables import cochrans_q  # hotovy Cochranov Q test

# === KROK 1: Nacitanie tabulky pravidiel ===

matica = pd.read_csv("in/matica_pravidiel.csv")              # binarna matica (~450 pravidiel) z ulohy 03

# Stlpce obdobi maju nazvy O1_2009 ... O4_2012 - vsetky zacinaju pismenom "O".
# Prejdeme nazvy vsetkych stlpcov tabulky (matica.columns) a do zoznamu odlozime
# len tie, ktore zacinaju "O". Tym ich vyberieme dynamicky (funguje, aj keby
# pribudli dalsie obdobia). startswith("O") = vrati True, ak nazov zacina na "O".
obdobia_stlpce = []
for nazov_stlpca in matica.columns:
    if nazov_stlpca.startswith("O"):
        obdobia_stlpce.append(nazov_stlpca)

print(f"Nacitanych pravidiel: {len(matica)}")                # kontrola - ocakavame ~450

# === KROK 2: Cochranov Q test ===
# Otazka: lisi sa pravdepodobnost vyskytu pravidla medzi rokmi?
# Test potrebuje cistu maticu cisel 0/1 (riadky = pravidla, stlpce = roky).
# matica[obdobia_stlpce] = vyber len stlpce rokov; .values = z pandas tabulky
# vytiahne len hole cisla (bez nazvov stlpcov a riadkov), tak ako to test chce.
binarna_matica = matica[obdobia_stlpce].values
result = cochrans_q(binarna_matica)                          # vrati objekt: .statistic (Q), .pvalue (p), .df (stupne volnosti)

print(f"\n=== Cochranov Q test ===")
print(f"Q statistika: {result.statistic:.4f}, p={result.pvalue:.6f}, df={result.df}")

# p < 0.05 = rozdiely medzi rokmi su skutocne (nie nahodne). Podla toho vyberieme text.
if result.pvalue < 0.05:
    zaver_q = "EXISTUJU rozdiely"
else:
    zaver_q = "Bez vyznamnych rozdielov"
print(f"Zaver: {zaver_q}")

# === KROK 2b: Kendallov koeficient W ===
# Cochran povie len ANO/NIE. Kendallovo W povie KOLKO - zhoda 0 az 1.
# Pre binarne data sa W da dopocitat priamo z Cochranovej Q statistiky.
n_rules = len(matica)                                        # n = pocet pravidiel
k_obdobi = len(obdobia_stlpce)                               # k = pocet obdobi (4)
# Vzorec W = Q / (n * (k - 1)). Menovatel je najvacsie mozne Q, takze W vyjde 0..1
# (0 = ziadna zhoda medzi rokmi, 1 = uplna zhoda). Detaily + priklad su v hlavicke.
kendall_w = result.statistic / (n_rules * (k_obdobi - 1))
print(f"\n=== Kendallov W (koeficient konkordancie) ===")
print(f"W = {kendall_w:.4f}  (n={n_rules}, k={k_obdobi})")

# Preklad cisla W na slovo (hranice su konvencia): cim vyssie W, tym
# podobnejsie su si pravidla naprie rokmi.
if kendall_w < 0.3:
    interpret = "slaba zhoda - pravidla sa medzi obdobiami vyrazne lisia"
elif kendall_w < 0.5:
    interpret = "stredna zhoda - ciastocne stabilne, ciastocne odlisne"
elif kendall_w < 0.7:
    interpret = "silnejsia zhoda - pravidla su prevazne stabilne naprie obdobiami"
else:
    interpret = "silna zhoda - pravidla su konzistentne naprie obdobiami"
print(f"Interpretacia: {interpret}")

# === KROK 3: Zhrnutie vysledkov (zosumarizovanie) ===
# Test povie, CI su rozdiely, ale nie KDE. Tu si spocitame konkretne pocetnosti,
# z ktorych zaver lepsie vidno.

# Pre kazdy rok scitame jeho stlpec. matica[stlpec].sum() = sucet stlpca; kedze su
# v nom len 0/1, sucet = pocet jednotiek = pocet pravidiel v danom roku.
pocty_pravidiel = []  # sem ulozime pocet pravidiel pre kazdy rok
for stlpec in obdobia_stlpce:
    pocty_pravidiel.append(matica[stlpec].sum())

sumar = pd.DataFrame({
    "Obdobie": obdobia_stlpce,        # nazvy rokov O1..O4
    "Pocet_pravidiel": pocty_pravidiel,
})
print(f"\n=== Pocty pravidiel po obdobiach ===")
print(sumar.to_string(index=False))                          # index=False = bez stlpca s cislami riadkov

# value_counts cez stlpec pocet_obdobi (z ulohy 03): kolko pravidiel sa
# vyskytlo v 1 / 2 / 3 / 4 rokoch. sort_index zoradi od 1 po 4.
counts = matica["pocet_obdobi"].value_counts().sort_index()
print(f"\nDistribucia poctu obdobi vyskytu:\n{counts.to_string()}")

# --- Konsolidovany zaver: spoji vysledky oboch testov do par viet ---
# stabilne = pravidla, ktore boli vo vsetkych obdobiach (pocet_obdobi == pocet rokov).
stabilne = (matica["pocet_obdobi"] == k_obdobi).sum()
print(f"\n=== ZHRNUTIE ===")
print(f"Cochranov Q = {result.statistic:.2f}, p = {result.pvalue:.6f} -> {zaver_q} medzi obdobiami.")
print(f"Kendallovo W = {kendall_w:.4f} -> {interpret}.")
print(f"Pocet pravidiel klesol z {pocty_pravidiel[0]} (prve obdobie) na {pocty_pravidiel[-1]} (posledne).")
print(f"Vo vsetkych {k_obdobi} obdobiach sa vyskytlo {stabilne} pravidiel (stabilne jadro).")

# === KROK 4: Vizualizacia (dva grafy vedla seba) ===
fig, axes = plt.subplots(1, 2, figsize=(14, 5))             # 1 platno, 2 grafy; axes[0]=vlavo, axes[1]=vpravo

# Lavy graf — pocet pravidiel po rokoch:
# vyska stlpca = kolko pravidiel preslo prahmi v danom roku. Vyssi = pravidelnejsie
# spravanie; klesajuce stlpce = spravanie sa stava roztrustenejsim. Prave tieto
# rozdiely vo vyske meria Cochranov Q.
axes[0].bar(sumar["Obdobie"], sumar["Pocet_pravidiel"], color="steelblue")
axes[0].set_title("Pocet asociacnych pravidiel po obdobiach")
axes[0].set_xlabel("Obdobie (rok)")
axes[0].set_ylabel("Pocet pravidiel")
for i, v in enumerate(sumar["Pocet_pravidiel"]):
    axes[0].text(i, v + 5, str(v), ha="center")             # hodnota nad stlpcom

# Pravy graf — stabilita pravidiel (distribucia pocet_obdobi):
# os X = v kolkych rokoch sa pravidlo vyskytlo (1-4), vyska = kolko pravidiel ma ten
# pocet. Stlpec nad "1" = jednorazove, nad "4" = stabilne jadro. Cim viac vpravo,
# tym podobnejsie su si roky -> vyssie Kendallovo W. Tento graf je vizualnym
# vysvetlenim cisla W.
axes[1].bar(counts.index, counts.values, color="coral")
axes[1].set_title("Distribucia pravidiel podla poctu obdobi vyskytu")
axes[1].set_xlabel("V kolkych obdobiach sa pravidlo vyskytuje")
axes[1].set_ylabel("Pocet pravidiel")
axes[1].set_xticks([1, 2, 3, 4])                            # na osi X len cele cisla 1..4
for i, v in zip(counts.index, counts.values):
    axes[1].text(i, v + 3, str(v), ha="center")             # hodnota nad stlpcom

plt.tight_layout()                                          # doladi okraje, aby sa nic neorezalo
plt.savefig("out/analyza.png", dpi=150)                     # uloz do PNG; dpi=150 = vyssia kvalita
print("\nGraf ulozeny -> out/analyza.png")
