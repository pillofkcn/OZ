# ==========================================================
# CV3 - Uloha 01: Doplnanie ciest (vstup zo sedeni STT_MEAN)
# ==========================================================
#
# CIEL:
#   Web server log nezaznamenava kliky, ktore prehliadac vybavi z pamati
#   (tlacidlo "spat", ulozene stranky). V logu tak vznikaju "skoky" - dve
#   po sebe iduce stranky, medzi ktorymi v skutocnosti chyba 1 medzikrok.
#   Tento skript taky chybajuci medzikrok doplni.
#
# TEORIA (pre laika):
#   - Web Usage Mining = analyza spravania pouzivatelov na webe.
#   - Sedenie (session) = postupnost klikov jedneho pouzivatela bez velkej
#     prestavky (urcili sme ich v cv2 metodou STT_MEAN).
#   - STT_MEAN: STT (Session Timeout Threshold) = casovy prah necinnosti
#     MEDZI DVOMA KLIKMI. _MEAN znamena, ze ako hodnota tohto prahu sa
#     pouzil PRIEMER casovych rozdielov medzi klikmi (z dat). NIE je to
#     o trvani sedenia.
#   - Mapa webu = zoznam vsetkych stranok webu + pre kazdu jej "rodicovska"
#     stranka (kade sa na nu da prirodzene dostat).
#   - Heuristika doplnenia: ak v logu vidime skok z neznamej stranky A na
#     znamu stranku B, dopisme medzi ne rodica stranky B - lebo pouzivatel
#     sa cez neho s vysokou pravdepodobnostou dostal na B.
#   - Ocakavame doplnit asi 750 zaznamov (zadanie).
#
# POZN. K ZJEDNODUSENIU vs PREDNASKA P8:
#   Prednaska ukazuje uplny BACKTRACK rodicovskym retazcom az po
#   spolocneho predka (priklad zo slidov: A->B->C->D->X sa doplni ako
#   A B C D C B A X). My robime zjednodusenu variantu - doplnime LEN
#   JEDNEHO kanonickeho rodica cieloveho URL. Vypocetne lacnejsie a na
#   nasom datasete postacuje.
#
# VSTUP:
#   in/cleaned_log4_stt_mean.csv  - ocisteny log so sedeniami zo cv2
#   in/mapa_webu.xlsx             - strom stranok webu ukf.sk
#
# VYSTUP:
#   out/cleaned_log4_doplnene.csv - povodny log + vlozene medzistranky
#
# POUZITE KNIZNICE:
#   pandas - praca s tabulkami (nacitanie CSV/Excel, prechod po riadkoch).
#
# ALGORITMUS (1 veta):
#   Idem log riadok po riadku a tam, kde po sebe iduce dva kliky nesedia
#   s mapou webu, vlozim medzi ne rodicovsku stranku ciela.
# ==========================================================

import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))  # umoznuje spustenie skriptu odkialkolvek (nielen z jeho priecinka)

import pandas as pd  # pandas = praca s tabulkami (Excel/CSV)

# === KROK 1: Nacitanie logu so sedeniami ===
df = pd.read_csv("in/cleaned_log4_stt_mean.csv")  # nacitame log; uz ma priradene sedenia z cv2
print(f"Nacitane: {len(df)} zaznamov")            # kontrolny vypis na obrazovku

# === KROK 2: Nacitanie a uprava mapy webu ===
mapa = pd.read_excel("in/mapa_webu.xlsx")  # mapa je v Exceli (pripravil ucitel)

# Excel ma styri stlpce; dame im jednoduche nazvy, aby sa s nimi lepsie pracovalo.
mapa.columns = ["idx", "URL", "Root", "ReferencePage"]

# Prvy riadok v Exceli je druha hlavicka (nie data), tak ho zahodime.
mapa = mapa.iloc[1:].reset_index(drop=True)  # vyhodime prvy riadok a prenumerujeme

