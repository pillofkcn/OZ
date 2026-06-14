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
# TEORIA (od nuly - akoby si to nikdy nevidel):
#
#   1) PRIPOMENUTIE: ASOCIACNE PRAVIDLO
#   Pravidlo ma tvar "ak X, tak typicky aj Y". Lava strana = antecedents,
#   prava = consequents. Priklad: {/uvod} => {/produkty}. Pravidla nasiel
#   v ulohe 02 algoritmus Apriori, zvlast pre kazdy rok.
#
#   2) PROBLEM: AKO POROVNAT 4 ROKY
#   Pre kazdy rok mame vlastny zoznam pravidiel. Niektore pravidla su
#   v jednom roku a v inom nie. Chceme jednu prehladnu tabulku, z ktorej
#   sa da povedat, ktore pravidlo bolo v ktorom roku.
#
#   3) RIESENIE A: PRAVIDLO AKO TEXT
#   Kazde pravidlo prepiseme do jedneho textu "antecedents => consequents".
#   Vyhoda: rovnaky text = rovnake pravidlo, takze ho vieme rozoznat naprie
#   rokmi (porovnavanie textov je jednoznacne).
#
#   4) RIESENIE B: BINARNA MATICA VYSKYTU
#   Postavime tabulku, kde:
#     - kazdy RIADOK = jedno unikatne pravidlo (zo vsetkych rokov dohromady),
#     - kazdy STLPEC = jeden rok (O1_2009 ... O4_2012),
#     - BUNKA = 1 ak sa pravidlo v tom roku objavilo, inak 0.
#   Je to "kto-kde" mapa: jednym pohladom vidno vyskyt pravidla v case.
#
#   5) PRECO PRAVE TAKATO MATICA
#   Nasledujuci test (Cochranov Q) potrebuje presne data 0/1 merane
#   opakovane na tych istych objektoch (tu: tie iste pravidla, merane v 4
#   rokoch). Tato matica je teda priamo jeho vstup. Stlpec pocet_obdobi
#   (sucet jednotiek v riadku) navyse hned ukaze, ako stabilne pravidlo je:
#   1 = bolo len v jednom roku, 4 = bolo vo vsetkych styroch.
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
os.chdir(os.path.dirname(os.path.abspath(__file__)))  # umoznuje spustenie skriptu odkialkolvek (nielen z jeho priecinka)

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
    # set(...) = mnozina: automaticky vyhodi pripadne duplicity a rychlo sa v nej overuje "je v nej?".
    pravidla_po_obdobiach[rok] = set(df["pravidlo"].tolist())
    print(f"Rok {rok}: {len(pravidla_po_obdobiach[rok])} pravidiel")  # kontrola (podla zadania aspon 10)

# === KROK 2: Zjednotenie vsetkych pravidiel zo vsetkych rokov ===
# union spoji vsetky 4 mnoziny do jednej; kazde pravidlo v nej bude prave raz,
# aj keby sa vyskytlo vo viacerych rokoch. *... = rozbali hodnoty slovnika ako
# samostatne argumenty pre union.
vsetky_pravidla = set().union(*pravidla_po_obdobiach.values())
print(f"\nUnikatnych pravidiel celkom: {len(vsetky_pravidla)}")

# === KROK 3: Vytvorenie binarnej matice (riadky=pravidla, stlpce=roky) ===
# Tabulka, kde pre kazde pravidlo a kazdy rok bude 1 (vyskytlo sa) alebo 0.
# Toto je presny vstup pre Cochranov Q test v dalsom skripte.

# Zaciatok: tabulka s jednym stlpcom "pravidlo". sorted = stabilne, vzdy rovnake poradie.
matica = pd.DataFrame({"pravidlo": sorted(vsetky_pravidla)})

# Pridame stlpce O1_2009 ... O4_2012. enumerate(obdobia, 1) = dvojice (1,2009),(2,2010)...
for i, rok in enumerate(obdobia, 1):
    nazov_stlpca = f"O{i}_{rok}"  # napr. "O1_2009"
    # Pre kazde pravidlo (apply ide po riadkoch): daj 1, ak je v mnozine pravidiel
    # daneho roku, inak 0. (in = overenie clenstva v mnozine.)
    matica[nazov_stlpca] = matica["pravidlo"].apply(
        lambda p: 1 if p in pravidla_po_obdobiach[rok] else 0
    )

# === KROK 4: Doplnkovy stlpec - v kolkych rokoch sa pravidlo vyskytlo ===
# sum(axis=1) = scitaj hodnoty v RIADKU (cez stlpce O1..O4). Vysledok:
# 1 = pravidlo bolo len v jednom roku (jednorazove), 4 = vo vsetkych rokoch (stabilne).
matica["pocet_obdobi"] = matica[[f"O{i}_{r}" for i, r in enumerate(obdobia, 1)]].sum(axis=1)

# === KROK 5: Ulozenie matice do CSV ===
matica.to_csv("out/matica_pravidiel.csv", index=False)  # index=False = bez stlpca s cislami riadkov

# === Zhrnutie pre kontrolu ===
print(f"\nVystupna matica: {matica.shape}")  # shape = (pocet pravidiel, pocet stlpcov)

# value_counts() spocita, kolko pravidiel ma pocet_obdobi 1, 2, 3, 4; sort_index zoradi podla 1->4.
print("\nPocet pravidiel podla poctu obdobi vyskytu:")
print(matica["pocet_obdobi"].value_counts().sort_index())

# Ukazka prvych 10 pravidiel; to_string() vypise plne texty bez skracovania.
print("\nUkazka prvych 10 pravidiel:")
print(matica.head(10).to_string())
