# =============================================================================
# CV4 / 05_prieskum_dat - Uloha 03: Cas straveny na strankach
# =============================================================================
#
# CIEL: Zistit, ktora kategoria obsahu na webe banky drzi navstevnika najdlhsie
#   a ci sa cas straveny na strankach menil v case (kvartaly, kriza).
#
# TEORIA (jednoducho):
#   - "Cas na stranke" (length) je odhadnuty: pozreme sa, kedy ten isty
#     pouzivatel klikol na dalsiu stranku, a rozdiel je nas odhad casu citania.
#   - Specialne hodnoty length: -1 = pouzivatel uz nic dalsie nestlacil
#     (nevieme, kedy odisiel), -2 = zmenila sa mu IP adresa (mozno to uz
#     ani nie je on), 0 = robot (automaticky program, nie clovek).
#   - "Kategoria" = o com je stranka (uvery, ucty, info...) - odvodene z URL.
#   - "Kvartal" = stvrtina roka (Q1 = jan-mar, Q2 = apr-jun...).
#   - "Kriza" = priznak, ci dany zaznam patril do obdobia financnej krizy (1)
#     alebo nie (0). Vymedzenie obdobia bolo urobene v predoslom cviceni.
#   - Priemer vs median: priemer je citlivy na extremne hodnoty (par dlhych
#     citani mu zdvihne hodnotu), median je "typicka" hodnota uprostred.
#
# VSTUP:  in/logs5.csv  - log s uz pripravenymi stlpcami length, category,
#                          yearQuartal, crisis
# VYSTUP: out/priemerny_cas_kategorie.csv  - tabulka kategoria -> priemer
#         out/heatmap_kategoria_kvartal.csv - matica kategoria x kvartal
#         out/cas_na_strankach.png         - graf (heatmap + boxplot)
#
# POUZITE KNIZNICE:
#   - pandas: praca s tabulkou (nacitanie CSV, agregacia, pivot)
#   - matplotlib: kreslenie grafov do PNG suboru
#
# ALGORITMUS: nacitaj log -> nechaj len realne casy -> spocitaj statistiky
#   po kategoriach -> sprav 2D maticu kategoria x kvartal -> porovnaj
#   krizu a po krize -> nakresli heatmap a boxplot.
# =============================================================================

import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))  # umoznuje spustenie skriptu odkialkolvek (nielen z jeho priecinka)

import pandas as pd              # tabulkove operacie (skupinky, pivot)
import matplotlib.pyplot as plt  # kreslenie heatmapy a boxplotu

# === KROK 1: Nacitanie logu a vyhodenie nevalidnych casov ===
# Nechame len realne kladne casy. Hodnoty -1 (nevieme kedy odisiel),
# -2 (zmena IP) a 0 (robot) nie su skutocny cas citania, preto ich
# do analyzy nezahrname.
print("Nacitavam dataset...")
df = pd.read_csv(
    "in/logs5.csv",
    sep=";",            # stlpce su oddelene bodkociarkou (nie ciarkou)
    quotechar='"',      # URL casto obsahuje ciarku, preto je v uvodzovkach
    low_memory=False,   # pandas si data prejde naraz a urci typy stlpcov spravne
)
# Nechame len riadky s kladnym casom; .copy() = vyrobi samostatnu tabulku
# (aby pandas neukazoval upozornenia pri buducich upravach).
df = df[df["length"] > 0].copy()
print(f"Po filtrovani (length > 0): {len(df)} zaznamov")

# === KROK 2: Priemerny cas po kategoriach ===
# Hlavna otazka: ktora kategoria obsahu zaujme ludi najviac?
# Pre kazdu kategoriu spocitame styri cisla naraz:
#   mean   = priemer (citlivy na velmi dlhe citania)
#   median = "stredna" hodnota (typicky pouzivatel)
#   std    = ako velmi sa casy lisia od priemeru (rozptyl)
#   count  = kolko zaznamov v kategorii mame (kontrola, ci je vzorka dost velka)
po_kat = df.groupby("category")["length"].agg(["mean", "median", "std", "count"]).round(2)
# Zoradime od najvyssieho priemeru po najnizsi - najzaujimavejsie kategorie hore.
po_kat = po_kat.sort_values("mean", ascending=False)
print(f"\n=== PRIEMERNY CAS PO KATEGORIACH ===")
print(po_kat.to_string())  # vypise celu tabulku bez skracovania stlpcov

