# ==========================================================
# CV5 - Uloha 01: Popisne statistiky datasetu
# ==========================================================
#
# CIEL:
#   Prva uloha prieskumu dat. Predtym, nez nieco pocitame alebo modelujeme,
#   chceme dataset spoznat: kolko mame zaznamov, ake kategorie obsahu v nom
#   su, kolko pouzivatelov a sedeni, a ako dlho ludia ostavaju na strankach.
#   Je to zakladny prehlad o datach, z ktoreho vychadza vsetko dalsie.
#
# TEORIA (od nuly):
#
#   1) CO JE POPISNA STATISTIKA
#   Dataset ma velmi vela riadkov - rucne sa neda precitat. Popisna statistika
#   je par cisel, ktore data ZHRNU: kolko toho je, co je typicke, ako velmi sa
#   hodnoty lisia. Nic nepredpoveda, len OPISUJE, co v datach mame.
#
#   2) FREKVENCNA TABULKA
#   Zhrn pre TEXTOVU (kategoricku) premennu: pre kazdu hodnotu spocita,
#   kolkokrat sa vyskytla. Napr. kolko klikov padlo na kazdu kategoriu obsahu.
#   Vidno z nej, ci nejaka hodnota vyrazne prevazuje, alebo su pocty vyrovnane.
#
#   3) describe() A JEHO CISLA (pre CISELNU premennu, napr. cas na stranke)
#   Funkcia describe() vypise naraz tieto cisla:
#     - count = kolko hodnot mame (velkost vzorky),
#     - mean (priemer) = sucet vsetkych hodnot delene ich poctom. Je citlivy:
#       par extremne velkych hodnot ho potiahne nahor.
#     - std (smerodajna odchylka) = typicka vzdialenost hodnoty od priemeru.
#       Mala std = hodnoty su blizko priemeru; velka std = su daleko od neho.
#     - min / max = najmensia a najvacsia hodnota,
#     - 25% / 50% / 75% = KVARTILY. Zober vsetky hodnoty zoradene od najmensej
#       po najvacsiu a rozdel ich na styri rovnako pocetne casti. 25% = hranica,
#       pod ktorou lezi stvrtina hodnot; 50% = MEDIAN (stred, polovica hodnot
#       je pod nim); 75% = hranica troch stvrtin.
#     Priemer vs median: ked sa vyrazne lisia, data su nesymetricke - par
#       velkych hodnot tahá priemer nahor, kym median ostane pri tom typickom.
#
#   4) HISTOGRAM
#   Graf rozdelenia ciselnej premennej. Rozsah hodnot rozdeli na intervaly
#   (bins) a pre kazdy nakresli stlpec = kolko hodnot don padlo. Ukaze TVAR
#   dat: kde su hodnoty nahustene, ci ma rozdelenie jeden vrchol, dlhy chvost...
#
#   5) DELENIE PREMENNYCH (prehlad stlpcov tohto datasetu)
#     DV = zavisla premenna (co sa pozeralo): category, webPart, urlExt
#     IV = nezavisla premenna (kedy / za akych podmienok): year, quartal,
#          week, crisis
#     Pouzivatel (kto): anonIP (anonymizovana IP), agent (prehliadac)
#     Ostatne: length (cas na stranke v sekundach),
#       internal (odkial pristup prisiel; celociselny kod 0/1/2 - viz nizsie)
#
# VSTUP:
#   in/logs5.csv - POSKYTNUTY bankovy dataset (zo studie v materials/), CSV s ';'.
#                  Nie je to vystup tvojich cv1-4, ale stlpce length, frame
#                  (sedenie), anonIP (user), unixTime zodpovedaju premennym,
#                  ktore si v cv1-4 sam pocital (Length, SESSION_ID, USER_ID,
#                  UNIXTIME).
#                  Pozn.: roboti (automaticke programy, ktore stranky cital
#                  prirychlo) su v datasete oznaceni hodnotou length = 0;
#                  nizsie ich z casovych statistik vyradime filtrom length > 0.
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
os.chdir(os.path.dirname(os.path.abspath(__file__)))  # nastavi pracovny priecinok na ten, kde lezi tento skript - vdaka tomu cesty "in/..." a "out/..." funguju aj ked skript spustis odinakial

