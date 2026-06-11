# ==========================================================
# CV5 - Uloha 02: Hladanie asociacnych pravidiel (Apriori)
# ==========================================================
#
# CIEL:
#   Pre kazdy rok (2009-2012) najst pravidla typu "ked clovek navstivil
#   kategoriu X, casto navstivil aj kategoriu Y". Inymi slovami hladame
#   skupiny kategorii, ktore sa na webe casto objavuju spolocne.
#
# TEORIA - vysvetlene jednoducho:
#   Predstav si nakupne kosiky v obchode. Kazdy clovek si dal do kosika
#   par veci. My chceme najst dvojice/trojice veci, co ludia kupuju
#   spolu (klasicky priklad: chlieb + maslo). Tu nie je obchod, ale web:
#   "kosik" = jedno sedenie (jedna navsteva webu), "veci v kosiku" =
#   kategorie stranok, ktore clovek pocas tej navstevy otvoril.
#
#   Tri cisla, podla ktorych hodnotime pravidla X => Y:
#     - support    = ako casto sa X aj Y vyskytnu spolu (podiel transakcii).
#                    Napr. 0.05 = "v 5% navstev sa to stalo".
#     - confidence = ked uz mam X, aka je sanca ze tam je aj Y.
#                    Napr. 0.5 = "v polovici pripadov ked je X, je aj Y".
#     - lift       = kolkokrat castejsie sa X a Y vyskytnu spolu, ako by
#                    sme cakali keby boli nezavisle. lift > 1 znamena
#                    "tie dve veci sa pritahuju" (suvisia).
#
#   Apriori je algoritmus, ktory tieto pravidla najde rozumne rychlo.
#   Postupne stavia vacsie a vacsie skupiny kategorii od najmensich.
#   Ked nejaka mala skupina nie je dost casta, vsetky vacsie skupiny
#   ktore ju obsahuju, zahodi (uz nemozu byt castejsie).
#
# VSTUP:  in/transakcie_{rok}.csv  - jeden riadok = jedno sedenie,
#                                    stlpec category = "kat1;kat2;kat3"
# VYSTUP: out/pravidla_{rok}.csv   - najdene pravidla a ich metriky
#
# POUZITE KNIZNICE:
#   - pandas:                tabulky a citanie CSV
#   - mlxtend (apriori,
#     TransactionEncoder,
#     association_rules):    samotny Apriori algoritmus a pomocnici
#
# ALGORITMUS: pre kazdy rok zvlast nacitame transakcie, prerobime ich
# na tabulku ano/nie (mal kategoriu / nemal), spustime Apriori a z toho
# vyrobime pravidla X => Y a ulozime ich.
# ==========================================================

import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))  # umoznuje spustenie skriptu odkialkolvek (nielen z jeho priecinka)

import pandas as pd
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori, association_rules

# --- Nastavenia ---
# MIN_SUPPORT = aspon v 5% sedeni musi byt skupina kategorii, inak ju zahodime.
# MIN_CONFIDENCE = pravidlo "ked X, tak aj Y" plati aspon v 50% pripadov.
MIN_SUPPORT = 0.05      # minimalna podpora 5%
MIN_CONFIDENCE = 0.5    # minimalna spolahlivost 50%

# Kazdy rok spracujeme samostatne, lebo nas zaujimaju pravidla pre dane obdobie.
for rok in [2009, 2010, 2011, 2012]:
    print(f"\n=== Rok {rok} ===")

    # === KROK 1: Nacitanie transakcii ===
    # Subor obsahuje vycistene sedenia z predoslej ulohy.
    df = pd.read_csv(f"in/transakcie_{rok}.csv")
    # Z textu "kat1;kat2;kat3" spravime zoznam ["kat1","kat2","kat3"].
    # Vysledok je zoznam zoznamov - presny tvar co Apriori potrebuje.
    transakcie = df["category"].str.split(";").tolist()
    print(f"Pocet transakcii: {len(transakcie)}")

    # === KROK 2: Prerobenie na tabulku ano/nie ===
    # Apriori potrebuje tabulku: riadky = sedenia, stlpce = vsetky kategorie,
    # bunka True/False = "obsahovalo to sedenie tuto kategoriu?".
    te = TransactionEncoder()
    te_array = te.fit(transakcie).transform(transakcie)
    # Zabalime do tabulky s nazvami stlpcov, aby pravidla pouzivali nazvy kategorii.
    df_te = pd.DataFrame(te_array, columns=te.columns_)

    # === KROK 3: Najdenie castych skupin kategorii ===
    # Apriori vrati skupiny kategorii, ktore sa objavuju v aspon 5% sedeni.
    # use_colnames=True = vo vystupe budu nazvy kategorii, nie cisla stlpcov.
    itemsets = apriori(df_te, min_support=MIN_SUPPORT, use_colnames=True)
    print(f"Frekventovanych itemsetov: {len(itemsets)}")

    # === KROK 4: Vytvorenie pravidiel X => Y ===
    # Z kazdej najdenej skupiny vyrobi vsetky mozne pravidla "ked X, tak Y"
    # a nechame len tie, kde spolahlivost (confidence) je aspon 50%.
    pravidla = association_rules(itemsets, metric="confidence", min_threshold=MIN_CONFIDENCE)
    print(f"Asociacnych pravidiel: {len(pravidla)}")

    # Lava aj prava strana pravidla je zatial specialna mnozina (frozenset).
    # Spravime z toho normalny text "kat1;kat2", aby sa to dalo precitat v Exceli.
    # sorted = aby bolo poradie kategorii vzdy rovnake (mnozina ho nema).
    pravidla["antecedents"] = pravidla["antecedents"].apply(lambda x: ";".join(sorted(x)))
    pravidla["consequents"] = pravidla["consequents"].apply(lambda x: ";".join(sorted(x)))

    # === KROK 5: Ulozenie pravidiel ===
    # Ulozime len 5 dolezitych stlpcov - obe strany pravidla a tri metriky.
    out_path = f"out/pravidla_{rok}.csv"
    pravidla[["antecedents", "consequents", "support", "confidence", "lift"]].to_csv(out_path, index=False)
    print(f"Ulozene -> {out_path}")
    # Ukazka prvych 5 pravidiel pre rychlu kontrolu (len ak nieco vzniklo).
    if len(pravidla) > 0:
        print(pravidla[["antecedents", "consequents", "support", "confidence"]].head(5).to_string())

print("\nHotovo!")
