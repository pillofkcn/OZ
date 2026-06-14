# ==========================================================
# CV5 - Uloha 02: Ako sa menila navstevnost banky v case
# ==========================================================
#
# CIEL:
#   Pozriet sa, ako sa pocas rokov 2009-2012 menil pocet pristupov na
#   stranky banky. Zaroven porovnat obdobie krizy vs po krize a sledovat,
#   ake kategorie obsahu (napr. ucty, uvery) ludia navstevovali kedy.
#
# TEORIA (od nuly - akoby si to nikdy nevidel):
#
#   1) JEDEN RIADOK = JEDNO OTVORENIE STRANKY
#   Log je zoznam pristupov. Kazdy riadok znamena, ze niekto v danom case
#   otvoril jednu stranku. Sam o sebe jeden riadok nehovori nic; sila je v
#   tom, ked ich SPOCITAME.
#
#   2) CASOVA AGREGACIA (z jednotlivych klikov spravime "navstevnost")
#   Agregovat = poskladat vela drobnych zaznamov do jedneho cisla. Ked vsetky
#   kliky roztriedime podla mesiaca a v kazdom mesiaci ich spocitame,
#   dostaneme pre kazdy mesiac jedno cislo = kolko pristupov v nom bolo.
#   Tomuto sa hovori "navstevnost za mesiac".
#
#   3) CASOVY RAD
#   Ked tie mesacne cisla zoradime za sebou v case (jan 2009, feb 2009, ...),
#   vznikne CASOVY RAD - postupnost hodnot v case. Nakresleny ako ciara hned
#   ukaze trend: rastie navstevnost, klesa, ma sezonne vlny?
#
#   4) PRIZNAK "crisis" (0/1)
#   Priznak = stlpec, ktory iba odlisuje dve situacie. Tu: crisis = 1 znamena
#   "pristup spada do obdobia financnej krizy" (zhruba do konca roku 2010),
#   crisis = 0 = "uz po krize". Rozdelenim dat podla neho vieme porovnat,
#   ci sa po krize chodilo na stranku viac alebo menej.
#
#   5) KONTINGENCNA TABULKA cez pivot / unstack (kategorie v case)
#   Chceme vidiet dve veci naraz: KEDY (kvartal) a CO (kategoria). Najprv
#   data zoskupime podla oboch a spocitame kliky. Vznikne "dlha" tabulka
#   (kvartal, kategoria, pocet). Funkcia unstack ju "rozhodi" na sirku: kazda
#   kategoria dostane vlastny stlpec, riadky su kvartaly. Takto sa daju
#   jednotlive kategorie pohodlne vykreslit ako samostatne ciary.
#
# VSTUP:
#   in/logs5.csv - POSKYTNUTY bankovy dataset (zo studie v materials/), CSV s ';'.
#                  Nie je to vystup tvojich cv1-4; stlpce length/frame/anonIP/
#                  unixTime zodpovedaju Length/SESSION_ID/USER_ID/UNIXTIME z cv1-4.
#                  Tu pouzivame najma: time (datum), category, crisis, yearQuartal.
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
# Nacitame CSV; sep=";" lebo stlpce su oddelene bodkociarkou,
# low_memory=False = pandas precita cely subor naraz a spravne urci typy stlpcov.
df = pd.read_csv("in/logs5.csv", sep=";", quotechar='"', low_memory=False)
# Stlpec "time" je zatial len TEXT. to_datetime ho podla zadaneho formatu
# (den.mesiac.rok hodina:minuta:sekunda) prerobi na skutocny datum, s ktorym
# sa da pocitat. errors="coerce" = pokazeny riadok nezhodi skript, da prazdnu hodnotu.
df["datum"] = pd.to_datetime(df["time"], format="%d.%m.%Y %H:%M:%S", errors="coerce")
# Z datumu vezmeme len rok+mesiac (napr. 2010-05). to_period("M") = "zaokruhli
# na mesiac". Vdaka tomu vieme kazdy klik zaradit do jeho mesiaca.
df["mesiac"] = df["datum"].dt.to_period("M")

# === KROK 2: Pocet pristupov za kazdy mesiac ===
# groupby("mesiac") roztriedi kliky do skupin podla mesiaca, .size() spocita
# riadky v kazdej skupine. Vysledok: pre kazdy mesiac jedno cislo = navstevnost.
mesacne = df.groupby("mesiac").size()
print(f"\nMesacne navstevy:")
# idxmin()/idxmax() = ktory mesiac (index) ma najmensiu/najvacsiu hodnotu.
print(f"  Min: {mesacne.min()} ({mesacne.idxmin()})")        # najslabsi mesiac
print(f"  Max: {mesacne.max()} ({mesacne.idxmax()})")        # najsilnejsi mesiac
print(f"  Priemer: {mesacne.mean():.0f}")                    # priemer cez mesiace; :.0f = bez desatinnych miest

