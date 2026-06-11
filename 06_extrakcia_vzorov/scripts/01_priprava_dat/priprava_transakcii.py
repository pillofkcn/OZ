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
# TEORIA - jednoducho:
#   Asociacne pravidlo = pravidlo typu "kto kupil chleb, kupil aj
#   maslo". V nasom pripade nejde o nakup, ale o navstevu kategorii
#   na webe banky pocas jedneho sedenia (sedenie = jedna navsteva
#   stranky od prichodu po odchod).
#   Transakcia (kosik) = mnozina veci, ktore patria spolu (sem
#   patria vsetky kategorie navstivene v jednom sedeni).
#   Aby z kosika vznikla aspon jedna dvojica typu A->B, musi mat
#   aspon 2 polozky. Kosiky s 1 polozkou nas teda nezaujimaju.
#
#   POZN. k typu modelu: Pouzivame TRANSAKCNY MODEL - kosik je
#   MNOZINA kategorii (poradie navstevy sa stratuje). Apriori (cv6)
#   toto vyzaduje. Alternativou by bol SEKVENCNY MODEL (zachovane
#   poradie), ktory by bol vstupom pre algoritmy ako PrefixSpan -
#   to vsak nie je v zadani tohto cvicenia.
#
# VSTUP:
#   in/logs5.csv - log banky, oddelovac ";", roky 2009-2012
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
df = pd.read_csv("in/logs5.csv", sep=";", quotechar='"', low_memory=False)  # nacitame log; sep=";" lebo stlpce su oddelene bodkociarkou; low_memory=False = pandas si data prejde celé a urci typy stlpcov spravne
print(f"Nacitanych: {len(df)} zaznamov")
print(f"Roky: {sorted(df['year'].unique())}")  # vypiseme aké roky su v datach (kontrola, ze sme nacitali vsetko)


# === KROK 2: Filter - vyber stlpcov a vyhodenie prazdnych kategorii ===

# Z celeho logu nas zaujimaju len tieto stlpce. Ostatne nepotrebujeme.
# .copy() vyrobi novu tabulku, aby pandas nehlasil varovanie pri uprave.
df = df[["frame", "anonIP", "category", "year", "yearQuartal"]].copy()

# Riadky bez kategorie nemozeme dat do kosika - vyhodime ich.
df = df.dropna(subset=["category"])
print(f"Po filtrovani: {len(df)} zaznamov")


# === KROK 3 + 4: Vytvorenie kosikov pre kazdy rok ===

for rok in sorted(df["year"].unique()):
    # Z celeho logu vyberieme len riadky pre aktualny rok.
    df_rok = df[df["year"] == rok]

    # Pre kazde sedenie chceme jeden riadok so zoznamom kategorii.
    # groupby("frame") = zoskupime riadky podla cisla sedenia.
    # set(x) = vyhodime duplicity (kazdu kategoriu chceme len raz).
    # sorted(...) = zoradime abecedne, aby kosik "A;B" a "B;A"
    #               vychadzal rovnako (aby vysledok bol stale rovnaky).
    # ";".join(...) = spojime kategorie do jedneho retazca, aby sa
    #                 dali ulozit do CSV.
    transakcie = (
        df_rok.groupby("frame")["category"]
        .apply(lambda x: ";".join(sorted(set(x))))
        .reset_index()
    )

    # Ponechame len kosiky s aspon 2 kategoriami.
    # Ak retazec obsahuje aspon jednu ';', znamena to, ze su v nom
    # aspon 2 polozky (bodkociarka je medzi nimi oddelovac).
    transakcie = transakcie[transakcie["category"].str.contains(";")]

    # Vysledok ulozime do CSV - kazdy rok vlastny subor.
    out_path = f"out/transakcie_{rok}.csv"
    transakcie.to_csv(out_path, index=False)  # index=False = nezapise pomocne cislovanie riadkov, vystup ostane cisty
    print(f"  {rok}: {len(transakcie)} transakcii -> {out_path}")

print("\nHotovo!")
