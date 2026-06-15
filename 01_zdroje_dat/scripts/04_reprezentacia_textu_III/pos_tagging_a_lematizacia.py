# ==========================================================
# CV1 - Uloha 04: Reprezentacia textu III - morfologia (POS tagging + lematizacia)
# ==========================================================
#
# CIEL: Pre kazde slovo v texte zistit jeho slovny druh (podstatne meno,
# sloveso, ...) a zakladny tvar (lemma). Predtym sme so slovami pracovali
# len ako s "kuskami textu". Teraz pridavame gramaticku informaciu, ktora
# pomaha pri pokrocilejsej analyze (napr. vybrat len podstatne mena).
#
# TEORIA (od nuly):
#
#   1) MORFOLOGIA A POS TAGGING
#   Morfologia = gramaticka informacia o slove (akeho je druhu, v akom tvare).
#   POS tagging ("part of speech" = slovny druh) kazdemu slovu prideli druh:
#   podstatne meno (NN), sloveso (VB), pridavne meno (JJ), prislovka (RB)...
#   Su to znacky tzv. Penn Treebank tagsetu (NN, NNS, VBG, JJR...) - prve
#   pismeno hovori hrubu kategoriu (N/V/J/R).
#
#   2) PRECO TAGGER POTREBUJE KONTEXT
#   Rovnake slovo moze byt rozny druh: "lead" je kov (podstatne meno) aj "viest"
#   (sloveso). Tagger preto pozera CELU vetu (susedne slova), nie slovo samo.
#   Dolezity dosledok: tagujeme PRED vyhadzovanim slov, aby mal tagger plnu vetu.
#
#   3) LEMMA (zakladny tvar)
#   Lemma = slovnikovy tvar slova: "running" -> "run", "cats" -> "cat",
#   "better" -> "good". Spaja rozne tvary toho isteho slova do jedneho.
#   WordNet (anglicky slovnik) pozna len 4 kategorie: noun (n), verb (v),
#   adjective (a), adverb (r) - preto detailny POS tag (VBG, JJR...) musime
#   preklopit na jedno z tychto 4 pismen, inak by lematizacia nebola presna.
#
#   4) STOP SLOVA
#   Velmi caste slova takmer bez vyznamu pre analyzu (the, is, on). Vyhadzujeme
#   ich, lebo by len zaplnali tabulku a nic nerozlisuju.
#
# VSTUP:  in/*.txt - 5 anglickych textovych suborov (z predoslych cviceni)
# VYSTUP: out/identifikacia.xlsx - tabulka so stlpcami:
#         Subor, ID_veta, Slovo, Tag, Lemma, Poradie, Slovny_Druh
#         Dvojica (Subor, ID_veta) jednoznacne identifikuje vetu.
#
# POUZITE KNIZNICE:
#   - nltk       - hotove nastroje na anglictinu (delic viet, POS tagger, slovnik)
#   - pandas     - tabulkove data + export do Excelu
#   - string     - obsahuje znak po znaku zoznam interpunkcie (! " # $ % ...)
#   - os         - praca s priecinkami a cestami
#
# ALGORITMUS: Pre kazdy subor: rozdel na vety -> kazdu vetu na slova ->
# uhadni slovne druhy -> vyhod interpunkciu a stop slova -> lematizuj
# -> pridaj riadok do tabulky -> uloz do Excelu.
# ==========================================================

import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))  # umoznuje spustenie skriptu odkialkolvek (nielen z jeho priecinka)

import os              # praca s priecinkami a nazvami suborov
import string          # string.punctuation = retazec vsetkych interpunkcnych znakov
import pandas as pd    # tabulky + export do Excelu
import nltk            # hlavna NLP kniznica pre anglictinu
from nltk.corpus import stopwords           # zoznam beznych "vyplnovych" slov (the, is, on)
from nltk.tokenize import word_tokenize, sent_tokenize  # delice na slova a vety
from nltk.stem import WordNetLemmatizer     # hladac zakladneho tvaru slova

# === KROK 0: Stiahnutie modelov ===
# Pri prvom spusteni si stiahne potrebne data; potom uz len overi cache.
nltk.download('punkt_tab')                          # model na delenie viet a slov
nltk.download('averaged_perceptron_tagger')         # POS tagger (starsi nazov)
nltk.download('averaged_perceptron_tagger_eng')     # POS tagger (novsi nazov pre AJ)
nltk.download('stopwords')                          # zoznamy stop slov pre rozne jazyky
nltk.download('wordnet')                            # slovnik na hladanie zakladnych tvarov

# Mnozinu pouzivame preto, ze hladanie "je tam toto slovo?" je v nej velmi rychle.
stop_words = set(stopwords.words('english'))
# Lemmatizer si raz nacita slovnik a potom ho pouzivame opakovane.
lemmatizer = WordNetLemmatizer()


def get_wordnet_pos(treebank_tag):
    """Preklopi detailny POS tag (napr. VBG, JJR) na jedno pismeno pre WordNet.

    WordNet pozna len 4 kategorie: n (podst. meno), v (sloveso),
    a (pridavne meno), r (prislovka). POS tagger ale vrati tag ako "VBG"
    alebo "JJR". Tu len pozrieme prve pismeno a vyberieme spravnu kategoriu.
    Ak slovo nepatri do tychto 4 (napr. spojka, predlozka), vratime "n"
    ako bezpecnu volbu - slovnik ho v takom pripade neupravi.
    """
    if treebank_tag.startswith('V'):
        return 'v'   # sloveso
    if treebank_tag.startswith('J'):
        return 'a'   # pridavne meno
    if treebank_tag.startswith('R'):
        return 'r'   # prislovka
    return 'n'       # podstatne meno (a vsetko ostatne ako bezpecna volba)

