# ==========================================================
# PROJEKT - Uloha 07: Rozdelenie klikov pouzivatela na sedenia
# ==========================================================
#
# CIEL:
#   Z dlheho zoznamu klikov jedneho pouzivatela urobime mensie skupiny
#   = "sedenia" (jedna navsteva webu, kym neodisiel a nevratil sa).
#   Hranicou medzi sedeniami je dlha pauza medzi dvoma klikmi.
#
# PODLA ZADANIA:
#   Zadanie projektu (zadanie.txt riadok 17-18) doslovne hovori:
#     "identifikujte sedenia na zaklade metody: Reference Length (pouzite
#      hodnotu pre podiel navigacnych stranok: 40%; v pripade nesplnenia
#      podmienky, pouzite STT_Q), h-ref."
#   Cize obe metody (RLength s p=0.4 + STT_Q ako fallback) su explicitne
#   v zadani - nemame v tom volnost.
#
# TEORIA (jednoducho, krok za krokom):
#
#   1) CO JE SEDENIE A PRECO PRAH
#   Predstav si, ze pouzivatel klika na stranky. Ked klika rychlo po sebe
#   (5s, 20s), je to to iste sedenie. Ked sa odmlci na hodinu a vrati sa,
#   je to nove sedenie. Potrebujeme prah (hranicu v sekundach) ktory
#   rozhodne "toto uz je nove sedenie".
#
#   2) PRECO PREDPOKLADAME EXPONENCIALNE ROZDELENIE PAUZ
#   Kliky cloveka na web su "nahodne nezavisle udalosti" - pouzivatel
#   neplanuje vopred kedy klikne, kazdy klik je viac-menej spontanny.
#   Takemuto procesu sa matematicky hovori Poissonov proces.
#   Vlastnost Poissonovho procesu: cas MEDZI udalostami je EXPONENCIALNE
#   rozdeleny - co znamena, ze:
#     - kratke pauzy su velmi caste (najcastejsie su skoro nulove pauzy),
#     - dlhe pauzy su zriedkave (cim dlhsia pauza, tym menej takychto),
#     - krivka hustoty monotonne klesa od nuly.
#   Analogia z bezneho zivota: cakanie na zastavke MHD, prichod
#   zakaznikov do obchodu - cas medzi udalostami ma podobny tvar.
#
#   3) ODKIAL POCHADZA VZOREC prah = -ln(1 - p) * priemer
#   Je to "inverzia" matematickej krivky exponencialneho rozdelenia.
#   Pre danu pravdepodobnost p najde hodnotu t, pod ktorou je p % vsetkych dat.
#     - p = 0.4 -> prah t hovori: "40 % pauz je kratsich nez t".
#     - tych 40 % povazujeme za NAVIGACNE STRANKY (clovek len rychlo
#       preklikava, hlada co ho zaujima - kratky cas na stranke).
#     - zvysnych 60 % su CONTENT STRANKY (clovek sa zastavil a citat
#       / pozeral - dlhsi cas na stranke).
#   Predpoklad metody: KONIEC SEDENIA = neobvykle dlha pauza, dlhsia nez
#   bezne content stranky. Ked pauza prekroci prah t, povazujeme to za
#   pravdepodobny koniec sedenia.
#
#   4) PRECO KS (KOLMOGOROV-SMIRNOV) TEST
#   Pred pouzitim RLength musime overit, ci nase data NAOZAJ vyzeraju
#   exponencialne. KS test je standardny test, ktory odpoveda na otazku:
#     "Vyzeraju tieto data ako dana teoreticka krivka?"
#   Princip: porovna ako sa hodnoty NAHROMADILI v nasich datach (empiricka
#   krivka) s tym, ako by sa nahromadili v idealnej exponenciale
#   (teoreticka krivka), a vezme NAJVACSI ROZDIEL medzi nimi.
#     - mala vzdialenost -> data sa podobaju krivke -> p-hodnota velka.
#     - velka vzdialenost -> data sa nepodobaju -> p-hodnota mala.
#   p-hodnota = pravdepodobnost ze by sme videli taku alebo este vacsiu
#               odchylku, KEBY data SKUTOCNE boli exponencialne.
#   Konvencia (v statistike):
#     - p >= 0.05 -> nemame dovod tvrdit ze to NIE je exp. -> pouzijeme RLength
#     - p <  0.05 -> data zjavne nie su exp.              -> fallback STT_Q
#
#   5) PRECO JE STT_Q DOBRY FALLBACK
#   STT_Q (Session Time Threshold - Quartile) pouzije statisticke pravidlo:
#     prah = Q3 + 1.5 * (Q3 - Q1)
#   kde Q1 = pod tymto je 25 % pauz, Q3 = pod tymto je 75 % pauz.
#   Toto je Tukey-ho pravidlo pre "neobvykle velke hodnoty" v boxplote
#   (vychadza zo statistiky, pouzitelne pre AKEKOLVEK rozdelenie).
#   Preco je dobre ako fallback:
#     - NEZAVISI od tvaru rozdelenia (RLength predpoklada exponencialu;
#       ked predpoklad neplati, RLength dava nezmysel).
#     - JE ROBUSTNY voci extremnym hodnotam (Q3 a IQR sa nedaj otrasit
#       par velmi velkymi cislami, na rozdiel od priemeru ktory by
#       vychylili napr. roboti co prezili cistenie).
#     - INTERPRETACIA: "ak je pauza extremne dlha, je to outlier = koniec sedenia".
#
#   ZHRNUTIE TOKU:
#     priemer pauz -> KS test -> ak p>=0.05: RLength, inak: STT_Q
#     -> NEW_SESSION = (pauza je NaN ALEBO pauza >= prah)
#     -> SESSION_ID = kumulativny sucet (kazda nova session += 1)
#
# VSTUP:  in/06_length.csv  - kliky s pauzou (Length) v sekundach medzi
#                              po sebe iducimi klikmi toho isteho pouzivatela
# VYSTUP: out/07_sedenia_rlength.csv - to iste + stlpec SESSION_ID
#         out/07_test_zaver.txt      - textovy zaznam pre obhajobu
#
# POUZITE KNIZNICE:
#   pandas - praca s tabulkami (citanie/zapis CSV, filtre)
#   numpy  - matematika (logaritmus)
#   scipy.stats.kstest - statisticky test podobnosti s krivkou
#
# ALGORITMUS:
#   Vypocitame priemer pauz, otestujeme rozdelenie, vyberieme prah,
#   oznacime kazdy klik s velkou pauzou ako "novy zaciatok" a postupne
#   ocislujeme sedenia.

