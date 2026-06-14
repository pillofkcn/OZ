# =============================================================================
# CV1 - Uloha 02: Reprezentacia textu I - vahove schemy
# =============================================================================
#
# CIEL: Mame tabulku, kde riadky su dokumenty a stlpce su slova. V bunke je
#   pocet, kolko raz sa slovo objavilo v dokumente. Tento "pocet" prerobime
#   na tri ine cisla, ktore sa lepsie hodia na porovnavanie dokumentov.
#
# TEORIA (od nuly - akoby si to nikdy nevidel):
#
#   1) PRECO TEXT PREVADZAME NA CISLA
#   Pocitac nevie porovnavat "slova", vie pocitat s cislami. Aby sme vedeli
#   povedat, ktore dokumenty su si podobne, musime kazdy dokument premenit na
#   rad cisel (vektor).
#
#   2) BAG-OF-WORDS A TABULKA DOKUMENTY x SLOVA
#   Najjednoduchsi model je "vrece slov" (bag-of-words): na poradi slov nezalezi,
#   zaujima nas len, ktore slova a kolkokrat su v dokumente. Z toho vznikne
#   tabulka: riadok = dokument, stlpec = slovo, bunka = pocet vyskytov. Kazdy
#   riadok je potom VEKTOR dokumentu (vektorovy model).
#
#   3) tf = TERM FREQUENCY (surovy pocet)
#   Cislo v bunke je tf = kolkokrat sa slovo objavilo v dokumente. Surove tf je
#   ale hrube: slovo "ten" je vsade a nic neprezradi, pritom ma velky pocet.
#   Preto tf prevadzame na rozumnejsie VAHY (vahove schemy):
#
#   - BINARNA: zaujima nas len "je tam slovo alebo nie" -> 1 alebo 0 (ignoruje pocet).
#   - LOGARITMICKA: tlmi velke pocty, lebo dolezitost nerastie linearne. Slovo
#     s tf=100 nema byt 100x dolezitejsie nez s tf=1. Vzorec: 1 + log10(tf)
#     (log tlmi: log10(10)=1, log10(100)=2; slovo s tf=1 dostane vahu 1, nie 0).
#   - IDF (inverzna dokumentova frekvencia): ako VZACNE je slovo v celej kolekcii.
#     Slovo v kazdom dokumente je nezaujimave (vaha ~0), slovo len v 1 dokumente
#     je specificke (vysoka vaha). Vzorec: log10(N / df_t), N = pocet dokumentov,
#     df_t = v kolkych dokumentoch sa slovo objavilo.
#   - TF-IDF: log-tf NASOBENE IDF. Slovo dostane vysoku vahu len ak je v dokumente
#     caste A ZAROVEN v celej kolekcii zriedkave = najlepsi rozlisovac dokumentov.
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

# Nacitame harok "wf". index_col=0 = prvy stlpec (nazvy dokumentov) pouzi ako
# popisky riadkov, nie ako data.
df = pd.read_excel("in/vektorova_reprezentacia.xlsx", sheet_name="wf", index_col=0)
N = len(df)                                   # N = pocet dokumentov (riadkov), ide do vzorca IDF
wf = df.values.astype(float)                  # cisla z tabulky ako numpy pole; float, aby log10 a delenie fungovali

# === KROK 2: Binarna reprezentacia ===

# (wf > 0) da pre kazdu bunku True/False (je tam slovo?), .astype(int) prevedie
# True->1, False->0. Vysledok: matica 1/0.
binary = (wf > 0).astype(int)

# === KROK 3: Logaritmicka frekvencia ===

# Chceme: ak je slovo v dokumente (tf>0), vaha = 1 + log10(tf), inak 0.
# Problem: log10(0) je minus nekonecno. Preto log10 ratame LEN tam, kde tf>0,
# inde necham 0. Rozklad zapisu:
#   np.log10(wf, where=wf>0, out=zeros) = log10 len pre bunky s tf>0, inde 0,
#   1 + ...                              = posun, aby slovo s tf=1 malo vahu 1,
#   np.where(wf>0, ..., 0)               = finalna poistka: kde nie je slovo, daj 0.
log_wf = np.where(wf > 0, 1 + np.log10(wf, where=wf > 0, out=np.zeros_like(wf)), 0)

# === KROK 4: IDF a TF-IDF ===

# df_t = v kolkych DOKUMENTOCH sa slovo objavilo. (wf>0) da maticu True/False,
# .sum(axis=0) scita po STLPCOCH (zhora dolu) = pocet dokumentov pre kazde slovo.
doc_freq = (wf > 0).sum(axis=0)
# IDF = log10(N / df_t). np.where(...>0, df_t, 1) je poistka proti deleniu nulou
# (ak by slovo nebolo nikde, namiesto 0 pouzijeme 1).
idf = np.log10(N / np.where(doc_freq > 0, doc_freq, 1))
# TF-IDF = log-tf * IDF. idf je rad cisel (jedno na slovo); numpy ho automaticky
# vynasobi s kazdym riadkom (broadcasting) -> kazda bunka log_wf sa nasobi IDF svojho slova.
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