import pandas as pd                  # pandas = kniznica na pracu s tabulkami (tzv. DataFrame = tabulka)
import matplotlib.pyplot as plt      # matplotlib = kniznica na kreslenie grafov

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
# shape = dvojica cisel (pocet riadkov, pocet stlpcov). shape[0] = pocet zaznamov, shape[1] = pocet stlpcov (premennych).
print(f"Rozmer datasetu: {df.shape[0]} riadkov, {df.shape[1]} stlpcov")

# === KROK 2: Frekvencie kategorickych premennych ===
# value_counts() = spocita, kolkokrat sa kazda hodnota v stlpci vyskytla, a
# vyrobi z toho tabulku (hodnota -> pocet). Takto hned vidno, ci nejaka
# hodnota vyrazne prevazuje, alebo su pocty vyrovnane.

cat_counts = df["category"].value_counts()                  # df["category"] = stlpec s kategoriou obsahu; spocitame kliky na kazdu kategoriu
year_counts = df["year"].value_counts().sort_index()        # pocet klikov za kazdy rok; sort_index() = zorad podla hodnoty (2009,2010,2011,2012), nie podla poctu
crisis_counts = df["crisis"].value_counts()                 # pocet klikov v case krizy (1) vs po krize (0)
internal_counts = df["internal"].value_counts()             # pocet klikov podla toho, odkial pristup prisiel (kod 0/1/2)

print(f"\n=== KATEGORIE ===")
print(cat_counts)
print(f"\n=== ROKY ===")
print(year_counts)
# crisis: 1 = obdobie financnej krizy (~2009-2010), 0 = po krize (~2011-2012)
print(f"\n=== KRIZA (1) vs PO KRIZE (0) ===")
print(crisis_counts)
# internal (kod, odkial pristup prisiel): 0 = mimo internej siete banky (zvonku,
# z internetu), 1 = z vnutornej siete banky (zamestnanci), 2 = z IT firmy, ktora
# web spravuje a vyvija. NIE je to True/False, su to tri rozne hodnoty.
print(f"\n=== INTERNAL ===")
print(internal_counts)

# === KROK 3: Popisne statistiky pre length (cas na stranke) ===
# df[df["length"] > 0] = ponechaj len riadky, kde je length kladny (realny cas
# citania v sekundach). Ostatne hodnoty NIE su realny cas, preto ich do
# statistiky neberieme:
#   length = 0  -> robot (program, ktory stranku navstivil prirychlo),
#   length = -1 -> koniec sedenia (cas na stranke prekrocil povoleny prah),
#   length = -2 -> koniec sedenia (pouzivatelovi sa zmenila IP adresa).
# Zapis df[podmienka]["length"] = z tabulky vyber riadky splnajuce podmienku
# a z nich potom uz len jeden stlpec length.
length_clean = df[df["length"] > 0]["length"]
print(f"\n=== LENGTH (cas na stranke, length > 0) ===")
# describe() = naraz vypise zhrn ciselneho stlpca: count (pocet), priemer,
# std (smerodajna odchylka = typicka vzdialenost od priemeru), min, kvartily
# 25% / 50% (median) / 75% a max. Tu opisuje typicke trvanie pohladu na stranku.
print(length_clean.describe())

# === KROK 4: Pocet unikatnych pouzivatelov a sedeni ===
# Doteraz sme pocitali kliky (riadky). Teraz chceme pocet ROZNYCH ludi a pocet
# ROZNYCH navstev. nunique() = spocita, kolko roznych (unikatnych) hodnot stlpec
# obsahuje (kazdu hodnotu zarata len raz, aj ked sa opakuje).

# anonIP = anonymizovana IP, beriem ju ako "pouzivatel". Je to len odhad:
# za jednou IP moze byt viac ludi (firma/NAT); presnejsie by bolo IP+prehliadac.
n_users = df["anonIP"].nunique()
# frame = cislo sedenia (jedna navsteva) -> pocet roznych navstev.
n_sessions = df["frame"].nunique()
print(f"\nUnikatnych pouzivatelov: {n_users}")
print(f"Unikatnych sedeni: {n_sessions}")
# Priemerny pocet sedeni na pouzivatela = pocet sedeni delene poctom pouzivatelov; vyssie cislo = ludia sa vracaju castejsie. :.1f = zaokruhli na 1 desatinne miesto.
print(f"Priemerny pocet sedeni na uzivatela: {n_sessions / n_users:.1f}")

