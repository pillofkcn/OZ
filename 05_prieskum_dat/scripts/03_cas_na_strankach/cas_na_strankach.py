# ==========================================================
# CV5 - Uloha 03: Cas straveny na strankach
# ==========================================================
#
# CIEL: Zistit, ktora kategoria obsahu na webe banky drzi navstevnika najdlhsie
#   a ci sa cas straveny na strankach menil v case (kvartaly, kriza).
#
# TEORIA (od nuly):
#
#   1) CO JE "length" (cas na stranke) A ODKIAL HO BERIEME
#   Log nezaznamenava, kedy clovek stranku zatvoril - vie len, KEDY na nu
#   klikol. Cas citania preto ODHADUJEME: ked ten isty pouzivatel klikol na
#   dalsiu stranku o minutu neskor, predpokladame, ze tu predoslu cital ~60 s.
#   Specialne (nevalidne) hodnoty length, ktore NIE su realny cas citania:
#     -1 = koniec sedenia, lebo cas na stranke prekrocil povoleny casovy prah,
#     -2 = koniec sedenia, lebo sa pouzivatelovi zmenila IP adresa,
#      0 = robot (automaticky program, ktory stranku navstivil prirychlo).
#   Preto pracujeme len so zaznamami, kde length > 0.
#
#   2) PRIEMER vs MEDIAN vs std (preco nestaci jedno cislo)
#   - priemer (mean) = sucet / pocet. Par velmi dlhych citani ho vytiahne hore,
#     takze sam o sebe moze byt zavadzajuci.
#   - median = prostredna hodnota po zoradeni (polovica je pod nou). Odolny voci
#     extremom = ukazuje, co je naozaj "typicke".
#   - std (smerodajna odchylka) = typicka vzdialenost casu od priemeru. Mala std
#     = casy su nahustene pri priemere; velka std = su rozhadzane.
#   Ked sa priemer a median lisia, data su nesymetricke (dlhy chvost dlhych citani).
#
#   3) PIVOT TABULKA (2D matica kategoria x kvartal)
#   Chceme jeden pohlad, kde riadok = kategoria, stlpec = kvartal a v bunke je
#   priemerny cas pre tu kombinaciu. pivot_table presne toto spravi: zoskupi
#   data podla dvoch rozmerov (riadky a stlpce) a do kazdej bunky da pozadovanu
#   statistiku (tu priemer).
#
#   4) HEATMAP (tepelna mapa)
#   Ta ista 2D matica nakreslena farebne: kazda bunka je stvorcek, ktoreho
#   FARBA zodpoveda hodnote (zlta = malo sekund, cervena = vela). Oko hned
#   najde, kde su "horuce" miesta - dlhe casy citania.
#
#   5) BOXPLOT (krabicovy graf) - cita sa takto:
#   Jedna "krabicka" zhrnie rozdelenie casov v jednej kategorii:
#     - spodok krabice = dolny kvartil Q1 (pod nim je 25 % hodnot),
#     - vrch krabice  = horny kvartil Q3 (pod nim je 75 % hodnot),
#     - ciara v krabici = MEDIAN (stred),
#     - vyska krabice  = IQR = Q3 - Q1 = rozsah strednej polovice dat (kde lezi
#                        prostrednych 50 % hodnot),
#     - "fuzy" (ciary nad/pod) = bezny rozsah hodnot,
#     - body za fuzmi = odlahle hodnoty (outliers, neobvykle dlhe/kratke casy).
#   Vyhoda: na jeden pohlad porovnas viac kategorii naraz - kde su casy
#   vyssie, kde rozhadzanejsie, kde su extremne hodnoty.
#
#   Pozn.: "kvartal" = stvrtina roka (Q1=jan-mar, Q2=apr-jun, ...).
#          "kriza" = priznak 0/1, ci zaznam spada do obdobia financnej krizy.
#
# VSTUP:  in/logs5.csv  - POSKYTNUTY bankovy dataset (zo studie v materials/),
#                          CSV s ';'. Stlpce length/frame/anonIP/unixTime
#                          zodpovedaju Length/SESSION_ID/USER_ID/UNIXTIME z cv1-4.
#                          Tu pouzivame: length, category, yearQuartal, crisis.
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
# ==========================================================

