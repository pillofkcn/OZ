# ==========================================================
# CV4 - Uloha 01: Popisne statistiky datasetu
# ==========================================================
#
# CIEL:
#   Toto je prva uloha prieskumu dat. Nasleduje po cisteni logov (cv1)
#   a po vytvoreni sedeni a casovych znamok (cv2-cv3). Chceme sa najprv
#   zorientovat: kolko zaznamov mame, ake kategorie obsahu existuju,
#   kolko mame pouzivatelov a ako dlho ludia ostavaju na strankach.
#   Bez tohto prehladu by sme isli "naslepo" do dalsich uloh.
#
# TEORIA (jednoducho):
#   - Popisne statistiky = zakladne cisla o datach: kolko, koho, kedy.
#   - Pouzivatelske premenne delime do skupin:
#       DV = Dependent Variable (zavisla premenna, co skumame - typicky obsah stranky),
#       IV = Independent Variable (nezavisla premenna, podmienky - typicky cas, kontext).
#       DV (co sa pozeralo)   = category, webPart, urlExt
#       IV (kedy sa pozeralo) = year, quartal, week, crisis
#       User (kto sa pozeral) = anonIP (anonymizovana IP), agent (prehliadac)
#       Ostatne               = length (cas na stranke), internal (interny/externy)
#   - Sedenie (session) = jedna navsteva, t.j. sekvencia kliknuti toho isteho
#     pouzivatela bez vacsej prestavky. Definovali sme to v cv2.
#   - Length (cas na stranke) = nepoznam priamo, lebo Apache log nezaznamenava
#     kedy clovek odisiel. Preto ho odhadujem ako rozdiel casov dvoch po sebe
#     iducich klikov toho isteho cloveka. Posledny klik v navsteve nema "dalsi",
#     takze tam length nepoznam (vyhodim ho filtrom length > 0).
#   - Frekvencna tabulka = pre kazdu hodnotu spocita, kolko krat sa vyskytuje.
#   - describe() = vypise pocet, priemer, smerodajnu odchylku, min, max a
#     kvartily (25%, 50% = median, 75%) — rychly suhrn ciselnej premennej.
#
# Pozn.: Podla CRISP-DM patri popisna statistika do typu ulohy Deskripcia dat
# a sumarizacia (prednaska P9) - su to odporucane metody pre prvotne porozumenie
# datam pred modelovanim.
#
# VSTUP:
#   in/logs5.csv  - vycisteny Apache log po cv1-cv3; CSV s ; ako oddelovacom
#
# VYSTUP:
#   stdout                      - vypisy frekvencii a describe()
#   out/popisne_statistiky.png  - 2x2 mriezka grafov
#
# POUZITE KNIZNICE:
#   - pandas      = praca s tabulkami (nacitanie CSV, pocitanie, filtrovanie)
#   - matplotlib  = kreslenie statickych grafov do PNG suboru
#
# ALGORITMUS:
#   Nacitaj CSV -> spocitaj frekvencie kategorickych premennych ->
#   spocitaj describe pre length -> spocitaj unikatnych userov a sedeni ->
#   vykresli 4 grafy do jedneho obrazku.
# ==========================================================

import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))  # umoznuje spustenie skriptu odkialkolvek (nielen z jeho priecinka)

import pandas as pd                  # pandas = praca s tabulkami (DataFrame)
import matplotlib.pyplot as plt      # matplotlib = kreslenie grafov

# === KROK 1: Nacitanie datasetu ===
print("Nacitavam dataset...")
# sep=";" lebo CSV pouziva bodkociarku; quotechar='"' lebo niektore polia
# (URL, prehliadac) maju vnutri ciarky; low_memory=False = pandas najprv
# precita cely subor a az potom urci typy stlpcov (spolahlivejsie).
df = pd.read_csv("in/logs5.csv", sep=";", quotechar='"', low_memory=False)
print(f"Rozmer datasetu: {df.shape[0]} riadkov, {df.shape[1]} stlpcov")  # kolko mame zaznamov a stlpcov

# === KROK 2: Frekvencie kategorickych premennych ===
# Pre kazdu premennu spocitame kolko krat sa kazda hodnota vyskytla.
# Vidime tym, ci je dataset rovnomerny (vsetky hodnoty zhruba rovnako)
# alebo nerovnomerny (par hodnot dominuje).

cat_counts = df["category"].value_counts()                  # kolko kliknuti pre kazdu kategoriu obsahu
year_counts = df["year"].value_counts().sort_index()        # kolko kliknuti za kazdy rok; sort_index = chronologicky 2009->2012
crisis_counts = df["crisis"].value_counts()                 # priznak: bolo to pocas financnej krizy?
internal_counts = df["internal"].value_counts()             # bol pristup z internej siete banky alebo z internetu?

