# ==========================================================
# CV5 - Uloha 01: Popisne statistiky datasetu
# ==========================================================
#
# CIEL:
#   Prva uloha prieskumu dat. Skor nez nieco pocitame alebo modelujeme,
#   chceme dataset "spoznat": kolko mame zaznamov, ake kategorie obsahu
#   v nom su, kolko pouzivatelov a sedeni, a ako dlho ludia ostavaju na
#   strankach. Je to ako prvy pohlad na mapu pred cestou.
#
# TEORIA (od nuly - akoby si statistiku nikdy nevidel):
#
#   1) CO JE POPISNA STATISTIKA
#   Mame tabulku s milionmi riadkov - rucne sa neda precitat. Popisna
#   statistika je par cisel, ktore tabulku ZHRNU: "kolko toho je", "co je
#   typicke", "ako velmi sa to lisi". Nic nepredpoveda, len OPISUJE co mame.
#
#   2) FREKVENCNA TABULKA
#   Najjednoduchsi zhrn pre TEXTOVU (kategoricku) premennu: pre kazdu hodnotu
#   spocita, kolkokrat sa vyskytla. Napr. kolko klikov padlo na kazdu
#   kategoriu obsahu. Hned vidno, ci je nieco dominantne alebo vyrovnane.
#
#   3) describe() A JEHO CISLA (pre CISELNU premennu, napr. cas na stranke)
#   Funkcia describe() vypise naraz tieto cisla:
#     - count  = kolko hodnot vobec mame (velkost vzorky),
#     - mean (priemer) = sucet vsetkych hodnot / ich pocet. Citlivy: par
#       extremne velkych hodnot ho vytiahne hore.
#     - std (smerodajna odchylka) = ako daleko su hodnoty typicky od priemeru.
#       Male std = hodnoty su nahustene pri priemere; velke std = su rozhadzane.
#     - min / max = najmensia a najvacsia hodnota,
#     - 25% / 50% / 75% = KVARTILY. Predstav si vsetky hodnoty zoradene od
#       najmensej po najvacsiu a rozdelene na styri rovnako pocetne kopy.
#       25% = hranica pod ktorou je stvrtina hodnot, 50% = MEDIAN (presny
#       stred, polovica je pod nim), 75% = hranica troch stvrtin.
#     Priemer vs median: ked sa lisia, data su "skosene" (par velkych hodnot
#       tahá priemer, median ostane pri tom, co je naozaj typicke).
#
#   4) HISTOGRAM
#   Graf rozdelenia ciselnej premennej. Rozsah hodnot rozseka na intervaly
#   ("zasobniky") a pre kazdy nakresli stlpec = kolko hodnot don padlo.
#   Ukaze TVAR dat (kde su nahustene, ci ma jeden vrchol, dlhy chvost...).
#
#   5) DELENIE PREMENNYCH (slovnik k tomuto datasetu)
#     DV = Dependent Variable (zavisla, "co" sa pozeralo): category, webPart, urlExt
#     IV = Independent Variable (nezavisla, "kedy/za akych podmienok"): year,
#          quartal, week, crisis
#     User (kto): anonIP (anonymizovana IP), agent (prehliadac)
#     Ostatne: length (cas na stranke), internal (z internej siete banky?)
#
# VSTUP:
#   in/logs5.csv - POSKYTNUTY bankovy dataset (zo studie v materials/), CSV s ';'.
#                  Nie je to vystup tvojich cv1-4, ale stlpce length, frame
#                  (sedenie), anonIP (user), unixTime zodpovedaju premennym,
#                  ktore si v cv1-4 sam pocital (Length, SESSION_ID, USER_ID,
#                  UNIXTIME). Roboti su uz vyfiltrovani (maju length 0).
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
# Nacitame CSV subor do tabulky (DataFrame = tabulka v pandas).
# Tri nastavenia a preco su tu:
#   sep=";"          - stlpce su oddelene bodkociarkou (nie ciarkou),
#   quotechar='"'    - polia ako URL maju vnutri ciarky; uvodzovky drzia
#                      taketo pole pohromade ako jednu hodnotu,
#   low_memory=False - pandas najprv precita cely subor a az potom urci typ
#                      kazdeho stlpca (inak pri velkom subore typy hada zle).
df = pd.read_csv("in/logs5.csv", sep=";", quotechar='"', low_memory=False)
# shape je dvojica (riadky, stlpce): shape[0] = pocet zaznamov, shape[1] = pocet premennych.
print(f"Rozmer datasetu: {df.shape[0]} riadkov, {df.shape[1]} stlpcov")

# === KROK 2: Frekvencie kategorickych premennych ===
# value_counts() = frekvencna tabulka: pre kazdu hodnotu spocita, kolkokrat
# sa v stlpci vyskytla. Hned vidno, ci jedna hodnota dominuje, alebo su
# vyrovnane.

cat_counts = df["category"].value_counts()                  # kolko klikov padlo na kazdu kategoriu obsahu
year_counts = df["year"].value_counts().sort_index()        # kolko klikov za kazdy rok; sort_index = zoradi roky chronologicky (2009->2012), nie podla poctu
crisis_counts = df["crisis"].value_counts()                 # kolko klikov pocas krizy vs po krize
internal_counts = df["internal"].value_counts()             # kolko klikov z internej siete banky vs z internetu

