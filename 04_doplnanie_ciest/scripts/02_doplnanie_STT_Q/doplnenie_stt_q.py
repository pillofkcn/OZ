# ==========================================================
# CV3 - Uloha 02: Doplnanie ciest (verzia STT_Q)
# ==========================================================
#
# CIEL:
#   Log od servera nezachyti vsetko, co pouzivatel videl. Ked klikne na
#   tlacidlo "Spat" v prehliadaci, stranka sa nacita z pamate prehliadaca
#   a server o tom nevie. V zazname potom chyba medzikrok. My ho domyslime
#   pomocou mapy webu (zoznam stranok a ich "rodicovskych" stranok).
#
# TEORIA pre laika:
#   - SEDENIE = jedna navsteva pouzivatela. Tu nam ich uz vyrobila predosla
#     uloha metodou STT_Q (stanovi hranicu necinnosti podla kvantilu casov
#     medzi klikmi — ked je pauza prilis dlha, zaciname nove sedenie).
#   - MAPA WEBU = strom stranok. Kazda stranka ma svojho "rodica" — stranku
#     o uroven vyssie (napr. rodic stranky /univerzita/kontakt je /univerzita).
#   - LOGIKA DOPLNANIA: ked v sedeni vidime preskok zo stranky A na stranku B,
#     a A v mape nie je ale B ano, pravdepodobne medzi nimi chyba rodic B
#     (pouzivatel sa cez "Spat" vratil na rodica a kliknul na B).
#
# VSTUP:
#   - in/05_stt_q.csv  - log po rozdeleni na sedenia metodou STT_Q
#   - in/mapa_webu.xlsx          - tabulka stranok a ich rodicov
#
# VYSTUP:
#   - out/02_doplnene.csv - povodny log + domyslene medzistranky
#
# POUZITE KNIZNICE:
#   - pandas: praca s tabulkami (nacitanie csv/xlsx, prechod po riadkoch).
#
# ALGORITMUS:
#   Prechadzame log po dvojiciach susednych riadkov; v rovnakom sedeni,
#   ked vidime preskok mimo mapy, vlozime medzi ne rodica cielovej stranky.
# ==========================================================

import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))  # umoznuje spustenie skriptu odkialkolvek (nielen z jeho priecinka)

import pandas as pd  # pandas = praca s tabulkami (CSV, Excel)

# === KROK 1: Nacitanie logu so sedeniami ===
df = pd.read_csv("in/05_stt_q.csv")  # nacitame log pripraveny predoslou ulohou
print(f"Nacitane: {len(df)} zaznamov")

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
# Pozn.: projekt na to pouziva funkciu url_to_path (cez urlparse), ktora ale
#   zahadzuje ?parametre (napr. /oznamy?start=20 -> /oznamy). Tu ich NECHAVAME -
#   query tu odlisuje rozne stranky a ich zliatim by pocet doplneni prestrelil
#   ocakavanie zo zadania (~750). Preto tu staci str.replace, nie url_to_path.
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

# === KROK 3 + 4: Hladanie preskokov a doplnanie medzistranok ===
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

# === KROK 5: Ulozenie vysledku ===
result = pd.DataFrame(new_rows)  # zo zoznamu slovnikov spravime tabulku
result.to_csv("out/02_doplnene.csv", index=False)  # index=False = bez stlpca s cislom riadku

# Vypisy pre kontrolu - zadanie ocakavalo cca 750 doplnenych zaznamov.
print(f"Doplnenych zaznamov: {added_count}")
print(f"Celkovy pocet zaznamov: {len(result)}")
