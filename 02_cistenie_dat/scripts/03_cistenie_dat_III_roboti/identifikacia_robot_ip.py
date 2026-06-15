# ==========================================================
# CV1 - Uloha 07: Najdenie IP adries robotov
# ==========================================================
#
# CIEL:
#   V logu webserveru chceme oddelit pristupy ludi od pristupov
#   automatickych programov (robotov, crawlerov - napr. Googlebot,
#   ktore prechadzaju web a indexuju stranky). Roboti by skreslili
#   analyzu spravania ludi, preto si tu vypiseme ich IP adresy
#   a v dalsej ulohe ich vyhodime z dat.
#
# JEDNODUCHA TEORIA:
#   robots.txt je maly subor na webe, ktory citaju IBA roboti -
#   je to pre nich navod, ktore stranky smu indexovat. Bezny clovek
#   v prehliadaci tento subor nikdy neotvori (neexistuje k nemu
#   ziadny link a sam si ho nepyta). Preto plati jednoduche pravidlo:
#   ak nejaka IP adresa stiahla robots.txt, je to skoro urcite robot.
#
#   Pozn.: Munk uvadza 4 sposoby identifikacie robotov: podla User-Agent retazca,
#   podla zoznamu znamych IP, podla pristupu k robots.txt (TUTO METODU pouzivame),
#   a podla pristupu k skrytemu odkazu. Robots.txt sme zvolili lebo je najspolahlivejsi
#   (bezny clovek tento subor nikdy nepyta).
#
# PRECO CITAME UZ OCISTENY LOG (a nie surovy):
#   Uloha 01 surovy log uz rozlozila na tabulku (stlpce IP, URL, ...) a robots.txt
#   pristupy v nej zostali (cistenie ich neodstranuje). Staci nam teda vyfiltrovat
#   riadky s robots.txt z tejto hotovej tabulky - nemusime surovy log parsovat
#   regexom druhykrat (to uz spravila uloha 01). Vysledok je rovnaky: 333 IP.
#
# VSTUP:
#   in/01_cleaned_log.csv - ocisteny log z ulohy 01 (tabulka so stlpcami
#                           IP, DateTime, RequestMethod, URL, StatusCode, ...).
#
# VYSTUP:
#   out/03_robot_ips.csv - jeden stlpec 'IP' s 333 riadkami
#                          (kazdy pristup k robots.txt = jeden riadok,
#                          aj ked ta ista IP pristupila viackrat).
#
# POUZITE KNIZNICE:
#   pandas - praca s tabulkou (nacitanie CSV, filter, ulozenie).
#
# ALGORITMUS:
#   Nacitaj ocisteny log -> vyber riadky, kde je v URL "robots.txt" ->
#   uloz ich IP adresy do CSV.
# ==========================================================

import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))  # umoznuje spustenie skriptu odkialkolvek (nielen z jeho priecinka)

import pandas as pd                # praca s tabulkou (CSV)

# === KROK 1: Nacitanie ocisteneho logu z ulohy 01 ===
df = pd.read_csv("in/01_cleaned_log.csv")  # tabulka uz ma stlpce IP, URL, ... (rozlozil ich skript 01)
print(f"Nacitane: {len(df)} zaznamov")

# === KROK 2: Vyber pristupov k robots.txt ===
# str.contains hlada podretazec v stlpci URL.
#   regex=False = "robots.txt" berieme doslovne (bodka je bodka, nie lubovolny znak),
#   case=False  = nezalezi na velkosti pismen,
#   na=False    = prazdne URL nepovazujeme za zhodu.
robots = df[df["URL"].str.contains("robots.txt", case=False, na=False, regex=False)]
print(f"Zaznamy s robots.txt: {len(robots)}")  # kontrola - ocakavame 333

# === KROK 3: Ulozenie IP adries do CSV ===
# Ponechavame aj duplicity - ak ta ista IP pytala robots.txt viackrat,
# bude v subore tolkokrat. Zadanie chce 333 zaznamov (nie 333 roznych IP).
robot_ips = robots["IP"].values                          # .values = vytiahne hodnoty stlpca IP ako jednoduche pole (aj s opakovaniami)
print(f"IP adries robotov: {len(robot_ips)}")            # 333 (vratane opakovani)
print(f"Unikatnych: {len(set(robot_ips))}")              # set(...) = mnozina (vyhodi opakovania); len(...) = kolko je z nich roznych (info na kontrolu)

robot_df = pd.DataFrame({"IP": robot_ips})               # tabulka s jednym stlpcom 'IP'
robot_df.to_csv("out/03_robot_ips.csv", index=False)     # ulozime do CSV; index=False = bez stlpca s poradovymi cislami
