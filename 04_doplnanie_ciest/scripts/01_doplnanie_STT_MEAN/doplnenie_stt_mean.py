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
#   in/04_stt_mean.csv  - ocisteny log so sedeniami zo cv2
#   in/mapa_webu.xlsx             - strom stranok webu ukf.sk
#
# VYSTUP:
#   out/01_doplnene.csv - povodny log + vlozene medzistranky
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
df = pd.read_csv("in/04_stt_mean.csv")  # nacitame log; uz ma priradene sedenia z cv2
print(f"Nacitane: {len(df)} zaznamov")            # kontrolny vypis na obrazovku

# === KROK 2: Nacitanie a uprava mapy webu ===
# Mapa webu je hotovy Excel od ucitela: pre kazdu stranku hovori jej "rodica"
# (stranku, z ktorej sa na nu prirodzene da dostat).
mapa_df = pd.read_excel("in/mapa_webu.xlsx")

# Excel ma 4 stlpce - pomenujeme si ich. Realne pouzijeme len dva:
#   URL           = adresa stranky (kam pouzivatel ide),
#   ReferencePage = jej rodicovska stranka (odkial sa na nu chodi).
# Stlpce idx a Root nepotrebujeme.
mapa_df.columns = ["idx", "URL", "Root", "ReferencePage"]

# Prvy riadok Excelu nie su data, ale druha hlavicka - zahodime ho.
mapa_df = mapa_df.iloc[1:].reset_index(drop=True)

# V Exceli su PLNE adresy (https://www.ukf.sk/univerzita), v logu su len CESTY
# (/univerzita). Aby sa dali porovnat, odrezeme z adries domenu - ostane len cesta.
# str.replace iba zmaze prefix "https://www.ukf.sk":
#   URL           -> cesta samotnej stranky,
#   ReferencePage -> cesta jej rodica, ulozime ju do noveho stlpca ref_path.
mapa_df["URL"] = mapa_df["URL"].str.replace("https://www.ukf.sk", "", regex=False)
mapa_df["ref_path"] = mapa_df["ReferencePage"].str.replace("https://www.ukf.sk", "", regex=False)

# Z hlavnej stranky ostane po odrezani domeny prazdny retazec; v logu sa pise "/".
mapa_df.loc[mapa_df["URL"] == "", "URL"] = "/"
mapa_df.loc[mapa_df["ref_path"] == "", "ref_path"] = "/"

# parent = slovnik {stranka: jej rodic}. dict(zip(...)) spari kazdu URL s jej
# ref_path, takze rodica lubovolnej stranky najdeme v jednom kroku.
# Pozn.: Excel ma kazdu stranku PRAVE RAZ (jeden zadany rodic), takze tu sa nic
#   nevybera. V projekte sa mapa stavia z logu, kde ma stranka VELA Referrerov,
#   tak sa tam berie NAJCASTEJSI (groupby + value_counts().idxmax()); tu to odpada.
parent = dict(zip(mapa_df["URL"], mapa_df["ref_path"]))

# map_paths = mnozina vsetkych stranok v mape (kluce slovnika). Sluzi na rychly
# test "je tato stranka v mape?" - hladanie cez `in` je v mnozine okamzite.
map_paths = set(parent.keys())
print(f"Mapa webu: {len(map_paths)} stranok")

# === KROK 3: Prechod logom a doplnanie medzistranok ===
# Postup: pre kazdy riadok logu ho najprv pridame do vystupu. Potom sa pozrieme
# na nasledujuci riadok a ak je medzi nimi "skok", vlozime medzistranku.
new_rows = []      # sem zbierame vystup (povodne zaznamy + doplnene)
added_count = 0    # kolko stranok sme doplnili (pre vypis)

# Premena DataFrame na zoznam slovnikov - iteracia je takto vyrazne rychlejsia.
records = df.to_dict("records")

# Prejdeme vsetky zaznamy. enumerate vrati dvojicu (i, curr):
#   i    = poradove cislo riadku (0, 1, 2, ...) - treba ho, aby sme sa vedeli
#          pozriet na NASLEDUJUCI riadok cez records[i+1],
#   curr = aktualny zaznam = jeden riadok logu ako slovnik (IP, URL, SESSION_ID...).
for i, curr in enumerate(records):
    new_rows.append(curr)                       # aktualny zaznam ide vzdy do vystupu

    if i + 1 >= len(records):                   # posledny zaznam uz nema naslednika, koncime
        continue

    next_row = records[i + 1]

    # Doplnat ma zmysel len v ramci jedneho sedenia. Ak nasledujuci zaznam
    # patri inemu sedeniu, ide o novu navstevu - tam ziadna "medzera" nie je.
    if curr["SESSION_ID"] != next_row["SESSION_ID"]:
        continue

    url_from = curr["URL"]                      # stranka, na ktorej pouzivatel je
    url_to = next_row["URL"]                    # stranka, na ktoru ide

    if url_from == url_to:                      # ta ista stranka (refresh) - netreba nic doplnat
        continue

    # Podmienka doplnenia: prva stranka v mape nie je, druha ano.
    # (Ked druha ma znameho rodica, vieme co medzi ne vlozit.)
    if url_from not in map_paths and url_to in map_paths:
        ref_page = parent.get(url_to)           # rodic druhej stranky z mapy (None ak nie je)

        # Vlozime len ak rodic existuje a nie je to ta ista stranka, z ktorej ideme
        # (inak by sme vytvorili duplikat).
        if ref_page and ref_page != url_from:
            doplneny = curr.copy()              # novy zaznam zdedi vsetky udaje od aktualneho (IP, cas, pouzivatel...)
            doplneny["URL"] = ref_page          # menime len URL na doplnenu stranku
            new_rows.append(doplneny)
            added_count += 1

# === KROK 4: Ulozenie vystupu ===
result = pd.DataFrame(new_rows)  # zo zoznamu riadkov urobime spat tabulku

# index=False = do CSV nezapiseme cisla riadkov, aby vystup vyzeral ako vstup.
result.to_csv("out/01_doplnene.csv", index=False)

print(f"Doplnenych zaznamov: {added_count}")       # kontrola voci ocakavanym ~750
print(f"Celkovy pocet zaznamov: {len(result)}")    # povodne + doplnene
