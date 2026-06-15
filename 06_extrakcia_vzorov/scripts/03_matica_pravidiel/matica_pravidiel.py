# ==========================================================
# CV6 - Uloha 03: Matica unikatnych pravidiel cez obdobia
# ==========================================================
#
# CIEL:
#   V predoslych skriptoch sme z log suboru vytahli "asociacne pravidla"
#   (typu: ked pouzivatel pozrel stranku A, casto pozrie aj stranku B)
#   zvlast pre roky 2009, 2010, 2011 a 2012. Tu vsetky pravidla spojime
#   do jednej velkej tabulky, kde kazdy riadok je jedno pravidlo a stlpce
#   hovoria, ci sa to pravidlo objavilo v danom roku (1) alebo nie (0).
#   Vystupom potom v dalsom skripte statisticky overujeme, ci sa spravanie
#   pouzivatelov medzi rokmi menilo.
#
# TEORIA (jednoducho):
#
#   1) PRIPOMIENKA: ASOCIACNE PRAVIDLO
#   Pravidlo "ak X, tak typicky aj Y", napr. {/uvod} => {/produkty}.
#   Nasiel ich v ulohe 02 algoritmus Apriori, zvlast pre kazdy rok.
#
#   2) PROBLEM: AKO POROVNAT 4 ROKY
#   Kazdy rok ma vlastny zoznam pravidiel a niektore pravidla su len v jednom
#   roku, ine vo viacerych. Chceme jednu tabulku, kde hned vidno, ktore pravidlo
#   bolo v ktorom roku.
#
#   3) AKO NA TO - DVA NAPADY
#   a) Pravidlo zapiseme ako jeden text "lava => prava". Rovnaky text = rovnake
#      pravidlo, takze ho lahko rozozname naprie rokmi (porovnanie textov je jasne).
#   b) Postavime tabulku 0/1:
#        - RIADOK  = jedno pravidlo (zo vsetkych rokov dohromady, kazde raz),
#        - STLPEC  = jeden rok (O1_2009 ... O4_2012),
#        - BUNKA   = 1 ak pravidlo v tom roku bolo, inak 0.
#
#   4) PRECO PRAVE TAKATO TABULKA
#   Dalsia uloha (Cochranov Q test) chce presne data 0/1 merane opakovane na tych
#   istych objektoch (tu: tie iste pravidla, kazde merane v 4 rokoch) - tato tabulka
#   je jeho priamy vstup. Stlpec pocet_obdobi (sucet jednotiek v riadku) navyse
#   hned ukaze, ake stabilne pravidlo je: 1 = len v jednom roku, 4 = vo vsetkych.
#
# VSTUP:
#   in/pravidla_2009.csv, ..., in/pravidla_2012.csv
#   Kazdy CSV ma stlpce 'antecedents' (lava strana) a 'consequents' (prava).
#
# VYSTUP:
#   out/matica_pravidiel.csv
#   Stlpce: pravidlo, O1_2009, O2_2010, O3_2011, O4_2012, pocet_obdobi.
#   Riadky: vsetky unikatne pravidla zo vsetkych rokov dohromady (~450).
#
# POUZITE KNIZNICE:
#   pandas - praca s tabulkami (nacitanie CSV, vytvorenie matice, ulozenie)
#
# ALGORITMUS:
#   Nacitaj 4 CSV -> spoj pravidla do jednej mnoziny -> pre kazde pravidlo
#   a kazdy rok zapis 1 (je tam) alebo 0 (nie je) -> uloz vysledok.

import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))  # nastavi pracovny priecinok na ten, kde lezi tento skript - vdaka tomu cesty "in/..." a "out/..." funguju aj ked skript spustis odinakial

import pandas as pd  # kniznica na pracu s tabulkami

# Styri obdobia (roky), pre ktore mame pravidla. Poradie tu urci poradie stlpcov O1..O4.
obdobia = [2009, 2010, 2011, 2012]

# === KROK 1: Nacitanie pravidiel z CSV suborov ===
# Pre kazdy rok si zostavime MNOZINU jeho pravidiel. Kazde pravidlo prepiseme
# na jeden text "lava => prava", aby sme to iste pravidlo vedeli rozoznat
# naprie rokmi (porovnanie textov je jednoznacne).

