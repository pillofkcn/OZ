# ==========================================================
# CV6 - Uloha 01: Priprava transakcii pre kazdy rok
# ==========================================================
#
# CIEL:
#   Z logov banky (logs5.csv) urobit TRANSAKCIE - co vsetko jeden
#   pouzivatel pozrel pocas jednej navstevy stranky. Tieto transakcie
#   v dalsich ulohach pouzijeme na hladanie vzorov "kto pozrel A,
#   pozrel aj B" (asociacne pravidla).
#
# TEORIA (od nuly):
#
#   1) CO HLADAME (transakcny model)
#   Mame vela TRANSAKCII - kazda transakcia je zoznam veci, ktore patria k sebe
#   (tu: kategorie stranok navstivene v jednom sedeni). V transakciach hladame
#   veci, ktore sa casto vyskytuju SPOLU. Z toho potom (v dalsich ulohach)
#   robime pravidla typu "ked sa vyskytlo A, casto sa vyskytlo aj B".
#   (Pozn.: metoda vznikla pre nakupne data, preto sa transakcii hovori aj
#   "kosik"; princip je rovnaky bez ohladu na to, ci ide o nakupy alebo web.)
#
#   2) AKO TO VYZERA V NASICH DATACH
#   - TRANSAKCIA = jedno SEDENIE = jedna navsteva webu (od prichodu po odchod).
#     V datach ju urcuje cislo sedenia "frame".
#   - POLOZKA = KATEGORIA stranky, ktoru clovek pocas tej navstevy otvoril
#     (uvery, ucty, info...).
#   Transakcia je teda MNOZINA kategorii navstivenych v jednom sedeni.
#
#   3) PRECO MNOZINA (transakcny model) A NIE PORADIE
#   Berieme len, CO bolo v transakcii, nie v akom PORADI. Preto kazdu kategoriu
#   dame do transakcie len raz a zoradime abecedne ("A;B" aj "B;A" je ta ista
#   transakcia). Toto vyzaduje algoritmus Apriori (cv6). Alternativa so
#   zachovanym poradim = SEKVENCNY MODEL (vstup pre algoritmy ako PrefixSpan),
#   ten ale v tomto zadani nie je.
#
#   4) PRECO TRANSAKCIA MUSI MAT ASPON 2 POLOZKY
#   Pravidlo "A => B" potrebuje aspon dve rozne polozky. Z transakcie s jedinou
#   kategoriou ziadnu dvojicu nevyrobime, takze taka transakcia je pre hladanie
#   pravidiel zbytocna a vyhodime ju.
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
#   Pre kazdy rok zoskupime log podla cisla sedenia, z kategorii sedenia
#   vyrobime transakciu (zoznam kategorii) a ulozime do CSV.

import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))  # nastavi pracovny priecinok na ten, kde lezi tento skript - vdaka tomu cesty "in/..." a "out/..." funguju aj ked skript spustis odinakial

import pandas as pd


# === KROK 1: Nacitanie logu ===

print("Nacitavam logs5.csv...")
# sep=";" = stlpce su oddelene bodkociarkou; quotechar='"' = pole, ktore ma
# vnutri ciarku (napr. URL), drzia uvodzovky ako jednu hodnotu; low_memory=False
# = pandas precita cely subor naraz a az potom urci typ kazdeho stlpca (inak
# pri velkom subore typy hada a moze sa pomylit).
df = pd.read_csv("in/logs5.csv", sep=";", quotechar='"', low_memory=False)
print(f"Nacitanych: {len(df)} zaznamov")
# unique() = zoznam roznych hodnot v stlpci. Tu vypiseme rozne roky (kontrola, ze mame data za 2009-2012).
print(f"Roky: {sorted(df['year'].unique())}")


# === KROK 2: Filter - vyber stlpcov a vyhodenie prazdnych kategorii ===

