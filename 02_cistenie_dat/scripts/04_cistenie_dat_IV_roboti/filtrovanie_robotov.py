# ==========================================================
# CV1 - Uloha 08: Odstranenie robotov z logu
# ==========================================================
#
# CIEL: Posledny krok cistenia dat. Chceme analyzovat spravanie
#   skutocnych ludi na webe. Roboti (napr. Googlebot) a automaticke
#   skripty (napr. curl) tiez generuju zaznamy v logu, ale ich
#   spravanie nie je ludske — chodia systematicky cez vsetky stranky.
#   Preto ich treba vyhodit, inak by skreslili dalsie analyzy.
#
# AKO ICH SPOZNAME:
#   1) Podla mena prehliadaca (stlpec "Agent"): roboti sa zvycajne
#      sami priznaju a maju v mene slovo "bot", "crawl" alebo "spider".
#   2) Podla IP adresy: v predoslej ulohe sme nasli IP, ktore sa
#      chovali podozrivo (prilis vela klikov, nelidske vzorce).
#   3) Niektori klienti vobec nepovedia, kto su (Agent = "-"). Realny
#      prehliadac to vzdy posle, takze prazdne pole je tiez podozrive.
#
# VSTUP:
#   in/01_cleaned_log.csv  - log po predoslych krokoch cistenia
#   in/03_robot_ips.csv    - zoznam IP adries oznacenych ako roboti
#
# VYSTUP:
#   out/04_cleaned_log.csv - finalny ocisteny log (~20000 riadkov)
#
# POUZITE KNIZNICE:
#   pandas - praca s tabulkovymi datami (DataFrame)
#
# ALGORITMUS: Postupne vyhodime 4 skupiny riadkov (UA-roboti,
#   skripty, prazdny Agent, robot IP) a ulozime vysledok.
# ==========================================================

import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))  # umoznuje spustenie skriptu odkialkolvek (nielen z jeho priecinka)

import pandas as pd  # kniznica na pracu s tabulkami

# === KROK 1: Nacitanie logu ===
df = pd.read_csv("in/01_cleaned_log.csv")  # nacitame tabulku zo suboru
print(f"Nacitane: {len(df)} riadkov")      # kolko riadkov mame na zaciatku

# === KROK 2: Vyhodenie robotov podla mena prehliadaca ===
# Roboti sa casto sami priznaju — v mene maju "bot", "crawl" alebo "spider"
# (napr. "Googlebot", "Baiduspider"). Hladame, ci sa niektore z tych slov
# vyskytuje v stlpci Agent.
#   case=False  = nezalezi na velkych/malych pismenach (Bot = bot = BOT)
#   na=False    = ak je policko prazdne, beriem to ako "nie je robot"
#                 (inak by prazdne hodnoty robili problem)
bot = df["Agent"].str.contains(r"bot|crawl|spider", case=False, na=False)
df = df[~bot]  # vlnovka znamena "opak" - nechame riadky, kde to NIE JE robot
print(f"Po odstraneni botov (Agent): {len(df)}")

# === KROK 3: Vyhodenie automatickych skriptov ===
# Toto nie su prehliadace, ale nastroje, ktore taha data automaticky:
#   cron   - planovane skripty na servery
#   curl   - nastroj na stahovanie z prikazoveho riadku
#   wget   - to iste, iny nastroj
#   libwww - kniznica pre Perl skripty
#   ltx71  - znamy automaticky skener webu
# Ziadny z nich nie je clovek pred obrazovkou.
auto = df["Agent"].str.contains(r"cron|curl|wget|libwww|ltx71", case=False, na=False)
df = df[~auto]  # nechame iba riadky, kde Agent nie je automaticky skript
print(f"Po odstraneni automatizovanych skriptov: {len(df)}")

# === KROK 4: Vyhodenie zaznamov s prazdnym Agent ===
# Pomlcka "-" je standardne oznacenie, ze klient vobec nepovedal kto je.
# Skutocny prehliadac to vzdy posle, takze prazdne policko je podozrive.
df = df[df["Agent"] != "-"]  # nechame iba riadky, kde Agent nie je "-"
print(f"Po odstraneni prazdnych agentov: {len(df)}")

# === KROK 5: Vyhodenie zaznamov z IP adries robotov ===
# V predoslej ulohe sme nasli IP adresy, ktore sa chovali ako roboti
# (prilis vela klikov, nelidske vzorce). Tu ich pouzijeme — aj keby
# robot klamal o svojom mene, IP adresu lahko nezmeni.
robot_ips = pd.read_csv("in/03_robot_ips.csv")["IP"].unique()  # nacitame zoznam podozrivych IP (bez duplikatov)
df = df[~df["IP"].isin(robot_ips)]  # nechame iba riadky, ktorych IP NIE JE v zozname robotov
print(f"Po odstraneni robot IP: {len(df)}")

# === KROK 6: Prerocislovanie a ulozenie ===
# Po vyhadzovani riadkov mame v cislovani diery (0, 3, 7, 12...).
# reset_index ich precisluje pekne od nuly (0, 1, 2, 3...).
# drop=True znamena, ze stare cislovanie zahodime, nepridame ho ako stlpec.
df = df.reset_index(drop=True)
print(f"\nFinal: {len(df)} riadkov")  # konecny pocet riadkov

# Ulozime finalny vyciteny log pre dalsie ulohy.
# index=False = neulozit cislovanie ako prvy stlpec (inak by sa pri
# nacitani objavil zvlastny stlpec "Unnamed: 0").
df.to_csv("out/04_cleaned_log.csv", index=False)
