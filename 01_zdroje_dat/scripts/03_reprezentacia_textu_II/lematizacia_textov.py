# ==========================================================
# CV1 - Uloha 03: Reprezentacia textu II - Lematizacia
# ==========================================================
#
# CIEL: Z anglickych textov vyrobime tabulku "ake slovo sa kolkokrat
# objavuje v ktorom dokumente". Tabulku potom prerobime na 4 verzie
# (rozne sposoby ako "vahovat" slova) — to potrebuju algoritmy strojoveho
# ucenia, lebo nevedia pracovat priamo s pismenkami, len s cislami.
#
# TEORIA (od nuly):
#
#   1) TOKENIZACIA (rozsekanie textu na kusky)
#   Pocitac dostane jeden dlhy retazec textu. Najprv ho musime rozdelit:
#     - na VETY (sentence tokenization) - nie len podla bodky, lebo bodka je aj
#       v skratkach ("Mr.", "U.S.A."); na to je sikovny model (Punkt),
#     - vetu na SLOVA (word tokenization). Jedno take slovo = TOKEN.
#
#   2) LEMATIZACIA (zjednotenie tvarov slova)
#   To iste slovo ma vela tvarov: "cat/cats", "run/running/ran". Pre analyzu
#   chceme, aby sa pocitali ako jedno. LEMA = zakladny slovnikovy tvar.
#   Lematizator ho najde v slovniku WordNet: "cats" -> "cat", "running" -> "run".
#   (STEMMING je lacnejsia alternativa - len odrezava koncovky podla pravidla,
#    napr. "running" -> "runn"; lematizacia je presnejsia, lebo pozna slovnik.)
#
#   3) VEKTOROVY MODEL (z textu cisla)
#   Aby sa dali dokumenty porovnavat, kazdy prerobime na VEKTOR cisel:
#   riadky = vsetky slova (lemy), ktore poznam; hodnota = kolkokrat je slovo
#   v dokumente. Tabulka slova x dokumenty = Vector Space Model.
#
#   4) VAHOVE SCHEMY (ten isty pocet sa da vyjadrit viacerymi sposobmi)
#       wf      = surovy pocet vyskytov,
#       binary  = bolo slovo v dokumente? 1 = ano, 0 = nie,
#       log     = 1 + log10(pocet); tlmi slova, co sa opakuju velakrat,
#       idf     = ako vzacne je slovo v celej kolekcii (vysvetlene nizsie).
#   IDF (inverse document frequency) = log10(N / df), N = pocet dokumentov,
#   df = v kolkych dokumentoch slovo je. Cim v menej dokumentoch, tym vyssia
#   IDF = slovo je "vzacne" a teda rozlisujuce (caste "the" ma IDF blizko 0).
#   Priklad: N=5, slovo v df=2 dok. -> idf=log10(5/2)=0.40; v 1 dok. -> log10(5)=0.70.
#
# VSTUP:  in/*.txt - 5 anglickych textovych suborov (kazdy = jeden dokument)
# VYSTUP: out/lemma_frekvencia.xlsx - 1 zosit, 4 harky (wf, binary, log, idf)
#
# POUZITE KNIZNICE:
#   - nltk    : kniznica pre spracovanie textu (delenie na vety/slova, lematizacia)
#   - WordNet : anglicky slovnik, podla ktoreho lematizator hada zakladne tvary
#   - numpy   : rychle pocty s polami cisel (logaritmy, podmieneny vyber)
#   - pandas  : tabulky (DataFrame) a ulozenie do Excelu
#   - os      : praca s cestami suborov tak, aby fungovala na Windows aj Linuxe
#
# ALGORITMUS: Nacitaj texty -> rozdel na vety -> rozdel na slova -> najdi
# zakladny tvar kazdeho slova -> spocitaj frekvencie -> odvod 3 dalsie verzie -> uloz.

import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))  # umoznuje spustenie skriptu odkialkolvek (nielen z jeho priecinka)