# Ponechame len 3 stlpce, ktore naozaj potrebujeme (vsetko ostatne zahodime).
# Co je v kazdom z nich:
#   frame    = cislo SEDENIA (jedna navsteva webu od prichodu po odchod);
#              zodpoveda SESSION_ID z cv1-4. Tu sluzi ako IDENTIFIKATOR
#              TRANSAKCIE - riadky s rovnakym frame patria do jednej transakcie.
#   category = KATEGORIA navstivenej stranky (uvery, ucty, Pricing List...).
#              Toto je POLOZKA transakcie - to, co hladame spolu vyskytovat.
#   year     = rok zaznamu (2009-2012). Pouzivame ho na rozdelenie transakcii
#              po rokoch (kazdy rok ide do vlastneho CSV).
# .copy() = vyrobi samostatnu kopiu tabulky, aby pandas pri dalsich upravach
# nevypisoval varovanie (ze menime iba "vyrez" povodnej tabulky).
df = df[["frame", "category", "year"]].copy()

# dropna(subset=["category"]) = vyhod riadky, kde kategoria chyba. Prazdna hodnota
# sa v pandas zapisuje ako NaN (Not a Number = chyba udaj). Bez kategorie niet
# co dat do transakcie, preto taky riadok zahodime.
df = df.dropna(subset=["category"])
print(f"Po filtrovani: {len(df)} zaznamov")


# === KROK 3 + 4: Vytvorenie transakcii pre kazdy rok ===

# Kazdy rok spracujeme zvlast (chceme transakcie za jednotlive obdobia).
for rok in sorted(df["year"].unique()):
    # Vyber len riadky daneho roku.
    df_rok = df[df["year"] == rok]

    # Ciel: z mnohych riadkov jedneho sedenia urobit 1 riadok = zoznam kategorii.
    # df_rok.groupby("frame") = zoberie tabulku roka a ROZDELI jej riadky do skupin
    # podla hodnoty v stlpci "frame" (cislo sedenia). Vsetky riadky s rovnakym frame
    # (= kliknutia v tom istom sedeni) padnu do jednej skupiny. Nevznikne bezna
    # tabulka, ale "zoskupeny" objekt, ktory sa da prejst cyklom.
    zoznam_transakcii = []  # sem budeme pridavat hotove transakcie (jeden slovnik = jeden riadok)

    # Cyklus berie skupiny jednu po druhej a v kazdom kroku vrati DVOJICU:
    #   cislo_sedenia = hodnota frame danej skupiny (cislo sedenia),
    #   skupina       = mala tabulka = vsetky riadky (kliknutia) tohto sedenia.
    for cislo_sedenia, skupina in df_rok.groupby("frame"):
        # set(...)    = z kategorii sedenia vyhod opakovania (kazdu kategoriu len raz),
        # sorted(...) = zorad ich abecedne (aby "A;B" a "B;A" bola ta ista transakcia).
        kategorie = sorted(set(skupina["category"]))

        # Chceme len transakcie s aspon 2 kategoriami - z jednej kategorie ziadne
        # pravidlo "A => B" nevznikne. Take sedenie preskocime (continue = chod na dalsie).
        if len(kategorie) < 2:
            continue

        # ";".join(...) = spoj kategorie do jedneho textu, napr. "ucty;uvery".
        text_kategorii = ";".join(kategorie)
        zoznam_transakcii.append({"frame": cislo_sedenia, "category": text_kategorii})

    # Zo zoznamu slovnikov spravime peknu tabulku so stlpcami frame, category.
    transakcie = pd.DataFrame(zoznam_transakcii)

    # Uloz transakcie daneho roku do vlastneho CSV.
    out_path = f"out/transakcie_{rok}.csv"
    transakcie.to_csv(out_path, index=False)  # index=False = nepridavaj stlpec s cislami riadkov
    print(f"  {rok}: {len(transakcie)} transakcii -> {out_path}")

print("\nHotovo!")
