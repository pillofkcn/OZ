# ==========================================================
# PROJEKT - Uloha 03: Filter robotov (User-Agent + IP)
# ==========================================================
#
# CIEL:
#   Z ocisteneho logu vyhodit pristupy, ktore neurobil clovek (robot
#   = automaticky program co prehladava web, napr. Googlebot). Bez
#   tohto kroku by neskorsie sedenia (= za sebou idiace kliky jedneho
#   pouzivatela) boli pokazene robotmi, ktori klikaju uplne inak ako
#   clovek (rychlejsie, na vsetko, bez prestavok).
#
# TEORIA - dva sposoby ako rozoznat robota:
#   1) Podla mena prehliadaca (pole "Agent" v logu): robot sa casto
#      sam prizna - v texte ma slovo "bot", "crawl" alebo "spider"
#      (napr. "Googlebot/2.1", "bingbot", "AhrefsBot").
#   2) Podla toho, ze IP adresa siahla na subor /robots.txt. Tento
#      subor je instrukcia pre robotov co maju indexovat. Bezny clovek
#      ho v prehliadaci nikdy neotvori - nevie ze existuje. Cize kazda
#      IP co si ho vyziadala je takmer urcite robot. Tento zoznam IP
#      adries sme pripravili v predchadzajucej ulohe.
#   Pouzivame OBE metody naraz - co prejde jednou, chyti druha.
#
# VSTUP:
#   - in/01_cleaned_log.csv  - ocisteny log z ulohy 01 (stlpce IP,
#                              Datetime, Agent, ...)
#   - in/02_robot_ips.csv    - zoznam IP adries, ktore aspon raz volali
#                              /robots.txt (z ulohy 02)
#
# VYSTUP:
#   - out/03_cleaned_log.csv - rovnaky log, ale uz len pristupy ludi
#
# POUZITE KNIZNICE:
#   - pandas: praca s tabulkou (nacitanie CSV, filtrovanie riadkov)
#
# ALGORITMUS:
#   Postupne aplikujeme 4 filtre: vyhlad. roboti (bot/crawl/spider),
#   automaticke nastroje (cron/curl/wget/...), pristupy bez mena
#   prehliadaca, a IP adresy zo zoznamu robotov.
# ==========================================================

import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))  # umoznuje spustenie skriptu odkialkolvek (nielen z jeho priecinka)

import pandas as pd  # pandas = kniznica na pracu s tabulkami

# === KROK 1: Nacitanie vstupov ===

df = pd.read_csv("in/01_cleaned_log.csv")  # nacitame ocisteny log z ulohy 01
print(f"Nacitane: {len(df):,} riadkov")    # vypiseme pocet riadkov ({:,} prida ciarky pre citatelnost)

# Z druheho suboru zoberieme stlpec IP a necham len unikatne hodnoty
# (kazdu IP raz). Ulahcia neskorsie hladanie - netreba prehladavat duplikaty.
robot_ips = pd.read_csv("in/02_robot_ips.csv")["IP"].unique()
print(f"Robot IP adries: {len(robot_ips):,}")  # kolko unikatnych roboti IP mame

# === KROK 2: Filter botov podla mena prehliadaca ===
#
# Roboti vyhladavacich sluzieb (Google, Bing, ...) sa zvycajne sami
# prizraju v mene prehliadaca. V texte maju slovo "bot", "crawl" alebo
# "spider" (Googlebot, bingbot, AhrefsBot, Baiduspider, ...).
# Pozrieme sa, ci v stlpci Agent niektore z tychto slov je.

# str.contains: pre kazdy riadok zistime, ci text obsahuje dane slovo.
# case=False = velke/male pismena nehraju rolu. na=False = ak je hodnota
# prazdna, povazuj to za "nenaslo sa" (inak by to hodilo chybu nizsie).
bot = df["Agent"].str.contains(r"bot|crawl|spider", case=False, na=False)
df = df[~bot]  # ~ znamena "negacia" - necham riadky kde bot NIE JE
print(f"Po odstraneni botov (Agent bot|crawl|spider): {len(df):,}")

# === KROK 3: Filter automatickych nastrojov ===
#
# Toto nie su klasicke vyhladavacie roboty, ale programy a skripty:
#   - cron    = automaticka uloha spustana podla casu (linux)
#   - curl    = nastroj programatorov na stahovanie stranok z prikazoveho riadku
#   - wget    = podobne ako curl, sluzi na hromadne stahovanie
#   - libwww  = stary nastroj na pisanie automatickych skriptov
#   - ltx71   = bezpecnostny skener (lieta po webe a hlada zranitelnosti)
# Aj tieto nepatria k realnym pouzivatelom, takze ich vyhodime.

auto = df["Agent"].str.contains(r"cron|curl|wget|libwww|ltx71", case=False, na=False)
df = df[~auto]  # necham len riadky, ktore nie su od tychto nastrojov
print(f"Po odstraneni automatizovanych skriptov: {len(df):,}")

# === KROK 4: Odstranenie pristupov bez mena prehliadaca ===
#
# Ked klient neposle ziadne meno prehliadaca, Apache server zapise do
# logu pomlcku "-". Normalny prehliadac (Chrome, Firefox) vzdy posle
# nieco. Takze "-" znaci bud jednoduchy skript alebo niekoho kto sa
# vedome skryva - v oboch pripadoch to nie je clovek surfujuci po webe.
df = df[df["Agent"] != "-"]  # necham len riadky kde Agent nie je "-"
print(f"Po odstraneni prazdnych agentov: {len(df):,}")

# === KROK 5: Filter podla zoznamu robotich IP adries ===
#
# Druhy sposob ako chytit robota: v ulohe 02 sme spravili zoznam IP
# adries, ktore aspon raz pozadali /robots.txt. Tento subor pyta len
# robot - normalny clovek nevie ze existuje. Cize tieto IP su robotmi
# aj ked v mene prehliadaca nemaju slovo "bot" (niektory bot sa moze
# skryvat za bezne meno prehliadaca).
#
# isin: pre kazdy riadok zistime, ci jeho IP je v zozname robotov.
# ~ negujem - necham len IP, ktore v zozname NIE SU.
df = df[~df["IP"].isin(robot_ips)]
print(f"Po odstraneni robot IP: {len(df):,}")

# === KROK 6: Reset indexu a zapis vystupu ===
#
# Po opakovanom filtrovani su povodne cisla riadkov "dierave" (napr.
# 0, 3, 7, 12, ...) lebo pandas si pamata kde riadok povodne stal.
# reset_index ich preocisluje od nuly po N-1, aby sa s tabulkou
# dalej dobre pracovalo. drop=True znaci "stare cisla zahod, nerob
# z nich novy stlpec".
df = df.reset_index(drop=True)
df.to_csv("out/03_cleaned_log.csv", index=False)  # zapis do CSV; index=False = neprida sa stlpec s cislami riadkov
print(f"\nFinal: {len(df):,} riadkov -> out/03_cleaned_log.csv")
