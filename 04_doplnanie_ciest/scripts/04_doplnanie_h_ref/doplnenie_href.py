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

# parents = slovnik {stranka: jej rodic}. Slovnik (dict) = tabulka dvojic
# kluc->hodnota, v ktorej podla kluca (stranky) okamzite najdeme hodnotu (rodica).
# zip(URL, ref_path) = spari k sebe i-tu URL a i-ty ref_path; dict(...) z tych
# dvojic postavi slovnik. Takze rodica lubovolnej stranky najdeme v jednom kroku.
# Pozn.: Excel ma kazdu stranku PRAVE RAZ (jeden zadany rodic), takze tu sa nic
#   nevybera. V projekte sa mapa stavia z logu, kde ma stranka VELA Referrerov,
#   tak sa tam berie NAJCASTEJSI (groupby + value_counts().idxmax()); tu to odpada.
parents = dict(zip(mapa_df["URL"], mapa_df["ref_path"]))

# map_paths = mnozina (set) vsetkych stranok v mape. parents.keys() = vsetky kluce
# slovnika (= vsetky stranky); set(...) z nich spravi mnozinu. Mnozina sluzi na
# rychly test "je tato stranka v mape?" - hladanie cez `in` je v nej okamzite
# (rychlejsie nez v obycajnom zozname).
map_paths = set(parents.keys())
print(f"Mapa webu: {len(map_paths)} stranok")

# === KROK 3 + 4: Prechod logom a doplnanie chybajucich stranok ===
#
# Postup: pre kazdu dvojicu susednych riadkov (A, B) v ramci toho isteho sedenia
# zistime, ci ide o medzeru. Ak ano, vlozime medzi ne rodica stranky B.
# Vysledne riadky zbierame do zoznamu a na konci z nich naraz vyrobime tabulku
# (je to rychlejsie ako pridavat po jednom do DataFrame).

new_rows = []      # sem zbierame vystup (povodne zaznamy + doplnene)
added_count = 0    # kolko stranok sme doplnili (pre vypis)

# to_dict("records") = prerobi tabulku (DataFrame) na ZOZNAM slovnikov, kde kazdy
# slovnik = jeden riadok logu (stlpec -> hodnota), napr. {"URL": "/a", "SESSION_ID": 1, ...}.
# Je to zoznam (nie jeden dict), lebo riadkov je vela. Konvertujeme az tu, lebo
# prechadzat obycajny Python zoznam je vyrazne rychlejsie ako riadky DataFrame.
records = df.to_dict("records")

# enumerate dava DVOJICU (i, curr): i = poradove cislo riadku (0, 1, 2, ...),
# curr = aktualny klik (jeden riadok logu ako slovnik). Index i potrebujeme preto,
# aby sme sa pri kazdom kliku vedeli pozriet aj na NASLEDUJUCI klik (records[i+1]) -
# doplnanie totiz porovnava vzdy dvojicu "tento klik -> dalsi klik".
for i, curr in enumerate(records):
    # Aktualny klik ide do vystupu VZDY - z povodneho logu nic nezahadzujeme,
    # pripadnu medzistranku len PRIDAME za neho (nizsie).
    new_rows.append(curr)

    # Ak sme na uplne poslednom zazname, nema za sebou ziadny "dalsi klik", s ktorym
    # by sme ho parovali -> niet co doplnat, ideme na dalsiu iteraciu cyklu.
    if i + 1 >= len(records):
        continue
    next_row = records[i + 1]                    # nasledujuci klik (len nan nahliadneme, neodstranujeme ho)

    # Dve stranky tejto dvojice, ktore budeme porovnavat:
    url_from = curr["URL"]                       # stranka AKTUALNEHO kliku (odkial pouzivatel ide)
    url_to = next_row["URL"]                     # stranka NASLEDUJUCEHO kliku (kam ide)

    # Tri podmienky doplnenia - medzistranku vlozime, len ak platia VSETKY:
    rovnake_sedenie = curr["SESSION_ID"] == next_row["SESSION_ID"]      # kliky z jedneho sedenia
    ina_stranka     = url_from != url_to                                # nie je to refresh tej istej stranky
    diera_v_mape    = url_from not in map_paths and url_to in map_paths # prva nie je v mape, druha ano

    if rovnake_sedenie and ina_stranka and diera_v_mape:
        rodic = parents.get(url_to)                # rodic stranky url_to = stranka, ktoru vlozime medzi url_from a url_to

        # Vlozime ju LEN ak: rodic vobec existuje (parents.get nieco vratil) A
        # zaroven to nie je ta ista stranka, z ktorej prave ideme (url_from) -
        # inak by sme vyrobili zbytocny duplikat.
        if rodic and rodic != url_from:
            # Doplnenie = novy "klik" na rodica, ktory zaradime hned za aktualny klik.
            # curr.copy() spravi samostatnu kopiu aktualneho riadku, takze novy zaznam
            # zdedi vsetky udaje (cas, IP, pouzivatel, SESSION_ID...). Kopia je dolezita,
            # aby riadok nizsie (zmena URL) neprepisal aj povodny curr.
            doplneny = curr.copy()
            doplneny["URL"] = rodic               # novemu zaznamu zmenime LEN URL na rodicovsku stranku
            new_rows.append(doplneny)             # zaradime ho do vystupu (hned za aktualny klik)
            added_count += 1                      # +1 do pocitadla doplnenych stranok

# === KROK 5: Ulozenie vysledku ===
result = pd.DataFrame(new_rows)  # zo zoznamu slovnikov vyrobime tabulku
result.to_csv("out/04_doplnene.csv", index=False)  # ulozime do CSV (bez stlpca s indexom)

print(f"Doplnenych zaznamov: {added_count}")  # vypiseme kolko sme doplnili (cakane: ~690)
print(f"Celkovy pocet zaznamov: {len(result)}")  # vypiseme finalny pocet riadkov vo vystupe
