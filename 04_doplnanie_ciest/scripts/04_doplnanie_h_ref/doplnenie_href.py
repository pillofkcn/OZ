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
#   - in/cleaned_log4_href.csv  ... ocisteny log z predchadzajuceho cvicenia,
#                                   uz ma rozpoznanych pouzivatelov a sedenia
#                                   (sedenie = jedna navsteva, sled klikov)
#   - in/mapa_webu.xlsx         ... excel so zoznamom stranok a ich rodicov
#
# VYSTUP:
#   - out/cleaned_log4_doplnene.csv  ... povodne riadky + nove doplnene riadky
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
df = pd.read_csv("in/cleaned_log4_href.csv")  # nacitame ocisteny log so sedeniami
print(f"Nacitane: {len(df)} zaznamov")  # vypiseme kolko riadkov sme nacitali (kontrola)

# === KROK 2: Nacitanie a uprava mapy webu ===
mapa = pd.read_excel("in/mapa_webu.xlsx")  # nacitame excel s mapou stranok webu UKF
mapa.columns = ["idx", "URL", "Root", "ReferencePage"]  # premenujeme stlpce na jednotne nazvy
mapa = mapa.iloc[1:].reset_index(drop=True)  # preskocime prvy riadok (povazujeme ho za hlavicku)

# Z plnej adresy "https://www.ukf.sk/univerzita" spravime kratku cestu "/univerzita".
# V logu su tiez len kratke cesty, takze sa to musi zhodovat.
mapa["path"] = mapa["URL"].str.replace("https://www.ukf.sk", "", regex=False)  # odrezeme domenu z URL
mapa["ref_path"] = mapa["ReferencePage"].str.replace("https://www.ukf.sk", "", regex=False)  # to iste pre rodicovsku stranku

# Ak po odrezani domeny nezostalo nic, je to hlavna stranka - oznacime ju "/".
mapa.loc[mapa["path"] == "", "path"] = "/"  # prazdna cesta = hlavna stranka
mapa.loc[mapa["ref_path"] == "", "ref_path"] = "/"  # to iste pre rodicovsku stranku

# Vyrobime slovnik: pre kazdu stranku si ulozime jej rodica.
# Napr. parent["/univerzita/kontakt"] = "/univerzita". Pouzijeme ho na rychle vyhladanie rodica.
parent = dict(zip(mapa["path"], mapa["ref_path"]))  # slovnik {stranka: rodicovska stranka}

# Mnozina vsetkych stranok z mapy - rychle overenie, ci je stranka v mape (operacia "in" je okamzita).
map_paths = set(mapa["path"].unique())  # mnozina vsetkych znamych stranok
print(f"Mapa webu: {len(map_paths)} stranok")  # vypiseme kolko stranok ma mapa (kontrola)

# === KROK 3 + 4: Prechod logom a doplnanie chybajucich stranok ===
#
# Postup: pre kazdu dvojicu susednych riadkov (A, B) v ramci toho isteho sedenia
# zistime, ci ide o medzeru. Ak ano, vlozime medzi ne rodica stranky B.
# Vysledne riadky zbierame do zoznamu a na konci z nich naraz vyrobime tabulku
# (je to rychlejsie ako pridavat po jednom do DataFrame).

new_rows = []  # sem zbierame vsetky riadky (povodne + doplnene) v spravnom poradi
added_count = 0  # pocitadlo, kolko stranok sme doplnili

for i in range(len(df)):
    # Kazdy povodny riadok zachovame - pridame ho do vystupu.
    new_rows.append(df.iloc[i].to_dict())  # pridame aktualny riadok ako slovnik

    # Pri poslednom riadku uz neexistuje dalsi - nie je co porovnavat, koncime.
    if i + 1 >= len(df):
        continue

    curr = df.iloc[i]  # aktualny riadok (stranka A)
    next_row = df.iloc[i + 1]  # nasledujuci riadok (stranka B)

    # Doplname len v ramci jedneho sedenia. Ked sa zmenilo sedenie, ide o ineho
    # pouzivatela alebo o novu navstevu - tam by doplnenie nedavalo zmysel.
    if curr["SESSION_ID"] != next_row["SESSION_ID"]:
        continue

    url_from = curr["URL"]  # adresa stranky A (odkial pouzivatel ide)
    url_to = next_row["URL"]  # adresa stranky B (kam pouzivatel ide)

    # Ak A a B su tie iste (refresh stranky), netreba nic doplnat.
    if url_from == url_to:
        continue

    # Hlavna podmienka doplnenia:
    #   - A nie je v mape webu (nevieme overit, kde je v strukture)
    #   - B je v mape webu (vieme zistit jeho rodica)
    # V takomto pripade vlozime rodica B ako medzistranku.
    if url_from not in map_paths and url_to in map_paths:
        ref_page = parent.get(url_to)  # zistime rodica stranky B (None ak nie je v mape)
        # Vlozime len ak rodic existuje a nie je rovny stranke A
        # (ak by bol rovny A, znamena to ze A je priamo rodicom B - ziadna diera).
        if ref_page and ref_page != url_from:
            new_row = curr.to_dict()  # skopirujeme udaje z A (USER_ID, SESSION_ID, cas...)
            new_row["URL"] = ref_page  # adresu zmenime na rodicovsku stranku
            new_rows.append(new_row)  # pridame doplneny riadok medzi A a B
            added_count += 1  # zvysime pocitadlo doplnenych zaznamov

# === KROK 5: Ulozenie vysledku ===
result = pd.DataFrame(new_rows)  # zo zoznamu slovnikov vyrobime tabulku
result.to_csv("out/cleaned_log4_doplnene.csv", index=False)  # ulozime do CSV (bez stlpca s indexom)

print(f"Doplnenych zaznamov: {added_count}")  # vypiseme kolko sme doplnili (cakane: ~690)
print(f"Celkovy pocet zaznamov: {len(result)}")  # vypiseme finalny pocet riadkov vo vystupe
