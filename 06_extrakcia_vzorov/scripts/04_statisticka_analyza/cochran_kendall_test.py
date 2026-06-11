# ==========================================================
# CV5 - Uloha 04: Statisticka analyza vysledkov
# ==========================================================
#
# CIEL:
#   Mame 4 rocne obdobia (O1=2009, O2=2010, O3=2011, O4=2012)
#   a pre kazde z nich sme v predoslych ulohach nasli "asociacne
#   pravidla" = pravidla typu "ked pouzivatel navstivi stranku A,
#   casto navstivi aj B". Tu chceme zistit: spravali sa pouzivatelia
#   v tychto 4 rokoch rovnako, alebo sa to medzi rokmi rozne lisi?
#
# TEORIA (jednoducho, bez zargonu):
#   Mame tabulku 450 pravidiel x 4 obdobia, v bunkach 0/1
#   (1 = pravidlo sa v danom roku objavilo, 0 = neobjavilo).
#
#   Pouzijeme dva statisticke testy:
#
#   1) Cochranov Q test (test rozdielov pre 4 roky naraz):
#      Polozi otazku: "je rovnako pravdepodobne, ze pravidlo
#      vznikne v O1, O2, O3 aj O4, alebo niektory rok vybocuje?"
#      Vystupom je cislo p (p-hodnota). Ak je p < 0.05, povieme
#      "ano, medzi rokmi su signifikantne rozdiely".
#
#   2) Kendallov koeficient W (sila zhody):
#      Cochran iba povie ANO/NIE. Kendall navyse povie KOLKO -
#      cislo od 0 do 1: 0 = roky sa sprava uplne inak, 1 = roky
#      maju temer identicke pravidla.
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

matica = pd.read_csv("in/matica_pravidiel.csv")              # nacitame 450 pravidiel z predoslej ulohy

# Najdeme stlpce obdobi - vsetky zacinaju pismenom "O" (O1, O2, O3, O4).
# Robime to dynamicky, aby skript fungoval aj keby pribudli dalsie obdobia.
obdobia_stlpce = [c for c in matica.columns if c.startswith("O")]

print(f"Nacitanych pravidiel: {len(matica)}")                # kontrolny vypis - ocakavame 450

# === KROK 2: Cochranov Q test ===
#
# Pytame sa: lisi sa pravdepodobnost vyskytu pravidla medzi rokmi?
# Test potrebuje 2D tabulku 0/1, kde riadky = pravidla, stlpce = roky.
# Vrati nam objekt s troma cislami: statistika, p-hodnota, stupne volnosti.

binarna_matica = matica[obdobia_stlpce].values               # vyber stlpcov O1..O4 ako cisla
result = cochrans_q(binarna_matica)                          # spustime hotovy test

print(f"\n=== Cochranov Q test ===")
print(f"Q statistika: {result.statistic:.4f}, p={result.pvalue:.6f}, df={result.df}")

# p < 0.05 znamena "rozdiely su skutocne, nie nahodne"
zaver_q = "EXISTUJU rozdiely" if result.pvalue < 0.05 else "Bez vyznamnych rozdielov"
print(f"Zaver: {zaver_q}")

# === KROK 2b: Kendallov koeficient W ===
#
# Cochran povie iba ANO/NIE. Kendall navyse povie KOLKO - cislo od 0 do 1.
# Pre binarne data sa W da rychlo vyratat zo statistiky Cochrana
# vzorcom: W = Q / (n * (k - 1)), kde n = pocet pravidiel, k = pocet obdobi.

n_rules = len(matica)                                        # pocet pravidiel (450)
k_obdobi = len(obdobia_stlpce)                               # pocet obdobi (4)
kendall_w = result.statistic / (n_rules * (k_obdobi - 1))    # W vzdy lezi v rozmedzi 0 az 1
print(f"\n=== Kendallov W (koeficient konkordancie) ===")
print(f"W = {kendall_w:.4f}  (n={n_rules}, k={k_obdobi})")