# === KROK 3: Porovnanie obdobia krizy a po krize ===
# Otazka: chodili ludia na stranku po krize viac alebo menej?
# df[df["crisis"] == 1] = vyber len riadky z obdobia krizy; potom rovnako
# ako v KROKu 2 spocitame kliky za mesiac. To iste pre po krize (crisis == 0).
kriza = df[df["crisis"] == 1].groupby("mesiac").size()
po_krize = df[df["crisis"] == 0].groupby("mesiac").size()
# Percentualna zmena priemernej mesacnej navstevnosti: (novy/stary - 1)*100.
# Vysledok +X% = narast po krize, -X% = pokles.
zmena_pct = (po_krize.mean() / kriza.mean() - 1) * 100

print(f"\n=== KRIZA vs PO KRIZE ===")
# :, = oddeli tisicky (1,234,567) pre citatelnost; :.0f = bez desatinnych miest.
print(f"Pocas krizy: priemer {kriza.mean():.0f}/mesiac, celkom {kriza.sum():,}")
print(f"Po krize:    priemer {po_krize.mean():.0f}/mesiac, celkom {po_krize.sum():,}")
print(f"Zmena: {zmena_pct:+.1f}%")                          # :+ = vzdy ukaz znamienko (+ aj -)

# === KROK 4: Pristupy po kategoriach a kvartaloch ===
# Chceme vediet, ci ma napr. "hypoteky" iny casovy vyvoj ako "ucty".
# groupby(["yearQuartal","category"]).size() = spocita kliky pre kazdu dvojicu
# (kvartal, kategoria). unstack() potom "rozhodi" kategorie do stlpcov, takze
# riadok = kvartal, stlpec = kategoria (vhodne na vykreslenie ciar).
# fill_value=0 = chybajucu kombinaciu (kategoria v kvartali nebola) vyplni 0,
# inak by v grafe vznikla diera.
kat_v_case = df.groupby(["yearQuartal", "category"]).size().unstack(fill_value=0)

# === KROK 5: Vykreslenie 2 grafov nad sebou ===
# subplots(2, 1) = 2 grafy pod sebou (2 riadky, 1 stlpec). axes[0] = horny, axes[1] = dolny.
fig, axes = plt.subplots(2, 1, figsize=(14, 10))

# Horny graf: mesacny vyvoj celkovej navstevnosti (casovy rad).
mesacne.plot(ax=axes[0], color="steelblue", linewidth=2)    # modra ciara, hrubsia pre citatelnost
# axvline = zvisla ciara; oznaci koniec krizy (12/2010), aby bolo vidno predel.
axes[0].axvline(x=pd.Period("2010-12"), color="red", linestyle="--", label="Koniec krizy")
axes[0].set_title("Mesacny pocet pristupov (2009-2012)")
axes[0].set_ylabel("Pocet pristupov")
axes[0].legend()                                            # zobrazi vysvetlivku k ciaram (popisky z "label")
axes[0].grid(alpha=0.3)                                     # jemna mriezka v pozadi; alpha=0.3 = slabo viditelna

# Dolny graf: vyvoj jednotlivych kategorii v case (kazda kategoria vlastna ciara).
# marker="o" = na kazdy kvartal da bodku (kvartalov je malo, bodky pomahaju oku).
kat_v_case.plot(ax=axes[1], kind="line", marker="o", linewidth=2)
axes[1].set_title("Vyvoj pristupov po kategoriach (kvartalne)")
axes[1].legend(loc="upper left", fontsize=8)                # legenda vlavo hore, mensie pismo (kategorii je vela)
axes[1].grid(alpha=0.3)

plt.tight_layout()                                          # doladi rozostupy, aby sa titulky neprekryvali
plt.savefig("out/navstevnost.png", dpi=150)                 # uloz obrazok; dpi=150 = vyssia kvalita

# Ulozime aj samotne tabulky do CSV, keby sme do nich chceli pozriet rucne.
# header=["pocet"] pomenuje jediny datovy stlpec (inak by ostal bez nazvu).
mesacne.to_csv("out/mesacne_navstevy.csv", header=["pocet"])
kat_v_case.to_csv("out/kategorie_v_case.csv")

print("\nGraf ulozeny -> out/navstevnost.png")