# === KROK 1: Najst vstupne subory ===
# sorted() = vzdy rovnake poradie suborov bez ohladu na operacny system.
# Filter .txt vyhodi napr. .gitkeep alebo ine pomocne subory.
files = sorted(f for f in os.listdir("in") if f.endswith(".txt"))

# Zoznam slovnikov - kazdy slovnik bude jeden riadok finalnej tabulky.
# Naplname ho postupne a az na konci z neho spravime DataFrame (je to rychlejsie
# ako pridavat riadky do tabulky jeden po druhom).
rows = []

# === KROK 2: Spracovanie kazdeho suboru ===
for fname in files:
    # encoding="utf-8" je dolezite na Windows, inak by mohli specialne znaky zlyhat.
    with open(os.path.join("in", fname), encoding="utf-8") as f:
        data = f.read()  # nacitame cely subor ako jeden retazec

    # --- Rozdelenie textu na vety ---
    # sent_tokenize nehlada len bodku - pozna skratky ("Dr. Smith" nie je koniec vety).
    sentences = sent_tokenize(data)

    # enumerate(..., 1) = cislujeme vety od 1 (citatelnejsie pre cloveka ako od 0).
    for sent_id, sentence in enumerate(sentences, 1):
        # word_tokenize oddeli interpunkciu od slov ("Hello," -> ["Hello", ","])
        # a rozdeli skratene tvary ("don't" -> ["do", "n't"]).
        words = word_tokenize(sentence)

        # --- POS tagging ---
        # Tagger pozre cele slova vo vete a kazdemu prideli slovny druh.
        # DOLEZITE: tagujeme PRED filtrovanim - tagger potrebuje plnu vetu vratane
        # stop slov a interpunkcie, aby mal kontext na rozhodovanie.
        # Vystup je zoznam dvojic: [("The","DT"), ("cat","NN"), ("sat","VBD")]
        tagged = nltk.pos_tag(words)

        # Pocitadlo poradia slov vo vete - zacina od 0 a zvysuje sa az ked
        # slovo prejde filtrami (cize cislujeme len slova ktore ostali).
        poradie = 0

        for word, tag in tagged:

            # --- Filter 1: vyhodit interpunkciu ---
            # Skontrolujeme, ci sa cely token sklada len z interpunkcnych znakov.
            # Toto chyti aj viacznakove tokeny ako "``", "''", "--", "...".
            if all(c in string.punctuation for c in word):
                continue
            # --- Filter 2: vyhodit stop slova ---
            # .lower() lebo zoznam stop slov je cely malymi pismenami,
            # inak by sa "The" na zaciatku vety nevyhodilo.
            if word.lower() in stop_words:
                continue

            # Slovo preslo filtrami, ide do vystupu - zvysime pocitadlo poradia.
            poradie += 1

            # --- Lematizacia ---
            # Slovnik vrati zakladny tvar slova. Argument pos= mu povie, ci hladat
            # ako sloveso/podstatne meno/atd. - bez toho by "using" ostalo "using",
            # s tym dostaneme "use". word.lower() = "Cats" aj "cats" -> "cat".
            lemma = lemmatizer.lemmatize(word.lower(), pos=get_wordnet_pos(tag))

            # --- Zostavenie riadku tabulky ---
            # POZOR na stlpec "Slovny_Druh": je to PRVE PISMENO Penn tagu (tag[0]),
            # cize hruba kategoria v znaceni Penn Treebank:
            #     N = podstatne meno, V = sloveso, J = pridavne meno, R = prislovka.
            # Preto pri pridavnom mene vidno "J" (z tagu "JJ"), NIE "A".
            # Pismeno "a" patri inemu znaceniu - WordNet (n/v/a/r) - a pouziva sa
            # len vnutri lematizacie (get_wordnet_pos -> argument pos=), do tabulky
            # sa nezapisuje. Su to teda dve rozne znacenia, kazde s vlastnym pismenom.
            rows.append({
                "Subor": fname,            # z ktoreho suboru slovo pochadza
                "ID_veta": sent_id,        # cislo vety v ramci tohto suboru
                "Slovo": word,             # povodne slovo z textu
                "Tag": tag,                # detailny POS tag (napr. "VBG", "NNS")
                "Lemma": lemma,            # zakladny tvar slova
                "Poradie": poradie,        # poradie slova vo vete (po filtracii)
                "Slovny_Druh": tag[0],     # prve pismeno Penn tagu = hruba kategoria N/V/J/R
            })

# === KROK 3: Ulozenie tabulky do Excelu ===
# Z listu slovnikov vznikne DataFrame; stlpce idu v poradi klucov zo slovnika.
df = pd.DataFrame(rows)
# index=False = nezapise riadkove cisla 0,1,2... do Excelu (su zbytocne).
df.to_excel("out/identifikacia.xlsx", index=False)

# Kontrolny vypis - kolko slov sme nakoniec ulozili.
print(f"Hotovo! Ulozene do out/identifikacia.xlsx")
print(f"Celkovy pocet slov: {len(rows)}")