# === KROK 5: Vizualizacia distribucii ===
# Cisla su presne, ale graf hned ukaze, ktora hodnota dominuje a aky tvar
# ma rozdelenie. Spravime 4 grafy do jedneho obrazka.

# subplots(2, 2) = vytvori obrazok s mriezkou 2x2 (styri grafy). Vrati dve veci:
# fig (cely obrazok) a axes (pole = ocislovana tabulka jednotlivych grafov), do
# ktoreho potom kreslime cez axes[riadok, stlpec]. figsize = velkost obrazka v
# palcoch (sirka, vyska).
fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# Lavy horny graf: kliky po kategoriach.
# barh() = horizontalny stlpcovy graf (vodorovne stlpce). Volime horizontalny, lebo nazvy kategorii su dlhe a zvisle by sa prekryvali.
axes[0, 0].barh(cat_counts.index, cat_counts.values, color="steelblue")
axes[0, 0].set_title("Pocet pristupov po kategoriach")
axes[0, 0].set_xlabel("Pocet pristupov")
axes[0, 0].set_ylabel("Kategoria obsahu")

# Pravy horny graf: kliky po rokoch.
# astype(str) prerobi rok (cislo) na text. Vdaka tomu matplotlib nakresli
# 2009-2012 ako 4 samostatne stlpce, nie ako body na spojitej ciselnej osi.
axes[0, 1].bar(year_counts.index.astype(str), year_counts.values, color="coral")
axes[0, 1].set_title("Pocet pristupov po rokoch")
axes[0, 1].set_xlabel("Rok")
axes[0, 1].set_ylabel("Pocet pristupov")

# Lavy dolny graf: kliky po kvartaloch (jemnejsie delenie nez roky).
yq = df["yearQuartal"].value_counts().sort_index()  # pocet klikov za kazdy kvartal (stvrtrok), zoradene chronologicky. Kvartal: Q1 = jan-mar, Q2 = apr-jun, Q3 = jul-sep, Q4 = okt-dec.
# Postup: na os X najprv dame cisla 0,1,2,... (range = postupnost cisel) a az
# potom im rucne priradime textove popisky "YYYY-QN". Takto sa zobrazi KAZDY
# kvartal; keby sme dali rovno textove popisky, matplotlib by niektore vynechal.
axes[1, 0].bar(range(len(yq)), yq.values, color="green")
axes[1, 0].set_xticks(range(len(yq)))               # set_xticks(...) = kde presne maju byt znacky (ciarky) na osi X
axes[1, 0].set_xticklabels(yq.index, rotation=45)   # set_xticklabels(...) = texty pri tych znackach; rotation=45 = otoc ich o 45 stupnov, aby sa neprekryvali
axes[1, 0].set_title("Pocet pristupov po kvartaloch")
axes[1, 0].set_xlabel("Kvartal")
axes[1, 0].set_ylabel("Pocet pristupov")

# Pravy dolny graf: histogram casu na stranke (tvar rozdelenia).
# hist() = histogram: rozdeli hodnoty do 50 intervalov (bins) a pre kazdy
# nakresli stlpec = kolko hodnot don padlo. Filter < 300 odreze velmi dlhe
# casy, aby par extremov nestlacilo zvysok grafu do jedneho uzkeho pruhu.
# alpha=0.7 = mierna priehladnost farby.
axes[1, 1].hist(length_clean[length_clean < 300], bins=50, color="purple", alpha=0.7)
axes[1, 1].set_title("Distribucia casu na stranke (length < 300s)")
axes[1, 1].set_xlabel("Cas na stranke (s)")
axes[1, 1].set_ylabel("Pocet klikov (frekvencia)")

plt.tight_layout()                                  # automaticky doladi medzery, aby sa nadpisy neprekryvali
plt.savefig("out/popisne_statistiky.png", dpi=150)  # uloz obrazok; dpi=150 = vyssia kvalita do reportu
print("\nGraf ulozeny -> out/popisne_statistiky.png")
