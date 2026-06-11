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
# VSTUP:
#   in/Log_jeden_den.log - surovy log webserveru za jeden den
#                          (riadky vo formate Apache combined log).
#
# VYSTUP:
#   out/07_robot_ips.csv - jeden stlpec 'IP' s 333 riadkami
#                          (kazdy pristup k robots.txt = jeden riadok,
#                          aj ked ta ista IP pristupila viackrat).
#
# POUZITE KNIZNICE:
#   re     - hladanie vzorov v texte (regex).
#   pandas - kniznica na pracu s tabulkami, tu len na ulozenie do CSV.
#
# PRECO NEPOUZIVAME pd.read_csv:
#   Log nie je klasicke CSV - obsahuje medzery a uvodzovky vnutri
#   policok, takze ho citame riadok po riadku rucne cez open().
#
# ALGORITMUS:
#   Precitame log po riadkoch -> kazdy riadok rozlozime regexom ->
#   ak je v URL "robots.txt", ulozime IP -> zapiseme do CSV.
# ==========================================================

import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))  # umoznuje spustenie skriptu odkialkolvek (nielen z jeho priecinka)

import re                          # kniznica na hladanie vzorov v texte
import pandas as pd                # kniznica na pracu s tabulkami (kvoli ulozeniu do CSV)

# === KROK 1: Pripravime si vzor (regex) na rozlozenie riadku logu ===
#
# Jeden riadok logu vyzera takto:
#   192.168.0.1 - - [10/Oct/2023:13:55:36 +0000] "GET /robots.txt HTTP/1.1" 200 234 "-" "Googlebot/2.1"
#
# Z riadku chceme vytiahnut hlavne dve veci:
#   - IP adresu (uplne na zaciatku)
#   - URL, ktoru navstevnik chcel (tu /robots.txt)
#
# Pouzivame ten isty vzor ako v predoslej ulohe, aby sme cislovali rovnako.
pattern = re.compile(
    r'^(\S+)\s+\S+\s+\S+\s+'        # 1. zatvorka: IP adresa zo zaciatku riadku
    r'\[([^\]]+)\]\s+'              # 2. zatvorka: datum a cas v hranatych zatvorkach
    r'"(\S+)\s+(\S+)\s*\S*"\s+'     # 3. zatvorka: metoda (GET/POST), 4. zatvorka: URL
    r'(\d{3})\s+'                   # 5. zatvorka: stavovy kod (napr. 200, 404)
    r'(\S+)\s+'                     # 6. zatvorka: velkost odpovede v bajtoch
    r'"([^"]*)"\s+'                 # 7. zatvorka: odkial pouzivatel prisiel (referer)
    r'"([^"]*)"'                    # 8. zatvorka: user-agent (info o prehliadaci/robotovi)
)

# === KROK 2 + 3: Prejdeme log a najdeme tych, co pytali robots.txt ===
#
# Citame log riadok po riadku (nie cely naraz), aby sme nepretazili pamat -
# log moze byt aj velmi velky. Ak je riadok poskodeny (neda sa rozlozit),
# ticho ho preskocime.
rows = []
with open("in/Log_jeden_den.log", encoding="utf-8", errors="replace") as f:  # errors='replace' = poskodene znaky nahradi, aby skript nespadol
    for line in f:
        m = pattern.match(line)                          # skusime rozlozit riadok podla vzoru
        if m:                                            # ak sa to podarilo (riadok ma spravny format)
            url = m.group(4)                             # vytiahneme URL (4. zatvorka vo vzore)
            if "robots.txt" in url.lower():              # zaujimaju nas len pristupy k robots.txt (case-insensitive)
                rows.append({"IP": m.group(1)})          # zapamatame si IP adresu (1. zatvorka vo vzore)

# Zo zoznamu slovnikov spravime tabulku (DataFrame) so stlpcom 'IP'.
df = pd.DataFrame(rows)
print(f"Zaznamy s robots.txt: {len(df)}")               # kontrolny vypis - ocakavame 333

# === KROK 4: Ulozime IP adresy do CSV suboru ===
#
# Ponechavame aj duplicity - ak ta ista IP pytala robots.txt viackrat,
# bude v subore tolko krat. Zadanie chce 333 zaznamov (nie 333 roznych IP).
robot_ips = df["IP"].values                              # zoznam vsetkych IP adries (aj s opakovaniami)
print(f"IP adries robotov: {len(robot_ips)}")           # 333 (vratane opakovani)
print(f"Unikatnych: {len(set(robot_ips))}")             # kolko je z nich roznych (info na kontrolu)

robot_df = pd.DataFrame({"IP": robot_ips})               # spravime novu tabulku s jednym stlpcom 'IP'
robot_df.to_csv("out/07_robot_ips.csv", index=False)    # ulozime do CSV; index=False = bez stlpca s poradovymi cislami