import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))  # nastavi pracovny priecinok na ten, kde lezi tento skript - vdaka tomu cesty "in/..." a "out/..." funguju aj ked skript spustis odinakial

import pandas as pd              # tabulkove operacie (skupinky, pivot)
import matplotlib.pyplot as plt  # kreslenie heatmapy a boxplotu

# === KROK 1: Nacitanie logu a vyhodenie nevalidnych casov ===
print("Nacitavam dataset...")
df = pd.read_csv(
    "in/logs5.csv",
    sep=";",            # stlpce oddelene bodkociarkou (nie ciarkou)
    quotechar='"',      # uvodzovky drzia pohromade pole, ktore vnutri ma ciarku (napr. URL)
    low_memory=False,   # precita cely subor naraz a spravne urci typy stlpcov
)
# Do analyzy pustime len realne casy citania: length > 0.
# Vyhodime tym specialne hodnoty -1 (koniec sedenia - prekroceny casovy prah),
# -2 (koniec sedenia - zmena IP) a 0 (robot) - to nie su skutocne casy citania.
# .copy() = vyrobi samostatnu kopiu tabulky, aby pandas pri dalsich upravach
# nevypisoval varovanie (ze menime iba "vyrez" povodnej tabulky).
df = df[df["length"] > 0].copy()
print(f"Po filtrovani (length > 0): {len(df)} zaznamov")

# === KROK 2: Priemerny cas po kategoriach ===
# Otazka: ktora kategoria udrzi ludi najdlhsie?
# groupby("category") roztriedi riadky do skupin podla kategorie. .agg([...]) =
# vypocitaj pre kazdu skupinu naraz viacero statistik; .round(2) zaokruhli na 2
# desatinne miesta:
#   mean   = priemer (citlivy na velmi dlhe citania),
#   median = stredna hodnota (typicky pouzivatel),
#   std    = smerodajna odchylka (typicka vzdialenost casu od priemeru),
#   count  = pocet zaznamov (kontrola, ci je vzorka dost velka).
po_kat = df.groupby("category")["length"].agg(["mean", "median", "std", "count"]).round(2)
# Zoradime zostupne podla priemeru (ascending=False = od najvacsieho po najmensi)
# -> najdlhsie citane kategorie budu hore.
po_kat = po_kat.sort_values("mean", ascending=False)
print(f"\n=== PRIEMERNY CAS PO KATEGORIACH ===")
print(po_kat.to_string())  # to_string() vypise celu tabulku bez skracovania

# === KROK 3: Cas po kategoriach a kvartaloch (2D matica) ===
# Chceme vidiet, ako sa priemerny cas v kategorii menil v case.
# pivot_table postavi 2D tabulku:
#   index="category"      -> riadky = kategorie,
#   columns="yearQuartal" -> stlpce = kvartaly 09Q1..12Q4,
#   values="length", aggfunc="mean" -> hodnota v bunke = priemer casov, ktore do
#                                      danej kombinacie (kategoria, kvartal) patria.
# Chybajuca kombinacia (kategoria v kvartali nebola) ostane prazdna (NaN).
heatmap_data = df.pivot_table(
    index="category", columns="yearQuartal", values="length", aggfunc="mean"
).round(1)

# === KROK 4: Porovnanie pocas krizy vs po krize ===
# Hypoteza: pocas krizy ludia mozno citali dlhsie. Spocitame priemerny cas
# pre kazdu dvojicu (crisis, category); unstack() otoci kategorie do stlpcov,
# takze riadok = obdobie (0/1), stlpec = kategoria.
kriza_porovnanie = df.groupby(["crisis", "category"])["length"].mean().unstack().round(2)
# groupby zoradi obdobia vzostupne -> prvy riadok crisis=0 (po krize), druhy
# crisis=1 (pocas krizy). Premenujeme indexy na zrozumitelne nazvy.
kriza_porovnanie.index = ["Po krize (0)", "Pocas krizy (1)"]
print(f"\n=== KRIZA vs PO KRIZE ===")
print(kriza_porovnanie.to_string())

