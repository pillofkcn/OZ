# ==========================================================
# PROJEKT - Uloha 09: Doplnenie chybajucich stranok do sedeni (RLength)
# ==========================================================
#
# CIEL:
#   V logu mame zaznamy o tom, na ktore stranky pouzivatel klikol.
#   Niekedy ale dve po sebe iduce kliky NEMAJU priame prepojenie
#   (na stranke A nie je odkaz na stranku C). Znamena to, ze
#   medzi nimi pouzivatel preslo este nejakou stranku B, ale jej
#   navsteva sa do logu nedostala (typicky kvoli pamati prehliadaca,
#   ktora vrati stranku bez toho aby sa spytala servera).
#   Tuto chybajucu stranku B tu doplname.
#
# TEORIA - jednoducho:
#   - SEDENIE = jedna navsteva pouzivatela (zoznam klikov od prichodu po odchod).
#     V projekte uz mame sedenia hotove z ulohy 07 (stlpec SESSION_ID).
#   - MAPA WEBU = zoznam, ktora stranka odkazuje na ktoru.
#     Kazdy zaznam v logu obsahuje pole "Referrer" = z ktorej stranky
#     pouzivatel prisiel. Takze dvojica (Referrer, URL) nam hovori
#     "zo stranky Referrer vedie odkaz na stranku URL". Z mnohych takych
#     dvojic poskladame mapu webu.
#   - DOPLNENIE: ked v sedeni vidime A potom C a tieto nie su priamo
#     prepojene v mape, najdeme najcastejsieho "rodica" stranky C
#     (z akej stranky sa na C najcastejsie chodi) a vlozime ho ako B.
#
# VSTUP:
#   in/07_sedenia_rlength.csv - log uz rozdeleny na sedenia (z ulohy 07).
#   Stlpce: IP, DateTime, URL, Referrer, Agent, UNIXTIME,
#           USER_ID, Length, SESSION_ID
#
# VYSTUP:
#   out/09_doplnene_rlength.csv - povodne zaznamy plus doplnene medzistranky.
#
# POUZITE KNIZNICE:
#   - pandas: praca s tabulkou (nacitanie CSV, filtrovanie, groupby).
#   - urllib.parse.urlparse: rozkuska URL na casti (domena, cesta...).
#
# ALGORITMUS (zhrnutie):
#   1) Z logu poskladame mapu webu (kto na koho odkazuje).
#   2) Prejdeme sedenie po sedeni, dvojicu po dvojici.
#   3) Ked dva susedne kliky nie su priamo prepojene, vlozime medzi
#      ne najcastejsieho rodica druhej stranky.
# ==========================================================

import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))  # umoznuje spustenie skriptu odkialkolvek (nielen z jeho priecinka)

import pandas as pd
from urllib.parse import urlparse


def url_to_path(url):
    """Z URL vyextrahuje len cestu bez domeny.

    Napriklad 'http://www.ukf.sk/foo' premeni na '/foo'.
    Preco: Referrer v logu byva plna adresa ('http://...'), ale stlpec URL
    byva uz len cesta ('/foo'). Aby sme ich mohli porovnavat, musime
    obe strany dostat do rovnakeho tvaru (cesta).
    """
    if not isinstance(url, str) or url == "-":   # '-' v logu znamena "ziadny referrer"
        return None
    if url.startswith("/"):                      # uz je to cesta, netreba parsovat
        return url
    try:
        path = urlparse(url).path                # vytiahneme cast za domenou
        return path or "/"                       # prazdne -> hlavna stranka '/'
    except Exception:
        return None


# === KROK 1: Nacitanie logu so sedeniami ===

df = pd.read_csv("in/07_sedenia_rlength.csv", low_memory=False)  # low_memory=False = pandas si data prejde a urci typy spravne
print(f"Nacitane: {len(df):,} zaznamov")


