# ==========================================================
# PROJEKT - Uloha 05: Identifikacia pouzivatelov
# ==========================================================
#
# CIEL:
#   Web log neobsahuje meno ani prihlasenie - nevieme kto stranku navstivil.
#   Musime to teda odhadnut z toho, co mame: IP adresu (kto sa pripojil)
#   a Agent (aky prehliadac/zariadenie pouzil). Kazdej dvojici (IP, Agent)
#   pridelime cislo USER_ID, ktore znamena "jeden pouzivatel".
#
# TEORIA - ako rozoznavame pouzivatelov bez prihlasenia:
#   - rovnaka IP + rovnaky prehliadac  = povazujeme za toho isteho cloveka
#   - rovnaka IP + iny prehliadac      = iny clovek (inak by neprepol prehliadac)
#   - ina IP                           = iny clovek (z ineho miesta v sieti)
#   Toto je odhad - nie je dokonaly:
#     * cela rodina za jednym routerom (NAT) ma rovnaku IP -> zlucia sa do jedneho
#     * mobil v aute meni vysielace -> jeden clovek vyzera ako viacero pouzivatelov
#   Lepsie by to vyriesili cookies alebo prihlasenie, ale tie v logu nemame.
#
# VSTUP:  in/04_obdobie.csv   - log z prideleneho 7-dnoveho obdobia (s UNIXTIME)
# VYSTUP: out/05_users.csv    - to iste + novy stlpec USER_ID (cele cislo od 1)
#
# POUZITE KNIZNICE:
#   - pandas : praca s tabulkou (nacitanie CSV, triedenie, skupinkovanie)
#
# ALGORITMUS (zhrnutie):
#   Zoradime data podla IP + Agent + casu, kazdej dvojici (IP, Agent)
#   pridelime cislo, ulozime do noveho CSV.
# ==========================================================

import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))  # umoznuje spustenie skriptu odkialkolvek (nielen z jeho priecinka)

import pandas as pd  # kniznica na pracu s tabulkami (CSV, triedenie, skupiny)

# === KROK 1: Nacitanie vstupu ===

# nacitame log z predoslej ulohy; low_memory=False = pandas si prejde cely subor
# naraz a spravne urci typy stlpcov (inak by mohol pomylit cislo a text)
df = pd.read_csv("in/04_obdobie.csv", low_memory=False)
print(f"Nacitane: {len(df):,} riadkov")  # vypis poctu riadkov s ciarkami medzi tisickami

# === KROK 2: Zoradenie podla IP, Agent, casu ===

# Preco triedime: v dalsej ulohe budeme pocitat cas medzi kliknutiami toho isteho
# cloveka. Aby to fungovalo, kliknutia kazdeho cloveka musia byt usporiadane
# chronologicky (od najstarsieho po najnovsie). Triedime po troch kluctoch:
#   1. IP       - vsetky kliknutia z jednej IP daj k sebe
#   2. Agent    - v ramci jednej IP rozdel podla prehliadaca
#   3. UNIXTIME - v ramci jedneho cloveka zorad od najstarsieho po najnovsie
df = df.sort_values(by=["IP", "Agent", "UNIXTIME"])

# === KROK 3: Prepocitanie poradia riadkov ===

# Po triedeni maju riadky stare cisla z povodneho poradia (napr. 42, 7, 19...).
# Prepiseme ich na nove cisla 0, 1, 2... aby boli pekne za sebou.
# drop=True = stare cisla zahodime (nepridame ich ako novy stlpec)
df = df.reset_index(drop=True)

# === KROK 4: Pridelenie USER_ID kazdemu riadku ===

# Dvojica (IP, Agent) = jeden pouzivatel. Kazdej unikatnej dvojici dame cislo.
# groupby([...]) = "rozdel data do skupin podla tychto stlpcov"
# .ngroup()      = "kazdej skupine pridel cislo 0, 1, 2..."
# + 1            = posun cislovanie tak, aby zacinalo od 1 (krajsie ako od 0)
#
# Priklad:
#   IP=1.2.3.4, Chrome   -> USER_ID = 1
#   IP=1.2.3.4, Firefox  -> USER_ID = 2  (iny prehliadac = iny clovek)
#   IP=5.6.7.8, Chrome   -> USER_ID = 3  (ina IP = iny clovek)
df["USER_ID"] = df.groupby(["IP", "Agent"]).ngroup() + 1

# === KROK 5: Ulozenie vystupu ===

# index=False = neukladaj cislovanie riadkov ako stlpec (bolo by to zbytocne)
df.to_csv("out/05_users.csv", index=False)

# nunique() = spocita kolko roznych hodnot je v stlpci (kolko mame pouzivatelov)
print(f"\nPocet identifikovanych pouzivatelov: {df['USER_ID'].nunique():,}")
print(f"Ulozene -> out/05_users.csv")
