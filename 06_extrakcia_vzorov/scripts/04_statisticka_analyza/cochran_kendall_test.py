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
# TEORIA (od nuly - akoby si tieto testy nikdy nevidel):
#
#   VYCHODISKO: tabulka ~450 pravidiel (riadky) x 4 obdobia (stlpce),
#   v bunkach 0/1 (1 = pravidlo sa v danom roku objavilo, inak 0).
#
#   1) PRECO SPECIALNY TEST (a nie obycajny chi-kvadrat)
#   Tie iste pravidla meriame OPAKOVANE v 4 rokoch - stlpce teda nie su
#   nezavisle skupiny, ale OPAKOVANE MERANIA na tych istych objektoch
#   (ako keby si toho isteho cloveka testoval 4-krat). Na taketo "parove"
#   data 0/1 sa hodi Cochranov Q test, nie chi-kvadrat (ten predpoklada
#   nezavisle skupiny).
#
#   2) COCHRANOV Q TEST (od nuly)
#   Otazka: je pravdepodobnost, ze sa pravidlo objavi, ROVNAKA vo vsetkych
#   4 rokoch, alebo niektory rok vybocuje? Pozera sa na to, ci sa pocty
#   jednotiek po stlpcoch (rokoch) lisia viac, nez by cakal pri nahode.
#   Je to zovseobecnenie McNemarovho testu (ten je pre 2 merania) na k>=3
#   merani. Vrati Q statistiku a p-hodnotu.
#     - H0 (nulova hypoteza) = "vsetky roky maju rovnaku pravdepodobnost".
#     - p < 0.05 -> H0 zamietame -> medzi rokmi SU signifikantne rozdiely,
#     - p >= 0.05 -> rozdiely mozu byt len nahoda.
#   (p-hodnota = sanca, ze by sme videli taky rozdiel cisto nahodou, keby
#    v skutocnosti ziadny nebol.)
#
#   3) KENDALLOV KOEFICIENT W (od nuly)
#   Cochran povie iba ANO/NIE (su rozdiely?). Kendallovo W povie KOLKO -
#   cislo 0 az 1, ktore meria ZHODU (konkordanciu) medzi rokmi:
#     0 = roky sa spravaju uplne inak, 1 = roky maju temer identicke pravidla.
#   Pre binarne data sa da vyratat priamo z Cochranovej statistiky:
#     W = Q / (n * (k - 1)),  kde n = pocet pravidiel, k = pocet obdobi.
#   Cochran + Kendall sa doplnaju: prvy hovori "ci", druhy "ako velmi".
#
# VSTUP:
#   in/matica_pravidiel.csv  - 450 pravidiel, stlpce O1..O4 (0/1)
#                              a stlpec pocet_obdobi (v kolkych
#                              rokoch sa pravidlo vyskytlo).
#
# VYSTUP:
#   out/analyza.png  - dva grafy vedla seba (pocty + distribucia)
#   stdout           - vysledky testov a sumarne tabulky
#
# POUZITE KNIZNICE:
#   - pandas: praca s tabulkou (citanie CSV, scitavanie stlpcov)
#   - matplotlib: kreslenie stlpcovych grafov
#   - statsmodels: hotova implementacia Cochranovho Q testu
#
# ALGORITMUS:
#   Nacitaj tabulku -> spusti Cochranov Q test -> vypocitaj
#   Kendallovo W -> vypis pocty -> nakresli 2 grafy.
# ==========================================================

import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))  # umoznuje spustenie skriptu odkialkolvek (nielen z jeho priecinka)

import pandas as pd                                          # praca s tabulkou
import matplotlib.pyplot as plt                              # kreslenie grafov
from statsmodels.stats.contingency_tables import cochrans_q  # hotovy Cochranov Q test

# === KROK 1: Nacitanie tabulky pravidiel ===

matica = pd.read_csv("in/matica_pravidiel.csv")              # binarna matica (~450 pravidiel) z ulohy 03

# Stlpce obdobi maju nazvy O1_2009 ... O4_2012 - vsetky zacinaju "O".
# Vyberieme ich dynamicky (funguje aj keby pribudli dalsie obdobia).
obdobia_stlpce = [c for c in matica.columns if c.startswith("O")]

print(f"Nacitanych pravidiel: {len(matica)}")                # kontrola - ocakavame ~450

# === KROK 2: Cochranov Q test ===
# Otazka: lisi sa pravdepodobnost vyskytu pravidla medzi rokmi?
# Test potrebuje cistu 0/1 maticu (riadky = pravidla, stlpce = roky).
# .values = vytiahne len cisla (bez nazvov stlpcov), tak ako to test chce.
binarna_matica = matica[obdobia_stlpce].values
result = cochrans_q(binarna_matica)                          # vrati objekt: .statistic (Q), .pvalue (p), .df (stupne volnosti)