# V mape su plne URL (https://www.ukf.sk/...), ale v logu su len cesty (/...).
# Odrezeme domenu, aby sa to dalo porovnavat.
mapa["path"] = mapa["URL"].str.replace("https://www.ukf.sk", "", regex=False)
mapa["ref_path"] = mapa["ReferencePage"].str.replace("https://www.ukf.sk", "", regex=False)

# Po odrezani domeny ostane z hlavnej stranky prazdny retazec; v logu sa pise "/".
mapa.loc[mapa["path"] == "", "path"] = "/"        # zjednotenie zapisu hlavnej stranky
mapa.loc[mapa["ref_path"] == "", "ref_path"] = "/"

# Vyrobime si slovnik: pre kazdu stranku jej rodicovska stranka.
# Vyhoda slovnika: hladanie rodica je okamzite (jeden krok).
parent = dict(zip(mapa["path"], mapa["ref_path"]))

# Mnozina vsetkych stranok mapy - rychly test "je tato stranka v mape?".
map_paths = set(mapa["path"].unique())
print(f"Mapa webu: {len(map_paths)} stranok")  # kontrolny vypis

# === KROK 3: Prechod logom a doplnanie medzistranok ===
# Postup: pre kazdy riadok logu ho najprv pridame do vystupu. Potom sa pozrieme
# na nasledujuci riadok a ak je medzi nimi "skok", vlozime medzistranku.
new_rows = []      # sem zbierame vsetky riadky vystupu (povodne + doplnene)
added_count = 0    # kolko sme doplnili (ocakavame okolo 750)

for i in range(len(df)):
    # Aktualny riadok vzdy zaradime do vystupu (ziaden riadok nestratime).
    new_rows.append(df.iloc[i].to_dict())

    # Pri poslednom riadku uz nie je co porovnavat, preskocime.
    if i + 1 >= len(df):
        continue

    curr = df.iloc[i]            # aktualny klik
    next_row = df.iloc[i + 1]    # nasledujuci klik v logu

    # Doplname iba v ramci toho isteho sedenia - medzi dvomi sedeniami nema
    # zmysel hladat medzikrok (iny cas, casto iny pouzivatel).
    if curr["SESSION_ID"] != next_row["SESSION_ID"]:
        continue

    url_from = curr["URL"]      # stranka, z ktorej pouzivatel odchadza
    url_to = next_row["URL"]    # stranka, na ktoru ide

    # Ak su obe URL rovnake (obnovenie stranky), nie je co doplnat.
    if url_from == url_to:
        continue

    # HLAVNA PODMIENKA:
    # Stranka, z ktorej ide, nie je v mape, ale stranka, kam ide, v mape je.
    # Toto je situacia "skoku" - dopisme rodica cielu, lebo cez neho sa tam
    # pouzivatel zrejme dostal.
    if url_from not in map_paths and url_to in map_paths:
        ref_page = parent.get(url_to)  # rodic cielovej stranky (alebo None ak nie je)

        # Doplnenie ma zmysel len ak rodic existuje a nie je to ta ista stranka,
        # z ktorej pouzivatel prave odchadza (inak by sme len duplikovali).
        if ref_page and ref_page != url_from:
            # Skopirujeme cely aktualny riadok (ten isty pouzivatel, sedenie, cas)
            # a zmenime iba URL na rodicovsku stranku.
            new_row = curr.to_dict()
            new_row["URL"] = ref_page
            new_rows.append(new_row)
            added_count += 1  # pocitame doplnenia

# === KROK 4: Ulozenie vystupu ===
result = pd.DataFrame(new_rows)  # zo zoznamu riadkov urobime spat tabulku

# index=False = do CSV nezapiseme cisla riadkov, aby vystup vyzeral ako vstup.
result.to_csv("out/cleaned_log4_doplnene.csv", index=False)

print(f"Doplnenych zaznamov: {added_count}")       # kontrola voci ocakavanym ~750
print(f"Celkovy pocet zaznamov: {len(result)}")    # povodne + doplnene
