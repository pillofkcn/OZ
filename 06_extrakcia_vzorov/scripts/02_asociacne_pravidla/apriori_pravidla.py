# ==========================================================
# CV6 - Uloha 02: Hladanie asociacnych pravidiel (Apriori)
# ==========================================================
#
# CIEL:
#   Pre kazdy rok (2009-2012) najst pravidla typu "ked clovek navstivil
#   kategoriu X, casto navstivil aj kategoriu Y". Inymi slovami hladame
#   skupiny kategorii, ktore sa na webe casto objavuju spolocne.
#
# TEORIA (jednoducho):
#
#   1) ASOCIACNE PRAVIDLO  X => Y
#   Cita sa "ked X, tak casto aj Y". Napr. {uvery} => {kalkulacka} =
#   "kto pozeral uvery, casto pozeral aj kalkulacku".
#   X = lava strana, Y = prava strana. Transakcia = jedno sedenie,
#   polozka = kategoria stranky (data z ulohy 01).
#
#   2) TRI CISLA, KTORYMI PRAVIDLO MERIAME (predstav si 1000 sedeni)
#     - support = ako casto su X aj Y SPOLU, z celku.
#         vzorec: support(X=>Y) = pocet(X a Y spolu) / pocet(vsetky sedenia)
#         spolu 50 z 1000 -> 50/1000 = 0.05 (5 %). Cim viac, tym dolezitejsie.
#     - confidence = ked uz mam X, ako casto je tam aj Y.
#         vzorec: confidence(X=>Y) = pocet(X a Y spolu) / pocet(X)
#                                  = support(X a Y) / support(X)
#         X je v 200 sedeniach, z nich 100 ma aj Y -> 100/200 = 0.5 (50 %).
#         Hovori, ako spolahlivo X "predpoveda" Y.
#     - lift = kolkokrat castejsie su X a Y spolu, nez keby vobec nesuviseli.
#         vzorec: lift(X=>Y) = confidence(X=>Y) / support(Y)
#         priklad: confidence 0.5, support(Y) 0.25 -> lift = 0.5/0.25 = 2.
#         1 = nesuvisia, >1 = X zvysuje sancu na Y (zaujimave), <1 = znizuje.
#         Preco: ak je Y caste uz aj samo, vysoka confidence klame - lift to opravi.
#
#   3) FREKVENTOVANA SKUPINA (itemset)
#   Skupina kategorii (napr. {uvery, kalkulacka}). "Frekventovana" = je aspon
#   v min_support podiele sedeni. Pravidla robime len z tychto - zo zriedkavych
#   nema zmysel.
#
#   4) APRIORI A JEHO TRIK
#   Vsetkych moznych skupin je privela na preverenie. Apriori pouzije logiku:
#   ak je mala skupina zriedkava, kazda vacsia skupina s nou je tiez zriedkava
#   (pridanim polozky pocet spolocnych sedeni nemoze narast). Preto male
#   zriedkave skupiny odreze a vacsie z nich uz vobec nepocita. Ide od
#   najmensich skupin (1 polozka -> 2 -> 3 ...) a zriedkave vetvy zahadzuje.
#
#   5) PRAHY (kde je hranica)
#   - min_support    = co je dost caste, aby nas to zaujimalo (tu 5 %).
#   - min_confidence = ako spolahlive musi pravidlo byt, aby preslo (tu 50 %).
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
os.chdir(os.path.dirname(os.path.abspath(__file__)))  # nastavi pracovny priecinok na ten, kde lezi tento skript - vdaka tomu cesty "in/..." a "out/..." funguju aj ked skript spustis odinakial

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
    # Transakcie sme pripravili v ulohe 01, kazdy rok ma vlastny subor.
    df = pd.read_csv(f"in/transakcie_{rok}.csv")
    # V CSV je transakcia ulozena ako jeden text "kat1;kat2;kat3". .str.split(";")
    # ten text rozseka na zoznam ["kat1","kat2","kat3"] (.str = textova operacia
    # pre cely stlpec naraz). .tolist() = prerobi pandas stlpec na obycajny zoznam,
    # takze dostaneme zoznam zoznamov (jeden vnutorny zoznam = jedna transakcia) -
    # presne tvar, ktory Apriori chce.
    transakcie = df["category"].str.split(";").tolist()
    print(f"Pocet transakcii: {len(transakcie)}")

    # === KROK 2: Prerobenie na tabulku ano/nie (one-hot kodovanie) ===
    # Apriori nevie pracovat so zoznamami kategorii, chce tabulku True/False:
    # riadok = transakcia, stlpec = jedna kategoria, bunka = "bola tato kategoria
    # v tejto transakcii?". Takemuto prepisu sa hovori one-hot kodovanie.
    te = TransactionEncoder()
    # fit() = TransactionEncoder si najprv prejde data a zisti zoznam vsetkych
    # kategorii (to budu stlpce); transform() = potom kazdu transakciu prepise na
    # riadok True/False. te_array je vysledna matica True/False.
    te_array = te.fit(transakcie).transform(transakcie)
    # Maticu zabalime do pandas tabulky (DataFrame) a stlpce pomenujeme nazvami
    # kategorii. te.columns_ = zoznam tych nazvov (podtrzitko na konci je zvyk pre
    # atribut, ktory vznikne az po zavolani fit()).
    df_te = pd.DataFrame(te_array, columns=te.columns_)

    # === KROK 3: Najdenie castych skupin kategorii (frekventovane itemsety) ===
    # apriori() prejde tabulku a vrati skupiny kategorii, ktore su aspon v
    # MIN_SUPPORT (5 %) transakcii. use_colnames=True = vo vystupe budu nazvy
    # kategorii, nie cisla stlpcov (s False by boli len cisla, necitatelne).
    # TU SA POCITA SUPPORT: vystupna tabulka ma stlpec "support" - pre kazdu
    # skupinu podiel transakcii, v ktorych sa vyskytuje (support nepocitame rucne,
    # robi to apriori).
    itemsets = apriori(df_te, min_support=MIN_SUPPORT, use_colnames=True)
    print(f"Frekventovanych itemsetov: {len(itemsets)}")

    # === KROK 4: Vytvorenie pravidiel X => Y ===
    # association_rules() z castych skupin vyrobi vsetky pravidla "ked X, tak Y"
    # a necha len tie dost spolahlive. metric="confidence" = filtruj podla
    # spolahlivosti; min_threshold=MIN_CONFIDENCE = necha len pravidla s
    # confidence aspon 50 %.
    # TU SA POCITAJU CONFIDENCE A LIFT: vystupna tabulka pravidiel ma stlpce
    # "confidence" a "lift" (aj "support") - dopocita ich tato funkcia podla
    # vzorcov z hlavicky, opat bez rucneho pocitania v nasom kode.
    pravidla = association_rules(itemsets, metric="confidence", min_threshold=MIN_CONFIDENCE)
    print(f"Asociacnych pravidiel: {len(pravidla)}")

    # Obe strany pravidla su zatial typu frozenset (nemenitelna mnozina poloziek).
    # Prerobime ich na obycajny text "kat1;kat2", aby sa dali ulozit a citat.
    # Pomocna funkcia: vezme mnozinu kategorii, zoradi ich abecedne (mnozina poradie
    # nema, takto je stabilne) a spoji do jedneho textu oddeleneho bodkociarkou.
    def mnozina_na_text(mnozina):
        return ";".join(sorted(mnozina))

    # apply(funkcia) = spusti tuto funkciu na kazdy riadok stlpca a vysledok zapise spat.
    pravidla["antecedents"] = pravidla["antecedents"].apply(mnozina_na_text)
    pravidla["consequents"] = pravidla["consequents"].apply(mnozina_na_text)

    # === KROK 5: Ulozenie pravidiel ===
    # Ulozime 5 stlpcov: obe strany pravidla + tri metriky (support/confidence/lift).
    out_path = f"out/pravidla_{rok}.csv"
    pravidla[["antecedents", "consequents", "support", "confidence", "lift"]].to_csv(out_path, index=False)
    print(f"Ulozene -> {out_path}")
    # Ak nejake pravidla vznikli, ukaz prvych 5 (head) na rychlu kontrolu.
    if len(pravidla) > 0:
        print(pravidla[["antecedents", "consequents", "support", "confidence"]].head(5).to_string())

print("\nHotovo!")
