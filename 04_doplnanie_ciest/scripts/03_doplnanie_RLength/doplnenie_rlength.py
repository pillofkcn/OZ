# ==========================================================
# CV3 - Uloha 03: Doplnanie ciest - RLength
# ==========================================================
#
# CIEL:
#   Server log zaznamenava iba stranky, ktore si pouzivatel naozaj vyziadal.
#   Ked sa vrati cez tlacidlo "Spat" alebo klikne na tu istu polozku z menu,
#   prehliadac ju zoberie zo svojej pamate (cache) a server o tom nevie.
#   V dosledku toho v sedeni (= postupnost klikov jedneho pouzivatela)
#   chybaju "medzistranky". Tieto chybajuce stranky doplname z mapy webu.
#
# PRIKLAD:
#   Pouzivatel sa dostane z /fakulta na /studium, ale v strome stranok ich
#   spaja /univerzita. Tato spojovacia stranka v logu chyba, doplname ju.
#
# VSTUP:
#   - in/cleaned_log4_rlength.csv → log po rozdeleni na sedenia metodou RLength
#                                   (RLength = sposob, ako urcit hranicu sedenia
#                                   podla case medzi klikmi, pripravene v cv2)
#   - in/mapa_webu.xlsx           → strom stranok UKF: pre kazdu URL je uvedena
#                                   jej "rodicovska" (referencna) stranka
#
# VYSTUP:
#   - out/cleaned_log4_doplnene.csv → log s vlozenymi medzistrankami
#
# POUZITE KNIZNICE:
#   - pandas → praca s tabulkami (nacitanie CSV/Excel, ulozenie vystupu)
#
# ALGORITMUS:
#   Prechadzame log po dvojiciach susednych klikov. Ak su z toho isteho sedenia
#   a medzi nimi chyba spojovacia stranka, vlozime ju z mapy webu.
# ==========================================================

import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))  # umoznuje spustenie skriptu odkialkolvek (nielen z jeho priecinka)

import pandas as pd  # kniznica na pracu s tabulkami

# === KROK 1: Nacitanie logu ===
df = pd.read_csv("in/cleaned_log4_rlength.csv")  # log uz ma stlpce IP, UNIXTIME, URL, USER_ID, SESSION_ID
print(f"Nacitane: {len(df)} zaznamov")

# === KROK 2: Nacitanie a uprava mapy webu ===
# Mapa webu hovori, ktora stranka je "rodicom" inej (cez ktoru sa na nu da dostat).
mapa = pd.read_excel("in/mapa_webu.xlsx")  # mapa je v Excel formate
mapa.columns = ["idx", "URL", "Root", "ReferencePage"]  # premenujeme stlpce na jednotne nazvy
mapa = mapa.iloc[1:].reset_index(drop=True)  # zahodime prvy datovy riadok (povodne sluzil ako hlavicka)

# Log obsahuje iba cesty (napr. "/univerzita"), nie cele URL.
# Mapu treba upravit do rovnakeho tvaru, inak by sa nic nezhodlo.
mapa["path"] = mapa["URL"].str.replace("https://www.ukf.sk", "", regex=False)            # odrezeme domenu z URL
mapa["ref_path"] = mapa["ReferencePage"].str.replace("https://www.ukf.sk", "", regex=False)  # to iste pre rodicovsku stranku

# Hlavna stranka po orezani zostane prazdny retazec — nahradime ju "/".
mapa.loc[mapa["path"] == "", "path"] = "/"          # koren mapy musi byt "/"
mapa.loc[mapa["ref_path"] == "", "ref_path"] = "/"  # to iste pre rodica

# Slovnik {stranka: jej rodic} — vyhladanie rodica je vdaka tomu velmi rychle.
parent = dict(zip(mapa["path"], mapa["ref_path"]))

# Mnozina vsetkych stranok z mapy — rychle zistenie "je tato stranka v mape?".
map_paths = set(mapa["path"].unique())
print(f"Mapa webu: {len(map_paths)} stranok")

# === KROK 3 + 4: Prechod logom a doplnenie chybajucich stranok ===
#
# Pre kazdu dvojicu (aktualny klik, dalsi klik) zistime, ci medzi nimi
# nechyba spojovacia stranka. Ak ano, vlozime ju do vystupu medzi ne.
# Tento skript riesi pripad: aktualna stranka NIE JE v mape, ale dalsia ANO
# → vlozime rodica tej dalsej stranky.

new_rows = []      # zoznam riadkov vystupu (povodne + doplnene v spravnom poradi)
added_count = 0    # kolko stranok sme doplnili (ocakavame okolo 850)

for i in range(len(df)):
    # Aktualny riadok vzdy zaradime do vystupu.
    new_rows.append(df.iloc[i].to_dict())

    # Ak je to posledny riadok, nemame s cim porovnavat.
    if i + 1 >= len(df):
        continue

    curr = df.iloc[i]          # aktualny klik
    next_row = df.iloc[i + 1]  # nasledujuci klik

    # Doplname iba v ramci toho isteho sedenia.
    # Ked sa SESSION_ID zmeni, je to uz iny pouzivatel/sedenie a skok nedava zmysel.
    if curr["SESSION_ID"] != next_row["SESSION_ID"]:
        continue

    url_from = curr["URL"]      # z ktorej stranky pouzivatel ide
    url_to = next_row["URL"]    # na ktoru stranku pouzivatel ide

    # Ked je to ta ista stranka (refresh), nie je co doplnit.
    if url_from == url_to:
        continue

    # Hlavna podmienka: aktualnu stranku v mape nemame (napr. uz neexistuje),
    # ale cielovu mame → vieme zistit jej rodica a vlozit ho ako spojovaciu stranku.
    if url_from not in map_paths and url_to in map_paths:
        ref_page = parent.get(url_to)  # rodicovska stranka cielovej stranky

        # Vkladame iba ak rodic existuje a nie je to ta ista stranka, z ktorej prichadzame
        # (nechceme cyklus "from -> from -> to").
        if ref_page and ref_page != url_from:
            # Skopirujeme aktualny riadok (IP, USER_ID, SESSION_ID, cas zostavaju)
            # a iba prepiseme URL na rodica — tak vznikne doplneny zaznam.
            new_row = curr.to_dict()
            new_row["URL"] = ref_page  # jedina zmena oproti aktualnemu riadku
            new_rows.append(new_row)   # vlozime medzi aktualny a nasledujuci klik
            added_count += 1

# === KROK 5: Ulozenie doplneneho logu ===
result = pd.DataFrame(new_rows)
result.to_csv("out/cleaned_log4_doplnene.csv", index=False)  # index=False = nepiseme cisla riadkov

# Kontrola voci zadaniu — ocakava sa okolo 850 doplnenych zaznamov.
print(f"Doplnenych zaznamov: {added_count}")
print(f"Celkovy pocet zaznamov: {len(result)}")