import numpy as np
import pandas as pd
import nltk
from nltk.tokenize import word_tokenize, sent_tokenize   # delenie textu na vety a vety na slova
from nltk.stem import WordNetLemmatizer                  # hlada zakladny tvar slova v slovniku WordNet

# === Stiahnutie pomocnych datasetov ===
# Tieto subory potrebuje nltk aby vedel co robi. Stiahne ich len raz,
# pri druhom spusteni iba overi, ze su uz na disku.
nltk.download('punkt_tab')                    # model na delenie textu na vety a slova
nltk.download('averaged_perceptron_tagger')   # rozpoznavac typu slova (podstatne meno, sloveso...)
nltk.download('stopwords')                    # zoznam beznych slov ("the", "is") - tu nepouzity
nltk.download('wordnet')                      # anglicky slovnik na hladanie zakladnych tvarov

# === Vytvorenie lematizatora ===
# Vytvorime ho RAZ pred slukou, aby sa nevyrabal znova pri kazdom slove (kvoli rychlosti).
# Pozn: bez urcenia typu slova vrati lematizator default ako podstatne meno,
# takze "running" zostane "running" namiesto "run". Pre tuto ulohu to staci.
lemmatizer = WordNetLemmatizer()

# === KROK 1: Najdeme vsetky textove subory ===
# sorted() zaruci, ze subory ideme vzdy v tom istom poradi - dolezite
# aby vystupna tabulka vyzerala rovnako pri kazdom spusteni.
# Filter na .txt vynecha pripadne pomocne subory v priecinku.
files = sorted(f for f in os.listdir("in") if f.endswith(".txt"))

# === KROK 2: Tokenizacia a lematizacia ===
# Pre kazdy dokument: rozsekneme text na vety, vety na slova, kazde slovo
# prerobime na zakladny tvar. Vysledok ulozime ako zoznam slov (s opakovaniami,
# lebo pocty spocitame az v dalsom kroku).
doc_lemmas = {}                                                     # mapa: nazov suboru -> zoznam zakladnych tvarov slov
for fname in files:
    with open(os.path.join("in", fname), encoding="utf-8") as f:    # utf-8 lebo web texty mozu mat aj specialne znaky
        data = f.read()                                             # nacitame cely subor naraz (subory su male)

    # Najprv text rozdelime na vety. Nemozeme len rozseknut podla bodky,
    # lebo bodka je aj v skratkach ("Mr.", "U.S.A."). Punkt model si s tym poradi.
    sentences = sent_tokenize(data)
    lemmas = []                                                     # tu nazbierame vsetky slova z tohto jedneho dokumentu
    for sentence in sentences:
        # Vetu rozdelime na slova. word_tokenize zachova kontrakcie ("don't")
        # a interpunkcia ide ako samostatny token.
        words = word_tokenize(sentence)
        for word in words:
            # .lower() = vsetko male pismo, aby "The" a "the" bolo to iste slovo.
            # lemmatize najde zakladny tvar v slovniku (napr. "cats" -> "cat").
            lemma = lemmatizer.lemmatize(word.lower())
            lemmas.append(lemma)                                    # pridame do zoznamu aj opakovania (pocty potrebujeme dalej)

    doc_lemmas[fname] = lemmas                                      # ulozime zoznam slov pre tento dokument

# === KROK 3: Zostavime tabulku poctov slov ===
# Riadky tabulky = vsetky unikatne slova z celeho korpusu.
# Stlpce = jednotlive dokumenty.
# V bunke = kolko krat sa to slovo objavilo v tom dokumente.

# Zoznam vsetkych UNIKATNYCH slov v korpuse (bez opakovani).
#   vnutorne "for lemmas in ... for l in lemmas" = prejdi vsetky dokumenty a v
#     kazdom vsetky slova (sploste do jedneho dlheho zoznamu),
#   dict.fromkeys(...) = vyhodi duplicity, ale ZACHOVA poradie prveho vyskytu
#     (obycajny set() by poradie premiesal).
all_lemmas = list(dict.fromkeys(l for lemmas in doc_lemmas.values() for l in lemmas))

