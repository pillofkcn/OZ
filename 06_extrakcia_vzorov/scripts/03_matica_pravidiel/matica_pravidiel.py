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
#   - Asociacne pravidlo ma tvar "ak X, tak typicky aj Y". Lava strana sa
#     vola antecedents, prava strana consequents. Priklad pravidla:
#       {/uvod} => {/produkty}  (kto pozrel uvod, casto pozrie produkty)
#   - Pravidla sme z dat extrahovali algoritmom Apriori (najde casto
#     spolu sa vyskytujuce skupiny stranok a postavi z nich pravidla).
#   - Aby sme vedeli porovnavat roky, kazde pravidlo prepiseme do textu
#     "antecedents => consequents". Rovnaky text = rovnake pravidlo.
#   - Vystupna binarna matica (samé 0 a 1) je presne to, co potrebuje
#     nasledujuci test (Cochran Q) — ten porovna, ci sa pravidla v rokoch
#     vyskytuju rovnako casto.
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

# styri obdobia (roky), pre ktore mame pravidla; poradie urci stlpce O1..O4
obdobia = [2009, 2010, 2011, 2012]

# === KROK 1: Nacitanie pravidiel z CSV suborov ===
# Pre kazdy rok si do "tasky" (mnozina) ulozime vsetky pravidla z toho roku.
# Pravidlo prepiseme do textovej podoby "lava_strana => prava_strana",
# aby sme rovnake pravidlo vedeli rozoznat v roznych rokoch.

pravidla_po_obdobiach = {}  # bude: { rok: mnozina textov pravidiel }
for rok in obdobia:
    df = pd.read_csv(f"in/pravidla_{rok}.csv")  # nacitame pravidla pre dany rok
    # spojime obe strany pravidla do jedneho textu, napr. "{/uvod} => {/produkty}"
    df["pravidlo"] = df["antecedents"] + " => " + df["consequents"]
    # ulozime ako mnozinu - automaticky vyhodi duplicity a rychlo sa v nej hlada
    pravidla_po_obdobiach[rok] = set(df["pravidlo"].tolist())
    # vypiseme pocet pravidiel pre kontrolu (musi byt aspon 10 podla zadania)
    print(f"Rok {rok}: {len(pravidla_po_obdobiach[rok])} pravidiel")

# === KROK 2: Zjednotenie vsetkych pravidiel zo vsetkych rokov ===
# Spojime vsetky styri mnoziny do jednej velkej - kazde pravidlo bude v nej
# presne raz, aj ked sa objavilo vo viacerych rokoch.
vsetky_pravidla = set().union(*pravidla_po_obdobiach.values())
print(f"\nUnikatnych pravidiel celkom: {len(vsetky_pravidla)}")

# === KROK 3: Vytvorenie binarnej matice (riadky=pravidla, stlpce=roky) ===
# Pre kazde pravidlo zapiseme do kazdeho stlpca 1 ak sa v danom roku objavilo,
# alebo 0 ak nie. Takato matica je vstup pre statisticke testy v dalsom skripte.

# vyrobime tabulku s jednym stlpcom 'pravidlo'; sorted = vzdy rovnake poradie
matica = pd.DataFrame({"pravidlo": sorted(vsetky_pravidla)})

# pridame stlpce O1_2009, O2_2010, O3_2011, O4_2012
for i, rok in enumerate(obdobia, 1):
    nazov_stlpca = f"O{i}_{rok}"  # napr. "O1_2009"
    # pre kazde pravidlo skontrolujeme, ci je v mnozine pravidiel daneho roku;
    # ak ano dame 1, inak 0
    matica[nazov_stlpca] = matica["pravidlo"].apply(
        lambda p: 1 if p in pravidla_po_obdobiach[rok] else 0
    )

# === KROK 4: Doplnkovy stlpec - pocet rokov, v ktorych sa pravidlo vyskytlo ===
# Pre kazde pravidlo scitame jednotky v stlpcoch O1..O4 (axis=1 = po riadku).
# Vysledok: 1 = pravidlo bolo iba v jednom roku (jednorazovo),
#          4 = pravidlo bolo vo vsetkych styroch rokoch (stabilne).
matica["pocet_obdobi"] = matica[[f"O{i}_{r}" for i, r in enumerate(obdobia, 1)]].sum(axis=1)

# === KROK 5: Ulozenie matice do CSV ===
# index=False = nezapisuj pomocne cislovanie riadkov (nepotrebujeme ho)
matica.to_csv("out/matica_pravidiel.csv", index=False)

# === Zhrnutie pre kontrolu ===
print(f"\nVystupna matica: {matica.shape}")  # rozmery (pocet pravidiel, pocet stlpcov)

# kolko pravidiel sa vyskytlo v 1, 2, 3 alebo 4 rokoch
print("\nPocet pravidiel podla poctu obdobi vyskytu:")
print(matica["pocet_obdobi"].value_counts().sort_index())

# ukazka prvych 10 pravidiel; to_string() vypise plne texty bez skracovania
print("\nUkazka prvych 10 pravidiel:")
print(matica.head(10).to_string())
