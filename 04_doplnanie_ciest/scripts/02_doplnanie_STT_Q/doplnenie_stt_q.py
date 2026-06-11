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
#   - in/cleaned_log4_stt_q.csv  - log po rozdeleni na sedenia metodou STT_Q
#   - in/mapa_webu.xlsx          - tabulka stranok a ich rodicov
#
# VYSTUP:
#   - out/cleaned_log4_doplnene.csv - povodny log + domyslene medzistranky
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
df = pd.read_csv("in/cleaned_log4_stt_q.csv")  # nacitame log pripraveny predoslou ulohou
print(f"Nacitane: {len(df)} zaznamov")

# === KROK 2: Nacitanie mapy webu ===
mapa = pd.read_excel("in/mapa_webu.xlsx")  # nacitame Excel so zoznamom stranok
mapa.columns = ["idx", "URL", "Root", "ReferencePage"]  # premenujeme stlpce na zname nazvy
# Prvy riadok je v skutocnosti druha hlavicka z Excelu (nie data), tak ho preskocime.
mapa = mapa.iloc[1:].reset_index(drop=True)  # vyhodime prvy riadok a precislujeme

# V mape su plne adresy (https://www.ukf.sk/...), v logu len cesty (/...).
# Aby sme ich vedeli porovnavat, odstranime z mapy zaciatok adresy.
mapa["path"] = mapa["URL"].str.replace("https://www.ukf.sk", "", regex=False)
mapa["ref_path"] = mapa["ReferencePage"].str.replace("https://www.ukf.sk", "", regex=False)
# Pre hlavnu stranku ostane po orezani prazdny retazec - premenime ho na "/".
mapa.loc[mapa["path"] == "", "path"] = "/"          # hlavna stranka portalu
mapa.loc[mapa["ref_path"] == "", "ref_path"] = "/"  # rodic na korenovej urovni

# Slovnik {stranka: jej rodic} - umozni nam rychlo zistit rodica lubovolnej stranky.
parent = dict(zip(mapa["path"], mapa["ref_path"]))

# Mnozina vsetkych stranok z mapy - rychle overenie ci stranka existuje v mape.
map_paths = set(mapa["path"].unique())
print(f"Mapa webu: {len(map_paths)} stranok")

# === KROK 3 + 4: Hladanie preskokov a doplnanie medzistranok ===
new_rows = []      # sem ukladame vysledne riadky (povodne + domyslene)
added_count = 0    # pocitadlo domyslenych zaznamov

for i in range(len(df)):
    # Aktualny riadok pridame do vysledku vzdy - nic nemazeme, iba doplname.
    new_rows.append(df.iloc[i].to_dict())

    # Pri poslednom riadku uz neexistuje "dalsi", takze nemame co porovnavat.
    if i + 1 >= len(df):
        continue

    curr = df.iloc[i]          # aktualny zaznam (odkial pouzivatel prisiel)
    next_row = df.iloc[i + 1]  # nasledujuci zaznam (kam pokracoval)

    # Doplname iba v ramci toho isteho sedenia - medzi roznymi sedeniami
    # je prirodzena medzera (pouzivatel odisiel) a nic nechyba.
    if curr["SESSION_ID"] != next_row["SESSION_ID"]:
        continue

    url_from = curr["URL"]      # stranka, na ktorej bol
    url_to = next_row["URL"]    # stranka, na ktoru sa presunul

    # Ak sa adresa nezmenila (F5 alebo to iste), niet co doplnat.
    if url_from == url_to:
        continue

    # KROK 4: detekcia chybajuceho medzikroku.
    # Ked startovacia stranka nie je v mape, ale cielova ano, predpokladame,
    # ze sa pouzivatel cez "Spat" vratil na rodica cielovej stranky a z neho
    # pokracoval - takze tu chyba rodic cielovej stranky.
    if url_from not in map_paths and url_to in map_paths:
        # .get() vrati rodica, alebo None ked nie je - bezpecnejsie ako parent[...].
        ref_page = parent.get(url_to)
        # Doplname len ked rodic existuje a nie je to ta ista stranka, z ktorej sme prisli
        # (inak by sme do logu pridali zbytocny duplikat).
        if ref_page and ref_page != url_from:
            # Novy riadok zdedi vsetko od aktualneho (pouzivatel, sedenie, cas, ...)
            # a zmenime mu len adresu na rodica - to je domysleny medzikrok.
            new_row = curr.to_dict()
            new_row["URL"] = ref_page  # jedina zmena - adresa na rodica cielovej stranky
            new_rows.append(new_row)   # vlozime ho medzi curr a next
            added_count += 1

# === KROK 5: Ulozenie vysledku ===
result = pd.DataFrame(new_rows)  # zo zoznamu slovnikov spravime tabulku
result.to_csv("out/cleaned_log4_doplnene.csv", index=False)  # index=False = bez stlpca s cislom riadku

# Vypisy pre kontrolu - zadanie ocakavalo cca 750 doplnenych zaznamov.
print(f"Doplnenych zaznamov: {added_count}")
print(f"Celkovy pocet zaznamov: {len(result)}")
