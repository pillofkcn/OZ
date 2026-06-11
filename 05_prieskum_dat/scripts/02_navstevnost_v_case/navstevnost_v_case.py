# ==========================================================
# CV5 - Uloha 02: Ako sa menila navstevnost banky v case
# ==========================================================
#
# CIEL:
#   Pozriet sa, ako sa pocas rokov 2009-2012 menil pocet pristupov na
#   stranky banky. Zaroven porovnat obdobie krizy vs po krize a sledovat,
#   ake kategorie obsahu (napr. ucty, uvery) ludia navstevovali kedy.
#
# TEORIA (jednoducho):
#   - V logu mame jeden riadok = jedno otvorenie stranky.
#   - Ked spocitame riadky za mesiac/kvartal, dostaneme "kolko ludi to
#     pouzivalo v danom case". To je zakladna casova agregacia.
#   - "Crisis" je priznak (0/1), ci dany pristup bol pocas financnej krizy
#     alebo uz po nej. Hranica je niekde okolo konca roku 2010.
#   - Kategoria = oznacenie obsahu stranky (z cv1 cisteneho logu).
#
# VSTUP:
#   in/logs5.csv - vycisteny log banky (stlpce time, category, crisis,
#                  yearQuartal, ...). Oddelovac je bodkociarka.
#
# VYSTUP:
#   out/mesacne_navstevy.csv  - pocet pristupov za kazdy mesiac
#   out/kategorie_v_case.csv  - pocet pristupov: riadok=kvartal, stlpec=kategoria
#   out/navstevnost.png       - 2 grafy (mesacny rad + kategorie v case)
#
# POUZITE KNIZNICE:
#   - pandas     - praca s tabulkou (citanie CSV, groupby, datumy)
#   - matplotlib - kreslenie grafov
#
# ALGORITMUS:
#   1) Nacitaj log a sprav z textu skutocny datum.
#   2) Spocitaj pristupy za mesiac.
#   3) Rozdel data na obdobie krizy a po krize.
#   4) Spocitaj pristupy po kvartaloch a kategoriach.
#   5) Nakresli 2 grafy a uloz CSV vystupy.
# ==========================================================

import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))  # umoznuje spustenie skriptu odkialkolvek (nielen z jeho priecinka)

import pandas as pd
import matplotlib.pyplot as plt

# === KROK 1: Nacitanie logu a prevod textu na datum ===
print("Nacitavam dataset...")
df = pd.read_csv("in/logs5.csv", sep=";", quotechar='"', low_memory=False)  # nacitame CSV; sep=";" lebo banka pouziva bodkociarku, low_memory=False = pandas si preberie cely subor naraz a spravne urci typy
df["datum"] = pd.to_datetime(df["time"], format="%d.%m.%Y %H:%M:%S", errors="coerce")  # text "28.05.2010 14:23:01" prerobime na realny datum; errors="coerce" = ak by bol riadok pokazeny, nehodi chybu ale prazdnu hodnotu
df["mesiac"] = df["datum"].dt.to_period("M")  # z datumu vytiahneme len mesiac a rok (napr. 2010-05); kazdy klik tak vieme priradit do meseiac-skupiny

# === KROK 2: Pocet pristupov za kazdy mesiac ===
# Zoskupime kliky podla mesiaca a spocitame ich. Vysledok je rad cisel:
# pre kazdy mesiac vieme, kolko otvoreni stranky tam padlo.
mesacne = df.groupby("mesiac").size()
print(f"\nMesacne navstevy:")
print(f"  Min: {mesacne.min()} ({mesacne.idxmin()})")        # mesiac s najmensou navstevnostou
print(f"  Max: {mesacne.max()} ({mesacne.idxmax()})")        # mesiac s najvacsou navstevnostou
print(f"  Priemer: {mesacne.mean():.0f}")                    # priemerny pocet pristupov za mesiac, zaokruhleny

# === KROK 3: Porovnanie obdobia krizy a po krize ===
# Rozdelime tabulku na 2 casti podla stlpca crisis a v kazdej spocitame
# kliky za mesiac. Potom porovname, ci po krize ludia chodili na stranku
# viac alebo menej.
kriza = df[df["crisis"] == 1].groupby("mesiac").size()      # nechame len riadky z obdobia krizy a spocitame ich za mesiac
po_krize = df[df["crisis"] == 0].groupby("mesiac").size()   # to iste pre obdobie po krize
zmena_pct = (po_krize.mean() / kriza.mean() - 1) * 100      # o kolko percent narastol/klesol priemer po krize oproti krize

print(f"\n=== KRIZA vs PO KRIZE ===")
print(f"Pocas krizy: priemer {kriza.mean():.0f}/mesiac, celkom {kriza.sum():,}")   # {:,} = oddeluje tisicky ciarkou pre citatelnost
print(f"Po krize:    priemer {po_krize.mean():.0f}/mesiac, celkom {po_krize.sum():,}")
print(f"Zmena: {zmena_pct:+.1f}%")                          # {:+} = vzdy zobrazi znamienko + alebo -

# === KROK 4: Pristupy po kategoriach a kvartaloch ===
# Chceme vediet, ci napr. "hypoteky" maju iny casovy vzorec ako "ucty".
# Zoskupime data dvojnasobne (kvartal + kategoria), spocitame kliky a
# rozhodime tabulku tak, aby kazda kategoria mala vlastny stlpec.
# fill_value=0 = ak nejaka kategoria nebola v danom kvartali navstivena,
# dame tam 0 namiesto prazdnej hodnoty (graf by sa inak prerusil).
kat_v_case = df.groupby(["yearQuartal", "category"]).size().unstack(fill_value=0)

# === KROK 5: Vykreslenie 2 grafov nad sebou ===
fig, axes = plt.subplots(2, 1, figsize=(14, 10))            # 2 grafy pod sebou, siroka plocha pre dlhu casovu os

# Horny graf: mesacny vyvoj celkovej navstevnosti
mesacne.plot(ax=axes[0], color="steelblue", linewidth=2)    # modra ciara, hrubsia aby bola dobre vidno
axes[0].axvline(x=pd.Period("2010-12"), color="red", linestyle="--", label="Koniec krizy")  # cervena prerusovana ciara oznaci, kde sa kriza skoncila
axes[0].set_title("Mesacny pocet pristupov (2009-2012)")
axes[0].set_ylabel("Pocet pristupov")
axes[0].legend()
axes[0].grid(alpha=0.3)                                     # jemna mriezka v pozadi pre lahsie citanie hodnot

# Dolny graf: vyvoj jednotlivych kategorii v case
kat_v_case.plot(ax=axes[1], kind="line", marker="o", linewidth=2)  # ciara s bodkami, lebo kvartalov je malo a bodky pomahaju oku
axes[1].set_title("Vyvoj pristupov po kategoriach (kvartalne)")
axes[1].legend(loc="upper left", fontsize=8)                # mensie pismo v legende, lebo kategorii je vela
axes[1].grid(alpha=0.3)

plt.tight_layout()                                          # automaticky upravi rozostupy, aby sa titulky neprekryvali
plt.savefig("out/navstevnost.png", dpi=150)                 # ulozime obrazok v dobrej kvalite na prezentaciu

# Uloz aj samotne tabulky, ak ich budeme potrebovat pozriet rucne
mesacne.to_csv("out/mesacne_navstevy.csv", header=["pocet"])  # header=["pocet"] = pomenuje stlpec v CSV, inak by bol bezmenny
kat_v_case.to_csv("out/kategorie_v_case.csv")

print("\nGraf ulozeny -> out/navstevnost.png")