import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))  # umoznuje spustenie skriptu odkialkolvek (nielen z jeho priecinka)

import pandas as pd
import numpy as np                # np.log je prirodzeny logaritmus (ln), pouzity vo vzorci RLength
from scipy.stats import kstest    # test ci data vyzeraju ako dana teoreticka krivka

# === KROK 1: Nacitanie dat ===

df = pd.read_csv("in/06_length.csv", low_memory=False)   # nacitame tabulku; low_memory=False = pandas si data prejde a urci typy stlpcov spravne
print(f"Nacitane: {len(df):,} riadkov")

# Pri prvom kliku pouzivatela nie je ziadna predchadzajuca pauza (Length je prazdne).
# Tieto prazdne hodnoty musime vyhodit, lebo statistika sa pocita len z cisel.
length_data = df["Length"].dropna()                      # vyhodime prazdne pauzy (prve kliky pouzivatelov)
mean_length = length_data.mean()                         # priemerna pauza medzi klikmi v sekundach
print(f"Priemer Length: {mean_length:.2f}s")

# === KROK 2: Statisticky test - vyzeraju data "ocakavane"? ===
#
# Test porovna nase data s krivkou exponencialneho rozdelenia. To je krivka,
# kde male hodnoty (kratke pauzy) su caste a velke hodnoty (dlhe pauzy) su
# zriedkave. Test vrati cislo p-hodnota:
#   p >= 0.05 -> data sa podobaju krivke, mozeme pouzit RLength
#   p <  0.05 -> data sa nepodobaju krivke, pouzijeme zalozny STT_Q

ks_stat, p_value = kstest(length_data, "expon", args=(0, mean_length))   # porovname pauzy s teoretickou krivkou; scale = priemer pauz
print(f"\nKS test:")
print(f"  KS statistika: {ks_stat:.4f}")   # cim mensie cislo, tym lepsie sa data podobaju krivke
print(f"  P-hodnota: {p_value:.6f}")       # cim vacsie, tym menej dovodov povedat ze data NIE su exponencialne

# === KROK 3: Vyber metody a vypocet prahu ===

