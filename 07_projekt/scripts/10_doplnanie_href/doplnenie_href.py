# ==========================================================
# PROJEKT - Uloha 10: Doplnenie chybajucich stranok do sedeni (metoda h-ref)
# ==========================================================
#
# CIEL:
#   Do navigacnych ciest pouzivatelov doplnit stranky, ktore server v logu
#   nezachytil, ale pouzivatel ich realne videl. Pracujeme so sedeniami,
#   ktore boli vytvorene predchadzajucim skriptom metodou h-ref.
#
# TEORIA (jednoducho):
#   Sedenie (session) = jedna navsteva jedneho pouzivatela na webe.
#   Pouzivatel klika z odkazu na odkaz. Niekedy ale server v logu zachyti
#   napr. stranku A a potom hned stranku C, hoci pouzivatel sa cez B
#   skutocne preklikal. Stane sa to vtedy, ked je B nacitana z pamate
#   prehliadaca (cache) alebo pouzivatel pouzil tlacidlo Spat - server
#   o tom nevie.
#   Metoda h-ref pozera, odkial pouzivatel prisiel (Referrer) a kde je
#   teraz (URL). Ked tieto nesedia, znamena to, ze cosi medzitym chyba.
#   My sa tu pokusame to chybajuce B najst a vlozit do logu, aby cesta
#   pouzivatela bola kompletna.
#
# AKO NAJDEME TO CHYBAJUCE B:
#   Postavime si "mapu webu" priamo z logu - pre kazdu stranku zistime,
#   z akeho odkazu k nej pouzivatelia najcastejsie prichadzali. Ten
#   najcastejsi odkaz povazujeme za "rodica" (najpravdepodobnejsiu
#   predoslu stranku). Ked v logu vidime divny prechod A -> C, vlozime
#   medzi ne rodica stranky C.
#
# VSTUP:
#   in/08_sedenia_href.csv - log z predoslej ulohy, kde uz ma kazdy klik
#   priradene cislo sedenia (SESSION_ID) podla metody h-ref.
#
# VYSTUP:
#   out/10_doplnene_href.csv - ten isty log + navyse vlozene chybajuce
#   medzistranky. Pocet riadkov bude o trochu vyssi ako vstup.
#
# POUZITE KNIZNICE:
#   - pandas: praca s tabulkou (nacitanie CSV, groupby, ulozenie).
#   - urllib.parse.urlparse: bezpecne rozlozi URL adresu na casti
#     (potrebujeme z plnej adresy vytiahnut len cestu bez domeny).
#
# ALGORITMUS (1 veta):
#   Postavime mapu webu z logu, potom prejdeme zaznamy po dvojiciach
#   a tam, kde nieco chyba, vlozime kanonickeho rodica.
# ==========================================================

import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))  # umoznuje spustenie skriptu odkialkolvek (nielen z jeho priecinka)

import pandas as pd                       # praca s tabulkami (CSV, groupby)
from urllib.parse import urlparse         # bezpecne rozlozenie URL adresy


def url_to_path(url):
    """Z plnej webovej adresy vytiahne len cestu (cast za domenou).

    PRECO TO ROBIME:
      V logu mame dva rozne tvary - Referrer byva plna adresa
      ('http://www.ukf.sk/foo'), ale URL byva uz len cesta ('/foo').
      Aby sme ich vedeli porovnat, musime ich zjednotit na rovnaky tvar.

    PRIKLADY:
      'http://www.ukf.sk/foo/bar' -> '/foo/bar'
      '/foo/bar'                  -> '/foo/bar'   (uz je cesta)
      '-'                         -> None         (chybajuca hodnota)
      'http://www.ukf.sk'         -> '/'          (hlavna stranka)
    """
    # ak to nie je text alebo je to znacka "-" (chyba hodnota), vratime nic
    if not isinstance(url, str) or url == "-":
        return None
    # ak uz zacina lomkom, je to cesta - netreba nic rozkladat
    if url.startswith("/"):
        return url
    try:
        # vytiahneme z adresy len cast za domenou (napr. /foo z http://ukf.sk/foo)
        path = urlparse(url).path
        # ak je cesta prazdna (adresa bez lomky na konci), vratime aspon "/"
        return path or "/"
    except Exception:
        # ak by parser zlyhal na divnej adrese, radsej vratime nic nez spadneme
        return None


# === KROK 1: Nacitanie logu so sedeniami ===
# nacitame log; low_memory=False = pandas si data prejde a urci typy spravne
df = pd.read_csv("in/08_sedenia_href.csv", low_memory=False)
print(f"Nacitane: {len(df):,} zaznamov")

# === KROK 2: Postavenie mapy webu z logu ===
# Kazdy riadok v logu hovori "pouzivatel prisiel na URL z Referrer".
# Pre kazdu stranku zistime, z akeho odkazu k nej chodili najcastejsie -
# to je jej "rodic" v nasej mape.

# (a) zoberieme len stlpce Referrer a URL; .copy() = vlastna kopia (aby nas pandas nevarovala)
mapa_df = df[["Referrer", "URL"]].copy()

# (b) Referrer prerobime na cestu bez domeny (aby bol porovnatelny s URL)
mapa_df["ref_path"] = mapa_df["Referrer"].apply(url_to_path)

# (c) nechame len odkazy z webu ukf.sk; externe (Google, Facebook) do mapy nepatria
# case=False = je nam jedno ci je text velkymi/malymi pismenami
# na=False = prazdne hodnoty neberieme ako zhodu
mapa_df = mapa_df[mapa_df["Referrer"].str.contains("ukf.sk", case=False, na=False)]

# (d) vyhodime riadky, kde sa Referrer nepodarilo prerobit na cestu
mapa_df = mapa_df.dropna(subset=["ref_path"])

# (e) pre kazdu stranku najdeme najcastejsi referrer = jej "rodica" v mape webu
# postup: rozdelime data podla URL, v kazdej skupine spocitame referrery
# a vyberieme ten s najvyssim poctom (idxmax = ktora hodnota mala najviac)
parent_series = mapa_df.groupby("URL")["ref_path"].agg(lambda x: x.value_counts().idxmax())

# prerobime na obycajny slovnik - rychlejsie sa v nom hlada
parents = parent_series.to_dict()

# mnozina vsetkych stranok v mape; hladanie "je v mnozine?" je velmi rychle
map_paths = set(parents.keys())

print(f"Pocet stranok v mape webu (postavena z logu): {len(map_paths):,}")

# === KROK 3: Doplnanie chybajucich medzistranok ===
# Prejdeme log po dvojiciach (aktualny + nasledujuci zaznam).
# Ked medzi nimi nieco nesedi, vlozime medzi ne rodica nasledujucej stranky.

new_rows = []        # sem postupne uklada vsetky zaznamy (povodne aj doplnene)
added_count = 0      # pocitadlo, kolko medzistranok sme doplnili

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

# === KROK 4: Ulozenie vystupu ===
# zoznam slovnikov prerobime spat na tabulku, aby sme ju mohli ulozit do CSV
result = pd.DataFrame(new_rows)

# index=False = neuklada cislovanie riadkov (inak by sa v CSV objavil zbytocny stlpec)
result.to_csv("out/10_doplnene_href.csv", index=False)

# vypisy do konzoly na rychlu kontrolu po behu
print(f"\nDoplnenych zaznamov: {added_count:,}")
print(f"Celkovy pocet zaznamov: {len(result):,}")
print(f"Ulozene -> out/10_doplnene_href.csv")