# === KROK 3: Cas po kategoriach a kvartaloch (2D matica) ===
# Chceme vidiet, ako sa cas v kategorii menil v case.
# Spravime tabulku, kde:
#   - riadky = kategorie (os Y),
#   - stlpce = kvartaly 09Q1..12Q4 (os X),
#   - bunka  = priemerny cas (ked viac casov spadne do tej istej bunky,
#              spriemerujeme ich).
# Ak nejaka kombinacia (kategoria, kvartal) v datach neexistuje, bunka
# zostane prazdna (NaN).
heatmap_data = df.pivot_table(
    index="category", columns="yearQuartal", values="length", aggfunc="mean"
).round(1)

# === KROK 4: Porovnanie pocas krizy vs po krize ===
# Hypoteza: pocas financnej krizy mohli ludia stravit viac casu citanim
# info materialov banky. Spocitame priemerny cas pre kazdu kombinaciu
# (kriza, kategoria) a otocime do prehladnej tabulky.
kriza_porovnanie = df.groupby(["crisis", "category"])["length"].mean().unstack().round(2)
# groupby zoradi automaticky vzostupne -> prvy riadok je crisis=0 (po krize),
# druhy je crisis=1 (pocas krizy). Premenujeme na zrozumitelne nazvy.
kriza_porovnanie.index = ["Po krize (0)", "Pocas krizy (1)"]
print(f"\n=== KRIZA vs PO KRIZE ===")
print(kriza_porovnanie.to_string())

# === KROK 5: Vizualizacia (heatmap + boxplot vedla seba) ===
# Vykreslime dva grafy naraz: vlavo farebnu maticu, vpravo krabicove grafy.
# Vizualne sa rychlejsie najdu vzory, ktore v cislach nevidno.
fig, axes = plt.subplots(1, 2, figsize=(16, 6))  # 1 riadok, 2 grafy vedla seba

# --- HEATMAP (lavy graf) ---
# Farebna mapa kategoria x kvartal. Zlta = malo casu, cervena = vela casu.
im = axes[0].imshow(heatmap_data.values, aspect="auto", cmap="YlOrRd")
# Musime rucne nastavit popisky osi (inak by tam boli len cisla 0,1,2...).
axes[0].set_xticks(range(len(heatmap_data.columns)))
axes[0].set_xticklabels(heatmap_data.columns, rotation=45)  # otocime, lebo '09Q1' sa nezmesti vodorovne
axes[0].set_yticks(range(len(heatmap_data.index)))
axes[0].set_yticklabels(heatmap_data.index)
axes[0].set_title("Priemerny cas na stranke (s) - kategoria x kvartal")
plt.colorbar(im, ax=axes[0], label="Cas (s)")  # farebna skala vedla grafu

# Do kazdej bunky napiseme aj cislo, aby sa hodnota dala presne precitat.
for i in range(len(heatmap_data.index)):
    for j in range(len(heatmap_data.columns)):
        axes[0].text(j, i, f"{heatmap_data.values[i, j]:.0f}", ha="center", va="center", fontsize=8)

# --- BOXPLOT (pravy graf) ---
# Orezeme na casy do 100 sekund. Bez orezania by velmi dlhe citania
# (par stoviek sekund) graf "zlapostili" a krabicky by sa zmackli na spodok.
df_box = df[df["length"] < 100]
# Pre kazdu kategoriu jedna krabicka ukazujuca rozptyl casov.
df_box.boxplot(column="length", by="category", ax=axes[1], rot=45)
axes[1].set_title("Distribucia casu na stranke po kategoriach (< 100s)")
axes[1].set_ylabel("Length (sekundy)")
plt.suptitle("")        # pandas pridava vlastny nadpis "Boxplot grouped by..."; zmazeme ho
plt.tight_layout()      # automaticky upravi rozostupy, aby sa popisky neprekryvali
plt.savefig("out/cas_na_strankach.png", dpi=150)  # ulozi do PNG (150 dpi = pekna kvalita)

# === Ulozenie tabuliek do CSV ===
# Tieto subory pouzijeme v sumare a pri obhajobe projektu.
po_kat.to_csv("out/priemerny_cas_kategorie.csv")
heatmap_data.to_csv("out/heatmap_kategoria_kvartal.csv")

print("\nGraf ulozeny -> out/cas_na_strankach.png")