print(f"\n=== Cochranov Q test ===")
print(f"Q statistika: {result.statistic:.4f}, p={result.pvalue:.6f}, df={result.df}")

# p < 0.05 = rozdiely medzi rokmi su skutocne (nie nahodne).
# Zapis "A if podmienka else B" = vyber A ak podmienka plati, inak B.
zaver_q = "EXISTUJU rozdiely" if result.pvalue < 0.05 else "Bez vyznamnych rozdielov"
print(f"Zaver: {zaver_q}")

# === KROK 2b: Kendallov koeficient W ===
# Cochran povie len ANO/NIE. Kendallovo W povie KOLKO - zhoda 0 az 1.
# Pre binarne data sa W da dopocitat priamo z Cochranovej Q statistiky.
n_rules = len(matica)                                        # n = pocet pravidiel
k_obdobi = len(obdobia_stlpce)                               # k = pocet obdobi (4)
# Vzorec W = Q / (n * (k - 1)). Menovatel = najvacsie mozne Q, takze W vyjde 0..1.
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

# === KROK 3: Sumarne pocty ===
# Test povie, CI su rozdiely, ale nie KDE. Tu si spocitame konkretne cisla.

# Pre kazdy rok scitame jeho stlpec: matica[c].sum() = pocet jednotiek = pocet
# pravidiel v danom roku. (list-comprehension to spravi pre vsetky roky.)
sumar = pd.DataFrame({
    "Obdobie": obdobia_stlpce,                               # nazvy rokov O1..O4
    "Pocet_pravidiel": [matica[c].sum() for c in obdobia_stlpce],
})
print(f"\n=== Pocty pravidiel po obdobiach ===")
print(sumar.to_string(index=False))                          # index=False = bez stlpca s cislami riadkov

# value_counts cez stlpec pocet_obdobi (z ulohy 03): kolko pravidiel sa
# vyskytlo v 1 / 2 / 3 / 4 rokoch. sort_index zoradi od 1 po 4.
counts = matica["pocet_obdobi"].value_counts().sort_index()
print(f"\nDistribucia poctu obdobi vyskytu:\n{counts.to_string()}")

# Pravidla, ktore vznikli LEN v jednom konkretnom roku (typicke spravanie roka).
print(f"\nUnikatne pre kazde obdobie:")
for c in obdobia_stlpce:
    others = [oc for oc in obdobia_stlpce if oc != c]        # zoznam vsetkych ostatnych rokov (okrem c)
    # Maska: pravidlo ma 1 v roku c A ZAROVEN 0 vo vsetkych ostatnych
    # (sucet ich stlpcov == 0). & = logicke "a zaroven" po riadkoch.
    unik = matica[(matica[c] == 1) & (matica[others].sum(axis=1) == 0)]
    print(f"  {c}: {len(unik)} pravidiel len v tomto obdobi")

# === KROK 4: Vykreslenie dvoch grafov vedla seba ===
# Lavy graf: kolko pravidiel ma kazdy rok. Pravy graf: ako stabilne su pravidla.
fig, axes = plt.subplots(1, 2, figsize=(14, 5))              # 1 riadok x 2 grafy; axes[0] vlavo, axes[1] vpravo

# --- Lavy graf: pocty pravidiel po rokoch ---
axes[0].bar(sumar["Obdobie"], sumar["Pocet_pravidiel"], color="steelblue")
axes[0].set_title("Pocet asociacnych pravidiel po obdobiach")
axes[0].set_ylabel("Pocet pravidiel")

# Napiseme hodnotu nad kazdy stlpec (v+5 = trochu nad vrchol). enumerate da poradie i = pozicia stlpca.
for i, v in enumerate(sumar["Pocet_pravidiel"]):
    axes[0].text(i, v + 5, str(v), ha="center")              # ha="center" = text vodorovne vycentrovany nad stlpcom

# --- Pravy graf: ako stabilne su pravidla ---
# os X = pocet rokov vyskytu (1..4), os Y = kolko pravidiel ma tento pocet.
axes[1].bar(counts.index, counts.values, color="coral")
axes[1].set_title("Distribucia pravidiel podla poctu obdobi vyskytu")
axes[1].set_xlabel("Pocet obdobi v ktorych sa pravidlo vyskytuje")
axes[1].set_ylabel("Pocet pravidiel")

# Na osi X chceme len cele cisla 1,2,3,4 (inak by matplotlib mohol dat aj 1.5, 2.5).
axes[1].set_xticks([1, 2, 3, 4])

# Hodnota nad kazdym stlpcom aj tu. zip spari index (pocet rokov) s vyskou stlpca.
for i, v in zip(counts.index, counts.values):
    axes[1].text(i, v + 3, str(v), ha="center")

plt.tight_layout()                                           # doladi okraje, aby sa nic neorezalo
plt.savefig("out/analyza.png", dpi=150)                      # uloz do PNG; dpi=150 = vyssia kvalita

print("\nGraf ulozeny -> out/analyza.png")
