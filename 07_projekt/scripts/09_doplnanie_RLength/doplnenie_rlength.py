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

parents = parent_series.to_dict()    # premenime na obycajny slovnik (rychlejsie vyhladavanie url -> rodic)
map_paths = set(parents.keys())      # mnozina vsetkych URL v mape (rychla kontrola "je tato URL v mape?")

print(f"Pocet stranok v mape webu (postavena z logu): {len(map_paths):,}")


# === KROK 3: Prechod po sedeniach a doplnenie medzistranok ===
# Ideme zaznam po zazname. Vzdy sa pozrieme aj na nasledujuci zaznam a pytame sa:
# "patria do toho isteho sedenia a je medzi nimi diera v mape webu?".
# Ak ano, vlozime medzi ne stranku, ktora je najcastejsim rodicom toho druheho.

new_rows = []        # sem zbierame vystup (povodne zaznamy + doplnene)
added_count = 0      # kolko stranok sme doplnili (pre vypis)

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
        rodic = parents.get(url_to)               # rodic stranky url_to = stranka, ktoru vlozime medzi url_from a url_to

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


# === KROK 4: Ulozenie vystupu ===

result = pd.DataFrame(new_rows)                                # zo zoznamu slovnikov spat tabulka
result.to_csv("out/09_doplnene_rlength.csv", index=False)      # index=False = nepridavat stlpec s cislami riadkov

print(f"\nDoplnenych zaznamov: {added_count:,}")
print(f"Celkovy pocet zaznamov: {len(result):,}")
print(f"Ulozene -> out/09_doplnene_rlength.csv")