# === KROK 2: Postavenie mapy webu z logu ===
# Mapa webu vznikne tak, ze pre kazdy zaznam (Referrer -> URL) povieme
# "zo stranky Referrer sa da odkliknut na URL". Z opakovani zistime,
# ktory referrer je pre kazdu stranku najcastejsi (= najpravdepodobnejsi rodic).

mapa_df = df[["Referrer", "URL"]].copy()                      # zobereme len tieto dva stlpce (kopia aby sme neprepisali povodne data)
mapa_df["ref_path"] = mapa_df["Referrer"].apply(url_to_path)  # z plnej adresy Referrera vyrobime cestu (porovnatelnu s URL)

# Nechame len Referrery z domeny ukf.sk - cudzie stranky (Google, Facebook)
# nepatria do mapy nasho webu, nehovoria nic o jeho vnutornej strukture.
mapa_df = mapa_df[mapa_df["Referrer"].str.contains("ukf.sk", case=False, na=False)]  # case=False ignoruje velkost pisma; na=False = NaN sa nepocita ako zhoda

mapa_df = mapa_df.dropna(subset=["ref_path"])                 # vyhodime riadky, kde sa Referrer nedal previest na cestu

# Pre kazdu URL najdeme najcastejsieho referrera - berieme ho ako "rodica" tej stranky.
# Postup: zoradime ref_path podla URL, v kazdej skupine spocitame ako casto sa
# ktory ref_path objavil a vyberieme ten s najvyssim poctom.
parent_series = mapa_df.groupby("URL")["ref_path"].agg(lambda x: x.value_counts().idxmax())

parent = parent_series.to_dict()    # premenime na obycajny slovnik (rychlejsie vyhladavanie url -> rodic)
map_paths = set(parent.keys())      # mnozina vsetkych URL v mape (rychla kontrola "je tato URL v mape?")

print(f"Pocet stranok v mape webu (postavena z logu): {len(map_paths):,}")


# === KROK 3: Prechod po sedeniach a doplnenie medzistranok ===
# Ideme zaznam po zazname. Vzdy sa pozrieme aj na nasledujuci zaznam a pytame sa:
# "patria do toho isteho sedenia a je medzi nimi diera v mape webu?".
# Ak ano, vlozime medzi ne stranku, ktora je najcastejsim rodicom toho druheho.

new_rows = []        # sem zbierame vystup (povodne zaznamy + doplnene)
added_count = 0      # kolko stranok sme doplnili (pre vypis)

# Premena DataFrame na zoznam slovnikov - iteracia je takto vyrazne rychlejsia.
records = df.to_dict("records")

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

    if url_from == url_to:                      # to ista stranka (refresh) - netreba nic doplnat
        continue

    # Podmienka doplnenia: prva stranka v mape nie je, druha ano.
    # (Ked druha ma znameho rodica, vieme co medzi ne vlozit.)
    if url_from not in map_paths and url_to in map_paths:
        ref_page = parent.get(url_to)           # najcastejsi rodic druhej stranky = nasa kandidatka na doplnenie

        # Vlozime len ak rodic existuje a nie je to ta ista stranka, z ktorej ideme
        # (inak by sme vytvorili duplikat).
        if ref_page and ref_page != url_from:
            doplneny = curr.copy()              # novy zaznam zdedi vsetky udaje od aktualneho (IP, cas, pouzivatel...)
            doplneny["URL"] = ref_page          # menime len URL na doplnenu stranku
            new_rows.append(doplneny)
            added_count += 1


# === KROK 4: Ulozenie vystupu ===

result = pd.DataFrame(new_rows)                                # zo zoznamu slovnikov spat tabulka
result.to_csv("out/09_doplnene_rlength.csv", index=False)      # index=False = nepridavat stlpec s cislami riadkov

print(f"\nDoplnenych zaznamov: {added_count:,}")
print(f"Celkovy pocet zaznamov: {len(result):,}")
print(f"Ulozene -> out/09_doplnene_rlength.csv")