print(f"\n=== KATEGORIE ===")
print(cat_counts)
print(f"\n=== ROKY ===")
print(year_counts)
# crisis: 1 = obdobie financnej krizy (~2009-2010), 0 = po krize (~2011-2012)
print(f"\n=== KRIZA (1) vs PO KRIZE (0) ===")
print(crisis_counts)
# internal: True = pristup z vnutornej siete banky (zamestnanci), False = zvonku
print(f"\n=== INTERNAL ===")
print(internal_counts)

# === KROK 3: Popisne statistiky pre length (cas na stranke) ===
# df[df["length"] > 0] = nechaj len riadky s kladnym casom. Hodnoty 0 a
# chybajuce su posledne kliky v navsteve (nevieme, kedy clovek odisiel),
# nie su to realne casy citania, tak ich do statistiky neberieme.
length_clean = df[df["length"] > 0]["length"]
print(f"\n=== LENGTH (cas na stranke, length > 0) ===")
# describe() = suhrn ciselneho stlpca naraz: count, priemer, std (rozptyl),
# min, kvartily 25%/50%(median)/75% a max. Tu = typicke trvanie pohladu na stranku.
print(length_clean.describe())

# === KROK 4: Pocet unikatnych pouzivatelov a sedeni ===
# Doteraz sme pocitali kliky. Teraz chceme vediet pocet roznych ludi a
# pocet navstev. nunique() = pocet ROZNYCH (unikatnych) hodnot v stlpci.

# anonIP = anonymizovana IP, beriem ju ako "pouzivatel". Je to len odhad:
# za jednou IP moze byt viac ludi (firma/NAT); presnejsie by bolo IP+prehliadac.
n_users = df["anonIP"].nunique()
# frame = cislo sedenia (jedna navsteva) -> pocet roznych navstev.
n_sessions = df["frame"].nunique()
print(f"\nUnikatnych pouzivatelov: {n_users}")
print(f"Unikatnych sedeni: {n_sessions}")
# Priemer sedeni na pouzivatela: cim viac, tym castejsie sa ludia vracaju. :.1f = 1 desatinne miesto.
print(f"Priemerny pocet sedeni na uzivatela: {n_sessions / n_users:.1f}")

# === KROK 5: Vizualizacia distribucii ===
# Cisla su presne, ale graf hned ukaze, ktora hodnota dominuje a aky tvar
# ma rozdelenie. Spravime 4 grafy do jedneho obrazka.

# subplots(2, 2) = mriezka 2x2; "axes" je pole grafov, do ktoreho potom
# kreslime cez axes[riadok, stlpec]. figsize = velkost v palcoch (sirka, vyska).
fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# Lavy horny graf: kliky po kategoriach.
# barh = HORIZONTALNY stlpcovy graf (nazvy kategorii su dlhe, zvislo by sa prekryvali).
axes[0, 0].barh(cat_counts.index, cat_counts.values, color="steelblue")
axes[0, 0].set_title("Pocet pristupov po kategoriach")

# Pravy horny graf: kliky po rokoch.
# astype(str) prerobi rok (cislo) na text, aby matplotlib kreslil 2009-2012
# ako 4 samostatne stlpce, nie ako body na spojitej ciselnej osi.
axes[0, 1].bar(year_counts.index.astype(str), year_counts.values, color="coral")
axes[0, 1].set_title("Pocet pristupov po rokoch")

# Lavy dolny graf: kliky po kvartaloch (jemnejsie delenie nez roky).
yq = df["yearQuartal"].value_counts().sort_index()  # frekvencie kvartalov, zoradene chronologicky
# Trik: na os X davame cisla 0,1,2,... (range) a az potom im rucne priradime
# textove popisky "YYYY-QN". Takto sa zobrazi KAZDY kvartal (pri textovej osi
# by matplotlib niektore mohol vynechat).
axes[1, 0].bar(range(len(yq)), yq.values, color="green")
axes[1, 0].set_xticks(range(len(yq)))               # kde maju byt znacky na osi
axes[1, 0].set_xticklabels(yq.index, rotation=45)   # popisky znaciek; rotacia 45 stupnov, aby sa neprekryvali
axes[1, 0].set_title("Pocet pristupov po kvartaloch")

# Pravy dolny graf: histogram casu na stranke (tvar rozdelenia).
# hist rozdeli hodnoty do 50 intervalov (bins) a pre kazdy nakresli stlpec
# = kolko hodnot don padlo. Filter < 300 odreze velmi dlhe casy, aby graf
# nebol "splosteny" par extremami. alpha=0.7 = mierna priehladnost farby.
axes[1, 1].hist(length_clean[length_clean < 300], bins=50, color="purple", alpha=0.7)
axes[1, 1].set_title("Distribucia casu na stranke (length < 300s)")

plt.tight_layout()                                  # automaticky doladi medzery, aby sa nadpisy neprekryvali
plt.savefig("out/popisne_statistiky.png", dpi=150)  # uloz obrazok; dpi=150 = vyssia kvalita do reportu
print("\nGraf ulozeny -> out/popisne_statistiky.png")