pravidla_po_obdobiach = {}  # slovnik { rok: mnozina textov pravidiel }
for rok in obdobia:
    df = pd.read_csv(f"in/pravidla_{rok}.csv")  # pravidla daneho roku z ulohy 02
    # Spojime obe strany do jedneho textu, napr. "{/uvod} => {/produkty}".
    df["pravidlo"] = df["antecedents"] + " => " + df["consequents"]
    # .tolist() = prerobi stlpec pravidiel na obycajny zoznam. set(...) = mnozina:
    # automaticky vyhodi pripadne duplicity a rychlo sa v nej overuje, ci nieco
    # obsahuje (test "je v nej?" je v mnozine okamzity).
    pravidla_po_obdobiach[rok] = set(df["pravidlo"].tolist())
    print(f"Rok {rok}: {len(pravidla_po_obdobiach[rok])} pravidiel")  # kontrola (podla zadania aspon 10)

# === KROK 2: Zjednotenie vsetkych pravidiel zo vsetkych rokov ===
# Chceme jeden zoznam vsetkych roznych pravidiel (kazde prave raz, aj keby bolo
# vo viacerych rokoch). Zacneme prazdnou mnozinou a postupne do nej pridame
# pravidla kazdeho roku. Mnozina sa o duplicity postara sama - to iste pravidlo
# v nej nikdy nebude dvakrat.
vsetky_pravidla = set()
for rok in obdobia:
    vsetky_pravidla.update(pravidla_po_obdobiach[rok])  # update = pridaj do mnoziny vsetky pravidla daneho roku
print(f"\nUnikatnych pravidiel celkom: {len(vsetky_pravidla)}")

# === KROK 3: Vytvorenie binarnej matice (riadky=pravidla, stlpce=roky) ===
# Tabulka, kde pre kazde pravidlo a kazdy rok bude 1 (vyskytlo sa) alebo 0.
# Toto je presny vstup pre Cochranov Q test v dalsom skripte.

# Zaciatok: tabulka s jednym stlpcom "pravidlo". sorted = stabilne, vzdy rovnake poradie.
matica = pd.DataFrame({"pravidlo": sorted(vsetky_pravidla)})

# Pridame stlpce O1_2009 ... O4_2012, jeden za druhym.
# enumerate(obdobia, 1) = prejde zoznam rokov a ku kazdemu prida poradove cislo
# od 1: (1,2009), (2,2010), (3,2011), (4,2012). Cislo i pouzijeme v nazve stlpca.
nazvy_stlpcov_obdobi = []  # nazvy stlpcov O1..O4 - zidu sa nam aj v KROKU 4
for i, rok in enumerate(obdobia, 1):
    nazov_stlpca = f"O{i}_{rok}"            # napr. "O1_2009"
    nazvy_stlpcov_obdobi.append(nazov_stlpca)
    pravidla_roku = pravidla_po_obdobiach[rok]  # mnozina pravidiel daneho roku

    # Pre kazde pravidlo v tabulke zapiseme 1 (bolo v tomto roku) alebo 0 (nebolo).
    stlpec = []  # sem nazbierame hodnoty 0/1, riadok po riadku
    for pravidlo in matica["pravidlo"]:
        if pravidlo in pravidla_roku:       # "in" = je toto pravidlo v mnozine roku?
            stlpec.append(1)
        else:
            stlpec.append(0)

    matica[nazov_stlpca] = stlpec           # hotovy zoznam 0/1 vlozime ako novy stlpec

# === KROK 4: Doplnkovy stlpec - v kolkych rokoch sa pravidlo vyskytlo ===
# Vezmeme len stlpce rokov (O1..O4, mame ich uz pripravene v nazvy_stlpcov_obdobi)
# a v kazdom RIADKU ich scitame. .sum(axis=1) = "scitaj naprie stlpcami, pre kazdy
# riadok zvlast". Kedze su to 0/1, sucet = pocet rokov, v ktorych pravidlo bolo:
# 1 = len v jednom roku (jednorazove), 4 = vo vsetkych rokoch (stabilne).
matica["pocet_obdobi"] = matica[nazvy_stlpcov_obdobi].sum(axis=1)

# === KROK 5: Ulozenie matice do CSV ===
matica.to_csv("out/matica_pravidiel.csv", index=False)  # index=False = bez stlpca s cislami riadkov

# === Zhrnutie pre kontrolu ===
print(f"\nVystupna matica: {matica.shape}")  # shape = dvojica (pocet riadkov=pravidiel, pocet stlpcov)

# value_counts() spocita, kolko pravidiel ma pocet_obdobi 1, 2, 3, 4 (teda kolko
# pravidiel bolo v 1 roku, kolko v 2 rokoch...). sort_index() zoradi vysledok
# podla poctu obdobi (1 -> 4), nie podla poctu pravidiel.
print("\nPocet pravidiel podla poctu obdobi vyskytu:")
print(matica["pocet_obdobi"].value_counts().sort_index())

# Ukazka prvych 10 pravidiel; to_string() vypise plne texty bez skracovania.
print("\nUkazka prvych 10 pravidiel:")
print(matica.head(10).to_string())
