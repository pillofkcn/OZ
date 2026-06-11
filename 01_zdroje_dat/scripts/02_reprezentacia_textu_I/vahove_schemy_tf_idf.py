# =============================================================================
# CV1 - Uloha 02: Reprezentacia textu I - vahove schemy
# =============================================================================
#
# CIEL: Mame tabulku, kde riadky su dokumenty a stlpce su slova. V bunke je
#   pocet, kolko raz sa slovo objavilo v dokumente. Tento "pocet" prerobime
#   na tri ine cisla, ktore sa lepsie hodia na porovnavanie dokumentov.
#
# TEORIA (pre laika):
#   - Surovy pocet (tf = term frequency) hovori len "kolko raz tam to slovo je".
#     To je hrube: slovo "ten" je vsade, ale nic neprezradi.
#   - BINARNA schema: zaujima nas len "je tam slovo alebo nie" (1 alebo 0).
#     Najjednoduchsie, ignoruje pocet.
#   - LOGARITMICKA schema: tlmi velke pocty. Slovo s tf=100 nedostane 100x
#     vyssiu vahu nez slovo s tf=1, lebo dolezitost neresie linearne.
#     Vzorec: 1 + log10(tf). Slovo s tf=1 dostane vahu 1 (nie 0).
#   - IDF (inverzna dokumentova frekvencia): hovori, ako vzacne je slovo
#     v celej kolekcii. Slovo, ktore je v kazdom dokumente, je nezaujimave
#     (vaha blizko 0). Slovo, ktore je len v 1 dokumente, je velmi specificke
#     (vysoka vaha). Vzorec: log10(N / df_t), kde N je pocet dokumentov
#     a df_t je v kolkych dokumentoch sa slovo objavilo.
#   - TF-IDF: spojenie log-tf a IDF. Slovo dostane vysoku vahu len ak je
#     v dokumente caste, ale v celej kolekcii zriedkave (= dobry rozlisovac).
#
# VSTUP: in/vektorova_reprezentacia.xlsx, harok "wf" - tabulka dokumenty x slova
#        s poctom vyskytov (raw tf).
#
# VYSTUP: out/vektorova_reprezentacia.xlsx - 5 harkov:
#   wf     - povodna tabulka (kopia vstupu pre kontrolu)
#   binary - 1/0 ci je slovo v dokumente
#   log    - logaritmicky utlmena frekvencia
#   idf    - jeden stlpec, IDF hodnota pre kazde slovo
#   tf-idf - kombinacia log-tf * idf (najpouzivanejsia schema)
#
# POUZITE KNIZNICE:
#   pandas - praca s Excel tabulkami a pomenovanymi riadkami/stlpcami
#   numpy  - rychle pocitanie nad celou tabulkou naraz (bez cyklov)
#
# ALGORITMUS: nacitaj tabulku, sprav binary/log/idf/tf-idf, uloz do 5 harkov.
# =============================================================================

import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))  # umoznuje spustenie skriptu odkialkolvek (nielen z jeho priecinka)

import numpy as np
import pandas as pd

# === KROK 1: Nacitanie vstupnej tabulky ===

# nacitame harok "wf"; index_col=0 = prvy stlpec su nazvy dokumentov (riadkove popisky)
df = pd.read_excel("in/vektorova_reprezentacia.xlsx", sheet_name="wf", index_col=0)
N = len(df)                                   # pocet dokumentov (riadkov) - potrebujeme do vzorca IDF
wf = df.values.astype(float)                  # vytiahneme cisla ako numpy pole; float aby log10 a delenie fungovali

# === KROK 2: Binarna reprezentacia ===

# pre kazdu bunku: je tam slovo (>0)? Ano = 1, nie = 0.
binary = (wf > 0).astype(int)

# === KROK 3: Logaritmicka frekvencia ===

# Vzorec: ak je slovo v dokumente (tf>0), vaha = 1 + log10(tf), inak 0.
# Preco zlozity zapis: log10(0) je minus nekonecno, takze pocitame log10 LEN
# tam, kde je tf>0. Na ostatnych miestach necham nulu.
log_wf = np.where(wf > 0, 1 + np.log10(wf, where=wf > 0, out=np.zeros_like(wf)), 0)

# === KROK 4: IDF a TF-IDF ===

# Pre kazde slovo spocitame v kolkych dokumentoch sa objavilo (df_t).
# sum(axis=0) = scitanie po stlpcoch (dokumenty zhora dolu pre kazde slovo).
doc_freq = (wf > 0).sum(axis=0)
# IDF = log10(N / df_t). Ak by nahodou df_t=0, nahradime 1 aby sme nedelili nulou.
idf = np.log10(N / np.where(doc_freq > 0, doc_freq, 1))
# TF-IDF = log-tf nasobene IDF. numpy automaticky nasobi kazdy riadok po stlpcoch.
tfidf = log_wf * idf

# === KROK 5: Zapis vsetkych harkov do jedneho Excel suboru ===

# ExcelWriter umoznuje zapisat viac harkov naraz; bez neho by sa kazdy zapis
# prepisoval a ostal by len posledny harok.
# Pri zapise obalujeme numpy polia do DataFrame s povodnym indexom a stlpcami,
# aby v Excel-i ostali nazvy dokumentov a slov (inak by bolo 0,1,2,...).
# np.round(..., 4) skrati desatinne miesta na 4 - citatelnejsie v Exceli.
with pd.ExcelWriter("out/vektorova_reprezentacia.xlsx") as w:
    df.to_excel(w, sheet_name="wf")                                                                       # povodna tabulka pre kontrolu
    pd.DataFrame(binary, index=df.index, columns=df.columns).to_excel(w, sheet_name="binary")             # 1/0 ci je slovo v dokumente
    pd.DataFrame(np.round(log_wf, 4), index=df.index, columns=df.columns).to_excel(w, sheet_name="log")   # logaritmicky utlmena tf
    # harok idf: jeden stlpec s IDF hodnotou pre kazde slovo (slova su riadky)
    pd.DataFrame({"idf": np.round(idf, 4)}, index=df.columns).to_excel(w, sheet_name="idf")
    pd.DataFrame(np.round(tfidf, 4), index=df.index, columns=df.columns).to_excel(w, sheet_name="tf-idf") # kombinacia log-tf * idf

# === Diagnosticky vypis ===

# kratke potvrdenie, ze skript dobehol a kolko mal dokumentov/slov
print("Hotovo! Vytvorene harky: wf, binary, log, idf, tf-idf")
print(f"Pocet dokumentov: {N}")
print(f"Pocet slov: {len(df.columns)}")