# === KROK 5: Vizualizacia (heatmap + boxplot vedla seba) ===
# Dva grafy naraz: vlavo farebna matica, vpravo krabicove grafy. V grafe sa
# vzory najdu rychlejsie nez v cislach.
fig, axes = plt.subplots(1, 2, figsize=(16, 6))  # 1 riadok, 2 grafy vedla seba: axes[0] vlavo, axes[1] vpravo

# --- HEATMAP (lavy graf) ---
# imshow nakresli maticu ako farebne stvorceky. cmap="YlOrRd" = farebna skala
# zlta->cervena (zlta = malo sekund, cervena = vela). aspect="auto" = roztiahne na plochu.
im = axes[0].imshow(heatmap_data.values, aspect="auto", cmap="YlOrRd")
# Osi by inak mali len cisla 0,1,2... Nastavime znacky (set_*ticks) a k nim
# textove popisky (set_*ticklabels) = nazvy kvartalov a kategorii.
axes[0].set_xticks(range(len(heatmap_data.columns)))
axes[0].set_xticklabels(heatmap_data.columns, rotation=45)  # rotacia, lebo '09Q1' sa vodorovne nezmesti
axes[0].set_yticks(range(len(heatmap_data.index)))
axes[0].set_yticklabels(heatmap_data.index)
axes[0].set_title("Priemerny cas na stranke (s) - kategoria x kvartal")
axes[0].set_xlabel("Kvartal")
axes[0].set_ylabel("Kategoria obsahu")
plt.colorbar(im, ax=axes[0], label="Cas (s)")  # farebna skala (legenda farieb) vedla grafu

# Do kazdej bunky vypiseme aj cislo, aby sa hodnota dala presne precitat.
# Dve vnorene slucky prejdu vsetky riadky (i) a stlpce (j) matice.
for i in range(len(heatmap_data.index)):
    for j in range(len(heatmap_data.columns)):
        # text(x=j, y=i, hodnota); ha/va="center" = vycentrovane v bunke, :.0f = cele cislo
        axes[0].text(j, i, f"{heatmap_data.values[i, j]:.0f}", ha="center", va="center", fontsize=8)

# --- BOXPLOT (pravy graf) ---
# Orezeme na casy < 100 s. Bez orezania by par velmi dlhych citani (stovky s)
# roztiahlo os a vsetky krabicky by sa zmackli dole.
df_box = df[df["length"] < 100]
# boxplot(by="category") = pre kazdu kategoriu jedna krabicka (Q1-Q3, median, fuzy,
# odlahle body) - viz vysvetlenie boxplotu v hlavicke. rot=45 = otoci popisky osi X.
df_box.boxplot(column="length", by="category", ax=axes[1], rot=45)
axes[1].set_title("Distribucia casu na stranke po kategoriach (< 100s)")
axes[1].set_xlabel("Kategoria obsahu")
axes[1].set_ylabel("Cas na stranke (s)")
plt.suptitle("")        # pandas sam prida nadpis "Boxplot grouped by..."; prazdnym retazcom ho zmazeme
plt.tight_layout()      # doladi rozostupy, aby sa popisky neprekryvali
plt.savefig("out/cas_na_strankach.png", dpi=150)  # uloz do PNG; dpi=150 = pekna kvalita

# === Ulozenie tabuliek do CSV ===
# Ulozime tabulku po kategoriach aj maticu kategoria x kvartal (do sumaru/obhajoby).
po_kat.to_csv("out/priemerny_cas_kategorie.csv")
heatmap_data.to_csv("out/heatmap_kategoria_kvartal.csv")

print("\nGraf ulozeny -> out/cas_na_strankach.png")
