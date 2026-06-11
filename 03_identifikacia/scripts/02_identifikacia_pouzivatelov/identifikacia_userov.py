# ==========================================================
# CV2 - Uloha 02: Identifikacia pouzivatelov
# ==========================================================
#
# CIEL: Kazdemu riadku v logu priradit cislo pouzivatela (USER_ID),
# aby sme neskor vedeli, ktore kliky patria tomu istemu cloveku.
#
# TEORIA (jednoducho):
#   Apache log subor neobsahuje meno ani prihlasenie - server iba zaznamenava
#   IP adresu (odkial pristup prisiel) a User-Agent (retazec, ktory hovori,
#   aky prehliadac a system pouzivatel ma, napr. "Chrome na Windows").
#   Nemame teda priamy sposob, ako rozlisit pouzivatelov.
#
#   Pouzivame jednoduchu uvahu: jeden clovek = jedna dvojica (IP, Agent).
#     - Rovnaka IP, iny prehliadac = beriem ako dvoch ludi (napr. dvaja
#       v jednej domacnosti pouzivaju jeden internet, ale kazdy ma iny PC).
#     - Ina IP, rovnaky prehliadac = tiez ini ludia (mobil vs notebook).
#   Nie je to dokonale (mobil meni IP, viacero ludi za firemnou sietou),
#   ale je to standardny postup, ked nemame cookies ani login.
#
# VSTUP:  in/cleaned_log4_unixtime.csv  (vystup z ulohy 01 - log s UNIXTIME)
# VYSTUP: out/cleaned_log4_users.csv    (rovnake stlpce + novy USER_ID)
#
# POUZITE KNIZNICE:
#   pandas - praca s tabulkovymi datami (citanie CSV, triedenie, grupovanie).
#
# ALGORITMUS (1 veta):
#   Zoradime data podla IP, Agent a casu, kazdej unikatnej dvojici (IP, Agent)
#   pridelime cislo od 1, a vysledok ulozime do noveho CSV.
# ==========================================================

import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))  # umoznuje spustenie skriptu odkialkolvek (nielen z jeho priecinka)

import pandas as pd  # pandas zvlada citanie CSV aj triedenie a grupovanie


# === KROK 1: Nacitanie logu ===
# Citame log z predoslej ulohy, kde sme uz pridali UNIXTIME (cas v sekundach).
df = pd.read_csv("in/cleaned_log4_unixtime.csv")


# === KROK 2: Zoradenie podla IP, Agent a casu ===
# Najprv triedime podla IP, pri rovnakej IP podla Agenta, pri zhode podla casu.
# Vdaka tomu budu vsetky kliky toho isteho cloveka pekne za sebou.
# A zaroven budu zoradene chronologicky (od najstarsieho po najnovsi klik).
df = df.sort_values(by=["IP", "Agent", "UNIXTIME"])

# Po triedeni maju riadky pomiesane povodne cisla (napr. 1523, 7, 9001...).
# Precislujeme ich na 0, 1, 2, ... aby sa s tabulkou dalo dalej pohodlne pracovat.
df = df.reset_index(drop=True)


# === KROK 3: Pridelenie cisla pouzivatela ===
# Zoskupime riadky podla dvojice (IP, Agent) - kazda jedinecna dvojica je
# jeden pouzivatel. Funkcia ngroup() kazdej skupine prideli cislo 0, 1, 2, ...
# Pripocitame +1, aby pouzivatelia zacinali cislom 1 (ludom sa to lepsie cita).
df["USER_ID"] = df.groupby(["IP", "Agent"]).ngroup() + 1


# === KROK 4: Ulozenie vysledku ===
# Ukladame cely log aj s novym stlpcom USER_ID; index=False = nepridavaj
# pomocny stlpec s cislami riadkov (inak by sa pri dalsom citani objavil navyse).
df.to_csv("out/cleaned_log4_users.csv", index=False)


# === Kontrolny vypis ===
# Vypiseme prvych 10 riadkov - vizualne overime, ze USER_ID je rozumne pridelene.
print(df[["IP", "Agent", "UNIXTIME", "USER_ID"]].head(10))
# Vypiseme celkovy pocet riadkov a pocet roznych pouzivatelov.
# Zadanie ocakava okolo 4040 pouzivatelov - male odchylky su normalne.
print(f"\nPocet zaznamov: {len(df)}")
print(f"Pocet identifikovanych pouzivatelov: {df['USER_ID'].nunique()}")
