# ==========================================================
# CV6 - Uloha 02: Hladanie asociacnych pravidiel (Apriori)
# ==========================================================
#
# CIEL:
#   Pre kazdy rok (2009-2012) najst pravidla typu "ked clovek navstivil
#   kategoriu X, casto navstivil aj kategoriu Y". Inymi slovami hladame
#   skupiny kategorii, ktore sa na webe casto objavuju spolocne.
#
# TEORIA (od nuly - akoby si asociacne pravidla nikdy nevidel):
#
#   1) CO JE ASOCIACNE PRAVIDLO X => Y
#   Pravidlo "X => Y" znamena: "ked je v kosiku X, casto je v nom aj Y".
#   X = lava strana (antecedent), Y = prava strana (consequent). Kosik =
#   jedno sedenie, polozky = kategorie stranok (z ulohy 01). Priklad:
#   {uvery} => {kalkulacka}  ("kto pozeral uvery, casto aj kalkulacku").
#
#   2) TRI CISLA, KTORYMI PRAVIDLO HODNOTIME
#   Majme 1000 sedeni (kosikov).
#     - support (podpora) = ako casto sa X aj Y vyskytnu SPOLU, ako podiel
#       zo VSETKYCH kosikov. Ak su X a Y spolu v 50 z 1000 -> support 0.05
#       (5%). Hovori "ako caste/dolezite je toto vobec".
#     - confidence (spolahlivost) = KED UZ mam v kosiku X, aka je sanca,
#       ze je v nom aj Y. = (kosiky s X aj Y) / (kosiky s X). Ak X je v
#       200 kosikoch a z nich 100 ma aj Y -> confidence 0.5 (50%). Hovori
#       "ako spolahlivo X "predpoveda" Y".
#     - lift (zdvih) = kolkokrat CASTEJSIE su X a Y spolu, nez keby spolu
#       nijako nesuviseli (boli nezavisle). lift = confidence / support(Y).
#         lift = 1  -> nezavisle (Y je s X presne tak caste ako vseobecne),
#         lift > 1  -> "pritahuju sa" (X zvysuje sancu na Y) = zaujimave,
#         lift < 1  -> "odpudzuju sa" (X znizuje sancu na Y).
#       Preco lift: confidence sama klame, ak je Y caste uz aj bez X.
#
#   3) FREKVENTOVANY ITEMSET
#   Itemset = skupina poloziek (napr. {uvery, kalkulacka}). "Frekventovany"
#   = vyskytuje sa aspon v min_support podiele kosikov. Pravidla sa robia
#   len z frekventovanych itemsetov (zo zriedkavych nema zmysel).
#
#   4) APRIORI A JEHO TRIK (anti-monotonia)
#   Naivne by sme museli preverit vsetky mozne skupiny kategorii - tych je
#   privela. Apriori vyuziva pravidlo: AK je nejaka mala skupina zriedkava,
#   tak KAZDA vacsia skupina, ktora ju obsahuje, je este zriedkavejsia
#   (pridanim polozky pocet kosikov nemoze narast). Preto staci, ze hned
#   ako je mala skupina pod prahom, vsetky jej nadskupiny zahodime bez
#   pocitania. Tym sa hladanie obrovsky zrychli. Apriori teda stava skupiny
#   od najmensich (1 polozka -> 2 -> 3 ...) a zriedkave vetvy odrezava.
#
#   5) PRAHY
#   - min_support    = co je dost caste, aby nas to zaujimalo (tu 5%).
#   - min_confidence = ako spolahlive musi pravidlo byt, aby preslo (tu 50%).
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
    # Transakcie (kosiky) sme pripravili v ulohe 01, kazdy rok ma vlastny subor.
    df = pd.read_csv(f"in/transakcie_{rok}.csv")
    # V CSV je kosik ulozeny ako jeden text "kat1;kat2;kat3". split(";") ho
    # rozseka spat na zoznam ["kat1","kat2","kat3"]. tolist() = zoznam takychto
    # zoznamov (jeden na kazdy kosik) - presne tvar, ktory Apriori chce.
    transakcie = df["category"].str.split(";").tolist()
    print(f"Pocet transakcii: {len(transakcie)}")

    # === KROK 2: Prerobenie na tabulku ano/nie (one-hot) ===
    # Apriori nevie pracovat so zoznamami kategorii, chce tabulku 0/1:
    # riadok = kosik, stlpec = jedna kategoria, bunka True/False = "bola
    # tato kategoria v tomto kosiku?".
    te = TransactionEncoder()
    te_array = te.fit(transakcie).transform(transakcie)  # fit = zisti vsetky kategorie, transform = vyrobi True/False maticu
    # Zabalime do DataFrame a stlpce pomenujeme nazvami kategorii (te.columns_).
    df_te = pd.DataFrame(te_array, columns=te.columns_)

    # === KROK 3: Najdenie castych skupin kategorii (frekventovane itemsety) ===
    # apriori vrati skupiny kategorii, ktore su aspon v MIN_SUPPORT (5%) kosikov.
    # use_colnames=True = vo vystupe budu nazvy kategorii, nie cisla stlpcov.
    itemsets = apriori(df_te, min_support=MIN_SUPPORT, use_colnames=True)
    print(f"Frekventovanych itemsetov: {len(itemsets)}")

    # === KROK 4: Vytvorenie pravidiel X => Y ===
    # Z castych skupin vyrobi vsetky pravidla "ked X, tak Y" a necha len tie so
    # spolahlivostou aspon MIN_CONFIDENCE (50%). metric/min_threshold = podla
    # akej metriky a od akej hranice pravidla filtrovat.
    pravidla = association_rules(itemsets, metric="confidence", min_threshold=MIN_CONFIDENCE)
    print(f"Asociacnych pravidiel: {len(pravidla)}")

    # Obe strany pravidla su zatial frozenset (specialna mnozina). Prerobime ich
    # na obycajny text "kat1;kat2", aby sa dali ulozit a citat. sorted = stabilne
    # poradie (mnozina poradie nema), join = spoji do jedneho retazca.
    pravidla["antecedents"] = pravidla["antecedents"].apply(lambda x: ";".join(sorted(x)))
    pravidla["consequents"] = pravidla["consequents"].apply(lambda x: ";".join(sorted(x)))

    # === KROK 5: Ulozenie pravidiel ===
    # Ulozime 5 stlpcov: obe strany pravidla + tri metriky (support/confidence/lift).
    out_path = f"out/pravidla_{rok}.csv"
    pravidla[["antecedents", "consequents", "support", "confidence", "lift"]].to_csv(out_path, index=False)
    print(f"Ulozene -> {out_path}")
    # Ak nejake pravidla vznikli, ukaz prvych 5 (head) na rychlu kontrolu.
    if len(pravidla) > 0:
        print(pravidla[["antecedents", "consequents", "support", "confidence"]].head(5).to_string())

print("\nHotovo!")
