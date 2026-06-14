# ==========================================================
# CV6 - Uloha 01: Priprava transakcii (kosikov) pre kazdy rok
# ==========================================================
#
# CIEL:
#   Z logov banky (logs5.csv) urobit "kosiky" - co vsetko jeden
#   pouzivatel pozrel pocas jednej navstevy stranky. Tieto kosiky
#   v dalsich ulohach pouzijeme na hladanie vzorov "kto pozrel A,
#   pozrel aj B" (asociacne pravidla).
#
# TEORIA (od nuly - akoby si to nikdy nevidel):
#
#   1) ANALYZA NAKUPNEHO KOSIKA (market basket analysis)
#   Klasicky priklad z obchodu: pozrieme sa na tisice nakupnych
#   blokov a hladame veci, ktore ludia kupuju SPOLU (chlieb + maslo).
#   Z toho sa daju robit pravidla "kto kupil chleb, kupi aj maslo".
#   My nemame obchod, ale web banky - princip je vsak rovnaky.
#
#   2) AKO SA TO PREKLOPI NA WEB
#   - TRANSAKCIA (kosik) = jedno SEDENIE = jedna navsteva webu (od
#     prichodu po odchod). V datach ho urcuje cislo sedenia "frame".
#   - POLOZKA (vec v kosiku) = KATEGORIA stranky, ktoru pocas tej
#     navstevy clovek otvoril (uvery, ucty, info...).
#   Kosik je teda MNOZINA kategorii navstivenych v jednom sedeni.
#
#   3) PRECO MNOZINA (transakcny model) A NIE PORADIE
#   Berieme len, CO bolo v kosiku, nie v akom PORADI. Preto kazdu
#   kategoriu dame do kosika len raz a zoradime abecedne ("A;B" aj
#   "B;A" je ten isty kosik). Toto vyzaduje algoritmus Apriori (cv6).
#   Alternativa so zachovanym poradim = SEKVENCNY MODEL (vstup pre
#   algoritmy ako PrefixSpan), ten ale v tomto zadani nie je.
#
#   4) PRECO KOSIK MUSI MAT ASPON 2 POLOZKY
#   Pravidlo "A => B" potrebuje aspon dve rozne polozky. Z kosika
#   s jedinou kategoriou ziadnu dvojicu nevyrobime, takze taky
#   kosik je pre hladanie pravidiel zbytocny a vyhodime ho.
#
# VSTUP:
#   in/logs5.csv - POSKYTNUTY bankovy dataset (zo studie v materials/),
#                  oddelovac ";", roky 2009-2012. Nie je to vystup cv1-4;
#                  stlpec frame (sedenie) zodpoveda SESSION_ID z cv1-4.
#
# VYSTUP:
#   out/transakcie_<rok>.csv pre kazdy rok zvlast
#   Tvar: 2 stlpce -> "frame" (cislo sedenia), "category" (zoznam
#         kategorii oddeleny ";")
#
# POUZITE KNIZNICE:
#   pandas - praca s tabulkami (nacitavanie CSV, filtrovanie,
#            zoskupovanie)
#
# ALGORITMUS:
#   Pre kazdy rok zoskupime log podla cisla sedenia, vyrobime
#   z kategorii kosik a ulozime do CSV.

import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))  # umoznuje spustenie skriptu odkialkolvek (nielen z jeho priecinka)

import pandas as pd


# === KROK 1: Nacitanie logu ===

print("Nacitavam logs5.csv...")
# sep=";" = stlpce oddelene bodkociarkou; low_memory=False = pandas precita
# cely subor naraz a spravne urci typy stlpcov.
df = pd.read_csv("in/logs5.csv", sep=";", quotechar='"', low_memory=False)
print(f"Nacitanych: {len(df)} zaznamov")
# unique() = zoznam roznych rokov; kontrola, ze mame data za 2009-2012.
print(f"Roky: {sorted(df['year'].unique())}")


# === KROK 2: Filter - vyber stlpcov a vyhodenie prazdnych kategorii ===

# Ponechame len stlpce, ktore potrebujeme (ostatne zahodime).
# .copy() = samostatna tabulka, aby pandas pri dalsich upravach nevypisoval varovanie.
df = df[["frame", "anonIP", "category", "year", "yearQuartal"]].copy()

# dropna(subset=["category"]) = vyhod riadky, kde kategoria chyba (NaN) -
# bez kategorie niet co dat do kosika.
df = df.dropna(subset=["category"])
print(f"Po filtrovani: {len(df)} zaznamov")


# === KROK 3 + 4: Vytvorenie kosikov pre kazdy rok ===

# Kazdy rok spracujeme zvlast (chceme transakcie za jednotlive obdobia).
for rok in sorted(df["year"].unique()):
    # Vyber len riadky daneho roku.
    df_rok = df[df["year"] == rok]

    # Cielom je: 1 sedenie = 1 riadok so zoznamom jeho kategorii.
    # Citaj retazec sprava dolava:
    #   groupby("frame")["category"] = poskladaj kategorie kazdeho sedenia,
    #   set(x)        = vyhod duplicity (kazda kategoria v kosiku len raz),
    #   sorted(...)   = zorad abecedne (aby "A;B" a "B;A" bol rovnaky kosik),
    #   ";".join(...) = spoj kategorie do jedneho textu "kat1;kat2;...",
    #   reset_index() = sprav z toho normalnu tabulku so stlpcami frame, category.
    transakcie = (
        df_rok.groupby("frame")["category"]
        .apply(lambda x: ";".join(sorted(set(x))))
        .reset_index()
    )

    # Necheme len kosiky s aspon 2 kategoriami. Ak text obsahuje ';', su v nom
    # aspon dve polozky (bodkociarka je oddelovac medzi nimi). Kosik s 1 polozkou
    # by ziadne pravidlo A=>B nedal.
    transakcie = transakcie[transakcie["category"].str.contains(";")]

    # Uloz transakcie daneho roku do vlastneho CSV.
    out_path = f"out/transakcie_{rok}.csv"
    transakcie.to_csv(out_path, index=False)  # index=False = nepridavaj stlpec s cislami riadkov
    print(f"  {rok}: {len(transakcie)} transakcii -> {out_path}")

print("\nHotovo!")