# Slovny preklad cisla W na zrozumitelnu interpretaciu
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
#
# Test povie ci rozdiely existuju, ale nie KDE. Tu si jednoducho
# spocitame, kolko pravidiel ma kazdy rok, aby sme videli cisla.

# .sum() scita 0/1 v stlpci = pocet jednotiek = pocet pravidiel v danom roku
sumar = pd.DataFrame({
    "Obdobie": obdobia_stlpce,                               # nazvy rokov O1..O4
    "Pocet_pravidiel": [matica[c].sum() for c in obdobia_stlpce],  # pocet pravidiel v kazdom roku
})
print(f"\n=== Pocty pravidiel po obdobiach ===")
print(sumar.to_string(index=False))                          # vypis bez cisla riadka

# Kolko pravidiel sa objavilo v 1 roku, kolko v 2 rokoch, atd.
# Stlpec "pocet_obdobi" sme vyratali uz v predoslej ulohe.
counts = matica["pocet_obdobi"].value_counts().sort_index()  # zoradime podla poctu rokov (1,2,3,4)
print(f"\nDistribucia poctu obdobi vyskytu:\n{counts.to_string()}")

# Pravidla, ktore vznikli IBA v jednom konkretnom roku
# (zaujimave, pretoze ukazuju typicke spravanie len pre dany rok).
print(f"\nUnikatne pre kazde obdobie:")
for c in obdobia_stlpce:
    others = [oc for oc in obdobia_stlpce if oc != c]        # vsetky ostatne roky okrem c
    # vyber: pravidlo je 1 v c A SUCASNE 0 vo vsetkych ostatnych rokoch
    unik = matica[(matica[c] == 1) & (matica[others].sum(axis=1) == 0)]
    print(f"  {c}: {len(unik)} pravidiel len v tomto obdobi")

# === KROK 4: Vykreslenie dvoch grafov vedla seba ===
#
# Lavy graf: kolko pravidiel ma kazdy rok (bohatost roka)
# Pravy graf: ako stabilne su pravidla (kolko ich je v 1, 2, 3, 4 rokoch)

fig, axes = plt.subplots(1, 2, figsize=(14, 5))              # 1 riadok x 2 stlpce, rozmer v palcoch

# --- Lavy graf: pocty pravidiel po rokoch ---
axes[0].bar(sumar["Obdobie"], sumar["Pocet_pravidiel"], color="steelblue")
axes[0].set_title("Pocet asociacnych pravidiel po obdobiach")
axes[0].set_ylabel("Pocet pravidiel")

# Cislo nad kazdym stlpcom, aby bolo presne citat z grafu
for i, v in enumerate(sumar["Pocet_pravidiel"]):
    axes[0].text(i, v + 5, str(v), ha="center")              # ha="center" = vycentrovane vodorovne

# --- Pravy graf: ako stabilne su pravidla ---
# os x = pocet rokov (1..4), os y = kolko pravidiel ma tento pocet rokov
axes[1].bar(counts.index, counts.values, color="coral")
axes[1].set_title("Distribucia pravidiel podla poctu obdobi vyskytu")
axes[1].set_xlabel("Pocet obdobi v ktorych sa pravidlo vyskytuje")
axes[1].set_ylabel("Pocet pravidiel")

# Vynutime celociselne popisy na osi x (inak by tam mohli byt 1.5, 2.5)
axes[1].set_xticks([1, 2, 3, 4])

# Cislo nad kazdym stlpcom aj v druhom grafe
for i, v in zip(counts.index, counts.values):
    axes[1].text(i, v + 3, str(v), ha="center")

plt.tight_layout()                                           # automaticky uprav okraje, aby sa nic neorezalo

plt.savefig("out/analyza.png", dpi=150)                      # ulozenie do PNG vo vyssej kvalite

print("\nGraf ulozeny -> out/analyza.png")