# Vyrobime prazdnu tabulku samych nul, rozmer = (pocet slov) x (pocet dokumentov).
wf = pd.DataFrame(0, index=all_lemmas, columns=files)
for fname, lemmas in doc_lemmas.items():
    for lemma in lemmas:
        # Za kazde slovo pripocitame 1 v bunke [slovo, dokument].
        # .at[] je rychlejsi sposob ako pristupit k jednej konkretnej bunke.
        wf.at[lemma, fname] += 1

# === KROK 4: Odvodene reprezentacie (binarna, log, idf) ===

# BINARNA = staci nam vediet ci sa slovo v dokumente objavilo aspon raz.
# (wf > 0) vrati True/False, .astype(int) prerobi na 1/0.
binary = (wf > 0).astype(int)

# LOGARITMICKA = 1 + log10(pocet), ak pocet > 0; inak 0.
# Dovod: slovo s 100 vyskytmi nie je 100x dolezitejsie ako s 1 vyskytom,
# logaritmus tlmi tento rozdiel.
vals = wf.values.astype(float)                                       # cisla z tabulky ako pole float (kvoli log10)

# log10 pocitame len tam, kde je pocet > 0 (inak by log10(0) dal -nekonecno).
# Tam kde je 0, necha vystup 0.
log_wf = np.where(vals > 0, 1 + np.log10(vals, where=vals > 0, out=np.zeros_like(vals)), 0)
log_df = pd.DataFrame(np.round(log_wf, 4), index=wf.index, columns=wf.columns)  # zaokruhlime na 4 desatinne miesta

# IDF: meria "vzacnost" slova v celej kolekcii dokumentov.
N = len(files)                                                       # pocet dokumentov v korpuse

# doc_freq[i] = v kolkych dokumentoch sa i-te slovo objavilo (aspon raz).
# (vals > 0) je tabulka True/False (1=je, 0=nie je). Slova su tu v RIADKOCH a
# dokumenty v STLPCOCH, takze .sum(axis=1) scita pre kazdy riadok (slovo) hodnoty
# naprie vsetkymi stlpcami (dokumentmi) = v kolkych dokumentoch slovo je.
doc_freq = (vals > 0).sum(axis=1)

# idf = log10(N / df). Cim v menej dokumentoch slovo je, tym vyssia hodnota.
# np.where zabranuje deleniu nulou (ak by sa slovo neobjavilo nikde, pouzijeme 1).
# Priklad: N=5, df=2 -> log10(5/2)=0.40 (caste slovo); df=1 -> log10(5)=0.70 (vzacne).
idf = np.log10(N / np.where(doc_freq > 0, doc_freq, 1))

# === KROK 5: Ulozenie do Excelu (1 subor, 4 harky) ===
# "with" zaruci, ze sa subor korektne uzavrie aj keby nieco zlyhalo.
with pd.ExcelWriter("out/lemma_frekvencia.xlsx") as w:
    wf.to_excel(w, sheet_name="wf")          # surove pocty vyskytov
    binary.to_excel(w, sheet_name="binary")  # 0 / 1 (bolo / nebolo)
    log_df.to_excel(w, sheet_name="log")     # logaritmicka verzia poctov
    # Cista IDF: jeden stlpec s vahou pre kazde slovo (nezavisi od dokumentu).
    pd.DataFrame({"idf": np.round(idf, 4)}, index=wf.index).to_excel(w, sheet_name="idf")

# Kratky vypis aby sme videli ze pipeline dobehol a kolko slov sme spracovali.
print(f"Hotovo! Ulozene do out/lemma_frekvencia.xlsx")
print(f"Pocet lem: {len(all_lemmas)}")
print(f"Pocet dokumentov: {len(files)}")
