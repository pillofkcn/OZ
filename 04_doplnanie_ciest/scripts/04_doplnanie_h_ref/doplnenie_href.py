# ==========================================================
# CV3 - Uloha 04: Doplnanie ciest metodou h-ref
# ==========================================================
#
# CIEL:
#   V logu zo servera nam chybaju niektore stranky, ktore pouzivatel videl.
#   Napriklad klikol z A rovno na B, ale podla mapy webu A a B nie su priamo
#   prepojene - nieco muselo byt medzi nimi. Tieto "diery" doplname.
#
# PRECO TO ROBIME:
#   - Server nezachyti stranky nacitane z kese prehliadaca.
#   - Server nezachyti pouzitie tlacidla "spat".
#   - Bez doplnenia by sme nevideli realnu cestu pouzivatela po webe.
#
# AKO TO ROBI METODA H-REF (jednoducho):
#   - Mame mapu webu = zoznam stranok a ich "rodicov" (nadradenych stranok).
#     Napr. stranka /univerzita/kontakt ma rodica /univerzita.
#   - Ak pouzivatel skocil z A na B a B je v mape, B ma niekoho ako rodica.
#     Predpokladame, ze tym rodicom pouzivatel presiel po ceste na B.
#   - Tohto rodica vlozime do logu medzi A a B ako "doplnenu" stranku.
#
# Pozn.: V prednaske P8 sa to, co my volame `rodic`, nazyva ODKAZUJUCA STRANKA
# (Reference Page) z mapy webu. Su to ekvivalentne pojmy: stranka, z ktorej
# je odkaz na cielovu stranku.
#
# POZN. K ZJEDNODUSENIU vs PREDNASKA P8:
#   Prednaska ukazuje uplny backtrack rodicovskym retazcom az po spolocneho
#   predka. My doplname len jedneho rodica cieloveho URL.
#
# VSTUP:
#   - in/09_href.csv  ... ocisteny log z predchadzajuceho cvicenia,
#                                   uz ma rozpoznanych pouzivatelov a sedenia
#                                   (sedenie = jedna navsteva, sled klikov)
#   - in/mapa_webu.xlsx         ... excel so zoznamom stranok a ich rodicov
#
# VYSTUP:
#   - out/04_doplnene.csv  ... povodne riadky + nove doplnene riadky
#
# POUZITE KNIZNICE:
#   - pandas: praca s tabulkami (nacitanie CSV/Excel, iteracia po riadkoch)
#
# ALGORITMUS (1 veta):
#   Prejdeme log po dvojiciach susednych riadkov a ak zdrojova stranka chyba
#   v mape ale cielova je v mape, vlozime medzi ne rodica cielovej stranky.
#
# OCAKAVANY VYSLEDOK: cca 690 doplnenych zaznamov (zo zadania).
# ==========================================================

import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))  # umoznuje spustenie skriptu odkialkolvek (nielen z jeho priecinka)

import pandas as pd  # pandas = kniznica na pracu s tabulkami v Pythone

# === KROK 1: Nacitanie logu ===
df = pd.read_csv("in/09_href.csv")  # nacitame ocisteny log so sedeniami
print(f"Nacitane: {len(df)} zaznamov")  # vypiseme kolko riadkov sme nacitali (kontrola)

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
#   ocakavanie zo zadania (~690). Preto tu staci str.replace, nie url_to_path.
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

# === KROK 3 + 4: Prechod logom a doplnanie chybajucich stranok ===
#
# Postup: pre kazdu dvojicu susednych riadkov (A, B) v ramci toho isteho sedenia
# zistime, ci ide o medzeru. Ak ano, vlozime medzi ne rodica stranky B.
# Vysledne riadky zbierame do zoznamu a na konci z nich naraz vyrobime tabulku
# (je to rychlejsie ako pridavat po jednom do DataFrame).

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
result = pd.DataFrame(new_rows)  # zo zoznamu slovnikov vyrobime tabulku
result.to_csv("out/04_doplnene.csv", index=False)  # ulozime do CSV (bez stlpca s indexom)

print(f"Doplnenych zaznamov: {added_count}")  # vypiseme kolko sme doplnili (cakane: ~690)
print(f"Celkovy pocet zaznamov: {len(result)}")  # vypiseme finalny pocet riadkov vo vystupe
