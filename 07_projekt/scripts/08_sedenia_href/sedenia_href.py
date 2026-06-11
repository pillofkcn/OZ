# ==========================================================
# PROJEKT - Uloha 08: Rozdelenie klikov na sedenia metodou h-ref
# ==========================================================
#
# CIEL:
#   Postupne kliky kazdeho navstevnika rozdelit do "sedeni" (session = jedna
#   navsteva webu od prichodu az po odchod). Pouzivame metodu h-ref, co je
#   alternativa k metode "Reference Length" z ulohy 07.
#
# TEORIA (jednoducho):
#   Predstavme si, ze pozerame zoznam klikov jedneho cloveka zoradenych v case.
#   Potrebujeme rozhodnut, kde sa jedna navsteva konci a kde zacina nova.
#   Metoda h-ref povie "tu zacina nove sedenie", ak je splnena aspon JEDNA
#   z troch vecí:
#     1) je to posledny klik daneho cloveka (dalsi klik patri inemu cloveku)
#     2) medzi tymto a dalsim klikom je dlha pauza (clovek asi odisiel)
#     3) clovek prisiel "zvonku" - v zazname je "-" v stlpci Referrer
#        (Referrer = stranka, z ktorej clovek priklikol; "-" znamena, ze
#        prisiel priamo z adresneho riadku, zalozky alebo externeho odkazu)
#
# VSTUP:
#   in/06_length.csv  - log po uloze 06, ma uz vypocitany stlpec Length
#                       (Length = pocet sekund medzi tymto a NASLEDUJUCIM
#                       klikom toho isteho cloveka; pre posledny klik je
#                       prazdne, lebo dalsi uz neexistuje)
#
# VYSTUP:
#   out/08_sedenia_href.csv - tie iste data + novy stlpec SESSION_ID
#                             (cislo sedenia, do ktoreho klik patri)
#
# POUZITE KNIZNICE:
#   pandas - praca s tabulkou (csv, filtre, vypocty po stlpcoch)
#
# ALGORITMUS (1 veta):
#   Pre kazdy klik rozhodneme "zacina tu nove sedenie?" (ano/nie), a potom
#   cislo sedenia ziskame tak, ze pocitame, kolko "ano" sme uz videli.
# ==========================================================

import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))  # umoznuje spustenie skriptu odkialkolvek (nielen z jeho priecinka)

import pandas as pd  # kniznica na pracu s tabulkami (csv, stlpce, filtre)

# === KROK 1: Nacitanie dat z predchadzajucej ulohy ===
# Potrebujeme stlpec Length, ktory uz vypocitala uloha 06.
df = pd.read_csv("in/06_length.csv", low_memory=False)  # nacitame log; low_memory=False = pandas spravne urci typy stlpcov
print(f"Nacitane: {len(df):,} riadkov")  # vypis s ciarkou ako oddelovacom tisicov

# === KROK 2: Vypocet hranice "dlhej pauzy" ===
# Za dlhu pauzu povazujeme cas, ktory je dlhsi nez priemerna pauza medzi
# klikmi v celom logu. Priemer ratame zo stlpca Length.
mean_length = df["Length"].mean()  # priemerny cas medzi klikmi v sekundach (.mean() preskoci prazdne hodnoty)
print(f"Casove okno (priemer Length): {mean_length:.2f}s")  # zaokruhlene na 2 desatinne miesta

# === KROK 3: Oznacime kliky, kde zacina nove sedenie ===
# Pre kazdy klik vyhodnotime tri podmienky. Ak plati aspon jedna, tu sa
# zacina nove sedenie. Znak | znamena "alebo" (postupne pre kazdy riadok).
# Zatvorky okolo podmienok su povinne, inak pandas pocita v zlom poradi.
df["NEW_SESSION"] = (
    (df["Length"].isna())              # a) prazdne Length = posledny klik cloveka, dalsi uz patri inemu
    | (df["Length"] >= mean_length)    # b) pauza do dalsieho kliku je dlhsia nez priemer = clovek asi odisiel
    | (df["Referrer"] == "-")          # c) klik prisiel zvonku (priamo, zo zalozky, z externeho odkazu)
)

# === KROK 4: Pridelenie cisla sedenia ===
# Trik: True sa pri scitavani sprava ako 1, False ako 0. Ked postupne
# scitavame zhora dole, cislo nam stupne vzdy, ked narazime na zaciatok
# noveho sedenia. Vsetky kliky medzi dvoma "zaciatkami" maju rovnake cislo.
#
# Priklad:
#   NEW_SESSION: [True, False, False, True, False, True]
#   po scitavani:[   1,     1,     1,    2,     2,    3]   <- SESSION_ID
df["SESSION_ID"] = df["NEW_SESSION"].cumsum()  # cumsum = postupny sucet zhora dole

# Pomocny stlpec uz nepotrebujeme, vystup ma mat len finalne cislo sedenia.
df = df.drop(columns=["NEW_SESSION"])

# === KROK 5: Ulozenie vystupu ===
# index=False = neukladaj cisla riadkov 0,1,2... ako extra stlpec.
df.to_csv("out/08_sedenia_href.csv", index=False)
print(f"\nPocet sedeni: {df['SESSION_ID'].nunique():,}")  # nunique = pocet roznych hodnot SESSION_ID
print(f"Ulozene -> out/08_sedenia_href.csv")