if p_value >= 0.05:
    # Data sa podobaju ocakavanej krivke -> pouzijeme RLength.
    # Vzorec hovori: ked 40% klikov povazujeme za rychle preklikavanie,
    # tak hranica pre "este to iste sedenie" je -ln(0.6) * priemerna pauza,
    # co vyjde priblizne 0.51 nasobok priemernej pauzy.
    metoda = "RLength"
    p = 0.4                                  # 40% klikov je len rychle preklikavanie (zo zadania)
    prah = -np.log(1 - p) * mean_length      # vzorec RLength: hranica medzi rychlym preklikom a citanim obsahu
    zaver = (
        f"KS test: p={p_value:.6f} >= 0.05\n"
        f"-> data MAJU exponencialne rozdelenie\n"
        f"-> pouzita metoda: RLength = -ln(1-{p}) * {mean_length:.2f} = {prah:.2f}s"
    )
else:
    # Data sa nepodobaju ocakavanej krivke -> pouzijeme zalozny STT_Q.
    # Vyuziva kvartily, ktore sa nedaju pokazit niekolkymi extremnymi hodnotami:
    # Q1 = pod nim je 25% pauz, Q3 = pod nim je 75% pauz.
    # Hranica Q3 + 1.5*(Q3-Q1) je standardna hranica pre "neobvykle velke" hodnoty.
    metoda = "STT_Q"
    q1 = length_data.quantile(0.25)          # pod touto pauzou je 25% vsetkych pauz
    q3 = length_data.quantile(0.75)          # pod touto pauzou je 75% vsetkych pauz
    iqr = q3 - q1                            # sirka stredu dat (medzi Q1 a Q3)
    prah = q3 + 1.5 * iqr                    # standardna hranica pre neobvykle velke pauzy
    zaver = (
        f"KS test: p={p_value:.6f} < 0.05\n"
        f"-> data NEMAJU exponencialne rozdelenie\n"
        f"-> fallback na STT_Q = Q3 + 1.5*IQR = {q3:.2f} + 1.5*{iqr:.2f} = {prah:.2f}s"
    )

print(f"\n=== POUZITA METODA: {metoda} ===")
print(zaver)

# === KROK 4: Oznacenie zaciatkov novych sedeni ===
#
# Pre kazdy klik povieme True/False ci je to zaciatok noveho sedenia.
# Zaciatok noveho sedenia je vtedy, ked:
#   (a) je to uplne prvy klik pouzivatela (Length je prazdne), alebo
#   (b) pauza pred nim bola dlhsia ako prah (pouzivatel sa medzitym vratil).

df["NEW_SESSION"] = (df["Length"].isna()) | (df["Length"] >= prah)   # True = zaciatok noveho sedenia

# === KROK 5: Cislovanie sedeni ===
#
# Postupne prejdeme tabulku zhora nadol a pocitame, kolkokrat sme uz videli
# zaciatok noveho sedenia. To cislo je SESSION_ID daneho riadku.
# Priklad:
#   NEW_SESSION: True, False, False, True, False, True
#   SESSION_ID:  1,    1,     1,     2,    2,     3

df["SESSION_ID"] = df["NEW_SESSION"].cumsum()    # spocitame True hodnoty zhora nadol = cislo sedenia
df = df.drop(columns=["NEW_SESSION"])            # pomocny stlpec uz nepotrebujeme

# === KROK 6: Ulozenie vystupu ===

df.to_csv("out/07_sedenia_rlength.csv", index=False)   # ulozime tabulku bez cisla riadkov
print(f"\nPocet sedeni: {df['SESSION_ID'].nunique():,}")
print(f"Ulozene -> out/07_sedenia_rlength.csv")

# Textovy zaznam o tom, ktora metoda bola pouzita a preco - pre obhajobu projektu.
with open("out/07_test_zaver.txt", "w", encoding="utf-8") as f:
    f.write("=== Zaver KS testu a vyber metody ===\n\n")
    f.write(f"Pocet hodnot Length: {len(length_data):,}\n")
    f.write(f"Priemer Length: {mean_length:.2f}s\n\n")
    f.write(f"KS statistika: {ks_stat:.4f}\n")
    f.write(f"P-hodnota: {p_value:.6f}\n\n")
    f.write(zaver + "\n\n")
    f.write(f"Pouzity prah: {prah:.2f}s\n")
    f.write(f"Pocet sedeni: {df['SESSION_ID'].nunique():,}\n")
print(f"Zaver ulozeny -> out/07_test_zaver.txt")