print(f"\n=== KATEGORIE ===")
print(cat_counts)
print(f"\n=== ROKY ===")
print(year_counts)
# crisis = 1 znamena obdobie krizy (~2009-2010), 0 = po krize (~2011-2012)
print(f"\n=== KRIZA (1) vs PO KRIZE (0) ===")
print(crisis_counts)
# internal = True znamena pristup z vnutornej siete banky (zamestnanci)
print(f"\n=== INTERNAL ===")
print(internal_counts)

# === KROK 3: Popisne statistiky pre length (cas na stranke) ===
# Berieme len pristupy kde length > 0. Nulove a chybajuce hodnoty zodpovedaju
# poslednemu kliku v navsteve (nepoznam cas, lebo "dalsi" klik neexistuje).
# describe() nam povie typicke trvanie pohladu na stranku.
length_clean = df[df["length"] > 0]["length"]               # vyhodime zaznamy bez znameho casu
print(f"\n=== LENGTH (cas na stranke, length > 0) ===")
print(length_clean.describe())                              # vypise priemer, median, kvartily, min, max

# === KROK 4: Pocet unikatnych pouzivatelov a sedeni ===
# Doteraz sme pocitali zaznamy (kliknutia). Teraz chceme vediet:
#   - kolko roznych ludi nam stranku navstivilo
#   - kolko navstev (sedeni) spolu spravili
# Pomer sedeni/uzivatel ukazuje, ako casto sa vracaju.

n_users = df["anonIP"].nunique()        # pocet unikatnych anonymizovanych IP (Pozn.: aproximacia - za jednou IP moze byt viacero ludi cez NAT/firmu; v cv3 robime presnejsie IP+Agent)
n_sessions = df["frame"].nunique()      # pocet roznych navstev (frame = identifikator sedenia z cv2)
print(f"\nUnikatnych pouzivatelov: {n_users}")
print(f"Unikatnych sedeni: {n_sessions}")
print(f"Priemerny pocet sedeni na uzivatela: {n_sessions / n_users:.1f}")  # priemer s 1 desatinnym miestom

# === KROK 5: Vizualizacia distribucii ===
# Cisla v tabulke su presne, ale graf hned ukaze ktora kategoria dominuje
# a aky tvar ma rozdelenie. Spravime 4 grafy do jedneho obrazka.

# subplots(2, 2) = mriezka 2 riadky x 2 stlpce; figsize v palcoch (sirka, vyska)
fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# Lavy horny: kategorie obsahu.
# barh = horizontalny stlpcovy graf, lebo nazvy kategorii su dlhe a
# zvisle by sa prekryvali.
axes[0, 0].barh(cat_counts.index, cat_counts.values, color="steelblue")
axes[0, 0].set_title("Pocet pristupov po kategoriach")

# Pravy horny: roky.
# astype(str) prerobi rok na text, aby matplotlib bral 2009-2012 ako
# samostatne stlpce a nie ako body na ciselnej osi.
axes[0, 1].bar(year_counts.index.astype(str), year_counts.values, color="coral")
axes[0, 1].set_title("Pocet pristupov po rokoch")

# Lavy dolny: rok-kvartal (jemnejsie ako roky).
yq = df["yearQuartal"].value_counts().sort_index()  # spocitaj kliky pre kazdy kvartal, zorad chronologicky
# Na os X davame cisla 0,1,2,... a manualne im priradime popisky "YYYY-QN".
# Takto matplotlib urcite ukaze kazdy kvartal (inak by mohol niektore preskocit).
axes[1, 0].bar(range(len(yq)), yq.values, color="green")
axes[1, 0].set_xticks(range(len(yq)))
axes[1, 0].set_xticklabels(yq.index, rotation=45)   # rotacia 45 stupnov aby sa popisky neprekryvali
axes[1, 0].set_title("Pocet pristupov po kvartaloch")

# Pravy dolny: histogram casu na stranke.
# hist = rozdeli hodnoty do 50 zasobnikov a ukaze kolko ich v kazdom je.
# Filter < 300 odreze velmi dlhe pristupy, aby bol graf citatelny.
axes[1, 1].hist(length_clean[length_clean < 300], bins=50, color="purple", alpha=0.7)
axes[1, 1].set_title("Distribucia casu na stranke (length < 300s)")

plt.tight_layout()                                  # automaticky upravi medzery aby sa nadpisy neprekryvali
plt.savefig("out/popisne_statistiky.png", dpi=150)  # dpi=150 = vyssia kvalita pre report
print("\nGraf ulozeny -> out/popisne_statistiky.png")
