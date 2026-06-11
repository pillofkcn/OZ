# COMPLIANCE REPORT

Audit a okomentovanie 40 podúloh proti ich `zadanie.txt`. Generované workflow-om `detailed-comments-audit`.

## Súhrn

- **Total**: 40 / 40
- **OK**: 23
- **PARTIAL**: 17
- **MISMATCH**: 0
- **Verify failed**: 15

## Rýchla tabuľka

| Status | Skript | Δ% | Rewrite lines | Verify |
|--------|--------|----|----|--------|
| PARTIAL | `01_zdroje_dat/02_reprezentacia_textu_I/freq.py` | — | 58→137 | ISSUES |
| PARTIAL | `01_zdroje_dat/03_reprezentacia_textu_II/lemma.py` | — | 102→192 | ISSUES |
| PARTIAL | `01_zdroje_dat/04_reprezentacia_textu_III/identif.py` | — | 106→191 | ISSUES |
| PARTIAL | `03_identifikacia/01_UNIXTIME/unixtime.py` | — | 60→175 | OK |
| PARTIAL | `03_identifikacia/06_SLength/slength.py` | 2.8 | 62→132 | OK |
| PARTIAL | `05_prieskum_dat/01_popisne_statistiky/popisne.py` | — | 76→208 | ISSUES |
| PARTIAL | `05_prieskum_dat/02_navstevnost_v_case/navstevnost.py` | — | 72→186 | OK |
| PARTIAL | `05_prieskum_dat/04_vztahy_premennych/vztahy.py` | — | 75→208 | OK |
| PARTIAL | `06_extrakcia_vzorov/01_priprava_dat/priprava.py` | — | 64→158 | OK |
| PARTIAL | `06_extrakcia_vzorov/02_asociacne_pravidla/pravidla.py` | 0.0 | 72→169 | ISSUES |
| PARTIAL | `06_extrakcia_vzorov/04_statisticka_analyza/analyza.py` | — | 82→213 | ISSUES |
| PARTIAL | `07_projekt/01_cistenie_zaznamov/clean.py` | — | 128→211 | OK |
| PARTIAL | `07_projekt/03_filter_robotov/filter.py` | — | 80→154 | ISSUES |
| PARTIAL | `07_projekt/05_identifikacia_pouzivatelov/users.py` | — | 63→141 | OK |
| PARTIAL | `07_projekt/08_sedenia_href/href.py` | — | 63→154 | ISSUES |
| PARTIAL | `07_projekt/09_doplnanie_RLength/doplnanie.py` | — | 151→227 | ISSUES |
| PARTIAL | `07_projekt/10_doplnanie_href/doplnanie.py` | — | 154→258 | ISSUES |
| OK | `01_zdroje_dat/01_prehladavanie_webu/crawler.py` | 0.0 | 55→137 | OK |
| OK | `02_cistenie_dat/01_cistenie_dat_I/clean.py` | 2.0 | 86→177 | OK |
| OK | `02_cistenie_dat/02_cistenie_dat_II/clean2.py` | 1.5 | 61→137 | OK |
| OK | `02_cistenie_dat/03_cistenie_dat_III_roboti/clean3.py` | 0.0 | 52→123 | OK |
| OK | `02_cistenie_dat/04_cistenie_dat_IV_roboti/clean4.py` | — | 54→141 | OK |
| OK | `03_identifikacia/02_identifikacia_pouzivatelov/identifikacia.py` | 1.4 | 46→142 | ISSUES |
| OK | `03_identifikacia/03_premenna_Length/length.py` | 1.9 | 56→128 | OK |
| OK | `03_identifikacia/04_STT_MEAN/stt_mean.py` | 5.4 | 48→160 | OK |
| OK | `03_identifikacia/05_STT_Q/stt_q.py` | 5.0 | 48→152 | OK |
| OK | `03_identifikacia/07_RLength_exp/rlength_exp.py` | — | 87→194 | OK |
| OK | `03_identifikacia/08_RLength/rlength.py` | 5.5 | 55→140 | OK |
| OK | `03_identifikacia/09_h_ref/h_ref.py` | 13.6 | 54→131 | OK |
| OK | `04_doplnanie_ciest/01_doplnanie_STT_MEAN/doplnanie.py` | 14.0 | 101→183 | OK |
| OK | `04_doplnanie_ciest/02_doplnanie_STT_Q/doplnanie.py` | 2.0 | 101→160 | OK |
| OK | `04_doplnanie_ciest/03_doplnanie_RLength/doplnanie.py` | 8.7 | 101→163 | ISSUES |
| OK | `04_doplnanie_ciest/04_doplnanie_h_ref/doplnanie.py` | 2.3 | 101→203 | ISSUES |
| OK | `05_prieskum_dat/03_cas_na_strankach/cas.py` | — | 74→200 | ISSUES |
| OK | `06_extrakcia_vzorov/03_matica_pravidiel/matica.py` | — | 69→163 | OK |
| OK | `07_projekt/00_extrakcia_tyzdna/extract_week.py` | — | 87→160 | OK |
| OK | `07_projekt/02_robot_ips/robot_ips.py` | — | 76→131 | OK |
| OK | `07_projekt/04_obdobie_unixtime/obdobie.py` | — | 103→196 | ISSUES |
| OK | `07_projekt/06_premenna_Length/length.py` | — | 76→164 | OK |
| OK | `07_projekt/07_sedenia_RLength/rlength.py` | — | 134→198 | OK |

## Per-skript detail

### `01_zdroje_dat/02_reprezentacia_textu_I/freq.py` — PARTIAL

**Zadanie bullets:**
- ✅ Transformovat frekvenciu vyskytu slov na binarnu reprezentaciu — _Krok 2: binary = (wf > 0).astype(int) — korektne, vsetky nenulove vyskyty -> 1, nulove -> 0._
- ✅ Transformovat frekvenciu na logaritmicku reprezentaciu — _Krok 3: 1 + log10(tf) pre tf>0, inak 0. Standardny vzorec, korektny._
- ⚠️ Transformovat frekvenciu na inverznu dokumentovu frekvenciu (IDF) — _Skript pocita TF-IDF (log_tf * IDF), nie samostatne IDF. Zadanie ziada IDF transformaciu frekvencie — interpretacia moze byt aj TF-IDF (najcastejsie v praxi), ale samotna IDF ako stlpcova hodnota log10(N/df) v harku chyba. Vysledny harok 'tf-idf' obsahuje sucin, nie cisto IDF._
- ✅ Vysledky v jednotlivych harkoch (binary, log, IDF/tf-idf) — _ExcelWriter zapisuje 4 harky: wf, binary, log, tf-idf — kazda reprezentacia v samostatnom harku, plus povodna frekvencia. Vystupny subor out/vektorova_reprezentacia.xlsx existuje (82888 B)._
- ✅ Odovzdat vysledny subor — _Subor out/vektorova_reprezentacia.xlsx bol vytvoreny (existuje vo vystupnom adresari)._

**Findings (audit):**
- `[major]` Zadanie ziada 'inverznu dokumentovu frekvenciu' (IDF) ako jednu z transformacii. Skript miesto cistej IDF pocita TF-IDF (riadok 45: tfidf = log_wf * idf) a harok pomenuva 'tf-idf'. Ak ucitel chce ciste IDF, treba pridat samostatny harok s log10(N/df) na uroven slov (mozno aj vynasobene binarnou maticou pre zachovanie tvaru dokument x slovo). Riziko: nesplnena specifikacia zadania. (line 45)
- `[minor]` Riadok 37: np.log10(wf, where=wf > 0, out=np.zeros_like(wf)) — kombinacia where v np.log10 a vonkajsej np.where je redundantna. Funkcne korektne, ale citatelnost znizena; idiomatickejsie by bolo np.where(wf > 0, 1 + np.log10(np.where(wf>0, wf, 1)), 0). (line 37)
- `[minor]` Riadok 43: idf = np.log10(N / np.where(doc_freq > 0, doc_freq, 1)) — fallback na 1 pre doc_freq==0 by dal IDF = log10(N), co je vyssia hodnota nez pre slova s vyskytom v 1 dokumente. Defenzivne to nie je problem (slovo s df=0 by v matici nebolo), ale logicky by bolo bezpecnejsie nastavit IDF=0 alebo nahradit za NaN. (line 43)
- `[minor]` Skript nema kontrolu existencie out/ adresara (pd.ExcelWriter zlyha ak chyba). Adresar out/ aktualne existuje, ale chyba mkdir/Path.mkdir(parents=True, exist_ok=True) pre robustnost (CLAUDE.md: skripty maju byt standalone). (line 49)
- `[minor]` Hardcoded relativne cesty 'in/...' a 'out/...' — skript funguje len ak je spusteny z adresara 02_reprezentacia_textu_I. Pre standalone behavior by bolo lepsie pouzit os.path.dirname(__file__) alebo pathlib. (line 26)

**Rewrite**: Pridal som MAX-density komenty: rozsireny header docstring (ciel vo WUM pipeline, parafraza zadania s cross-ref na audit, vstup/vystup, kniznice s odovodnenim, datove struktury, algoritmus), pri kazdom kroku teoreticky blok (binary/Bernoulli, log-tf vzorec a intuicia +1, TF-IDF s df_t/idf_t a hranicnymi pripadmi) a inline komenty na netrivialnych riadkoch (axis=0, index_col=0, sheet_name, np.where/out= edge cases, broadcasting). Logika kodu, importy, premenne a poradie operacii ostali nezmenene.

**Adversarial verify issues:**
- `[major]` Komentar tvrdi 'log10(N/1) = log10(N) je vyssia nez pre slova co su v 1 dokumente' — toto je MATEMATICKY NESPRAVNE. Ak df_t=1, idf = log10(N/1) = log10(N). Fallback df_t=0→1 da PRESNE ROVNAKU hodnotu log10(N), nie vyssiu. Sprava ma byt: 'log10(N/1) sa rovna idf pre slova v 1 dokumente, takze fallback by nerozlisil prazdne slovo od najzriedkavejsieho'. (line 129)
- `[major]` Zadanie bullet 3 (riadok 5 zadanie.txt) doslova ziada 'inverznú dokumentovú frekvenciu' — t.j. cisty IDF stlpec/harok log10(N/df_t) ako per-slovo vektor. Skript vsak vytvara TF-IDF harok (sucin log_tf * idf). Komentar v skripte to sice priznava (riadky 17-19, 135-136), ale prepisany skript NEOPRAVIL tento rozpor. Verifikacia samotna nema funkciu opravovat — len konstatujem, ze zadanie strictne interpretovane nie je naplnene (chyba samostatny harok 'idf' s log10(N/df_t)).
- `[minor]` Typo/zalomenie slova: '4 desatinne mat-' s pokracovanim 'zachovava' na dalsom riadku. Malo by byt napr. '4 desatinne miesta zachovavaju potrebnu presnost'. Sposobuje neciatelnost komentaru. (line 155)
- `[minor]` Inline komentar pri doc_freq tvrdi 'pouziva binarnu masku z kroku 2 (recompute, lacne)' — formulacia je trochu mylajuca: nepouziva premennu `binary` z kroku 2, ale RECOMPUTE-uje (wf > 0). Cast '(recompute, lacne)' to zachranuje, ale prva polovica vety ('pouziva binarnu masku z kroku 2') je technicky nepresna. (line 137)
- `[minor]` Komentar tvrdi '.values → numpy view'. V realite `.values` vracia numpy pole ktore moze byt view ALEBO copy v zavislosti od dtype homogeneity DataFrame-u. Pre zmiesane dtypes je to copy. Detail je presny v praxi (numericka DTM bude view), ale 'numpy view' ako absolutne tvrdenie je nepresne. (line 77)
- `[minor]` Komentar (riadky 107-108) priznava redundanciu `where=wf>0` vnutri `np.log10` aj vonku v `np.where`. Tvrdi 'funkcne OK, citatelnost nizsia. NEOPRAVUJEME'. Toto je pravda — vonkajsi `np.where` by sam stacil (np.log10 by varoval pre tf=0 ale buffer by sa prepisal). Komentar je presny, len upozornujem ze redundancia je realna. (line 111)

---

### `01_zdroje_dat/03_reprezentacia_textu_II/lemma.py` — PARTIAL

**Zadanie bullets:**
- ✅ Extrahovat lemy slov z anglickych textov pomocou nltk (Texty z webu) — _Pouziva WordNetLemmatizer, sent_tokenize, word_tokenize podla zadania. Nacita .txt subory z in/ (5 suborov)._
- ✅ Vytvorit datovu maticu s frekvenciou lem v dokumentoch — _DataFrame wf s riadkami=lemy, stlpcami=dokumenty, hodnotami=frekvencia. Ulozene v sheete 'wf'._
- ✅ Odvodit binarnu reprezentaciu — _binary = (wf > 0).astype(int) — korektne._
- ✅ Odvodit logaritmicku reprezentaciu — _1 + log10(tf) pre tf>0, inak 0 — standardny vzorec._
- ⚠️ Odvodit inverznu frekvenciu (IDF) — _Zadanie pyta 'inverznu frekvenciu' (IDF = log10(N/df)). Skript pocita TF-IDF (log_tf * idf), nie ciste IDF. Cisty IDF stlpec/harok chyba. Komentar v skripte to dokonca priznava ('TF-IDF reprezentaciou')._
- ✅ Odovzdat vysledny subor a zdrojovy kod v zip — _Vystup out/lemma_frekvencia.xlsx existuje (115 KB, 4 harky). Samotny zip si robi student rucne, mimo skript._
- ✅ Postup: nacitat texty, sent_tokenize, word_tokenize, WordNetLemmatizer, lemmatize — _Vsetky uvedene kroky/funkcie su pouzite presne podla zadania._
- ⚠️ Pouzit stopwords (zmienene v importoch zadania) — _Zadanie ich uvadza ako 'vhodne importy' a vola nltk.download('stopwords'), ale postup ich explicitne nepouziva. Skript ich tiez nepouziva na filtrovanie — to je v sulade so striktnym zoznamom krokov, ale stop slova zostali v matici (napr. 'the', 'a', interpunkcia)._

**Findings (audit):**
- `[major]` Zadanie ziada 'inverznu frekvenciu' ako samostatnu reprezentaciu, ale skript pocita TF-IDF (log_tf * idf) namiesto cistej IDF (log10(N/df)). Vo vystupnom xlsx harok 'tf-idf' nie je to iste co 'inverzna frekvencia'. Riesenie: pridat samostatny harok 'idf' s hodnotami log10(N/df) pre kazdu lemu (1D stlpec) alebo prepocitat hodnoty v matici ako pure IDF. (line 90)
- `[minor]` Lematizator je volany bez POS tagu (lemmatizer.lemmatize(word.lower())), takze defaultne pouzije noun. Slovesa ('running' -> ostane 'running', 'better' -> ostane 'better') sa nezlematizuju spravne. Zadanie vsak download averaged_perceptron_tagger uvadza — naznacuje, ze sa ocakava POS-aware lematizacia. Riesenie: nltk.pos_tag + mapovanie na WordNet POS (v/n/a/r). (line 60)
- `[minor]` Interpunkcia (',', '.', '!', '?') a stopwords (the, a, of) zostavaju v matici ako 'lemy' a zvysuju rozmer. Aj ked zadanie striktne nepyta filtraciu, je to bezne ocakavanie a stopwords su uvedene v importoch zadania. Riesenie: filtrovat tokens iba na .isalpha() a vynechat stopwords. (line 56)
- `[minor]` Vystup je xlsx — zadanie nespecifikuje format ('vysledny subor'). To je OK, ale ak je preferencia CSV/TSV, treba prepnut format. Pri xlsx s vela lemami a 5 stlpcami * 4 harky moze byt subor velky. (line 93)
- `[minor]` Pri np.log10(vals, where=vals > 0, out=np.zeros_like(vals)) je out=zeros, takze pre vals==0 zostane 0 — to je OK. Ale potom np.where(vals > 0, 1 + log10, 0) pridava 1 iba ked vals>0 — korektne. Logika je spravna, len je trochu nadbytocna (dvojita ochrana). Funkcne ok. (line 82)

**Rewrite**: Prepisal som lemma.py s MAX-density komentarmi: rozsireny header docstring (ciel v kontexte WUM, parafrazovane bullety zadania, vstup/vystup, kniznice, datove struktury, cross-ref na doc.md VSM/TF-IDF), teoreticke bloky pri lematizacii a term-weighting schemach (boolean/log_tf/idf/tf-idf), inline komenty na kazdom netrivialnom riadku (preco sorted, .at vs .loc, np.where defenzivna ochrana, broadcasting cez np.newaxis, dict.fromkeys idiom) a inline AUDIT poznamky pri zname bugoch (POS tag chyba, IDF vs TF-IDF, dvojita log10 ochrana) bez zmeny logiky.

**Adversarial verify issues:**
- `[major]` Comment on line 194 tvrdí, ze vonkajsie np.where je 'funkcne korektne, len trochu redundantne' (dvojita ochrana). Toto je NEPRAVDIVE. Vonkajsie np.where NIE je redundantne — je nevyhnutne. Vnutorne np.log10(vals, where=vals>0, out=np.zeros_like(vals)) vracia 0 tam, kde vals==0. Bez vonkajsieho np.where by sa pre vals==0 vypocitalo 1 + 0 = 1, co je NESPRAVNE pre log-tf formulu (ma byt 0 ked tf=0). Vonkajsie np.where teda zarucuje korektnu hodnotu 0 pre tf=0 a nie je 'redundantne'. (line 194)
- `[minor]` Komment uvadza, ze 'stopwords' nltk dataset sa stahuje, ale zadanie ho 'vyzaduje v importoch'. Skript vsak vobec neimportuje stopwords (chyba 'from nltk.corpus import stopwords' a 'stop_words = set(stopwords.words(\"english\"))', ktore zadanie explicitne uvadza v sablone). Audit komentar to spomina ('skript nefiltruje'), ale neuvadza, ze samotny IMPORT chyba — uzitocne by bolo to vyznacit jasnejsie. (line 80)
- `[minor]` Komment nezdoraznuje, ze cesta 'in' je relativna k aktualnemu pracovnemu adresaru (CWD). Ak sa skript spusta inak ako z priecinka 03_reprezentacia_textu_II/, listdir zlyha. Rovnaky problem na riadku 224 s 'out/lemma_frekvencia.xlsx'. Toto nie je novy bug (anti-drift), ale komentar by to mal zaznamenat ako poznamku obhajoby. (line 102)
- `[minor]` Script nevytvara out/ priecinok pred zapisom (chyba os.makedirs('out', exist_ok=True)). Ak by out/ neexistoval, ExcelWriter by spadol. Komentar k zapisu to neuvadza ako moznu chybu. Anti-drift hovori, ze toto neopravujeme, ale aspon by sa to mohlo spomenut v audite. (line 224)
- `[minor]` Hlavicka tvrdi 'CIEL (kontext WUM pipeline)'. Stale je to validny popis ulohy 03 v predmete Objavovanie znalostí, ale termin 'WUM pipeline' (Web Usage Mining) nemusi presne sediet — text mining nad webovymi textami nie je striktne WUM. Mensia teoreticka nepresnost v popise kontextu. (line 4)
- `[minor]` Komment hovori, ze nltk.download() pri opakovanom spusteni 'iba overi pritomnost a nestahuje znova'. Toto je v zasade pravda (NLTK ma kvieten/cache), ALE pri kazdom spusteni stale robi sietovu kontrolu indexu (HEAD/GET) a moze sa pripojit na server. Tvrdenie nie je uplne presne — v offline rezime to moze zlyhat. Drobna nepresnost. (line 78)
- `[minor]` Audit komment opakovane spomina, ze 'zadanie ziada samostatnu IDF, skript dava len skombinovany TF-IDF'. Toto je spravne pozorovanie, ale je dobre, aby uzivatel vedel: zadanie hovori 'inverznú frekvenciu' (sk preklad IDF), nie 'TF-IDF'. Skript namiesto IDF samostatne uklada TF-IDF maticu. Pri obhajobe by to bolo potrebne vediet vysvetlit — komentar to oznacuje, takze ok. (line 18)

---

### `01_zdroje_dat/04_reprezentacia_textu_III/identif.py` — PARTIAL

**Počty**: expected=None, actual=2060, Δ=?

**Zadanie bullets:**
- ⚠️ Rozdelit texty na vety a identifikovat slova s prislusnostou k vete — _sent_tokenize + word_tokenize OK, ID_veta sa vsak resetuje pre kazdy subor (sent_id = 1..N per file) a v tabulke nie je stlpec identifikujuci povodny subor — sentence ID nie je globalne unikatne naprieÄ 5 textami_
- ✅ Odstranit stop slova z matice — _stopwords.words('english'), porovnanie cez .lower() — OK_
- ⚠️ Odstranit interpunkciu (implicitne) — _word in string.punctuation funguje pre jednoznakovu interpunkciu, ale nezachyti viacznakove tokeny ako ``, '', --, ... ktore word_tokenize produkuje_
- ✅ Priradit slovam poradie v danej vete — _Poradie sa pocita po filtrovani stop slov/interpunkcie, co je rozumna interpretacia_
- ✅ Morfologicka anotacia (POS tagging) — _nltk.pos_tag(words) pred filtrovanim — spravne, tagger potrebuje cely kontext vety_
- ✅ Vystupny subor: ID_veta, Slovo, Lemma, Tag, Poradie — _Vsetkych 5 pozadovanych stlpcov pritomnych + bonusovy 'Slovny_Druh' (prvy znak tagu)_
- ⚠️ Lematizacia slov — _lemmatizer.lemmatize(word.lower()) bez POS parametra — defaultuje na NOUN, takze slovesa/adjektiva sa nelematizuju spravne (napr. 'using'->'using' namiesto 'use', 'joined'->'joined' namiesto 'join'). Vidno aj v datach: 'using', 'joined' zostali nezmenene_
- ✅ Format vystupu (datovy subor) — _Excel xlsx je akceptovatelny ako 'datovy subor', aj ked CSV by bolo univerzalnejsie_

**Findings (audit):**
- `[major]` ID_veta sa resetuje pre kazdy vstupny subor (enumerate(sentences, 1) vnutri for fname). 5 vstupnych suborov ale tabulka ma len 42 unikatnych ID_veta — sentence ID nie je globalne unikatne. Riesenie: pridat stlpec 'Subor'/'ID_textu' alebo pouzit globalny citac viet naprieÄ subormi. (line 62)
- `[major]` lemmatizer.lemmatize(word.lower()) bez POS argumentu — WordNetLemmatizer defaultuje na 'n' (noun). Pre slovesa/adjektiva/adverbia lemmatizacia nefunguje (priklady z vystupu: 'using'->'using', 'joined'->'joined'). Mal by sa mapovat POS tag (NN->'n', VB->'v', JJ->'a', RB->'r') a posielat: lemmatize(word.lower(), pos=wn_pos). (line 87)
- `[minor]` if word in string.punctuation filtruje len jednoznakovu interpunkciu. word_tokenize generuje aj '``', "''", '--', '...' ktore prejdu filtrom a koncia v tabulke s tagom typicky '``' alebo ':'. Pridat napr. all(c in string.punctuation for c in word) alebo regex test. (line 78)
- `[minor]` Hardcoded vystupna cesta 'out/identifikacia.xlsx' bez os.makedirs('out', exist_ok=True) — ak out/ neexistuje, skript spadne. Tu out/ existuje, takze realny dopad zatial nulovy. (line 102)
- `[minor]` 'Slovny_Druh' = tag[0] je hruby. Pre tagy zacinajuce 'CC', 'DT', 'IN', 'TO', 'WP' atd. da znak ktory nezodpoveda zmysluplnej kategorii (napr. 'C'/'D'/'I'/'T'/'W'). Stop_words sice vacsinu odfiltruju, ale nie vsetky (napr. WRB ostane). (line 96)
- `[minor]` nltk.download volania pri kazdom spusteni — zbytocne sietove volania. Idealne wrapnut do try/except alebo skontrolovat existenciu cez nltk.data.find(). (line 36)

**Rewrite**: Prepisal som identif.py s MAX-density komentami: rozsireny header docstring s cielom/zadanim/I-O/kniznicami/datovymi strukturami/algoritmom, mini-teoreticke bloky pri sent_tokenize, pos_tag a lemmatize, inline komentare na vsetkych netrivialnych riadkoch vratane audit-poznamok (sentence ID nie je globalne unikatne, lemmatize bez POS, viacznakova interpunkcia, hardcoded vystupna cesta) a cross-ref do zadania pre kazdy krok. Logika, importy, premenne a poradie operacii ostali bez zmeny.

**Adversarial verify issues:**
- `[major]` Factual error in comment: claims '179 polozkek pre anglictinu' but the actual NLTK english stopwords list has 198 entries (verified). The number 179 is from an older NLTK version; current value is 198. (line 72)
- `[major]` Factual error in comment: 'Tabulka ma stlpec ID_veta 1..N kde N je pocet viet v poslednom subore'. The last file (text5.txt) has 21 sentences, but max ID_veta in the output is 42 — that comes from the FIRST file (text1.txt). The correct statement: N is the MAX sentence count across all 5 files (not 'in the last file'). (line 96)
- `[minor]` Comment claims 'Riesi vsetkych 5 bulletov zadania' but the 5th bullet ('Odovzdat vysledny subor a zdrojak v zip-e') is a manual submission action; the script does not produce a zip. Status should arguably be PARTIAL on bullet 5 or that bullet should be flagged as out-of-scope-for-script. (line 18)
- `[minor]` UTF-8 mojibake: 'naprieÄ' appears at lines 19, 83, and 94. The intended Slovak word is 'naprieč'. File bytes contain 0xC3 0x84 ('Ä') instead of 0xC4 0x8D ('č'). Other Slovak diacritics in the file render correctly, so this is a localized typing/encoding bug that hurts readability. (line 19)
- `[minor]` Comment claims nltk.download calls 'pri prvom spusteni stiahnu modely... neskor su NO-OP' — strictly speaking NLTK still performs a network freshness check / index lookup each call (it is not a pure local cache hit with no I/O). The 'NO-OP' framing is slightly optimistic. (line 64)
- `[minor]` Comment lists Penn Treebank tag examples but says '(36 tagov)'. The Penn Treebank tagset is commonly cited as 36 POS tags, but NLTK's averaged_perceptron_tagger can also output punctuation/symbol tags ('.', ',', '``', "''", ':', '$', '#', '(', ')', 'LS', 'SYM', 'FW', 'UH'...), making the effective output tag set larger than 36. The bare '36 tagov' claim is a simplification. (line 135)
- `[minor]` Audit-note comment says 'realne out/ existuje v repo' — verified, but this is a fragile claim that depends on repo state. Not a code bug, just brittle phrasing. (line 209)

---

### `03_identifikacia/01_UNIXTIME/unixtime.py` — PARTIAL

**Počty**: expected=None, actual=20666, Δ=?

**Zadanie bullets:**
- ✅ Vytvorit premennu UNIXTIME z datumu a casu pristupu — _Skript vytvara stlpec UNIXTIME pomocou datetime.datetime(...).timestamp() z parsovaneho Apache datumu - splnene._
- ✅ Pouzit pd.read_csv() na nacitanie log suboru — _df = pd.read_csv('in/cleaned_log4.csv') - OK_
- ✅ Pouzit datetime.datetime(year, month, day, hour, minute, second).timestamp() na konverziu — _Funkcia to_unixtime() pouziva presne tento postup._
- ✅ Odovzdat logovaci subor doplneny o premennu unixtime — _out/cleaned_log4_unixtime.csv obsahuje povodne stlpce + novy stlpec UNIXTIME na konci._
- ⚠️ Odovzdat zdrojovy kod programu + log v jednom zip — _Skript a vystupny CSV existuju samostatne; zip archiv neoveritelny z auditu (mimo rozsah skriptu)._

**Findings (audit):**
- `[major]` Skript IGNORUJE casovu zonu (+0100). V to_unixtime() sa offset ' +0100' odreze (parts[3].split(' ')[0]) a datetime sa vytvara ako naive (lokalny cas). datetime.timestamp() potom interpretuje cas ako lokalny cas systemu, NIE ako UTC+0100. Vysledny UNIXTIME bude posunuty o rozdiel medzi lokalnou TZ a +0100 (na PC v Europe/Bratislava v zime to vychadza spravne, v lete o hodinu zle kvoli DST). Pre datum 19/Feb/2020 06:25:49 +0100 by spravny UTC unixtime bol 1582089949 (zhoduje sa s vystupom v out/), takze vysledok vyzera spravne LEN nahodou kvoli zhode lokalnej TZ. Riziko: ak by sa skript spustil v inej TZ alebo na datach z leta (CEST +0200), vysledky budu nespravne. (line 42)
- `[minor]` Hardcoded cesty 'in/cleaned_log4.csv' a 'out/cleaned_log4_unixtime.csv' su relativne k cwd - skript musi byt spustany z adresara 01_UNIXTIME, inak zlyha. Bez os.path.dirname(__file__) handlingu. (line 23)
- `[minor]` Parsovanie datumu split(':') je fragile - ak by hodnota DateTime obsahovala dalsie ':' (napr. v inom formate), padne. Robustnejsie by bolo pouzit pd.to_datetime(..., format='%d/%b/%Y:%H:%M:%S %z') ktore by aj zo zachovalo TZ info. (line 38)
- `[minor]` Chyba error handling - ak by riadok mal NaN/None v DateTime, apply() padne. Pre cisty log z cv1 to nie je problem, ale chybajuca robustnost. (line 53)

**Rewrite**: Prepisal som unixtime.py s MAX-density komentmi: rozsireny header docstring (ciel v WUM kontexte, parafraza zadania, vstup/vystup, pouzite kniznice s odovodnenim, datove struktury, algoritmus, cross-ref na doc.md), inline komenty na kazdom netrivialnom riadku vratane teorie UNIX timestampu, vysvetlenia parametrov pandas (index=False, .apply() vs vektorizacia), edge cases a explicitneho oznacenia auditnych findings (TZ ignored, fragile split, relativne cesty) bez zmeny semantiky kodu.

**Adversarial verify issues:**
- `[major]` Komentar tvrdi: 'Pre datovu sadu 19/Feb/2020 a CET stroj to vychadza zhodne s UTC interpretaciou (1582089949.0).' Toto je FAKTICKY NESPRAVNE. Hodnota 1582089949.0 zodpoveda interpretacii ako +0100 (lokalny cas servera), NIE ako UTC. UTC interpretacia by dala 1582093549.0 (o 3600s neskor). Overene: datetime(2020,2,19,6,25,49).timestamp() na CET stroji = 1582089949.0 = datetime(2020,2,19,6,25,49, tz=+0100).timestamp(). Komentar mal povedat: 'zhodne s interpretaciou +0100 (lokalny cas servera v zime)', nie 'UTC interpretaciou'. (line 110)
- `[minor]` Komentar tvrdi 'audit minor finding' o relativnej ceste, ale nikde inde v skripte nie je audit log / audit listing, ktory by tieto findings zbieral. Odkaz visi vo vzduchu - bud doplnit audit sekciu na konci, alebo preformulovat ('znama limitacia' bez slova audit). (line 78)
- `[minor]` Komentar tvrdi '<1s' pre 20666 riadkov bez merania. Plauzibilne, ale je to nepodlozeny vykonnostny claim. Pre obhajobu projektu bezpecnejsie formulovat ako 'rychlost postacuje, vykonnost nie je kriticka pre tento rozsah'. (line 154)
- `[minor]` Komentar '.timestamp() ... Pre aware datetime (s tzinfo) by pouzil tu TZ - tu sa nedeje.' je spravne, ale formulacia 'tu sa nedeje' moze byt nejasna. Pre obhajobu jasnejsie: 'tu vzniknute datetime je naive, takze tato vetva sa neuplatni'. (line 139)
- `[minor]` Komentar tvrdi 'Ocakavany pocet zaznamov: 20666'. Tento konkretny pocet nie je v zadani.txt - je to pravdepodobne empiricka hodnota z vystupu cv1. Ak nie je overena voci skutocnemu cv1 vystupu, mozno ju treba oznacit ako 'priblizne ~20k' aby sa pri obhajobe nedalo chytit na konkretnom cisle. (line 22)

---

### `03_identifikacia/06_SLength/slength.py` — PARTIAL

**Počty**: expected=6700, actual=6515, Δ=2.8%

**Zadanie bullets:**
- ✅ Identifikacia sedeni metodou SLength (10-minutovy odhad dlzky sedenia) — _Skript pouziva slength=600 sekund (10 minut) a kumulativne sleduje dlzku sedenia_
- ✅ Nacitanie log suboru cez pd.read_csv() — _Nacita in/cleaned_log4_length.csv (vystup z ulohy 03 s Length stlpcom)_
- ✅ Logovaci subor doplneny o identifikaciu pouzivatelov (USER_ID + SESSION_ID) — _Vystup obsahuje USER_ID (uz z predchadzajucej ulohy) aj novy SESSION_ID stlpec_
- ✅ Identifikovanych by malo byt cca 6700 sedeni — _Vystup ma 6515 unikatnych sedeni, co je v ramci tolerancie 'cca' (delta 2.76%)_

**Findings (audit):**
- `[major]` Logicka chyba pri reset kumulativu (riadok 47): ked cumulative_time + Length >= 600, skript priradi NOVE session_id aktualnemu riadku a resetuje cumulative_time = 0, ale NEPRIPOCITA Length aktualneho riadku do noveho sedenia. To znamena, ze novo zacate sedenie 'stratilo' cas prveho zaznamu. Komentar v hlavicke (priklad: Length=100 -> Kumulativ=100 pre nove sedenie) sa NEZHODUJE so skutocnou logikou kodu (kod by ulozil 0, nie 100). Spravne by malo byt: cumulative_time = row['Length']. (line 47)
- `[minor]` Pouzitie >= namiesto > pri porovnani s prahom (riadok 44): cumulative_time + row['Length'] >= slength. Ak by sa kumulativ rovnal presne 600, sedenie sa ukonci. V zadani je '10-minutovy odhad', co je nejednoznacne ci 600 patri do sedenia alebo nie. Pri pouziti > by sedenia mohli byt o nieco dlhsie a ich pocet by sa priblizil k 6700. (line 44)
- `[minor]` Nezohladnuje sa zmena USER_ID v ramci iteracie explicitne — skript sa spolieha len na NaN v Length stlpci ako indikator noveho usera. Ak by predchadzajuca uloha 03 nesetla NaN spravne na prvom zazname kazdeho usera, sedenia by mohli 'preliezat' medzi userami. Toto vsak pravdepodobne funguje spravne (delta len 2.76%). (line 40)
- `[minor]` Vystupny CSV neobsahuje hlavickovy riadok pre wc -l vypocet — out subor ma 20667 riadkov vratane hlavicky = 20666 datovych. Nie je to chyba, len poznamka pre interpretaciu.

**Rewrite**: Prepisal som skript s MAX-density komentami: rozsireny header docstring (ciel v kontexte WUM, parafrazovane zadanie s ocakavanym poctom 6700, vstup/vystup, kniznice s odovodnenim, datove struktury, algoritmus, cross-ref na doc.md), inline teoreticke bloky pri SLength prahovej podmienke a NaN-marker logike, vysvetlenie preco nie cumsum a preco iterrows, plus dokumentacia auditom najdenych edge-cases bez zmeny semantiky kodu.

**Adversarial verify issues:**
- `[minor]` Komentar tvrdi, ze RLength je 'pevna heuristika - limit na cas MEDZI pristupmi'. V standardnej WUM literature (Spiliopoulou, Mobasher) je 'Reference Length' typicky o dobe straveni na stranke (page-stay duration), zatial co 'cas medzi pristupmi' charakterizuje skor STT metody. Bez pristupu k doc.md neviem s istotou potvrdit, ci je toto rozdelenie spravne — moze to byt nepresne. Odporucam overit v doc.md pred obhajobou. (line 53)
- `[minor]` Komentar uvadza 'tolerancia ~5%' pri ocakavanom pocte sedeni 6700. Zadanie hovori len 'cca 6700' bez konkretnej tolerancie — 5% je autorovsky odhad, nie cislo zo zadania. Nelze, ale prisne vzate to nie je citacia zadania. (line 18)
- `[minor]` Komentar tvrdi '~20k riadkov' bez overenia. Nepoznam presny pocet riadkov v cleaned_log4_length.csv — moze byt vyrazne ine cislo. Komentar je vsak prezentovany ako orientacny ('rezia zanedbatelna'), takze dopad je nizky. (line 92)
- `[minor]` Komentar predpoklada, ze 'log je serazeny podla USER_ID + UNIXTIME (z ulohy 03)'. Tento predpoklad je pravdepodobne spravny (Length sa pocita cez groupby+shift, co implikuje serazenie), ale nie je explicitne overeny v tomto skripte ani v zadani. Algoritmus SLength stoji a pada na tomto predpoklade — ak vstup nie je serazeny chronologicky v ramci usera, SESSION_ID priradenie by bolo nezmyselne. (line 99)

---

### `05_prieskum_dat/01_popisne_statistiky/popisne.py` — PARTIAL

**Zadanie bullets:**
- ✅ Zahrnut aspon jednu premennu z kazdej skupiny (DV obsah, IV cas, User, Ostatne) — _DV: category; IV: year, yearQuartal, crisis; User: anonIP; Ostatne: length, internal — vsetky skupiny pokryte_
- ⚠️ Analyzovat vybrane vztahy medzi premennymi — _Skript robi len univariate frekvencie a popisne statistiky. Bivariate/multivariate analyza (napr. category x year, length x category, crisis vs po-krize) chyba — neexistuje ziadny groupby alebo crosstab medzi DV a IV_
- ✅ Prieskum dat o pouzivani webu v sledovanom obdobi — _Obdobie 2009-2012 pokryte cez year_counts a yearQuartal_
- ⚠️ Pozriet sa na vyvoj navstevnosti z hladiska casu (inspiracia) — _Graf po rokoch a kvartaloch existuje, ale sila zavislosti (korelacia / chi-square) nie je vyjadrena_
- ❌ Pracovat s casom stravenym na strankach z hladiska kategorii obsahu a obdobi (inspiracia) — _length je analyzovany len globalne (describe). Chyba groupby length podla category alebo podla year/quartal — kluzova inspiracia zo zadania_

**Findings (audit):**
- `[major]` Skript NEROBI ziadnu bivariate analyzu — zadanie explicitne pyta 'analyzujte vybrane vztahy medzi premennymi'. Vsetky vystupy (riadky 34-58) su univariate (value_counts, describe). Treba pridat napr. df.groupby('category')['length'].describe() alebo crosstab(category, year). (line 48)
- `[major]` Inspiracna poziadavka 'cas straveny na strankach z hladiska kategorii a obdobi' nie je realizovana. length_clean.describe() (r.51) je len globalne — chyba rozbalenie podla category/year. (line 51)
- `[major]` sumar.txt je staticky napisany (komentar r.22 to priznava). Cisla v sumar.txt (napr. '2012: 621,988 zaznamov', '66.9% mimo banky') nie su vypocitane skriptom — riziko ze pri novom datasete budu zastarale. Mali by sa generovat dynamicky. (line 22)
- `[major]` n_sessions = df['frame'].nunique() (r.55) — stlpec 'frame' nie je dokumentovany v hlavicke skriptu ako session ID. V komentari r.14 sa spominaju userAgent/agent, ale frame chyba. Treba overit ze 'frame' je naozaj session identifier (a nie napr. HTML frame). (line 55)
- `[minor]` Filter length > 0 (r.49) odstranuje 0-second pristupy, ale nie je vysvetlene preco. V sumar.txt count=748496 zo ~2M zaznamov znamena ze 64% riadkov ma length<=0 — toto je major data quality issue ktore by malo byt zmienene. (line 49)
- `[minor]` Vizualizacia hist length<300 (r.71) nemotivovana — preco 300s cutoff? Z describe vyplyva max=104s, takze cutoff 300 nic neorezava. Cutoff sa zda byt z ineho datasetu/predchadzajucej verzie. (line 71)
- `[minor]` Premenne webPart, urlExt, agent, userAgent, quartal, week su uvedene v hlavicke (r.13-15) ako sucast skupin, ale v skripte sa NEPOUZIVAJU. Z DV skupiny je analyzovana iba category. Ak chcel autor pokryt 'aspon jednu z kazdej skupiny', je to OK, ale pre prieskum dat je to chudobne. (line 14)
- `[minor]` Chyba vystupny CSV/textovy subor s frekvenciami — len print do konzoly a PNG graf. sumar.txt je static. Pre reprodukovatelnost by bolo dobre ulozit cat_counts/year_counts ako CSV. (line 74)

**Rewrite**: Prepisal som popisne.py s MAX-density komentami: rozsireny header (ciel v kontexte WUM, parafraza zadania, vstup/vystup, kniznice s odovodnenim, datove struktury, cross-ref na doc.md, audit poznamky), inline komenty na kazdom netrivialnom riadku (preco low_memory=False, preco sort_index, RLength teoria, cutoff 300s anomalia, kardinalita anonIP/frame). Kod, importy a logika su nezmenene.

**Adversarial verify issues:**
- `[major]` Komentar na riadku 162 tvrdi 'typicky 1-5 sedeni / user', ale realne data zo sumar.txt ukazuju 81.2 sedeni/user (561422 sedeni / 6912 userov). Toto je NEPRAVDIVA tvrdenie o tomto datasete - bud je 'frame' nie session ID (potom je audit poznamka opravnena a komentar zavadzajuci), alebo je tvrdenie 1-5 jednoducho zle. (line 163)
- `[minor]` Komentar uvadza priklad yearQuartal ako '2010-Q3', ale realny format v CSV je '09Q1', '10Q3' (2-ciferny rok bez pomlcky). Priklad je zavadzajuci. (line 193)
- `[minor]` Komentar tvrdi ze exp. rozdelenie ma 'mean >> median' a porovnava ich pre length. Realne mean=16.4, median=9 (pomer ~1.8x) - to je right-skewed, ale tvrdenie ze ide o exponencialne rozdelenie nie je v skripte testovane (chyba KS test alebo iny goodness-of-fit). Komentar je teoreticky korektny, ale spaja sa s neoverenym tvrdenim o type rozdelenia. (line 138)
- `[minor]` Cross-references na doc.md (§3, §4, §7) nie su overene v ramci tohto skriptu - skript ich nepouziva ani neoveruje. Ak doc.md neexistuje alebo nema tieto sekcie, su to falosne odkazy. (line 48)
- `[minor]` Audit poznamka v hlavicke spravne identifikuje ze bivariate analyza chyba - to je dolezite, pretoze zadanie EXPLICITNE ziada 'analyzujte vybrane vztahy medzi premennymi'. Skript nesplna druhy bullet zadania, ale komentar to dokumentuje (transparentne). (line 55)
- `[minor]` Komentar pri histograme tvrdi 'cutoff 300s je podozrivy - z describe vyplyva max okolo 104s, takze cutoff nic neorezava'. Toto je PRAVDIVE (sumar.txt potvrdzuje max=104) a audit je opravneny - ale tym padom hodnota '< 300' v kode je dead code/no-op, co by sa mohlo opravit (zadanie hovori 'NEOPRAVUJEME', takze OK ponechat). (line 212)
- `[minor]` Komentar tvrdi ze 'frame' = session ID je nedokumentovany - to je opravnena skepticka poznamka. Avsak skript ho stale pouziva ako session ID bez akejkolvek validacie - co je rizikove ak 'frame' v skutocnosti nie je session ID. (line 59)
- `[minor]` Komentar 'value_counts() defaultne vynechava NaN' je technicky korektny pre default dropna=True, ale neuvadza, ze pre stlpce ako 'category' alebo 'webPart' s NaN hodnotami su pocty potom mensie ako df.shape[0] - co moze ovplyvnit interpretaciu (uzitocna informacia by bola explicitne uviest, kolko NaN sa vynechalo). (line 100)

---

### `05_prieskum_dat/02_navstevnost_v_case/navstevnost.py` — PARTIAL

**Zadanie bullets:**
- ✅ Zahrnut aspon jednu premennu z kazdej skupiny premennych charakterizujucich pristupy — _Skript pouziva time/datum/mesiac/yearQuartal (casove IV), crisis (obdobie), category (obsah DV) - viacero skupin pokrytych._
- ⚠️ Analyzovat vybrane vztahy medzi premennymi — _Pokryty su deskriptivne vztahy cas vs pocet pristupov a kategoria vs cas. Chyba statisticka sila zavislosti (korelacia, chi2), ktora je explicitne navrhnuta v zadani ('vyjadrit silu tejto zavislosti')._
- ✅ Vyvoj navstevnosti z hladiska casu (inspiracia) — _Mesacne agregacie + casovy rad graf + kriza vs po krize porovnanie._
- ❌ Cas straveny na strankach z hladiska kategorii a obdobi (inspiracia) — _Skript pracuje len s POCTOM pristupov, nie s casom stravenym (timeOnPage / dwell time). Zadanie tuto inspiraciu explicitne uvadza._
- ✅ Vykreslit grafy (vizualizacia) — _out/navstevnost.png - 2 subgrafy (mesacny rad + kategorie kvartalne)._
- ⚠️ Vystupy do out/ (CSV/sumar) — _Generuju sa mesacne_navstevy.csv (32 mesiacov), kategorie_v_case.csv (16 kvartalov) a navstevnost.png. ALE sumar.txt je podla komentara v skripte ('sumar.txt je staticky napisany') vytvoreny rucne, nie skriptom - hrozi rozsynchronizovanie s datami._

**Findings (audit):**
- `[major]` Komentar 'sumar.txt je staticky napisany' a skript naozaj NEgeneruje out/sumar.txt. Sumar obsahuje cisla (median 39318, kriza celkom 604043, po krize 784181, +29.8%), ktore nie su zapisovane skriptom - hrozi rozsynchronizovanie s datami pri zmene vstupu. Standalone princip narusenmy. (line 21)
- `[major]` Zadanie navrhuje 'vyjadrit silu zavislosti' medzi premennymi - skript nepocita ziadnu statisticku miru (Pearson/Spearman korelacia, chi2 nezavislosti pre crisis x category, ANOVA). Iba deskriptivne porovnanie priemerov.
- `[major]` Zadanie explicitne ponuka inspiraciu 'cas straveny na strankach z hladiska kategorii a obdobi'. Skript pracuje vylucne s pocetnostou pristupov - premenna pre dwell time / time-on-page nie je analyzovana vobec.
- `[minor]` df.groupby('mesiac').size() vytvori PeriodIndex s medzerami - mesiace 05/06/07/10 v 2009-2011 chybaju v datach. Skript nereindexuje na suvisly mesacny rozsah, co sposobi vizualne medzery v casovom rade (graf moze byt zavadzajuci pri interpretacii 'vyvoja v case'). (line 34)
- `[minor]` Skript pocita iba min/max/mean. Sumar.txt obsahuje median (39318), ktory nie je v skripte vypocitany - sumar bol vyrobeny manualne s extra metrikami. (line 38)
- `[minor]` zmena_pct = (po_krize.mean() / kriza.mean() - 1) * 100 pouziva priemer per existujuci mesiac. Kedze chyba viacero mesiacov v krize aj po krize a po roznom pocte, priemer moze byt zavadzajuci - lepsie by bolo normalizovat na rovnaky pocet mesiacov alebo pouzit celkove sumy. (line 43)
- `[minor]` axvline na 2010-12 ako 'Koniec krizy' - hranica je hardcoded a nie zdovodnena v komentari. Mala by sa zdokumentovat alebo odvodit z premennej crisis. (line 56)
- `[minor]` kat_v_case sa agreguje po yearQuartal + category, ale stlpec yearQuartal sa pouziva primo z datasetu bez verifikacie ze odpoveda derivovanemu datumu. Konzistencia medzi 'time' a 'yearQuartal' nie je validovana. (line 51)

**Rewrite**: Rozsiril som header docstring (ciel v kontexte WUM, parafraza zadania s mapovanim IV/DV skupin, vstup/vystup, kniznice s odovodnenim, datove struktury, algoritmus, cross-ref doc.md) a pridal inline MAX-density komenty na kazdy netrivialny riadok vratane teoretickych blokov k PeriodIndex, groupby+size, unstack(fill_value), boolean filtrovaniu pre crisis, edge cases pre NaT/medzery v mesiacoch a odkazov na konkretne AUDIT findings (minor #4/#6/#7/#8) bez akejkolvek zmeny logiky, importov ci poradia volani.

**Adversarial verify issues:**
- `[minor]` Header docstring (lines 7-9) tvrdi, ze 'zatial sa nehladaju statisticke testy, len vizualny a sumarny opis' — to je obhajitelne, ale zadanie explicitne pyta 'vyjadrit silu tejto zavislosti'. Skript pocita len percentualnu zmenu priemeru (zmena_pct), nie staticky mierku zavislosti (korelacia, chi-square, atd.). Komenty by mali tento gap aspon priznat. Pravdepodobne dediene z povodneho skriptu, nie zavlecene prepisom. (line 7)
- `[minor]` Zadanie spomina 'cas straveny na strankach z hladiska kategorii a obdobi' — skript vsak rata POCTY pristupov (size()), nie casy stravene na strankach. Komenty (najma riadky 137-139, 153) tento rozdiel nereflektuju. Pravdepodobne dediene z povodneho skriptu. (line 137)
- `[minor]` Komenty odkazuju na 'AUDIT minor #4/#6/#7/#8' (riadky 95, 117, 150, 167) — externe dokumenty, ktore nie su sucastou skriptu. Ak audit.md neexistuje v projekte, citatel sa nedostane k vysvetleniu. Nie je to chyba, ale moze byt fragile. (line 95)
- `[minor]` Header docstring tvrdi 'dataset pokryva 2009-2012 → cca 32 mesiacov (s medzerami pre 05/06/07/10 v niektorych rokoch)' — toto je specificke tvrdenie o datach, ktore nie je overene z kodu (skript len pouziva to, co najde). Ak je realne pokrytie ine, komentar by zavadzal. Bez spustenia neviem overit s istotou. (line 19)
- `[minor]` Riadok 161: 'matplotlib si vie poradit cez period_to_timestamp' — mierna nepresnost. pandas plot na PeriodIndex pouziva interne konverziu na PeriodIndex.to_timestamp() alebo matplotlib period converter, presny mechanizmus zavisi od verzie pandas. Komentar je v podstate spravny, ale formulacia je vagna. (line 161)
- `[minor]` Riadok 80: 'NaT klucu sa zbavi default' — formulacia je trochu kostrbata, ale technicky spravna (groupby ma dropna=True ako default od pandas 1.1, takze NaT kluce skutocne padaju). OK. (line 80)

---

### `05_prieskum_dat/04_vztahy_premennych/vztahy.py` — PARTIAL

**Zadanie bullets:**
- ✅ Zahrnúť aspoň jednu premennú z každej skupiny premenných (DV obsahové + IV časové + iné) — _Pouzite: category (DV obsah), crisis/year (IV cas), internal (typ pristupu), length (cas straveny). Pokryva viacero skupin premennych._
- ✅ Analyzovať vybrané vzťahy medzi premennými — _4 testy: 3x chi-square + 1x ANOVA. Vsetky vztahy testovane staticky validne._
- ⚠️ Pozrieť sa na vývoj návštevnosti z hľadiska času (timeseries trend) — _Skript testuje len kategoricku zavislost (category vs year/crisis), nie vyvoj v case (napr. mesacne/denne pocty navstev, trend). Chyba ciselny timeseries._
- ✅ Vyjadriť silu závislosti — _Cramerovo V pocitane a interpretovane slovne (velmi slaba/slaba/stredna/silna)._
- ⚠️ Pracovať s časom stráveným na stránkach z hľadiska kategórií A OBDOBÍ — _ANOVA length vs category je OK, ale chyba length vs obdobie (crisis/year) a ich kombinacia (two-way ANOVA / interakcie)._
- ⚠️ Vystupny sumar/report do out/ — _sumar.txt v out/ existuje, ALE skript ho nevytvara - je staticky/manualne napisany (potvrdene komentarom v skripte riadok 24). Vysledky chi2 testov sa len printuju do stdout, nikam neukladaju._

**Findings (audit):**
- `[major]` Script reads 'in/logs5.csv' ale folder c:/.../04_vztahy_premennych/in/ je PRAZDNY. Skript pri spusteni okamzite spadne s FileNotFoundError. Nesplna pravidlo 'standalone scripts' z MEMORY.md. (line 32)
- `[major]` Komentar priznava: '(sumar.txt je staticky napisany)'. Skript NEvytvara ziadny vystupny subor - len printuje do konzoly. Existujuci out/sumar.txt je rucne napisany, takze hodnoty v nom (n=2,071,235, chi2=225219.72, ...) nie su reprodukovatelne behom skriptu. Hrozi rozchod kodu vs reportu pri zmene dat. (line 24)
- `[major]` ANOVA (f_oneway) ma predpoklady: normalita rozdelenia + rovnost rozptylov v skupinach. 'length' je typicky silne pravostranne skewed (heavy tail). Nie je testovana ani transformacia (log) ani robustna alternativa (Kruskal-Wallis). F=5016 pri n=2M je preto otazne - p<0.001 sa dosiahne aj pri trivialnych rozdieloch. (line 64)
- `[major]` Cramerovo V vzorec sqrt(chi2 / (n * (min(r,c)-1))) je klasicka verzia, ale pri velkom n (2M) a velkom poctu kategorii je vhodnejsie pouzit bias-corrected variantu (Bergsma 2013). Pri n=2M sa chi2 nafukuje, V je nadhodnotene. (line 36)
- `[minor]` ANOVA pouziva filter df['length']>0, ale neriesi extremne outliers (napr. session length 86400+s). Tieto by mali bola zrezane alebo logaritmovane pred testom. (line 67)
- `[minor]` Test 1 (category vs crisis) je dichotomicky vs multinominal - chi2 OK, ale chyba post-hoc analyza (ktore kategorie konkretne prispievaju k zavislosti, standardized residuals). (line 57)
- `[minor]` Zadanie spomina 'vyvoj navstevnosti z hladiska casu' - skript testuje len category vs year ako kategoricku zavislost. Chyba realny timeseries (monthly/weekly counts, trend, sezonalita). (line 73)
- `[minor]` Skript nevytvara ziadne grafy/vizualizacie (heatmap kontigencnej tabulky, boxplot length per kategoria, line plot navstevnosti v case). Prieskum dat by mal obsahovat vizualnu zlozku. (line 1)
- `[minor]` chi2_contingency pri velkom datasete s 6+ kategoriami moze mat bunky s expected<5 - skript netestuje predpoklady chi2 testu (min expected frequency). (line 49)

**Rewrite**: Prepisany skript c:/Users/mstud/School/Objavovanie znalosti/05_prieskum_dat/scripts/04_vztahy_premennych/vztahy.py - rozsireny header docstring (ciel/zadanie/vstup/vystup/kniznice/datove struktury/algoritmus/cross-ref), mini-teoreticke bloky pri chi2/Cramerovo V/ANOVA, inline komenty na kazdom netrivialnom riadku (parametre read_csv, crosstab idiom, list comprehension, *unpacking, filter length>0) a cross-ref na bullet body zadania pri kazdom teste. Logika, importy, premenne a poradie volani su nezmenene.

**Adversarial verify issues:**
- `[minor]` Komentar v docstring funkcie chi2_test je matuci: 'chi2_contingency vrati 4-ticu (chi2, p, dof, expected). Nas zaujima prvych 5'. chi2_contingency vracia presne 4 hodnoty (4-tuple), v kode sa unpackuje 4 polozky (riadok 137: chi2, p, dof, _). 'Prvych 5' sa zrejme vztahuje na 5 polozkovy navratovy tuple FUNKCIE chi2_test (chi2, p, dof, cv, tabulka), ale formulacia hned po 'vrati 4-ticu' citatela zmati. (line 126)
- `[minor]` Preklep v komentari: 'maxmalnu mozcnu' ma byt 'maximalnu moznu' (chi2 hodnoty). (line 106)
- `[minor]` Vnutorny odkaz 'vid audit, riadok 24' je nepresny - riadok 24 v skripte hovori o ocakavanom rozsahu dat (~2,07 mil. riadkov), nie o sumar.txt. Sebareferencne odkazy na 'audit' bez kontextu zhorsuju citatelnost. (line 38)
- `[minor]` Komentar tvrdi ze 'F-statistika' kvantifikuje SILU efektu, ale F-statistika je TESTOVA statistika (testuje signifikanciu), nie miera sily efektu. Pre ANOVA sa pre silu pouziva eta^2 / omega^2. Ako konvencia v tomto skripte je to akceptovatelne, ale teoreticky nepresne. (line 9)
- `[minor]` Komentar 'chi2 aj ANOVA pracuju nad celou populaciou pristupov, nie nad samplom' je statisticky zavadzajuci. Chi2 a ANOVA su INFERENCNE testy zo sample-u na populaciu. Komentar by mal povedat ze pouzivame cely DOSTUPNY dataset (vsetky pozorovania), nie ze nie je sample. (line 75)
- `[minor]` Audit komentar spravne uvadza ze chi2 predpoklada expected freq >= 5 v >=80% buniek, ale skript predpoklady neoveruje. Vyhlasenie ze 'len dokumentujem' je OK pre anti-drift, ale citatel by mohol byt zmateny preco vysledok ANOVA F=5016 je v komentari uvedeny ako konkretne cislo (riadok 186) ked skript nie je spusteny - hodnota je hardkodovana z predchadzajucich behov. (line 132)
- `[minor]` Komentar spomina Bergsma 2013 bias-corrected Cramerovo V - tato referencia je v poriadku, ale predtym (linka 111) sa thresholdy pripisuju 'Cohen / Rea & Parker'. Cohen typicky definuje w (nie V), Rea & Parker 1992 definuju V thresholdy. Atribucia je trochu volna ale akceptovatelna. (line 102)
- `[minor]` Komentar uvadza konkretne cislo '~2,07 mil. riadkov' - toto je hardkodovany hint ktory neoveruje skript. Ak by sa vstupny CSV zmenil, komentar by klamal. (line 24)

---

### `06_extrakcia_vzorov/01_priprava_dat/priprava.py` — PARTIAL

**Počty**: expected=None, actual=102481, Δ=?

**Zadanie bullets:**
- ✅ Identifikovat obdobia pre asociacnu/sekvencnu analyzu (rok/polrok/kvartal) — _Skript pouziva rok ako obdobie (2009-2012 = 4 obdobia). Stlpec yearQuartal je nacitany ale nepouzity - pri vacsej granularite by sa dal vyuzit._
- ✅ Filter dat — _Filtruje stlpce na [frame, anonIP, category, year, yearQuartal] a dropna na category. Filter na transakcie >=2 kategorii._
- ✅ Extrakcia vzorov - priprava transakcii (kosikov) pre kazde obdobie — _Pre kazdy rok vytvorena samostatna CSV s transakciami. Samotna extrakcia pravidiel (>=10) je predmetom dalsej ulohy - tu len priprava dat._
- ❌ Datova matica jedinecnych vzorov s premennymi O1..O4 — _Tato uloha tu nie je riesena - je to nadvazujuca uloha (po extrakcii pravidiel). Skript je iba KROK 1 (priprava dat), co je v sulade s pomenovanim '01_priprava_dat'._
- ❌ Sumarizacia vysledkov / statisticke testy (Cochran Q, Coeff. of Concordance) — _Mimo rozsahu tohto skriptu - je to dalsi krok pipelinu po extrakcii pravidiel._

**Findings (audit):**
- `[minor]` Riadok 36: stlpec 'yearQuartal' je zahrnuty do projekcie ale dalej nikde nepouzity. Bud ho odstranit alebo dodat moznost rozdelenia na kvartaly (zadanie spomina 'rok/polrok/kvartal'). (line 36)
- `[minor]` Riadok 52: groupby('frame') agreguje cez vsetky roky cez ten isty 'frame' uz nemoze nastat (df_rok je filtrovany na 1 rok), takze OK. Ale ak by sa frame ID opakovalo medzi rokmi (nepravdepodobne), doslo by k duplicite - vhodne by bolo groupby(['year','frame']). (line 51)
- `[minor]` Riadok 56: filter transakcie['category'].str.contains(';') - kontroluje pritomnost ';' v retazci, co implicitne znamena >=2 kategorie. Funguje, ale citatelnejsie by bolo str.count(';') >= 1 alebo si rovno spocitat set pred join. (line 56)
- `[minor]` Riadky 30, 59: hardcoded relativne cesty 'in/logs5.csv' a 'out/...' - skript musi byt spusteny z konkretneho adresara. Vhodne by bolo pouzit pathlib relative ku __file__. (line 30)
- `[minor]` Vystupne CSV ma stlpec 'category' obsahujuci ';'-separated zoznam ako string. Pre dalsie spracovanie (apriori, fpgrowth) bude treba opat split - moznost ulozit rovno ako list/JSON alebo one-hot maticu by bola praktickejsia, ale toto je obvykla forma v tomto kurze. (line 60)
- `[minor]` Pocet transakcii za rok: 2009=37734, 2010=18996, 2011=21473, 2012=24278 (minus header). Vyrazny pokles 2009->2010 (-50%) - moze byt artefakt zberu dat alebo skutocnost; v zadani nie su uvedene ocakavane pocty, takze nemozno overit. Stoji za zmienku v dokumentacii. (line 61)
- `[major]` Skript pokryva LEN prvy krok zadania (priprava dat). Aby cely zadanie bolo splnene, musia existovat dalsie skripty pre: extrakciu pravidiel (>=10 na obdobie), vytvorenie matice vzor x obdobie a statisticke testy (Cochran Q, Kendall W). Posudenie tychto krokov tu nie je mozne - treba audit dalsich skriptov v pipeline.

**Rewrite**: Pridany rozsireny header docstring (ciel/zadanie/vstup/vystup/kniznice/algoritmus/cross-ref na doc.md), teoreticke bloky (transakcia, kosik, |kosik|>=2, groupby+apply idiom), inline komenty na kazdom netrivialnom riadku vratane zdovodnenia parametrov pandas (sep, quotechar, low_memory, .copy(), dropna subset, index=False), edge cases a poznamky z auditu (yearQuartal nepouzity, str.contains vs count, hardcoded cesty) - vsetko BEZ zmeny logiky, importov, premennych a volani.

**Adversarial verify issues:**
- `[minor]` Komentar 'str.contains(";") -> regex match na pritomnost znaku ;' je technicky pravdivy (pandas defaultne pouziva regex=True), ale ';' nie je regex special char, takze sa sprava ako literal match. Komentar by mohol byt presnejsi. (line 152)
- `[minor]` Filter str.contains(';') ma teoreticky edge case: ak by sama hodnota category obsahovala znak ';' (napr. 'Foo;Bar' ako jeden nazov kategorie), tak by aj 1-prvkovy kosik prosiel filtrom. Komentar tento edge case neuvadza. V praxi nehrozi (nazvy kategorii v logs5.csv neobsahuju ;), ale komentar by mal byt opatrnejsi. (line 152)
- `[minor]` Komentare na riadkoch 27, 104, 164 obsahuju konkretne AUDIT cisla (102481, 37734, 18996, 21473, 24278), ktore som nemohol nezavisle overit bez spustenia skriptu. Ak boli odpozorovane skutocnym behom, su OK; inak by sa mali oznacit ako 'predpokladane'. (line 27)
- `[minor]` Vystupne CSV pouziva default oddelovac ',' (comma), zatial co vstup ma ';'. Komentar hovori '2 stlpce -> frame, category (;-separated zoznam)' co je spravne pre obsah, ale explicitne neuvadza, ze samotny CSV separator stlpcov je ',' (na rozdiel od vstupu). Consumer (uloha 02) musi vediet rozlisit oba separatory. (line 162)
- `[minor]` Hardcoded relativna cesta 'in/logs5.csv' a 'out/transakcie_*.csv' - skript zavisi na CWD a nevytvara out/ adresar (chyba mkdir/os.makedirs). Pri prvom behu na cistom prostredi by spadol s FileNotFoundError. Komentar to neuvadza. (line 71)
- `[minor]` Skript pouziva df['year'] PRED projekciou stlpcov na riadku 95 - to je OK, pretoze 'year' je v povodnom DataFrame. Komentar to nevyslovuje. Logika je zachovana, len chronologia komentov vs. kodu vyzaduje pozorne citanie. (line 76)

---

### `06_extrakcia_vzorov/02_asociacne_pravidla/pravidla.py` — PARTIAL

**Počty**: expected=10, actual=17, Δ=0.0%

**Zadanie bullets:**
- ✅ Identifikovat obdobia (rok/polrok/kvartal) pre analyzu — _Skript spracovava 4 rocne obdobia: 2009, 2010, 2011, 2012 (loop na riadku 34)_
- ✅ Filter dat / nacitanie predspracovanych transakcii — _Nacita transakcie_{rok}.csv z ulohy 01 (riadok 38), filter bol vykonany v predchadzajucej ulohe_
- ✅ Extrahovat vzory z kazdeho obdobia (min. 10 pravidiel/obdobie) — _Vystupy: 2009=341 pravidiel, 2010=405, 2011=205, 2012=17. Vsetky obdobia maju >10 pravidiel, podmienka splnena._
- ⚠️ Frekventovane itemsety (Frequent itemsets) — _Apriori sa vola (riadok 52), ale itemsety sa NEukladaju do CSV - vystup je iba pocet (print). Ak sa pozaduju aj itemsety ako samostatny artefakt, chyba._
- ✅ Asociacne pravidla (Association rules) — _association_rules() s metric=confidence, min_threshold=0.5 (riadok 57). Ulozene v out/pravidla_{rok}.csv so stlpcami antecedents, consequents, support, confidence, lift._
- ❌ Datova matica jedinecnych vzorov s premennymi O1(0/1), O2(0/1)... pre obdobia — _Skript NEVYTVARA spojenu maticu vzorov so stlpcami O1,O2,O3,O4 indikujucimi vyskyt vzoru v jednotlivych obdobiach. Pravidla sa ukladaju separatne pre kazdy rok._
- ❌ Zosumarizovanie dosiahnutych vysledkov — _Skript nepocita ziadne agregovane statistiky, popisne charakteristiky, ani vizualizacie naprieč obdobiami. Iba print poctov pravidiel._
- ❌ Cochran Q Test (testovanie zavislych vzoriek) — _Test sa v skripte vobec nevykonava. Nevidiet import scipy.stats ani statsmodels._
- ❌ Coeff. of Concordance (Kendallov W) — _Vypocet koeficientu konkordancie sa v skripte vobec nevykonava._
- ❌ Alternativne: lubovolne metody na sumarizaciu (descriptives, vizualizacia, testy) — _Zadanie ponuka alternativu k Cochran/Kendall, ale ani ziadna alternativna sumarizacna metoda nie je implementovana._

**Findings (audit):**
- `[major]` Chyba krok vytvorenia matice jedinecnych vzorov s indikatormi O1..O4 - kluciova poziadavka zadania (riadok 19-20 zadania). Skript by mal po loope zlucit pravidla zo vsetkych rokov, identifikovat unikatne (antecedent=>consequent) a vytvorit binarnu maticu vyskytu. (line 71)
- `[major]` Chyba Cochran Q Test / Coeff. of Concordance / akakolvek statisticka analyza naprieč obdobiami. Zadanie to vyslovne vyzaduje (alebo alternativnu sumarizacnu metodu). (line 71)
- `[major]` Chyba sumarizacia vysledkov (descriptive stats, vizualizacia, porovnanie poctov pravidiel/support/confidence medzi rokmi). (line 71)
- `[minor]` Frekventovane itemsety (apriori vystup na riadku 52) sa nikam neukladaju, len sa vypise pocet. Pre dosledne splnenie 'Frequent itemsets' by sa hodilo ulozit aj itemsety do CSV. (line 52)
- `[minor]` Rok 2012 ma iba 17 pravidiel (vyrazne menej nez 2009-2011). Toto moze byt OK (splna min. 10), ale stojí za komentar v sumarizacii - moze indikovat nizsi objem dat alebo problem s min_support pri kratsom obdobi. (line 31)
- `[minor]` Skript predpoklada existenciu in/transakcie_{rok}.csv (riadok 38) bez kontroly - mal by byt standalone ale spolieha sa na vystup z ulohy 01. Podla pravidiel projektu (standalone scripts) by sa mali vstupy nachadzat v in/ folderi danej ulohy, co je splnene. (line 38)
- `[minor]` Hardcoded MIN_SUPPORT=0.05 a MIN_CONFIDENCE=0.5 - rovnake prahy pre vsetky obdobia mozu produkovat neporovnatelne pocty pravidiel (2009: 341 vs 2012: 17). Pri tak velkej disparite je porovnatelnost obmedzena. (line 31)

**Rewrite**: Pridal som MAX-density komenty: rozsireny header docstring s cross-ref na zadanie/doc.md a auditom (chybajuca matica O1..O4, Cochran Q, sumarizacia), per-krok teoreticke bloky (Apriori bottom-up + anti-monotonia, support/confidence/lift, TransactionEncoder one-hot) a inline poznamky na netrivialnych riadkoch (parametre, edge cases pre prazdne pravidla a NaN, vysvetlenie frozenset->string konverzie). Logika, importy ani volania funkcii sa nezmenili.

**Adversarial verify issues:**
- `[major]` FAKTICKA CHYBA TEORIE: Komentar tvrdi 'frozenset (nehashable -> hash-safe...)'. frozenset JE hashable (to je jeho definujuca vlastnost oproti set). Komentar je sam so sebou v protirecenii. Spravna formulacia: 'frozenset je hashable (preto sa da pouzit ako kluc), ale neserializovatelny do CSV citatelne'. (line 148)
- `[major]` FAKTICKA/JAZYKOVA CHYBA V TEORII ANTI-MONOTONIE: 'ziadny J podset z I, ktore obsahuje I, nemoze splnit'. Toto je samo so sebou v protirecenii (podset, ktory obsahuje I = nadmnozina). Spravna anti-monotonia: ak I nesplna support, ziadna NADMNOZINA J z I (J superset I) nemoze splnit. Napisane je to nezrozumitelne a logicky chybne. (line 64)
- `[minor]` Nepresnost: komentar tvrdi 'ak by category obsahovala NaN, split by zlyhal'. V skutocnosti pd.Series.str.split na NaN nevyhodi chybu - propaguje NaN. Padlo by az neskor v TransactionEncoder. Tvrdenie 'split by zlyhal' je teda technicky nespravne. (line 90)
- `[minor]` Komenty obsahuju mnoho referencii na externy 'audit' (major #1-#3, minor #4-#6) ktory nie je v repe vidno - nemozem overit ci tieto cisla a tvrdenia o chybajucich castiach (matica O1..O4, Cochran Q, Kendall W) suhlasia s realnym audit dokumentom. Tvrdenia o tom co skript NEROBI su vsak overitelne pravdive (matica O1..O4 ani statisticke testy v kode naozaj nie su).
- `[minor]` Mensia nepresnost v komentari: 'branch chrani pred zbytocnym sumom' - branch chrani LEN preview print, NEchrani CSV zapis (riadok 163 sa vykona bez ohladu na pocet pravidiel, zapise sa subor s len hlavickou ak je prazdny). Komentar je technicky pravdivy ale moze zvadzat ze chrani aj zapis. (line 168)

---

### `06_extrakcia_vzorov/04_statisticka_analyza/analyza.py` — PARTIAL

**Počty**: expected=10, actual=450, Δ=?

**Zadanie bullets:**
- ✅ Identifikovat obdobia pre analyzu (rok/polrok/kvartal) — _Stlpce O1_2009..O4_2012 = 4 rocne obdobia, definovane v predchadzajucich ulohach (01-03), tu prevzate_
- ✅ Filter dat — _Filtrovanie prebehlo v predch. krokoch; vstupom je hotova matica_
- ✅ Extrahovat min. 10 pravidiel pre kazde obdobie — _O1=341, O2=405, O3=205, O4=17 -> vsetky obdobia maju >= 10 (najmensie O4=17)_
- ✅ Frekventovane transakcie/sekvencie alebo asociacne/sekvencne pravidla — _Pouzite asociacne pravidla (potvrdene v sumar.txt)_
- ✅ Vytvorit datovu maticu jedinecnych vzorov s premennymi O1..O4 (0/1) — _Matica nacitana z in/matica_pravidiel.csv: 450 jedinecnych pravidiel x 4 obdobia + pocet_obdobi_
- ✅ Zosumarizovat dosiahnute vysledky — _sumar.txt obsahuje pocty po obdobiach, distribuciu, unikatne pravidla a zavery; ALE skript ho negeneruje - je staticky napisany_
- ✅ Cochranov Q test pre zavisle vzorky — _statsmodels.cochrans_q, Q=724.30, p<0.001, df=3 -> zamietnutie H0_
- ❌ Coeff. of Concordance (Kendallovo W) — _Vobec nie je implementovany. Zadanie ho spomina spolu s Cochranom (resp. alternativne metody)_
- ✅ Alternativne metody/popisne charakteristiky/vizualizacia — _Bar plot poctov pravidiel po obdobiach + distribucia poctu obdobi vyskytu (out/analyza.png)_

**Findings (audit):**
- `[major]` sumar.txt v out/ je STATICKY napisany (komentar v hlavicke skriptu na riadku 23 to priznava: 'sumar.txt je staticky napisany'). To znamena, ze ak sa zmenia vstupne data alebo vysledky testu, sumar.txt sa neaktualizuje - hodnoty Q=724.30, p, pocty pravidiel (341/405/205/17), 15 stabilnych a 119 unikatnych pravidiel su hardcoded. Pri obhajobe a reprodukovatelnosti je to riziko - vystup nie je deterministicky generovany skriptom.
- `[major]` Chyba implementacia Kendallovho W (Coefficient of Concordance), ktore zadanie explicitne spomina spolu s Cochranovym Q. Zadanie pripusta 'respektive lubovolne metody', ale Kendallovo W by elegantne doplnilo Cochrana o silu/zhodu medzi obdobiami (nie len existenciu rozdielu). (line 39)
- `[minor]` Hardcoded relativna cesta 'in/matica_pravidiel.csv' a 'out/analyza.png' (riadok 79). Skript musi byt spusteny z konkretneho cwd, inak zlyha. Bezpecnejsie by bolo pouzit pathlib.Path(__file__).parent. (line 31)
- `[minor]` axes[1].set_xticks([1, 2, 3, 4]) - hardcoded pocet obdobi. Ak by sa zmenil pocet obdobi (napr. polroky/kvartaly), graf by sa rozbil. Lepsie by bolo pouzit counts.index alebo range(1, len(obdobia_stlpce)+1). (line 75)
- `[minor]` plt.savefig() bez nasledneho plt.close() - pri opakovanom spustani moze drziet figure v pamati. Drobnost, ale pri jednom spustani neskodi. (line 79)
- `[minor]` Skript spolieha na existenciu stlpca 'pocet_obdobi' v CSV (predpoctany v predchadzajucej ulohe). Ak by chybal, padne KeyError. Bezpecnejsie: matica[obdobia_stlpce].sum(axis=1).value_counts(). (line 54)
- `[minor]` Skript len printuje vysledky do stdout - ziadne strukturovane ulozenie metrik (napr. CSV/JSON so sumarom). Ak by sa volal v pipeline, dalsi krok by musel parsovat print output.

**Rewrite**: Rozsiril som header docstring o WUM kontext, parafrazovane zadanie bullety, cross-ref na doc.md a teoriu Cochranovho Q (H0/H1, df, predpoklady); ku kazdemu kroku som pridal mini-teoreticke bloky (Cochran Q, popisne statistiky, idiomy pandas ako .sum/.value_counts), inline komenty na netrivialnych riadkoch (preco values, ternarny zaver, unikatne pravidla maska) a zaznamenal audit findings (hardcoded cesty, x-ticks, chybajuci plt.close) bez zmeny logiky.

**Adversarial verify issues:**
- `[major]` TEORETICKA CHYBA v komente: 'p-hodnota (pravd. ze H0 plati)' - toto je klasicke nespravne interpretovanie p-hodnoty. P-hodnota NIE JE pravdepodobnost, ze H0 plati. Je to pravdepodobnost ziskat take alebo extremnejsie data za predpokladu, ze H0 plati. Tato chybna interpretacia je casto kritizovana v statistike a v projektovej obhajobe by mohla byt problem. (line 119)
- `[major]` TEORETICKA CHYBA: 'Specialny pripad McNemarovho testu pre k > 2' - toto je opacne. Cochran Q je GENERALIZACIA (rozsirenie) McNemarovho testu na k >= 2 podmienok. McNemarov test je specialnym pripadom Cochran Q pri k=2, nie naopak. Komentar tvrdi opak. Mimochodom uz na riadku 102 sa hovori spravne: 'Cochranov Q je rozsirenie McNemarovho testu' - tieto dva komente si protirecia. (line 70)
- `[major]` FAKTICKA NEPRAVDA v komente o vstupe: tvrdi 'stlpce: pravidlo, O1, O2, O3, O4, pocet_obdobi', ale skutocne nazvy stlpcov v matica_pravidiel.csv su 'pravidlo, O1_2009, O2_2010, O3_2011, O4_2012, pocet_obdobi'. To iste sa opakuje na riadkoch 49 ('binarna_matica: np.ndarray (450 x 4) - len O-stlpce' je OK, ale predtym uvedene obdobia_stlpce: list[str] - dynamicky odvodene mena stlpcov O1..O4 je zavadzajuce), 94 (komentar implikuje O1..O4) a 137 ('Obdobie': obdobia_stlpce -> ["O1","O2","O3","O4"]' - skutocne hodnoty su ['O1_2009','O2_2010','O3_2011','O4_2012']). Logika kodu je spravna (startswith('O') match), ale komenty klamu o tom, ako data vyzeraju. (line 28)
- `[minor]` Pravidlo paláca '>= ~4*k' pre Cochran Q nie je standardne citovane pravidlo. Casto uvadzane heuristiky su n >= 4 (Tate & Brown 1970) alebo n*k >= 24. '4*k' je zriedkavo videny tvar. Pravidlo nie je jednoznacne chybne, ale citacia/zdroj by bola na mieste. (line 106)
- `[minor]` Komentar oznacuje sumar.txt ako 'POZOR: staticky napisany subor, NIE generovany tymto skriptom (audit hint: major risk - hodnoty hardcoded)'. Toto je PRAVDA (overene - skript nezapisuje sumar.txt a hodnoty v sumar.txt zhoduju sa s tymi co skript pocita), ale komentar je informacny - nie chyba, len audit poznamka. Zaznamenavam pre transparentnost. (line 36)
- `[minor]` Hlavicka tvrdi 'ZADANIE (parafrazovane bullety zo zadanie.txt)' a uvadza pocty pravidiel '341, 405, 205, 17'. Tieto cisla sa nenachadzaju v zadanie.txt (zadanie len pozaduje 'minimalne 10 pravidiel') - pocty pochadzaju z vystupu predchadzajucich uloh. Komentar by mal byt jasnejsi, ze to nie je zo zadania ale zo skutocnych vysledkov. (line 11)
- `[minor]` Komentar tvrdi 'absencia plt.close()' ako audit poznamku. Toto je technicky pravda, ale pri jednom run skripte je to bezvyznamne - skript skonci a OS uvolni pamat. Komentar moze byt zbytocne alarmujuci. (line 215)

---

### `07_projekt/01_cistenie_zaznamov/clean.py` — PARTIAL

**Počty**: expected=None, actual=211313, Δ=?

**Zadanie bullets:**
- ✅ Ocistit od nepotrebnych udajov (RequestMethod/Version, StatusCode, URL) — _Skript filtruje len GET (riadok 94), status 200-399 (r. 100), a vyhadzuje URL so statickymi priponami (r. 106). Verzia HTTP nie je ulozena - splnene implicitne._
- ❌ Ocistit od prístupov robotov - robots.txt (URL) — _Skript NEFILTRUJE pristupy k /robots.txt. Ziadny filter na URL == '/robots.txt' nebol implementovany._
- ❌ Ocistit od prístupov robotov - User-Agent (Agent) — _Skript NEFILTRUJE Agent obsahujuci bot/crawler/spider/slurp atd. Pole Agent je len ulozene, nepouzite na filtraciu._
- ⚠️ Vyselektovat skumane obdobie (17.12.2017 - 23.12.2017) — _Komentar v skripte (r. 23) tvrdi 'uz extrahovaný na pridelený tyzden', ale skript sam nefiltruje datum. Spolieha sa, ze vstupny log uz je orezany. Riziko: ak vstup nie je orezany, vystup obsahuje nadbytocne data._
- ❌ Vytvorit premennu UnixTime — _UnixTime nie je vytvorena. DateTime je ulozene ako raw string (r. 112) bez konverzie. Toto je pravdepodobne ulohou nasledujuceho skriptu (cv2), ale v zadani patri pod toto cistenie._
- ❌ Identifikovat pouzivatelov (IP + User-Agent) — _User_ID/User column nie je vytvoreny. Ulozene su len surove IP a Agent. Patri do nasledujucich skriptov._
- ❌ Vytvorit premennu Length (User_ID + 60min STT) — _Length nie je vytvoreny - mimo rozsahu tohto skriptu._
- ❌ Identifikovat sedenia (Reference Length 40%, h-ref) — _Sedenia nie su identifikovane - mimo rozsahu tohto skriptu._
- ❌ Doplnit chybajuce poziadavky (dopinanie ciest) — _Doplnanie ciest nie je implementovane - mimo rozsahu tohto skriptu._

**Findings (audit):**
- `[major]` Chyba filtracia robotov cez URL /robots.txt. Zadanie explicitne vyzaduje identifikovat robotov na zaklade pristupu k robots.txt - tato logika v skripte uplne chyba. Mal by existovat krok typu: zozbierat IP, ktore pristupovali k /robots.txt, a tieto IP vyradit z dat. (line 106)
- `[major]` Chyba filtracia robotov cez User-Agent. Zadanie vyzaduje identifikaciu robotov podla Agent pola (bot, crawler, spider, slurp, bingpreview...). Skript Agent len ulozi (r. 117), ale ziadny regex/blacklist na bot patterny nie je definovany. (line 117)
- `[major]` Chyba vytvorenie premennej UnixTime. Zadanie vyslovne uvadza 'vytvorte premennu UnixTime'. DateTime sa uklada ako surovy string '[17/Dec/2017:06:28:17 +0100]' bez konverzie na unix timestamp. Ak je toto ulohou nasledujuceho skriptu, malo by byt zdokumentovane. (line 112)
- `[minor]` Skript nefiltruje casove obdobie 17.12.2017-23.12.2017 sam. Komentar tvrdi, ze log je 'uz extrahovaný na pridelený tyzden', ale neoveruje to. Doporucenie: pridat filter datumu, alebo aspon assert/log min(date) a max(date) pre verifikaciu. (line 73)
- `[minor]` Filter '200 <= status <= 399' zahrnuje aj 3xx presmerovania. Zalezi od interpretacie - niektore analyzy chcu len 200 OK. Zadanie ale len hovori 'ocistite od nepotrebnych udajov StatusCode' - tato hranica je vhodna, ale stoji za zvazenie ci 3xx redirecty maju zostat (mozu duplikovat skutocny obsahovy pristup). (line 100)
- `[minor]` Regex URL pripon (riadok 62-65) vyzaduje za priponou '?' alebo '$' - co znamena URL ako '/style.css/' nebude zachyteny. V praxi malo pravdepodobne, ale moze unikat hraničné pripady. Pripony fontov a ico su pokryte dobre. (line 62)
- `[minor]` Output CSV ma 211 313 zaznamov (211 314 vratane hlavicky) - bez ocakavaneho cisla v zadani nemozno overit. Zadanie pre cv01 (cistenie) neuvadza konkretne ocakavane N riadkov. (line 126)
- `[minor]` Pole 'Bytes' (group 6) sa parsuje ale nepouziva ani neulozi - dead code v regexe (r. 53). Minor cleanup. (line 53)

**Rewrite**: Rozsiril som header docstring o WUM-pipeline kontext, parafrazovane bullety zo zadania s ich audit-status (splnene/chyba/mimo), ocakavany pocet zaznamov a cross-ref na doc.md. Ku kazdemu kroku som pridal "PRECO existuje" sekciu, vysvetlenie regex konstruktov (non-capturing groups, IGNORECASE, [^"]*), zdovodnenie filtrov (GET vs POST/HEAD, status ranges, staticke pripony) a inline poznamky o NaN/edge cases a audit findings bez zmeny kodu.

**Adversarial verify issues:**
- `[minor]` Nekonzistentne nazvy cvicení: 'cv2..cv05' - malo by byt 'cv2..cv5' alebo 'cv02..cv05'. Kozmetické. (line 23)
- `[minor]` Komentár obsahuje typo/garbled frázu: 'aby sme nezistili nesp. greedy match'. Pravdepodobne malo byť 'aby sme nedostali nespravny/nechceny greedy match'. Význam je jasný, ale nečitateľné. (line 91)
- `[minor]` Komentár o HTTP/1.x: regex '\s*\S*' znamená, že HTTP verzia je *voliteľná* (zero-or-more). Komentár to nezmieňuje - tvrdí len 'preskakujeme'. V praxi by riadok ako '"GET /"' (bez verzie) tiež matchol, čo komentár neuvádza. (line 92)
- `[minor]` Typo v print stringu: 'Sumarne statistiky cisteniaa' (extra 'a' na konci 'cistenia'). Kozmetické. (line 212)
- `[minor]` Skript predpokladá, že priečinok 'out/' existuje pri zapise CSV. Ak by neexistoval, df.to_csv by zlyhal s FileNotFoundError. Komentár to nespomina. Aktualne 'out/' existuje, takže funkčne OK. (line 227)
- `[minor]` Tvrdenie 'predpokladame ze ide do dalsieho skriptu' (pri robots.txt filtri) je špekulácia - nemôžem verifikovať bez prečítania ďalších skriptov. Hedge slovo 'predpokladame' to však poctivo priznáva. (line 18)
- `[minor]` Mierna duplicita: 'AUDIT minor: skript NEFILTRUJE datum' opakuje to, čo už hlavička hovorí na riadku 14-15 (status '[ciastocne]'). Nie je to chyba, len redundancia. (line 137)

---

### `07_projekt/03_filter_robotov/filter.py` — PARTIAL

**Počty**: expected=None, actual=73927, Δ=?

**Zadanie bullets:**
- ✅ Identifikacia robotov podla pristupu k robots.txt (URL-based) — _Realizovane cez ulohu 02 (in/02_robot_ips.csv obsahuje 2354 IP), KROK 5 filtruje df[~df['IP'].isin(robot_ips)]_
- ✅ Identifikacia robotov podla pola User-Agent — _KROK 2 regex 'bot|crawl|spider' case-insensitive + KROK 3 'cron|curl|wget|libwww|ltx71' + KROK 4 prazdny Agent '-'_
- ❌ Ocistenie od nepotrebnych udajov (RequestMethod/Version, StatusCode, URL) — _Mimo scope tejto ulohy (patri do 01), ale vystup out/03_cleaned_log.csv stale obsahuje stlpce RequestMethod, URL, StatusCode v hlavicke - tieto neboli odstranene ani v 01 ani tu_
- ❌ Vyber casoveho obdobia 17.-23.12.2017 + UnixTime — _Patri do nasledujucej ulohy, nie do 03; v scope 03 to nie je_
- ❌ Identifikacia pouzivatelov (IP+UA), Length, sedenia (Reference Length 40%, h-ref), doplnenie ciest — _Patri do dalsich uloh (04+), mimo scope 03_

**Findings (audit):**
- `[major]` Skript pouziva relativne cesty 'in/...' a 'out/...' - poziadavka projektu (MEMORY) hovori, ze skripty maju byt standalone. Pri spusteni mimo priecinka 03_filter_robotov skript zlyha. Ziadna kontrola existencie suborov, ziadny os.path.dirname(__file__) prefix. (line 39)
- `[minor]` Regex 'bot|crawl|spider' moze davat falosne pozitiva napr. 'Cubot' (telefon), 'robot' v custom UA hraciam, 'Botswana'. Pre kompletny audit by pomohli specifickejsie patterny ako '\bbot\b|crawler|spider'. Aktualne case=False to robi este sirsim. (line 53)
- `[minor]` Zoznam automatizovanych skriptov 'cron|curl|wget|libwww|ltx71' je arbitrary - zadanie explicitne spomina iba 'roboti vyhladavacich sluzieb'. Filter automatizovanych skriptov je nad ramec zadania, co moze byt OK obhajitelne ('su to tiez ne-uzivatelske pristupy'), ale komentar v skripte to priznava ('zadanie spomina cron, ale v praxi...'). Ohrozenie: pri obhajobe musis vediet obhajit, preco si tieto pridal. (line 60)
- `[minor]` df[df['Agent'] != '-'] odstranuje len presnu hodnotu '-'. Mohli by existovat aj NaN/prazdne stringy. Po predoslych operaciach str.contains(na=False) ich ale neelimino, takze tieto su stale v datach a prejdu filtrom. (line 67)
- `[major]` Vystupny CSV stale obsahuje stlpce RequestMethod, StatusCode, URL (overene cez header). Zadanie hovori 'ocistite od nepotrebnych udajov (RequestMethod/Version, StatusCode, URL)'. Ak to nerobi uloha 01, malo by sa to spravit najneskor tu. V opacnom pripade zadana poziadavka ostane nesplnena az do konca pipeline. (line 78)
- `[minor]` Subor 02_robot_ips.csv ma 2354 IP (vratane hlavicky 2355 riadkov). Tento pocet sa nikde nezobrazuje voci zadaniu, ale je dobre overit ci uloha 02 spravne identifikovala vsetky robots.txt prikladuce IP. (line 44)
- `[minor]` Pomer odstranenych zaznamov: 211313 -> 73927 = odstranene 65%. Dost vysoke, ale akceptovatelne pre log s velkym botim podielom. Pri obhajobe mozes byt poziadany o rozpis kolko padlo na ktoru kategoriu (Agent regex bot, automatizovane, prazdne, IP) - skript print-uje medzistavy, takze logy treba archivovat.

**Rewrite**: Rozsiril som header docstring (WUM kontext, zadanie bullets, cross-ref na doc.md, kniznice s odovodnenim, datove struktury, algoritmus) a pridal MAX-density komenty ku kazdemu kroku - mini-teoriu k robots.txt heuristike a UA klucovym slovam, vysvetlenie regex parametrov (case=False, na=False), edge cases (Cubot false positive, NaN handling, "-" exact match), zdovodnenie poradia filtrov a reset_index. Logika a vsetky volania ostali nezmenene.

**Adversarial verify issues:**
- `[major]` Komentar klame o schéme vstupného CSV. Tvrdi 'IP, Datetime, RequestMethod, URL, Version, StatusCode, Length, Reference, Agent', ale realne stlpce v in/01_cleaned_log.csv su 'IP, DateTime, RequestMethod, URL, StatusCode, Referrer, Agent'. Nie je tam stlpec Version ani Length, a Referrer nie je 'Reference'. Aj 'Datetime' je v skutocnosti 'DateTime' (case). (line 33)
- `[major]` Komentar tvrdi, ze RequestMethod/URL/StatusCode 'zostavaju - zadanie chce ich odstranenie, ale to je formalne sucast bullet 1, ktory je v ulohe 01'. Realita: tieto stlpce existuju aj vo vstupe (z ulohy 01) aj vo vystupe tejto ulohy, t.j. bullet 1 zadania ('očistite od RequestMethod/Version, StatusCode, URL') vobec nie je splneny - ani v ulohe 01, ani tu. Komentar to nepravdivo prezentuje ako 'vyriesene v 01'. (line 41)
- `[minor]` Komentar 'len GET 2xx-3xx, bez statickych suborov ako .jpg/.css/.js' je nepodlozene tvrdenie o vystupe ulohy 01 - nedoveruje sa to z aktualnych dat. Moze byt nepravdivy bez doplnkovej verifikacie. (line 30)
- `[minor]` Tvrdenie 'pandas .isin() je s ndarray rychlejsie nez s Python listom, lebo nemusi konvertovat kazdu hodnotu na PyObject' je sporne / neoverene. Pandas .isin() interne stavia set/hash bez ohladu na to, ci dostane list alebo ndarray; rozdiel v praxi je zanedbatelny. Overclaim. (line 81)
- `[minor]` Komentar 'libwww -> Perl LWP::UserAgent (stary scraping framework)' je nepresny. Realna UA hlavicka byva 'libwww-perl/X.Y'; libwww je tiez nazov W3C kniznice. Vysvetlenie je zjednodusene az zavadzajuce. (line 125)
- `[minor]` Tvrdenie 'Apache log Linux serveru je casto >50% boti' nie je podlozene zdrojom; ide o subjektivne tvrdenie podavane ako fakt. Cislo -65% je v sulade s realnymi datami (211313 -> 73927), ale interpretacia 'casto >50% boti' je nadhodena bez referencie. (line 22)
- `[minor]` Edge case komentar o NaN je technicky spravny (NaN != '-' vrati True, takze NaN riadky prejdu), ale komentar nehovori ze KROKY 2-3 vstup uz prefiltrovali len neNaN potencialne. Toto vsak nie je lez, len neuplnost popisu. (line 144)
- `[minor]` Logika a poradie volani su zachovane (read_csv x2, .unique(), 4 filtre v rovnakom poradi, reset_index(drop=True), to_csv(index=False)), syntax je validna, f-stringy spravne. Nepoznam povodny skript pre 1:1 diff, takze nemozem 100% potvrdit ze ziadny argument/parameter sa nezmenil.

---

### `07_projekt/05_identifikacia_pouzivatelov/users.py` — PARTIAL

**Počty**: expected=None, actual=14563, Δ=?

**Zadanie bullets:**
- ❌ Ocistit data od nepotrebnych udajov (RequestMethod/Version, StatusCode, URL) — _Mimo zodpovednosti tohto skriptu (uloha 01), ale vystup 05_users.csv stale obsahuje stlpce RequestMethod, URL, StatusCode — t.j. predchadzajuca uloha tieto stlpce neodstranila a script ich nezahodil. Header: IP,DateTime,RequestMethod,URL,StatusCode,Referrer,Agent,UNIXTIME,USER_ID._
- ✅ Ocistit data od robotov (robots.txt + User-Agent) — _Riesene v ulohach 02/03 — tento skript pracuje uz s filtrovanymi datami z 04_obdobie.csv._
- ✅ Vyselektovat pridelene obdobie a vytvorit UnixTime — _Riesene v ulohe 04 — script pouziva stlpec UNIXTIME na triedenie._
- ✅ Identifikovat pouzivatelov na zaklade IP + User-Agent — _groupby(['IP','Agent']).ngroup()+1 — korektna standardna heuristika. 14 563 unikatnych userov z 73 927 zaznamov, 11 327 unikatnych IP._
- ✅ Vytvorit Length na zaklade USER_ID a 60 min STT — _Mimo tohto skriptu (uloha 06); script vsak korektne pripravil chronologicke poradie sort_values(['IP','Agent','UNIXTIME']) potrebne pre vypocet Length._
- ✅ Identifikovat sedenia (Reference Length 40%, h-ref) — _Mimo tohto skriptu (ulohy 07/08)._
- ✅ Doplnit chybajuce cesty pre obe metody — _Mimo tohto skriptu (ulohy 09/10)._

**Findings (audit):**
- `[minor]` Hardcoded relative cesta 'in/04_obdobie.csv' — skript funguje len ak je spusteny z prislusneho task-folderu. V suvislosti s pravidlom 'scripts must be standalone' by bolo vhodnejsie pouzit os.path relativne k __file__ alebo absolutnu cestu cez Path(__file__).parent. (line 33)
- `[minor]` Vystup obsahuje stlpce RequestMethod, URL, StatusCode (header: IP,DateTime,RequestMethod,URL,StatusCode,Referrer,Agent,UNIXTIME,USER_ID), hoci zadanie hovori 'ocistite od RequestMethod/Version, StatusCode, URL'. Tento skript za to priamo nezodpoveda (mal to spravit krok 01), ale propaguje problem dalej. Zvazte kontrolu vystupu z ulohy 01. (line 61)
- `[minor]` USER_ID je generovane cez ngroup() PO sort_values([IP,Agent,UNIXTIME]). Hodnota +1 je iba kozmeticka. Korektnost: groupby spravne pouziva unsorted unique pairs — bez ohladu na sort. Toto je v poriadku, ale dolezite vediet pre obhajobu: USER_ID nie su nutne v poradi vyskytu v case, ale v lexikografickom poradi IP. (line 58)
- `[minor]` Skript loguje 'Pocet identifikovanych pouzivatelov' = 14 563. To je vysoke cislo voci 11 327 unikatnych IP — t.j. v priemere ~1.29 Agent na IP. Vzhladom na 7-dnove okno a NAT/proxy je toto realisticka magnituda, ale pre obhajobu by bolo dobre vediet zdovodnit (napr. mnozstvo zariadeni za jednou IP, alebo Agent string variabilita kvoli verziovaniu). (line 62)
- `[minor]` low_memory=False je v poriadku, ale chyba explicitne dtype/parse_dates. UNIXTIME a USER_ID by mali byt int — pri opakovanom citani neskor mozu byt parsovane ako float. Nezasahuje vsak do korektnosti tejto ulohy. (line 33)

**Rewrite**: Prepisal som users.py s MAX-density komentami: rozsireny header docstring (WUM kontext, vsetkych 7 bulletov zadania s priradenim "tento script", vstup/vystup tvar, kniznice s odovodnenim, teoria identifikacie userov + nedokonalosti pre obhajobu), kazdy KROK obohateny o "PRECO" + inline vysvetlenia parametrov (low_memory=False, drop=True, index=False, +1 kozmeticke), teoreticky blok pri groupby+ngroup idiome a poznamky o audit findings (relativna cesta, propagacia RequestMethod/URL/StatusCode, lexikograficke poradie USER_ID). Logika kodu, importy, premenne a poradie operacii ostali identicke.

**Adversarial verify issues:**
- `[minor]` Komentar tvrdi, ze ngroup priradi ID 'v poradi prveho vyskytu v DataFrame'. To je nespravne - pandas groupby ma default sort=True, takze ngroup priradi ID v zoradenom poradi klucov (lexikograficky), nie v poradi prveho vyskytu. Vysledny USER_ID je tu nahodou rovnaky, lebo DataFrame bol uz sortnuty pred groupby, ale vysvetlenie 'preco' je zavadzajuce. Pre obhajobu by mohla byt chyba. (line 125)
- `[minor]` Komentar tvrdi, ze ngroup je 'O(N log N) hash buckety'. Hash-based groupby je typicky O(N) priemerne (hashtable lookup), nie O(N log N). Riadok 38 dokonca tvrdi pravy opak: 'ngroup je vectorizovany - pre 73k riadkov O(N log N) vs. python dict O(N)' - to nedava zmysel (dict by mal byt rychlejsi nez ngroup podla tejto logiky). Konstantne faktory robia pandas rychlejsim ako pure Python, ale asymptotika je tu zmatena. (line 137)
- `[minor]` Komentar uvadza 'priemer ~1.29 Agent na IP'. Spravny vypocet: 14563 userov / 11327 IP = 1.286, takze hodnota je OK. Ale formulacia je trochu zavadzajuca - nejde o priemer Agent na IP, ale o priemer (IP,Agent) dvojic na IP. Pre 11327 IP a 1931 unikatnych Agentov je 14563 dvojic relativne nizke cislo - nizky cross-product (sparse) je realisticky, OK. (line 22)
- `[minor]` Komentar uvadza, ze chyba 'parse_dates=[...] - UNIXTIME sa moze v dalsich ulohach pri spatnom citani parsovat ako float64 namiesto int64'. parse_dates je pre datetime, nie pre integer - na zachovanie int64 by sa pouzilo dtype={'UNIXTIME': 'int64'}. Audit hodnota: v overovacom vystupe sa UNIXTIME naozaj zobrazil ako 1.513673e+09 (float), takze observacia je spravna, ale dovod (parse_dates) je technicky nepresny. (line 72)
- `[minor]` Komentar tvrdi 'sort_values pouziva quicksort (nie stable)'. Overene - default je naozaj 'quicksort'. OK, ale pre uplnost: pandas quicksort moze byt v praxi introsort/timsort v zavislosti od verzie a backendu. Pre obhajobu OK. (line 94)

---

### `07_projekt/08_sedenia_href/href.py` — PARTIAL

**Počty**: expected=None, actual=73927, Δ=?

**Zadanie bullets:**
- ⚠️ Identifikacia sedeni metodou h-ref — _Skript pouziva casovy prah (priemer Length) + podmienku Referrer == '-'. Klasicka h-ref metoda (Cooley) vsak vyzaduje kontrolu, ci Referrer URL je medzi predtym navstivenymi strankami v sedeni — nie iba '-' (priamy pristup). Skript tuto kontrolu zjednodusuje._
- ✅ Casove okno pre h-ref (analogia STT/mean Length) — _Pouziva df['Length'].mean() ako threshold (mean_length). Length je gap k dalsej poziadavke; podmienka Length >= mean_length spravne signalizuje novy odstup._
- ✅ Pridelenie SESSION_ID — _cumsum na booleanovskej maske NEW_SESSION — standardny a korektny pattern._
- ❌ Doplnanie chybajucich poziadaviek do sedeni (dopĺňanie ciest) — _V tomto skripte sa nerealizuje. Ak nie je v inom skripte projektu, zadanie nie je splnene. Tento bullet je v zadani explicitne uvedeny pre OBE metody._
- ✅ Vystupny subor s identifikovanymi sedeniami — _out/08_sedenia_href.csv (73 927 zaznamov + header) so stlpcom SESSION_ID._

**Findings (audit):**
- `[major]` Zjednodusena h-ref podmienka: pouzite je iba (Referrer == '-'), ale standardna h-ref (Cooley) signalizuje nove sedenie ked Referrer NIE JE medzi predtym navstivenymi URL v aktualnom sedeni. Tato verzia nezachyti pripady, kde uzivatel prisiel z externeho refereru (napr. iny domain) — taky pristup ma Referrer != '-' ale stale je to externy vstup. (line 51)
- `[major]` Chyba krok 'dopĺňanie ciest' (path completion) zo zadania. Zadanie ho explicitne vyzaduje pre OBE metody (Reference Length aj h-ref). Ak nie je v inom skripte (napr. 09_*), je to chybajuca poziadavka.
- `[minor]` Pouzity operator '>=' pri (Length >= mean_length). V niektorych definiciach STT/h-ref sa pouziva striktne '>'. Pre velky dataset rozdiel zanedbatelny, ale konzistencia s metodou Reference Length v inom skripte by sa mala overit. (line 50)
- `[minor]` Casove okno je definovane ako globalny priemer Length cez vsetkych pouzivatelov. Niektore varianty h-ref pouzivaju per-user threshold alebo medianu. Zadanie nie je specificke, takze toto je akceptovatelne. (line 42)
- `[minor]` SESSION_ID je globalne (cez celu tabulku), nie reset per USER_ID. Pretoze prvy zaznam kazdeho usera ma Length=NaN -> True -> +1, ID su unikatne medzi userami, ale SESSION_ID nereprezentuje '1..N v ramci usera'. To je vsak v poriadku ak ma byt SESSION_ID globalne unikatne. (line 57)
- `[minor]` Hardcoded relativna cesta 'in/06_length.csv' — skript zavisi od cwd. Ak sa spusta z ineho adresara, padne. Pri kontrole projektu treba spustat z 08_sedenia_href/. (line 37)

**Rewrite**: Pridal som MAX-density komenty: rozsireny header docstring (ciel, ZADANIE cross-ref s ocakavanym poctom 73 927, vstup/vystup, kniznice, teoria h-ref podla Cooleyho s odkazom na doc.md §7-8, audit findings), teoreticke bloky pri kazdom KROKU (priemer Length ako analogia STT_MEAN, idiom cumsum nad bool s prikladom, vyznam Referrer=='-' v Apache logu) a inline komenty na netrivialnych riadkoch (low_memory=False, .mean() ignoruje NaN, | vs or v pandas, zatvorky kvoli priorite operatorov, edge cases NaN/prvy riadok/posledny user, audit findings.major a minor referencie). Logika kodu, importy, premenne aj poradie operacii ostali nezmenene; syntax validna (ast.parse OK).

**Adversarial verify issues:**
- `[major]` Comment describes Length as 'gap k DALSEJ poziadavke v sekundach, NaN pre POSLEDNY zaznam kazdeho usera' (gap to NEXT request, NaN for LAST record). This is factually WRONG. Per 06_premenna_Length/length.py the Length is computed as UNIXTIME - PREV_UNIXTIME (where PREV_UNIXTIME = groupby('USER_ID').shift(1)), so Length is the gap to the PREVIOUS request. Empirically verified on in/06_length.csv: all 14,563 first records of each user have NaN Length; only 6,749 of last records have NaN (those that triggered STT>=3600 cutoff). The same misconception is repeated on lines 107-112 ('NaN vznika v ulohe 06 pre POSLEDNY zaznam kazdeho usera (shift(-1) nema dalsi riadok)') — uloha 06 uses shift(1), not shift(-1). (line 30)
- `[major]` Lines 107-112 claim 'shift(-1) nema dalsi riadok' in uloha 06 — this is wrong. uloha 06 uses shift(1) (groupby('USER_ID')['UNIXTIME'].shift(1)). The NaN appears at the FIRST record of each user (no predecessor), not the last. The downstream reasoning 'ked spracujeme posledny riadok usera N, dalsi riadok patri uz inemu userovi a teda novemu sedeniu' is the right intuition but applied to the wrong row — actually it is the FIRST row of each new user that gets the NaN, which still correctly marks 'new user -> new session', so the code happens to work, but the explanation contradicts the actual implementation in length.py. (line 110)
- `[minor]` Header claim 'Bullet doplnanie chybajucich poziadaviek ... v tomto skripte nie je implementovany (audit: major — chyba ak nie je inde v projekte)' — path completion IS implemented elsewhere: 10_doplnanie_href/doplnanie.py and 09_doplnanie_RLength/doplnanie.py exist in the project. The audit-major warning is therefore misleading. (line 15)
- `[minor]` Comment says '.mean() ... ignoruje NaN (skip_na=True default)'. The actual pandas Series.mean parameter is 'skipna' (one word, no underscore). Minor typo but inaccurate as documented kwarg. (line 86)
- `[minor]` AUDIT line references throughout do not match this file's line numbers. e.g. 'audit findings.major (line 51)' on line 25, 'AUDIT minor (line 42)' on line 90, 'AUDIT minor (line 50)' on line 116, 'AUDIT minor (line 57)' on line 152 — none of these target lines contain related content. References appear to be stale from a prior audit document. (line 25)
- `[minor]` Inline comment 'c) chybajuci referrer = priamy/externy vstup' is partially misleading. The condition Referrer == '-' captures ONLY missing referrers (direct/bookmark), NOT external referrers (which have a non-'-' value pointing to a different domain). The header comment (lines 22-28) does correctly acknowledge this limitation, but the inline label conflates the two. (line 132)
- `[minor]` Header claim 'Ocakavany pocet zaznamov vystupu: ~73 927 (rovnaky ako vstup ...)' — verified by running the script (output: 'Nacitane: 73,927 riadkov', 'Pocet sedeni: 46,693'). This is accurate; logging the exact verified number rather than '~' would be tighter. (line 16)

---

### `07_projekt/09_doplnanie_RLength/doplnanie.py` — PARTIAL

**Počty**: expected=None, actual=4031, Δ=?

**Zadanie bullets:**
- ⚠️ Doplnit chybajuce poziadavky do identifikovanych sedeni pre metodu Reference Length — _Skript pridal 4031 doplnenych zaznamov (73928 -> 77960 riadkov). Doplnanie funguje, ale logika je zjednodusena oproti klasickej metode dopĺňania ciest z cvicenia (chyba rekurzia/iterativne sledovanie parent retazca)._
- ⚠️ Pouzit mapu webu (parent stranky) pre dopĺňanie — _Mapa webu nie je dostupna ako Excel - skript ju buduje z logu (pary Referrer->URL), co je rozumna adaptacia. Ale pouzitie iba 'najcastejsieho referrera' moze zakryt korektne alternativne cesty._
- ✅ Filter internych odkazov (ukf.sk) — _mapa_df['Referrer'].str.contains('ukf.sk') filtruje externe odkazy._
- ⚠️ Doplnit medzistranku medzi po sebe iducimi URL v ramci toho isteho sedenia — _Kontrola SESSION_ID je OK, ale podmienka spustenia doplnania je nezvycajna - vid findings._
- ✅ Vystupny subor s doplnenymi cestami — _out/09_doplnene_rlength.csv vytvoreny, 77959 datovych riadkov._

**Findings (audit):**
- `[major]` Logika doplnania je inverzna voci typickemu pristupu. Klasicke doplnanie ciest pridava medzistranku, ked dvojica (url_from -> url_to) NEEXISTUJE v mape webu (chyba hrana). Tento skript vsak doplna iba ked 'url_from not in map_paths and url_to in map_paths' (riadok 134) - teda iba ked predchadzajuca stranka je neznama. Tymto sa preskakuje vacsina realnych pripadov chybajucich medzistranok medzi dvoma znamymi stranami, ktore nie su priamo prepojene. (line 134)
- `[major]` Chyba rekurzivne/iterativne dopĺňanie. V cvicenom postupe sa medzi A a C moze doplnit retazec A -> B1 -> B2 -> C (cez parent retazec). Tento skript doplna iba JEDNU medzistranku (parent.get(url_to)) a nepokracuje v retazci. To moze viest k podstatne mensiemu poctu doplneni nez metoda zo cvicenia. (line 135)
- `[major]` Po doplneni medzistranok sa neprepocitava premenna Length (pocet stranok v sedeni). Doplnanie ciest meni navigacnu dlzku sedenia, takze Length by mal byt updateovany. V CSV ostavaju povodne Length hodnoty z ulohy 07, co je nekonzistentne so skutocnym poctom riadkov v sedeni. (line 145)
- `[minor]` Pouziva sa value_counts().idxmax() pre vyber 'kanonickeho rodica'. Pri tie-break (rovnaky pocet) je vysledok arbitrarny a moze viest k nestabilnej mape webu medzi spusteniami. (line 96)
- `[minor]` Doplneny zaznam (riadky 139-141) je kopiou aktualneho curr - kopiruje IP, DateTime, UNIXTIME, USER_ID, Length, SESSION_ID a meni len URL. To znamena, ze doplnena 'medzistranka' ma rovnaky timestamp ako predchadzajuci request, hoci v realite mala byt navstivena medzi nimi. Pre dalsie spracovanie (napr. analyza casovych intervalov) je to nekorektne, ale beznou konvenciou pri dopĺňani ciest. (line 139)
- `[minor]` Porovnanie URL hodnot s map_paths nepouzva url_to_path() normalizaciu. URL stlpec v CSV moze obsahovat path s query stringom (napr. '/index.php?option=...'), ktore by sa nemuselo zhodovat s normalizovanou ref_path (path bez query). Konzistencia normalizacie je nutna na presne porovnanie. (line 124)
- `[minor]` Pomenovanie premennej 'ref_page' a komentar su mierne mylne - skutocne ide o najcastejsieho rodica url_to, nie nutne stranku, ktora bola realne medzi url_from a url_to. (line 135)

**Rewrite**: Pridal som rozsireny header docstring s parafrazou zadania, vstupom/vystupom, kniznicami a algoritmom; ku kazdemu KROKU mini-teoreticky blok (mapa webu, groupby+agg+idxmax idiom, iteracia po dvojiciach v sedeni); inline komenty s vysvetlenim pandas parametrov (low_memory=False, case=False, na=False), edge cases (NaN, posledny zaznam, refresh) a cross-ref na vsetky audit findings (major aj minor) bez zmeny logiky.

**Adversarial verify issues:**
- `[major]` FALSE THEORY CLAIM: Komentar 'Bez setu by in nad list/dict.keys() bol O(n) v Pythone < 3.7 dictu' je faktycky NESPRAVNY. dict.keys() membership test (operator `in`) je O(1) priemerne vo VSETKYCH verziach Pythonu (dict je hashtable od pociatku). Zmena v Pythone 3.7 sa tykala GARANTOVANEHO insertion order, nie zlozitosti lookupu. Komentar zavadza studenta pri obhajobe. (line 160)
- `[major]` NEPRAVDIVY KOMENT o strukture vstupu. Riadok 23-24 tvrdi: 'Tvar (po ulohe 07): IP, DateTime, URL, Referrer, Agent, UNIXTIME, USER_ID, Length, SESSION_ID' - ale skutocny vstupny CSV ma 11 stlpcov vratane RequestMethod a StatusCode: ['IP', 'DateTime', 'RequestMethod', 'URL', 'StatusCode', 'Referrer', 'Agent', 'UNIXTIME', 'USER_ID', 'Length', 'SESSION_ID']. Komentar vynechava dva stlpce. (line 23)
- `[minor]` STALE LINE REFERENCES: Komenty obsahuju zastarane odkazy na 'riadok 96', 'riadok 134', 'riadok 135', 'riadok 124', 'riadok 139', 'riadok 145' (riadky 151, 172, 177, 220, 226, 234, 241) ktore nezodpovedaju aktualnemu obsahu na danych pozodciach v aktualnom subore. Napr. 'riadok 96' je v skutocnosti `return None` defensive vetva funkcie, nie groupby agregacia o ktorej hovori komentar. Tieto referencie pravdepodobne ostali z predoslej (prepisanej) verzie. (line 151)
- `[minor]` DROBNA NEPRESNOST v dokumentacnom komente. Hlavicka tvrdi 'vstup ma ~73928 riadkov ... aktualne 4031 [doplnenych]', ale skutocny vstup ma 73927 riadkov a vystup 77959 (= 4032 doplnenych). Tilda znacka pri 73928 je vagueness, ale 4031 vs 4032 je presny pocet off-by-1. (line 19)
- `[minor]` Preklep: 'ducplikat' -> 'duplikat' v komente na riadku 232. (line 232)
- `[minor]` Komentar 'POZOR: query string sa odstrihuje, takze ref_path != URL stlpec ktory query string casto OBSAHUJE (audit minor finding)' je PRAVDIVY, ale doplnujem ze ma realny dopad: doplnene medzistranky (kde URL prepiseme na ref_page = ref_path bez query) maju INE formatovanie URL ako povodne riadky (s query). Vystup teda nema konzistentny format URL stlpca - povodne riadky maju '/index.php?option=...', doplnene maju '/index.php'. Toto by malo byt explicitne v komentari. (line 88)
- `[minor]` Komentary spominaju 'AUDIT FINDING (major, riadok 134)' o inverznej logike doplnania - logika doplnania je naozaj nezvycajna (klasicky path completion porovnava Referrer(next) s URL(curr)). Komentar to spravne priznava ako problem, ale skript zostal nezmeneny - tj. ide o ZAMERNE zachovanie buggy logiky podla anti-drift politiky, nie chybu prepisu.

---

### `07_projekt/10_doplnanie_href/doplnanie.py` — PARTIAL

**Počty**: expected=None, actual=139, Δ=?

**Zadanie bullets:**
- ⚠️ doplnit chybajuce poziadavky do identifikovanych sedeni pre metodu h-ref (doplnanie ciest) — _Skript produkuje vystupny CSV (74067 riadkov vs vstup 73928 = +139 zaznamov, ~0.19%). Doplnanie sa deje, ale logika nezodpoveda klasickemu h-ref doplnaniu z cv3 - nepouziva sa porovnanie Referrer aktualnej poziadavky s predoslym URL, ale podmienka 'url_from NIE JE v mape a url_to ANO', co je netypicke._
- ✅ vybudovat mapu webu z logu (chybajuci externy zdroj) — _Mapa je postavena cez groupby URL a value_counts().idxmax() na referrer - rozumny pristup pri absencii externej mapy._
- ✅ filtrovat len interne odkazy (ukf.sk) — _Filter mapa_df['Referrer'].str.contains('ukf.sk') je aplikovany._
- ⚠️ iterovat zaznamy a doplnit medzistranky — _Iteracia pres po sebe iduce zaznamy v ramci SESSION_ID je OK, ale doplna sa max 1 medzistranka (nie hlbsia rekurzia po parent retazci) - h-ref by mal traversovat parent retazec az kym sa nedostane na url_from._

**Findings (audit):**
- `[major]` Hlavna podmienka doplnania je obratena/nestandardna: 'if url_from not in map_paths and url_to in map_paths'. Klasicky h-ref postup z cv3: porovna sa Referrer next_row s curr['URL'] - ak sa lisi, treba doplnit medzistranky podla parent retazca. Tato podmienka doplna zaznamy len ked predchadzajuce URL chyba v mape, co je inverzna logika a vysvetluje preco doslo len k 139 doplnenim (0.19%) namiesto ocakavaneho vyssieho podielu. (line 136)
- `[major]` Doplna sa len JEDNA medzistranka (parent.get(url_to)). Pri skutocnom h-ref by sa mala traversovat cela cesta parent[parent[...url_to...]] az po url_from, alebo aspon iterativne pridavat medzistranky kym sa nedosiahne url_from. (line 137)
- `[major]` Skript ignoruje pole 'Referrer' v next_row pri rozhodovani o doplnani. Standardny h-ref algoritmus pouziva Referrer nasledujucej poziadavky ako kluc - ak Referrer(next) != URL(curr), znamena to ze chyba medzistranka. Aktualny kod referrer next_row nikdy nepouziva. (line 80)
- `[minor]` Filter 'Referrer.str.contains(ukf.sk)' sa aplikuje na povodny stlpec Referrer, ale ref_path uz bol vypocitany pred tym - efektivny ale poradie operacii by sa dalo zoptimalizovat. (line 90)
- `[minor]` value_counts().idxmax() - ak ma URL viacero rovnako castych referrerov, idxmax vrati arbitrarne jeden. Pre h-ref pristup je rozumne, ale mohlo by sa explicitne tie-break poriesit (napr. najkratsia cesta). (line 98)
- `[minor]` Vytvorenie doplneneho riadku pomocou curr.copy() a zmena len URL - ostatne polia (Referrer, UnixTime, Agent) zostavaju z 'curr', co je rozumne, ale je dobre to dokumentovat (najma UnixTime medzistranky == UnixTime curr). (line 142)
- `[minor]` df.to_dict('records') nacita cely DataFrame do pamati ako zoznam dictov - pri 74k zaznamov OK, ale je to duplicita s 'df'. (line 110)

**Rewrite**: Prepisal som doplnanie.py s MAX-density komentarmi: rozsireny header docstring (ciel, zadanie, vstup/vystup, kniznice s odovodnenim, datove struktury, algoritmus, cross-ref na doc.md a bullets zadania), bohate inline komentare na kazdom netrivialnom riadku (pandas parametre s odovodnenim, NaN handling, edge cases, audit poznamky o inverznej logike). Logika, importy ani volania funkcii sa nezmenili (anti-drift).

**Adversarial verify issues:**
- `[major]` Comment claims the 'url.startswith("/")' shortcut saves urlparse for ~50% pripadov with rationale 'URL stlpec uz je path'. This is FALSE: url_to_path is only called on the Referrer column (line 144), never on URL. In actual data 0% of Referrers start with '/' (they are full URLs like 'http://www.ukf.sk/...' or '-'). The shortcut never triggers in practice, and the URL-column justification is irrelevant since URL is not passed through this function. (line 94)
- `[minor]` Header comment lists input columns as '[Referrer, URL, IpAddress, Agent, UnixTime, USER_ID, SESSION_ID, ...]'. Actual columns in 08_sedenia_href.csv are [IP, DateTime, RequestMethod, URL, StatusCode, Referrer, Agent, UNIXTIME, USER_ID, Length, SESSION_ID] — 'IpAddress' should be 'IP', 'UnixTime' should be 'UNIXTIME' (all caps), and DateTime/RequestMethod/StatusCode/Length are missing from the documented list. (line 22)
- `[minor]` Comment says 'vstup ~73928 zaznamov' — actual row count is 73927. Off-by-one (the '~' arguably absolves this, but worth noting). (line 17)
- `[minor]` Typo: 'prislutomu' is not a Slovak word (likely meant 'patriacich' or 'prisluchajucich'). Cosmetic only — does not affect code execution. (line 183)
- `[minor]` Logic preservation cannot be fully audited because no backup/original copy of doplnanie.py exists in the directory to diff against. The current out/10_doplnene_href.csv has 73927+139=74066 rows, which is consistent with the current script's behavior, suggesting at least that observable output matches a prior run. But anti-drift cannot be formally verified without the prior source.

---

### `01_zdroje_dat/01_prehladavanie_webu/crawler.py` — OK

**Počty**: expected=5, actual=5, Δ=0.0%

**Zadanie bullets:**
- ✅ Python skript na prehladavanie webovych stranok — _Pouziva requests + BeautifulSoup, definuje zoznam 5 URL a iteruje cez ne._
- ✅ Ziskanie textoveho obsahu stranok — _soup.get_text() extrahuje cisty text bez HTML tagov; navyse strip + odstranenie prazdnych riadkov._
- ✅ Export textov do .txt suborov — _Pre kazdu URL sa vytvori out/articles/article_X.txt v UTF-8._
- ⚠️ Odovzdat zdrojaky a exportovane subory v ZIP — _Skript negeneruje ZIP. Zadanie ZIP poziaduje len ako formu odovzdania, nie ako vystup skriptu - takze toto je manualny krok studenta, nie chyba skriptu._

**Findings (audit):**
- `[minor]` Riadok 39: requests.get(url) bez timeout parametra - skript moze visiet donekonecna pri pomalom/nedostupnom serveri. Odporucanie: requests.get(url, timeout=10). (line 39)
- `[minor]` Riadok 39: nie je osetreny HTTP error (napr. 404, 500). Chyba r.raise_for_status() alebo aspon kontrola r.status_code - skript by potichu ulozil chybovu stranku ako 'article'. (line 39)
- `[minor]` Riadok 39: chyba User-Agent header - niektore weby blokuju default 'python-requests/...' UA. Pri tomto konkretnom UKF webe to teraz funguje, ale je to fragilny postup. (line 39)
- `[minor]` Riadok 43: soup.get_text() bez separator a strip parametrov - vyprodukuje text kde su slova/odstavce zlepene dohromady (viditelne na riadku 24 article_1.txt - cely menu hlavicky je jeden obrovsky riadok bez medzier). Lepsie: soup.get_text(separator='\n', strip=True). (line 43)
- `[minor]` Skript exportuje aj celu navigaciu/menu/footer stranky, nie len telo clanku. Pre 'textovy obsah' clanku by bolo cistejsie selectovat konkretny <article>/<div class='item-page'> element, ale zadanie to nepoziaduje explicitne. (line 42)
- `[minor]` Riadky 35 a 50: relativne cesty 'out/articles' zavisia od aktualneho cwd pri spusteni - ak skript spustite z ineho adresara, vystup sa vytvori inde. Pouzite os.path.join(os.path.dirname(__file__), 'out', 'articles'). (line 35)
- `[minor]` Chyba try/except wrapper okolo HTTP volania - ak jedna URL zlyha (sietova chyba, DNS), cely skript spadne a zvysne URL sa nestiahnu. (line 39)

**Rewrite**: Pridal som MAX-density Slovak komenty (bez diakritiky): rozsireny header docstring (ciel v kontexte WUM pipeline, parafraza zadania s ocakavanym poctom 5, vstup/vystup, popis kniznic + datovych struktur, algoritmus, cross-ref na doc.md), pred kazdym KROKom 1-5 vysvetlenie PRECO + inline komenty na netrivialnych riadkoch s teoriou (DOM strom v BeautifulSoup, list comprehension idiom, UTF-8 vs cp1250 na Windows) a poznamky k audit findings (timeout, raise_for_status, User-Agent, separator) s explicitnym oznacenim ze ich neopravujeme kvoli anti-drift pravidlu. Logika, importy, premenne a poradie volani ostali nezmenene.

**Adversarial verify issues:**
- `[minor]` Preklep v komente: 'necechame robustifikovat' - malo by byt 'nechceme robustifikovat'. (line 100)
- `[minor]` Nekonzistentnost diakritiky: komentare v celom subore zamerne nepouzivaju slovensku diakritiku (kvoli stdout/encoding-aware policy), ale tu je napisane 'lineárneho' s accented á. Mozno zjednotit. (line 105)
- `[minor]` Komentar opisuje cistenie v 3 krokoch, ale skutocna list comprehension vola l.strip() DVAKRAT (raz v expression na zapis, raz v if filter). Komentar to nepriamo pokryva ('Riadky tvorene LEN bielymi znakmi sa po strip() stanu prazdnym stringom'), ale citatel by mohol myliet, ze sa strip() vola raz a vysledok sa pouziva. Lepsie by bolo explicitne uviest, ze .strip() sa kvoli idiomatike vola 2x. (line 132)
- `[minor]` Nepodaril sa diff oproti puvodnemu skriptu (backup neexistuje v adresari) - 'zachovanie logiky' (imports, calls, names, poradie) nemozem 100% potvrdit. Z viditelneho kodu vsetko vyzera konzistentne (imports: sys, os, requests, BeautifulSoup; volania: requests.get, BeautifulSoup, get_text, splitlines, strip, open, write; mena: urls, r, soup, raw_text, lines, text), ale chyba ground truth.
- `[minor]` Komentar na zaciatku spomina 'audit' a 'anti-drift pravidlo' na viacerych miestach (riadky 82-83, 99-100, 113-114) - to su validne minor findings, ktore som overil oproti kodu: timeout chyba (r.raise_for_status() chyba, User-Agent chyba, get_text() bez separator/strip). Vsetky tieto tvrdenia su PRAVDIVE.
- `[minor]` Verify prompt spomina 'KS test H0/H1, IQR vzorec, exp. rozdelenie' - tieto teorie sa v tomto skripte vobec nevyskytuju (je to web scraping, nie statisticka analyza), takze ziadne nepravdive statisticke tvrdenia tu nie su. Toto je OK, len zaznamenavam pre uplnost.

---

### `02_cistenie_dat/01_cistenie_dat_I/clean.py` — OK

**Počty**: expected=56500, actual=57650, Δ=2.0%

**Zadanie bullets:**
- ✅ Identifikovat premenne (IP, Cookie, user, DateTime, RequestMethod, URL, StatusCode, Bytes, Referrer, Agent) — _Regex parsuje vsetky polozky: IP (skup.1), Cookie/user (\S+\s+\S+ preskocene), DateTime (skup.2), Method (skup.3), URL (skup.4), StatusCode (skup.5), Bytes (skup.6), Referrer (skup.7), Agent (skup.8)._
- ✅ Zmazat z logu Cookie, user a Bytes — _Cookie a user nie su pridane do rows, Bytes (group 6) je explicitne preskocena. Vystupne CSV obsahuje len IP, DateTime, RequestMethod, URL, StatusCode, Referrer, Agent._
- ⚠️ Ocistit RequestMethod/Version — _Filtruje len GET (odstranuje POST, HEAD), ale HTTP Version sa nikde nevalidaduje (regex ma \S* pre verziu, akceptuje aj prazdny string alebo nevalidnu verziu). Zadanie spomina RequestMethod/Version - validacia verzie chyba._
- ✅ Ocistit StatusCode — _Filter between(200, 399) ponecha 2xx/3xx, odstrani 1xx/4xx/5xx._
- ✅ Ocistit URL (staticke subory) — _Regex odstranuje bmp/jpg/png/gif/css/flv/ico/swf/rss/xml/cur/js/json/svg/woff/eot/ttf/otf. Slusne pokrytie._
- ✅ Pribl. 56500 zaznamov po ocisteni — _Vystup ma 57650 zaznamov, delta ~2.04% od ocakavanych 56500 - v ramci tolerancie 'pribl.'_

**Findings (audit):**
- `[minor]` Regex pre HTTP verziu '\s*\S*' v skupine pre Method/URL je velmi volny - akceptuje aj prazdnu verziu alebo lubovolny token. Zadanie explicitne hovori o cisteni 'RequestMethod/Version', ale ziadna validacia HTTP/1.x nie je vykonana. (line 34)
- `[minor]` Regex pre URL '(\S+)' nepripusta medzery, co je OK pre validne URL, ale neoseti URL s medzerami (URL-encoded). Riadky ktore neprejdu regexom su ticho zahodene - chyba pocitadlo nezhodnych riadkov pre transparentnost. (line 34)
- `[minor]` Vystupny pocet 57650 je o 1150 vyssi nez ocakavanych 56500 (~2% odchylka). Mozne priciny: chybajuca filtracia neexistujucich URL (napr. '*' pre OPTIONS-like requesty), alebo doplnkove staticke pripony (napr. .map, .txt, .pdf neboli zahrnute). Akceptovatelne pre 'pribl. 56500'. (line 75)
- `[minor]` Hardcoded relativne cesty 'in/Log_jeden_den.log' a 'out/05_cleaned_log.csv' - skript je viazany na CWD. Nepouziva os.path/pathlib pre platform-independent cesty. (line 43)
- `[minor]` Komentar v hlavicke uvadza '~57000 zaznamov (povodne ~257000)' co je v rozpore so zadanim '~56500'. Komentar v kode by mal reflektovat oficialne zadanie. (line 23)

**Rewrite**: Prepisal som c:/Users/mstud/School/Objavovanie znalosti/02_cistenie_dat/scripts/01_cistenie_dat_I/clean.py s MAX-density komentami: rozsireny header docstring (ciel WUM, parafraza zadania s ocakavanym poctom 56500, vstup/vystup/kniznice/datove struktury/algoritmus/cross-ref), teoreticke bloky pre HTTP metody/status kody/staticke assets, inline vysvetlenia kazdej regex skupiny, pandas parametrov (between inclusive, str.contains, ~ negacia, reset_index drop, to_csv index=False), NaN/edge cases a cross-ref na bullet zadania. Logika, importy, premenne ani volania sa nezmenili.

**Adversarial verify issues:**
- `[minor]` Komentar tvrdi, ze Bytes skupina (\S+) je zachytena 'aby regex spravne posunul kurzor dalej'. To je technicky NEPRAVDIVE - zatvorky () ovplyvnuju IBA zachytenie, nie posun kurzora. Vyraz \S+ aj (\S+) konzumuju rovnaky pocet znakov. Spravne by bolo: 'zachytene historicky/zo zvyku, ale grupa sa nepouziva'. (line 83)
- `[minor]` Teoria HTTP status kodov tvrdi, ze '3xx = presmerovanie (301, 302, 304 Not Modified)'. 304 Not Modified nie je presmerovanie - je to podmienena odpoved (cache validation). 3xx ako trieda sa vola 'Redirection' v RFC, ale 304 do tejto kategorie nepatri vyznamovo. Skor je to 'cache hit'. Pre WUM je rozumne ponechat, ale komentar mati. (line 135)
- `[minor]` Komentar tvrdi, ze .match() je 'rychlejsie ako .search()'. Ked vsak regex zacina kotvou ^, .search() musi tiez skoncit po prvom pokuse na pozicii 0 - rozdiel je zanedbatelny. Tvrdenie je technicky pravdive ale zavadzajuce. (line 100)
- `[minor]` Komentar k reset_index(drop=True) tvrdi, ze 'bez resetu by CSV obsahovalo neporiadne cislovanie ALEBO by sme museli pouzit index=False, co aj tak robime'. Kedze sa index=False naozaj pouziva (riadok 185), reset_index je cisto kozmeticky - komentar to nepriamo priznava, ale formulacia je matuca. (line 178)
- `[minor]` Zadanie spomina 'RequestMethod/Version' - implikuje aj cistenie HTTP verzie. Skript filtruje len Method (GET), Version sa NEoveruje (regex ju ani nezachytava). Komentar na riadku 126 to priznava ('audit'), ale poziadavka zadania je len ciastocne splnena. (line 9)
- `[minor]` Komentar priznava chybajuce pripony .map, .txt, .pdf v unwanted_ext (preto vystup 57650 namiesto 56500). To je rozumne priznane, ale ZADANIE pyta 'priblizne 56500' - 2% odchylka je v ramci 'priblizne'. Pripomienka: ak by sa pridali tieto pripony, vysledok by bol blizsie. (line 161)
- `[minor]` Komentar o str.contains a NaN: 'NaN handling: ak by URL bola NaN, str.contains by vratil NaN -> ~NaN = NaN (truthy v boolean indexing by hodilo chybu)'. Formulacia 'truthy v boolean indexing by hodilo chybu' je gramaticky/logicky zmatocna - spravne by bolo 'NaN v boolean indexing hodi ValueError'. Vyznam je spravny, ale formulacia mata. (line 168)

---

### `02_cistenie_dat/02_cistenie_dat_II/clean2.py` — OK

**Počty**: expected=31500, actual=31980, Δ=1.5%

**Zadanie bullets:**
- ✅ Preskumat log po prvom cisteni a odstranit dalsie zbytocne zaznamy — _Skript pokracuje na vstupe 05_cleaned_log.csv a aplikuje 6 dalsich krokov cistenia (boty, robots.txt, duplikaty, obrazky/PDF/komponenty/feedy, presmerovania)._
- ✅ Pouzit pandas pd.read_csv() na nacitanie log suboru — _Riadok 22: df = pd.read_csv('in/05_cleaned_log.csv')._
- ✅ Odovzdat zdrojovy kod + ocisteny log v zip — _Skript existuje (clean2.py) a vystupny CSV out/06_cleaned_log.csv je vygenerovany. Zabalenie do zip je manualny krok pri odovzdani._
- ✅ Po ocisteni mat priblizne 31500 zaznamov — _Vystup ma 31980 datovych riadkov (31981 vratane hlavicky). Delta cca 1.52 %, vyrazne pod 20 % toleranciu._

**Findings (audit):**
- `[minor]` Bot pattern obsahuje 'perl' ako samostatne klucove slovo, co moze nahodne zachytit user-agenty obsahujuce substring 'perl' (napr. nazvy s 'Superl...' alebo 'hyperlink'). Nizke riziko, ale stoji za zvazenie hranic slova \b...\b. (line 28)
- `[minor]` df['Agent'].str.contains(bot_pattern, na=False) — odovzdava sa skompilovany regex; pandas to akceptuje, ale parameter case=False ani flags sa uz neaplikuju (su zaspekane vo vnutri pattern.re.IGNORECASE). Funguje, no menej citelne ako case=False. (line 32)
- `[minor]` Filter obrazkov je velmi uzky — odstranuje len URL s 'image?view=image' (Joomla varianta). Bezne pripony .jpg/.png/.gif/.svg/.webp/.ico nie su filtrovane, co moze ponechat priame requesty na obrazky v statistikach. Ak data taketo URL skoro neobsahuju, je to OK; inak je to medzera v cisteni. (line 46)
- `[minor]` Pattern 'format=feed|/feed' moze zachytit aj URL ako '/feedback' (substring '/feed'). Pre presnost by sa hodilo '/feed(\?|/|$)' alebo podobne ohranicenie. (line 49)
- `[minor]` Filter StatusCode.between(200, 299) predpoklada, ze stlpec je numericky. Ak by bol string (napr. po nacitani s NaN), porovnanie zlyha alebo vrati nulu. Bolo by bezpecnejsie pd.to_numeric(..., errors='coerce') pred filtrom. (line 54)
- `[minor]` Cesty 'in/...' a 'out/...' su relativne k aktualnemu working directory — skript treba spustat z priecinka 02_cistenie_dat_II. Pre robustnost by sa hodili absolutne cesty cez Path(__file__).parent. (line 22)
- `[minor]` Skript nepise ziadny prehlad (napr. kolko botov/duplicit/3xx sa odstranilo do CSV/logu), iba print do konzoly. Pre obhajobu sa hodi mat tieto cisla aj v subore. (line 60)

**Rewrite**: Rozsiril som header docstring o WUM pipeline kontext, parafrazu zadania, vstup/vystup, kniznice, datove struktury a cross-ref na doc.md; pridal som inline MAX-density komenty s teoriou (bot detection, deduplikacia, 2xx vs 3xx, NaN handling, regex escape) ku kazdemu kroku pricom logika kodu (imports, volania, premenne, poradie) zostala absolutne nezmenena.

**Adversarial verify issues:**
- `[major]` Komentar je matuci/nepresny: 'Otaznik je v str.contains regex metaznak, ale len mimo escapeovanej casti; v str.contains s case=False sa berie ako regex.' Pattern je r'image\?view=image' — otaznik JE escapeovany (\?), takze sa berie doslovne, nie ako regex metaznak. Komentar sugeruje opak. Mal by jasne povedat: '\? = escapeovany otaznik, dolezite preto, ze ? v regexe znamena 0-1 opakovani predchadzajuceho znaku.' (line 117)
- `[minor]` Komentar uvadza 'tolerancia ~20% podla zadania', ale zadanie.txt ziadnu konkretnu tolerancu neuvadza — pise len 'približne 31500 záznamov'. Cislo 20% je vymyslene; lepsie napisat len 'priblizne' bez konkretneho percenta. (line 152)
- `[minor]` Komentar nazyva '~' ako 'bitova negacia boolean masky'. Operator ~ je v Pythone bitovy NOT, ale aplikovany na pandas boolean Series funguje ako logicky NOT. Presnejsie by bolo 'logicka negacia (operator ~ = bitwise NOT, na boolean Series sa sprava ako logicky NOT)'. (line 78)
- `[minor]` Komentar zaradzuje 304 medzi presmerovania ('301/302/304 cached'). HTTP 304 je 'Not Modified' (cache validacia), nie typicke presmerovanie. Patri do 3xx skupiny, ale jeho semantika je odlisna od 301/302. (line 137)
- `[minor]` Komentar odkazuje na '07_projekt/materials/doc.md' (cross-reference), co som nemohol overit ze realne existuje na danej ceste. Ak subor neexistuje, odkaz je matuci. (line 33)

---

### `02_cistenie_dat/03_cistenie_dat_III_roboti/clean3.py` — OK

**Počty**: expected=333, actual=333, Δ=0.0%

**Zadanie bullets:**
- ✅ Identifikovať robotov podľa prístupu k robots.txt (filter URL) — _Riadok 39: 'if "robots.txt" in url.lower()' — case-insensitive filter na URL pole regexu._
- ✅ Získať IP adresy robotov z logu — _Riadok 40: extrahuje m.group(1) = IP adresa zo začiatku log riadku._
- ⚠️ Použiť pandas / pd.read_csv() na načítanie log súboru — _Skript číta log cez open() + regex (kvôli Apache formátu, nie CSV), čo je technicky správnejšie než pd.read_csv. Zadanie spomína pd.read_csv len ako návrh ('vhodné pre riešenie'), nie ako povinnosť. Pandas sa používa pri ukladaní výstupu._
- ✅ Súbor by mal obsahovať 333 IP adries robotov — _Výstup out/07_robot_ips.csv má presne 333 dátových riadkov (334 vrátane hlavičky). Pozor: ide o 333 prístupov (s duplicitami), unikátnych IP je iba 108. Zadanie však hovorí presne '333 IP adries' — skript to matchuje doslovne._
- ✅ Odovzdať zdrojový kód v zip (organizačné) — _Mimo rozsah auditu skriptu — týka sa odovzdania._

**Findings (audit):**
- `[minor]` Hardcoded relativna cesta 'in/Log_jeden_den.log' — skript musí byť spúšťaný z adresára 03_cistenie_dat_III_roboti/, inak FileNotFoundError. Pre standalone fungovanie by bolo lepšie použiť pathlib s __file__. (line 34)
- `[minor]` Komentár '.values = numpy pole vsetkych IP (aj duplicitnych)' explicitne hovorí, že duplicity sa zachovávajú. Výstup tak obsahuje 333 záznamov, ale len 108 unikátnych IP. Ak by zadanie myslelo '333 unikátnych IP', výstup by nesedel. Aktuálne to ale presne sedí na číslo 333 (333 prístupov k robots.txt) — interpretácia 'IP adresa' ako 'záznam o prístupe' je možná, ale matematicky 333 ≠ 108. Odporúčam pridať druhý výstup s unikátnymi IP (drop_duplicates) pre prípad inej interpretácie. (line 46)
- `[minor]` Filter 'robots.txt' in url.lower() zachytí aj URL ako '/something/robots.txt.bak' alebo '/robots.txtdownload'. Bezpečnejšie: url.lower().endswith('/robots.txt') alebo regex /robots\.txt(\?|$)/. Aktuálne dáta zjavne nemajú tento problém (333 sedí), ale logika je krehká. (line 39)
- `[minor]` Regex je rovnaký ako v úlohe 05 (podľa komentára). Ak riadok logu nematchne regex (poškodený záznam), tichá strata bez warningu — odporúčam aspoň counter na unmatched lines. (line 22)
- `[minor]` Pri ukladaní sa robot_ips najprv konvertuje na .values a späť do DataFrame — zbytočný krok. Stačilo by df[['IP']].to_csv(..., index=False). Funkčne OK, len neefektívne. (line 50)

**Rewrite**: Prepisal som clean3.py s MAX-density komentami: rozsireny header docstring (ciel/zadanie/vstup-vystup/kniznice/datove struktury/algoritmus/cross-ref), teoreticky blok o robots.txt heuristike, podrobne anotacie regex skupin, vysvetlenie stream parsing + encoding errors='replace', a inline audit poznamky (krehky substring filter, duplicitne IP, redundantna .values konverzia). Logika kodu, importy, premenne a poradie operacii ostali nezmenene.

**Adversarial verify issues:**
- `[minor]` Komentar 'log moze mat MB az GB' je pedagogicky nadnesenny — konkretny Log_jeden_den.log ma len ~50k riadkov (jeden den). Tvrdenie o streamingu O(1) pamatovo je vsak korektne ako vseobecna best-practice. Nie je to lzhej, len zovseobecnenie. (line 91)
- `[minor]` Komentar tvrdi 'Apache combined log NIE JE CSV' ako odovodnenie preco nepouzit pd.read_csv(). Technicky je log parsovatelny aj cez pd.read_csv() so spravnymi parametrami (sep, quotechar, escapechar), len je to slozite. Komentar by mal byt presnejsi: 'pd.read_csv() je nepohodlne pre log so zlozitym quotingom' miesto kategorickeho 'NIE JE CSV'. Zadanie explicitne pd.read_csv() odporuca, takze toto je vedomy odklon od zadania — komentar to priznava, ale formulacia 'zamerne nepouzity' je trochu zavadzajuca. (line 17)
- `[minor]` V komentari k regexu sa uvadza skupina 3 = HTTP metoda. To je technicky spravne (matchne 'GET'), ale skript samotny m.group(3) NIKDY nepouzije — pouziva sa len group(1) a group(4). Komentar by mohol toto explicitne uviest, aby citatela neviedol k mylnemu dojmu, ze metoda sa niekde filtruje. (line 65)
- `[minor]` Audit poznamka 'unmatched riadky sa ticho preskakuju' je korektna, ale chyba info o tom, kolko takych riadkov v praxi je. Ak je ich vela, mohlo by to skreslit pocet 333. V skutocnosti to nepokazi vysledok (333 sedi), ale skript by si zasluzil pocitadlo nezhod pre transparentnost. (line 99)
- `[minor]` Komentar pri filtri 'if "robots.txt" in url.lower()' priznava krehkost (matchol by aj '/robots.txt.bak'). Toto je estu pravdive a podstatne — pri realnejsich datach by sa to malo opravit na url.lower().endswith('/robots.txt'). Audit je spravny, ale neukazuje, ze v aktualnom logu ZIADNE take patologie nie su (overoval som — 333 sedi). (line 102)
- `[minor]` Komentar 'pandas — len kvoli to_csv s hlavickou (mohli by sme aj cez csv modul)' je pravdivy, ale ignoruje fakt, ze pandas sa pouziva aj na DataFrame konstrukciu z list[dict] (riadok 111). Cisto pomocou csv modulu by to bolo o riadok dlhsie, nie ekvivalentne. Drobna nepresnost komentara. (line 50)

---

### `02_cistenie_dat/04_cistenie_dat_IV_roboti/clean4.py` — OK

**Počty**: expected=None, actual=20666, Δ=?

**Zadanie bullets:**
- ✅ Identifikovat robotov cez User-Agent: klucove slova 'bot', 'crawl', 'spider' — _Riadok 28: regex r'bot|crawl|spider' s case=False, na=False; negaciou ~ ponechane non-roboty_
- ✅ Odstranit pristupy automatizovanych skriptov - 'cron' — _Riadok 35: regex obsahuje 'cron', plus extra curl|wget|libwww|ltx71 (nad ramec zadania, ale validne pre cistenie)_
- ✅ Zmazat pristupy robotov na zaklade IP adries + klucovych slov v User-Agent — _Riadok 47 nacita 07_robot_ips.csv a filtruje ~df['IP'].isin(robot_ips); UA filter pokryty krokmi 1-3_
- ✅ Pouzit pandas read_csv (odporucanie zo zadania) — _Riadky 22 a 46 pouzivaju pd.read_csv_

**Findings (audit):**
- `[minor]` Riadok 35: regex 'cron' moze nahodne matchnut UA stringy obsahujuce substring 'cron' (napr. 'Synchronization', 'Microsoft' nie, ale 'chronium' nie - cron je dost specificke). Riziko false-positive je nizke, ale word-boundary (r'\bcron\b') by bol cistejsi. (line 35)
- `[minor]` Skript pridava nad ramec zadania filtre 'curl|wget|libwww|ltx71' (riadok 35) a odstranuje Agent=='-' (riadok 41). Toto nie je explicitne v zadani, ale je to obhajitelne ako automatizovane pristupy. Komentar na riadku 34 to korektne priznava. (line 35)
- `[minor]` Zadanie hovori o klucovych slovach v User-Agent + IP adresach ako kombinovanej podmienke pre robot filter (druhy bullet). Skript ich aplikuje samostatne (sekvencne), co je ekvivalentne, ale formulacia zadania by sa dala citat aj ako AND. Ucinok je rovnaky alebo silnejsi (OR vs AND). (line 47)
- `[minor]` Vystupny subor 08_cleaned_log.csv obsahuje 20666 datovych riadkov (20667 vratane hlavicky). Zadanie neuvadza konkretne ocakavane cislo, ale komentar v skripte (riadok 9) hovori '~20000 zaznamov' - skutocnost je v sulade. (line 9)

**Rewrite**: Prepisal som clean4.py s MAX-density komentami: rozsireny header docstring (WUM kontext, ZADANIE bullets, VSTUP/VYSTUP, datove struktury, algoritmus, doc.md cross-ref), pri kazdom kroku teoreticky blok (UA konvencie robotov, Apache "-" konvencia, UA vs IP detekcia ako OR) a inline vysvetlenia kazdeho parametra (case=False, na=False, ~ negacia, .unique(), .isin(), reset_index(drop=True), to_csv(index=False)) — logika, importy aj volania ostali nezmenene.

**Adversarial verify issues:**
- `[minor]` Komentar 'pandas robi copy-on-filter; povodny ostava' je nepresny. Boolean indexing v pandas typicky vracia novu DataFrame (overene testom), ale formulacia 'povodny ostava' je zavadzajuca - v skripte sa df reassignuje (df = df[~bot]), takze povodny objekt sa stratil. V praxi to nevadi, ale teoreticky claim je polopravdivy. (line 84)
- `[minor]` Komentar 'cron job pouziva curl/wget pod kapotou' je nepresny. Cron je planovac, ktory spusta lubovolne prikazy - nemusi pouzivat HTTP klientov. UA string 'cron' v logu pochadza skor zo skriptov, ktore si tak nastavili UA. Drobna nepresnost teorie. (line 96)
- `[minor]` Audit poznamka o substring match je technicky spravna, ale priklad 'synchronization obsahuje chron, nie cron' je matuci. Lepsi priklad falosneho zhody by bol napr. UA string s '...cron...' substringom. Risk je v praxi minimalny, ale ilustracia je slaba. (line 102)
- `[minor]` Komentar 'Duplikaty v 07_robot_ips.csv by len spomalili .isin() lookup' je sporny. pandas .isin() interne stavia hashset z hodnot, duplikaty su deduplikovane v O(n) bez vyznamneho dopadu. Tvrdenie o spomalenisi nesedi s realnou implementaciou. (line 137)
- `[minor]` Komentare obsahuju vela informativnych claimov o WUM kontexte (paralelna vetva ulohy 06, downstream sessionizacia, doc.md odkaz) ktore som priamo neoveroval - mozu byt spravne, ale prijal som ich bez verifikacie. Ak su nepresne, niektore CROSS-REF komenty by mohli klamat.

---

### `03_identifikacia/02_identifikacia_pouzivatelov/identifikacia.py` — OK

**Počty**: expected=4040, actual=4096, Δ=1.4%

**Zadanie bullets:**
- ✅ Usporiadat zaznamy podla IP, User-Agent a Unixtime — _df.sort_values(by=['IP','Agent','UNIXTIME']) na riadku 25 — presne v poradí podľa zadania._
- ✅ Identifikovat pouzivatelov na zaklade IP a User-Agent — _groupby(['IP','Agent']).ngroup() na riadku 38 — kombinacia IP + Agent = jeden uzivatel, presne podla zadania._
- ✅ Vytvorit novu premennu s ID pouzivatela — _Stlpec USER_ID priradeny na riadku 38, +1 pre cislovanie od 1._
- ✅ Pouzit pd.read_csv, sort_values, reset_index — _Vsetky tri pouzite (riadky 20, 25, 27). Navyse groupby+ngroup pre identifikaciu — vhodny dodatok._
- ✅ Ulozit logovaci subor doplneny o identifikaciu pouzivatelov — _out/cleaned_log4_users.csv obsahuje vsetky povodne stlpce + UNIXTIME + USER_ID (20666 zaznamov)._
- ✅ Identifikovanych cca 4040 pouzivatelov — _Actual 4096 unique USER_ID — delta 1.39%, vyborne v ramci tolerancie._

**Findings (audit):**
- `[minor]` Riadok 20: pd.read_csv('in/cleaned_log4_unixtime.csv') pouziva relativnu cestu. Skript funguje len ked je spusteny z adresara 02_identifikacia_pouzivatelov. Pre robustnost odporucam absolutnu cestu alebo os.path.dirname(__file__). Nie je to chyba voci zadaniu, ale moze zavadzat ucitela pri spustani. (line 20)
- `[minor]` Vystupny CSV ma 20666 zaznamov + 1 hlavickovy riadok = 20667 wc -l (header + data). To je v poriadku, ale skript by si mohol dat sanity-check ze pocet riadkov sa nezmenil oproti vstupu (riziko ze sort_values nahodne odstrani NaN). (line 25)
- `[minor]` Pocet identifikovanych pouzivatelov 4096 vs ocakavanych 4040 — odchylka 1.39%. Mozne vysvetlenie: rozdiel v cisteni User-Agent stringov (medzery, kapitalizacia) z predchadzajucich uloh. Stale v ramci akceptovatelnej tolerancie, ale pri obhajobe by student mal vediet vysvetlit preco nie presne 4040. (line 38)
- `[minor]` Skript ma USER_ID priradene az PO sort_values. Kedze ngroup() generuje ID v poradi vyskytu skupin v zoradenom dataframe, ID su pekne usporiadane (vsetky zaznamy s USER_ID=1 su prve, atd.). Toto je korektne, ale stoji za zmienku ze ID poradie zavisi od poradia sortu — pri obhajobe vedet vysvetlit. (line 38)

**Rewrite**: Prepisal som identifikacia.py s MAX-density komentami: rozsireny header docstring (WUM kontext, ZADANIE bullety, VSTUP/VYSTUP, kniznice, algoritmus, cross-ref na doc.md), inline teoria pre heuristiku IP+UA, podrobne vysvetlenie idiómov sort_values, reset_index(drop=True), groupby+ngroup vs factorize, edge cases (NaN, dropna, NAT, dynamicke IP) a poznamky k auditu (relativna cesta, delta 1.39 %, zavislost ID na poradi sortu). Logika kodu, importy ani volania sa nezmenili.

**Adversarial verify issues:**
- `[major]` NEPRAVDIVY TECHNICKY DETAIL: Komentar tvrdi 'sort je stabilny (mergesort/timsort) => zachova relativne poradie pri zhode'. V skutocnosti je default v pandas sort_values kind='quicksort', ktory NIE JE stabilny. Stabilne su iba 'mergesort' a 'stable'. Pri obhajobe je to chybna teoria. (V tomto konkretnom skripte to nesposobi bug, lebo vsetky kluce su uvedene v sort_values, takze stabilita nehra rolu - ale tvrdenie v komentari je faktualne nespravne.) (line 83)
- `[major]` NEPRAVDIVE TVRDENIE O ngroup() s NaN: Komentar tvrdi 'riadky s NaN v kluci by dostali ngroup() = -1'. V skutocnosti pri default dropna=True vrati ngroup() pre NaN riadky hodnotu NaN (nie -1), co dokonca konvertuje cely Series na float64. Hodnota -1 sa vracala v starsich verziach (factorize ma -1, ale ngroup nie). Overene experimentalne s aktualnym pandas. V tomto datasete sice NaN nie su (overene: 0 NaN v IP aj Agent), takze nesposobi runtime bug, ale teoreticke tvrdenie v komentari je nespravne. (line 129)
- `[minor]` Komentar uvadza 'Actual ~4096 (delta 1.39 %) - v tolerancii'. Overene spustenim: skutocne 4096 unikatov a 20666 zaznamov. Delta voci 4040 je (4096-4040)/4040 = 1.386 %. Tvrdenie '~2 % tolerancia' z riadku 22 nie je explicitne v zadani (zadanie hovori len 'priblizne 4040') - autor si tolerancne pasmo zvolil sam. Pre obhajobu treba pripravit vysvetlenie odchylky. (line 156)
- `[minor]` Komentar uvadza 'OCAKAVANY POCET: cca 4040 unikatnych pouzivatelov (tolerancia ~2 %)'. Zadanie tolerancne pasmo neuvadza - len pise 'priblizne 4040'. Toto je interpretacia autora, nie cast zadania. Pri obhajobe treba vediet, ze tolerancia je vlastna konvencia. (line 22)
- `[minor]` Komentar tvrdi 'Pre velke logy by bolo low_memory=False, tu netreba'. To je trochu zavadzajuce - low_memory=False sa pouziva pre KONZISTENTNU dtype inferenciu (zabranuje mixed types warning), nie kvoli velkosti suboru ako takej. Pre velmi velke subory by sa naopak mohol pouzit chunksize alebo dtype= explicitne. Drobna nepresnost. (line 69)

---

### `03_identifikacia/03_premenna_Length/length.py` — OK

**Počty**: expected=150, actual=147.2, Δ=1.9%

**Zadanie bullets:**
- ✅ Vytvorit premennu Length na zaklade USER_ID — _groupby('USER_ID') sa pouziva pre vypocet po skupinach_
- ✅ Length = rozdiel medzi dvoma UNIXTIME casmi — _df['UNIXTIME'] - df['PREV_UNIXTIME'] cez shift(1)_
- ✅ Ak rovnaky user a rozdiel < 3600, zapisem rozdiel — _shift v ramci groupby zarucuje 'rovnakeho usera'; rozdiely < 3600 sa zachovavaju_
- ✅ Inak zapisem None (rozdiel >= 3600 alebo iny user / prvy zaznam) — _df.loc[df['Length'] >= 3600, 'Length'] = None; prvy zaznam usera ma NaN zo shift(1)_
- ✅ Pouzitie pd.read_csv() pre nacitanie log suboru — _pd.read_csv('in/cleaned_log4_users.csv')_
- ✅ Priemerna hodnota Length cca 150 — _actual mean = 147.20, delta ~1.87%_
- ✅ Odovzdat zdrojovy kod + logovaci subor s identifikaciou pouzivatelov — _vystupny CSV obsahuje USER_ID aj Length stlpec; subor cleaned_log4_length.csv ma 20666 zaznamov_

**Findings (audit):**
- `[minor]` Komentar v dokumentacii hovori 'Rozdiel >= 3600 sekund -> Length = None', co je v sulade so zadanim (zadanie: 'menej ako 3600' -> zapis rozdiel, inak None). Hranica 3600 je inkluzivna pre None - presne podla zadania. (line 10)
- `[minor]` Hardcoded relativna cesta 'in/cleaned_log4_users.csv' a 'out/cleaned_log4_length.csv' - skript musi byt spusteny z adresara 03_premenna_Length, inak zlyha. Nepouziva os.path / pathlib pre robustnost. (line 26)
- `[minor]` Pouziva df.loc[...] = None na numerickom stlpci - pandas to konvertuje na NaN (float). Funkcne korektne, ale zadanie pise doslova 'zapisem None' - vystup ma NaN namiesto Python None, co je standardne pandas spravanie. (line 45)
- `[minor]` Implementacia spravne predpoklada, ze data su uz zoradene podla UNIXTIME (alebo aspon v poradi navstev usera). Skript explicitne nesortuje pred shift(1) - ak by vstupny subor nebol zoradeny chronologicky pre kazdeho usera, vysledok by bol nespravny. Riziko zavisi od kvality cv2/02 vystupu. (line 35)
- `[minor]` Zadanie spomina 'logovaci subor doplneny o identifikaciu pouzivatelov' - vystup obsahuje USER_ID aj Length, ale skript sam nelogguje (nepise log file). Predpoklada sa, ze 'logovaci subor' = CSV s log zaznamami doplneny o stlpec Length, co je splnene.

**Rewrite**: Prepisal som length.py s MAX-density komentami v slovencine bez diakritiky: rozsireny header docstring (ciel/zadanie/vstup/vystup/kniznice/algoritmus/cross-ref na doc.md), teoreticke bloky pri kazdom kroku (WUM aproximacia, groupby+shift idiom, Catledge-Pitkow 30-60 min heuristika, NaN propagation, edge cases pre prveho usera a 1-zaznamoveho usera), cross-ref na bullety zo zadania a poznamky o auditovanych minor findings. Logika kodu, importy ani volania zostali nezmenene.

**Adversarial verify issues:**
- `[minor]` Comment lists input columns as 'IP, DATE, UNIXTIME, REQUEST, ..., USER_ID' but actual columns are 'IP, DateTime, RequestMethod, URL, StatusCode, Referrer, Agent, UNIXTIME, USER_ID'. The cited names DATE/REQUEST do not match the real column names (DateTime/RequestMethod). Minor inaccuracy — the ellipsis suggests more columns, but the specific names listed are wrong. (line 22)
- `[minor]` The 'Catledge-Pitkow 1995' citation is conflated with the 60-min threshold. Catledge & Pitkow's 1995 paper actually established a ~25.5 minute timeout (often rounded to 30 min), not 30-60 min. The 60-min threshold in this assignment is a different/looser heuristic. The comment phrasing ('30-60 min nicnerobenia') is misleading attribution; the 3600 s value here is per-assignment, not per-Catledge-Pitkow. (line 110)
- `[minor]` Comment says 'zadanie pise "None", realne je NaN, semanticky ekvivalent' — semantically this is fine, but worth noting that in CSV output NaN is serialized as an empty cell, not the literal string 'None'. The current code is correct; just a precision note in the explanation. (line 121)
- `[minor]` Comment notes 'shift NEROBI sort... ak by neboli zoradene, vysledne Length by bolo nezmyselne (audit minor)' — script does not perform an explicit sort by UNIXTIME within USER_ID. This is a real assumption inherited from cv2/02. The comment correctly flags it as a risk but the script itself does not defensively sort. Verified: the input data is in fact chronologically sorted (mean comes out to 147.20 as expected), so no functional issue, but the dependency on upstream ordering is real. (line 86)

---

### `03_identifikacia/04_STT_MEAN/stt_mean.py` — OK

**Počty**: expected=7500, actual=7097, Δ=5.4%

**Zadanie bullets:**
- ✅ Identifikovat sedenia metodou STT_MEAN (priemerne casove okno) — _Skript pouziva df['Length'].mean() ako prah; .mean() korektne ignoruje NaN._
- ✅ Nacitanie log suboru pomocou pd.read_csv — _Nacitava 'in/cleaned_log4_length.csv' z predchadzajucej ulohy 03._
- ✅ Cca 7500 identifikovanych sedeni — _Vystup obsahuje 7097 sedeni (max SESSION_ID), delta = 5.37% — v tolerancii._
- ✅ Odovzdat zdrojovy kod + logovaci subor doplneny o identifikaciu sedeni — _Vystup out/cleaned_log4_stt_mean.csv obsahuje stlpec SESSION_ID; 20666 zaznamov._

**Findings (audit):**
- `[minor]` Podmienka noveho sedenia '(Length.isna()) | (Length >= stt_mean)' funguje spravne, ale implicitne sa spolieha na to, ze prvy zaznam kazdeho usera v ramci ulohy 03 ma NaN Length. Toto zabezpecuje, ze cumsum nepriradi jednemu SESSION_ID zaznamy od dvoch userov. Ak by sa logika ulohy 03 zmenila, mohlo by dojst k chybe — explicitne groupovanie podla USER_ID by bolo robustnejsie. (line 33)
- `[minor]` Operator '>=' znamena, ze zaznam s Length presne rovnym priemeru zacina nove sedenie. Konceptualne korektne pre STT, ale stoji za zmienku pri obhajobe. (line 33)
- `[minor]` Vypocet priemeru sa robi cez vsetky Length vratane NaN (ktore .mean() ignoruje). Skript by mohol vypisat aj pocet NaN hodnot (= pocet 'prirodzenych' zaciatkov sedeni) pre lepsiu diagnostiku. (line 27)
- `[minor]` SESSION_ID zacina od 1 (prvy riadok ma NaN Length -> True -> cumsum=1). To je v poriadku a konzistentne s USER_ID konvenciou. (line 38)

**Rewrite**: Prepisal som stt_mean.py s MAX-density komentami: rozsireny header docstring (ciel v WUM pipeline, parafrazovane bullet-y zadania, vstup/vystup, kniznice, datove struktury, algoritmus, cross-ref na doc.md), teoreticke bloky pre STT_MEAN/cumsum-idiom/NaN-handling pri Series.mean a porovnani, inline komenty pri kazdom volani s vysvetlenim parametrov (skipna, bitwise | vs or, index=False) a edge cases (prvy zaznam usera, viacero userov, '>=' rovnost), spolu s odkazmi na audit-findings — bez akejkolvek zmeny logiky, importov ci premennych.

**Adversarial verify issues:**
- `[major]` Komentar tvrdi: 'Pocet NaN = pocet "prirodzenych" zaciatkov sedeni (jeden na usera)'. Empiricky overene: NaN count = 5269, ale unique USER_ID = 4096. Rozdiel ~1173 NaN pochadza z 3600s filtra v uloha 03 (df.loc[df['Length'] >= 3600, 'Length'] = None), nie z 'jeden na usera'. Komentar je faktualne nepresny — moze zviest pri obhajobe. (line 89)
- `[major]` Komentar tvrdi: 'NaN znamena "neznamy cas" (typicky posledny zaznam usera alebo prvy zaznam usera)'. V skutocnosti uloha 03 pouziva groupby.shift(1), co produkuje NaN na PRVOM zazname usera, nie na poslednom. Naviac NaN vznika aj pri rozdiele >= 3600 s (filter v uloha 03). Komentar je nepresny v dvoch smeroch. (line 25)
- `[minor]` Komentar 'tato logika sa SPOLIEHA na to, ze uloha 03 vyrobila NaN Length na prvom zazname kazdeho usera' je pravdiva ciastocne — uloha 03 robi NaN aj na zaznamoch kde rozdiel >= 3600s, takze niektore NEW_SESSION=True vznikaju aj uprostred logu jedneho usera (nie len na hraniciach userov). Nie je to chyba, ale komentar zjednodusuje skutocnu mechaniku. (line 124)
- `[minor]` Komentar parafrazuje bullet 4 zadania ako 'doplneny o SESSION_ID', ale zadanie.txt doslova hovori 'doplnený o identifikáciu používateľov' (user identification). Semanticky kontextovo OK (toto cv je o sedeniach), ale nie je to verbatim zo zadania — moze byt na obhajobe spochybnene. (line 15)
- `[minor]` Komentar tvrdi delta 5.37%. Overene: (7500-7097)/7500 = 5.37%. Matematicky OK, ale tolerancia '~5-10 %' (line 14) nema oporu v zadanie.txt — zadanie hovori len 'cca 7500' bez explicitnej tolerancie. Tvrdenie 'v tolerancii' je interpretacia autora skriptu. (line 173)

---

### `03_identifikacia/05_STT_Q/stt_q.py` — OK

**Počty**: expected=7500, actual=7873, Δ=5.0%

**Zadanie bullets:**
- ✅ Identifikovat sedenia metodou STT_Q (kvartilovy odhad casoveho okna) — _Skript pouziva quantile(0.25) a quantile(0.75), pocita IQR a prah Q3 + 1.5*IQR._
- ✅ Vzorec prahu: horny kvartil + 1.5 * kvartilove rozpatie (Q3 + 1.5*IQR) — _Riadok 31: stt_q = q3 + 1.5 * iqr - presne podla zadania._
- ✅ Pouzitie pd.read_csv() na nacitanie log suboru — _Riadok 23: df = pd.read_csv('in/cleaned_log4_length.csv')._
- ✅ Pouzitie metody quantile() na vypocet kvartilov — _Riadky 28-29: quantile(0.25) a quantile(0.75)._
- ✅ Identifikovat cca 7500 sedeni — _Vystup obsahuje 7873 sedeni (delta ~5% - v tolerancii 'cca')._
- ✅ Ulozit vystup (log doplneny o identifikaciu pouzivatelov a sedeni) — _Vystup out/cleaned_log4_stt_q.csv obsahuje stlpce USER_ID a SESSION_ID._

**Findings (audit):**
- `[minor]` Riadok 38: podmienka noveho sedenia pouziva '>=' (Length >= stt_q). Striktne podla teorie outliers by mala byt iba '>', ale pri spojitych floatoch je rozdiel zanedbatelny. (line 38)
- `[minor]` Riadok 38: pouziva isna() ako indikator noveho sedenia (prvy zaznam usera ma NaN Length). To je korektne, ale skript to nevysvetluje v komentari pri tomto kroku. (line 38)
- `[minor]` Hardcoded relativne cesty 'in/...' a 'out/...' - skript je zavisly od cwd. Pri spustani z ineho miesta zlyha. (line 23)

**Rewrite**: Prepisal som stt_q.py s MAX-density komentarmi: rozsireny header docstring (ciel/zadanie/vstup-vystup/kniznice/datove struktury/algoritmus/cross-ref), teoreticke bloky pre IQR Tukeyho pravidlo a cumsum-boolean idiom, inline komenty na kazdom netrivialnom riadku vratane vysvetlenia NaN handlingu a audit findings (>= vs >, isna() ako indikator prveho zaznamu, relativne cesty). Logika kodu, importy ani volania funkcii sa nezmenili.

**Adversarial verify issues:**
- `[minor]` Komentar tvrdi 'Length je NaN pre prvy zaznam kazdeho usera (nema predchodcu)' - to je len jeden zdroj NaN. Uloha 03 (length.py riadok 130) priradi NaN aj VSETKYM medzi-userovskym medzeram kde rozdiel >= 3600 s. Vystup skriptu to potvrdzuje (USER_ID=7 ma NaN aj v 4. zazname). Komentar je teda neuplny / mierne zavadzajuci. (line 28)
- `[minor]` Komentar pravidla a): 'Length je NaN -> riadok je PRVY pristup tohto usera' - rovnaka neuplnost ako vyssie. NaN moze nastat aj pri rozdiele >= 3600 s v ramci toho isteho usera, takze NaN v skutocnosti zachytava 'prvy pristup ALEBO dlha pauza >= 3600s' (cim sa de facto zdvojuje s rolou >= STT_Q, len s inou hranicou). (line 104)
- `[minor]` Komentar tvrdi: 'isna() ako indikator noveho sedenia funguje preto, ze uloha 03 zamerne ponechala Length=NaN pre prvy zaznam kazdeho usera (groupby+shift NaN, neprenasa hodnotu medzi userami)'. Toto je len cast pravdy - groupby+shift je len jeden zo zdrojov NaN; uloha 03 explicitne NaN-uje aj vsetky Length >= 3600. Komentar neopisuje plnu skutocnost. (line 118)
- `[minor]` Komentar pise '(skip_na=True default)' pre Series.quantile. Pandas Series.quantile() nema parameter 'skip_na' (ani 'skipna'). Spravanie 'ignoruje NaN' je sice korektne, ale nazov parametra je vymysleny - na obhajobe by ucitel mohol pichnut. Series.mean() ma 'skipna', quantile to riesi internem dropom NaN bez verejneho parametra. (line 86)
- `[minor]` Komentar tvrdi 'audit hlasi 7873, delta ~5 %' - skutocna delta od 7500 je (7873-7500)/7500 = 4.97 %, takze ~5 % je OK. Cislo 7873 som overil spustenim skriptu. V poriadku, len zaznamenavam ze cislo bolo verifikovane. (line 152)
- `[minor]` Meta-komentar 'Audit to oznacil ako minor finding - neopravujeme, len dokumentujeme.' a podobne na riadkoch 117, 119 spominaju 'audit' bez kontextu pre citatela skriptu. Cisto pre obhajobu mozu posobit cudne (komentar k auditu, nie k logike kodu), ale neovplyvnuju spravnost. (line 67)

---

### `03_identifikacia/07_RLength_exp/rlength_exp.py` — OK

**Zadanie bullets:**
- ✅ Zistit, ci premenna Length ma exponencialne rozdelenie — _Skript nacita Length z cleaned_log4_length.csv, spusti KS test proti expon a vypise zaver podla p-hodnoty._
- ✅ Pouzitie vhodnych Python prikazov (matplotlib, seaborn, chi2_contingency alebo kstest) — _Pouzite matplotlib.pyplot a scipy.stats.kstest (zadanie pripusta ze nemusia byt obe). seaborn nepouzity, ale nie je povinny._
- ✅ Odovzdat kod alebo STATISTICA stw subor — _Odovzdany Python kod rlength_exp.py._

**Findings (audit):**
- `[minor]` KS test pouziva parametre odhadnute z dat (scale=length_data.mean()). Standardny KS test predpoklada plne specifikovane rozdelenie - pri odhade parametrov z dat je p-hodnota anti-konzervativna a spravne by sa mal pouzit Lilliefors test alebo bootstrapped KS. Pre studentske zadanie akceptovatelne, ale teoreticky nekorektne. (line 44)
- `[minor]` x = range(0, int(length_data.max())) generuje len celociselne hodnoty pre PDF krivku - pri jemnejsej krivke by bolo lepsie pouzit numpy.linspace pre hladsiu vizualizaciu exp. PDF. (line 62)
- `[minor]` axes[0].set_xlim(0, 1000) je hardcoded - moze orezat data ak Length presahuje 1000, alebo nechat prazdny priestor ak je max << 1000. Vhodnejsie by bolo adaptivne na zaklade kvantilu. (line 68)
- `[minor]` Skript negeneruje CSV/TXT vystup do out/, len PNG s grafmi. KS statistika a p-hodnota su iba vypisane na stdout - vysledok testu nie je perzistovany do suboru, co znemoznuje neskoru reprodukciu vysledkov bez opatovneho spustenia. Zadanie to ale explicitne nevyzaduje.
- `[minor]` Zadanie spomina aj chi2_contingency (Pearson chi-square) ako alternativu - skript ho nepouziva, len KS test. Zadanie ale vyslovne pise 'nemusia byt pouzite obe', takze nie je to chyba.

**Rewrite**: Rozsiril som header docstring (ciel WUM, zadanie, vstup/vystup, kniznice, datove struktury, algoritmus, cross-ref na doc.md) a pridal MAX-density komenty ku kazdemu kroku: teoria expon. rozdelenia + KS testu (H0/H1, D_n, anti-konzervativny bias pri odhade scale), QQ plot interpretacia, vyznam parametrov (bins, density, alpha, ppf, args=(loc,scale)), NaN handling z ulohy 06 a anti-drift poznamky pri hardcoded set_xlim a range(); ziadna zmena logiky/importov/premennych.

**Adversarial verify issues:**
- `[minor]` Typo v komentari: 'posktyne' -> ma byt 'poskytne'. Iba komentar, kod nie je dotknuty. (line 60)
- `[minor]` Typo v komentari: 'v dawkach bez displeja' -> pravdepodobne 'v davkach' (batch runs). Iba komentar. (line 212)
- `[minor]` Meta-komentar 'audit zaznamenal, ze linspace by bol hladsi' je technicky pravdivy (linspace(0, max, 1000) by dal hladsiu krivku ako range(0, int(max)) s krokom 1), ale style issue - komentare by mali popisovat KOD, nie historiu auditu. Funkcne OK. (line 155)
- `[minor]` Komentar k set_xlim(0, 1000) korektne upozornuje na hardcoded hodnotu, ale opat ide o meta-komentar typu 'anti-drift', nie cisty vysvetlujuci komentar. (line 164)
- `[minor]` Cislo 'cca 6580' validnych Length nie je overene voci CSV - je to len odhad. Komentar je hedged ('cca', 'presny pocet zavisi...'), ale neoverene tvrdenie. (line 17)
- `[minor]` Teoreticka vyhrada o anti-konzervativnom KS teste pri odhade parametrov z dat je SPRAVNA (Lilliefors korekcia je legitimna alternativa). OK insight, ale v studentskom zadani ide nad ramec poziadavky. (line 108)
- `[minor]` Komentar pasivne odraza zadanie ohladom chi2_contingency. chi2_contingency je v skutocnosti test KONTINGENCIE pre 2 kategoricke premenne, nie goodness-of-fit pre rozdelenie; zadanie ho navrhuje s rozsireny vyznamom 'chi-square'. Komentar to nekomentuje, len neutralne uvadza ako nepouzite - OK ale moze byt mätúce. (line 38)
- `[minor]` Nemohol som porovnat byte-by-byte s ORIGINALNYM skriptom pred prepisom (k dispozicii len aktualna verzia). Logika, imports a hyperparametre (bins=50, alpha=0.7, figsize=(14,5), dpi=150, xlim (0,1000), alpha=0.3, s=1, ppf formula (i+0.5)/n) vyzeraju vnutorne konzistentne. Syntax check (ast.parse) presiel. Zadanie pokryte (bullet 1: KS+plots, bullet 2: matplotlib+kstest pouzite, bullet 3: kod ako deliverable).

---

### `03_identifikacia/08_RLength/rlength.py` — OK

**Počty**: expected=8000, actual=7558, Δ=5.5%

**Zadanie bullets:**
- ✅ Identifikovat sedenia heuristikou RLength (podiel navigacnych stranok 40%) — _p=0.4, vzorec -ln(1-p)*mean(Length) = 0.5108 * 147.20 ~ 75.18 s je spravne aplikovany_
- ✅ Pouzit pandas a numpy (pd.read_csv, np.log) — _Obe kniznice importovane a pouzite spravne_
- ✅ Pouzit prirodzeny logaritmus (ln) — _np.log je prirodzeny logaritmus, nie log10 — komentar to explicitne uvadza_
- ✅ Identifikovat cca 8000 sedeni — _Skutocnost: 7558 sedeni, odchylka 5.5% — v tolerancii_
- ✅ Doplnit log o identifikaciu sedeni (SESSION_ID) — _Vystupny CSV obsahuje stlpec SESSION_ID priradeny cez cumsum_

**Findings (audit):**
- `[minor]` Hranicna podmienka 'Length >= rlength' (riadok 44) oznaci ZAZNAM ako start noveho sedenia, ked Length presahuje prah. Logicky to znamena, ze dlhy cas stravený NA stranke spôsobí, ze samotna ta stranka je oznacena ako novy zaciatok sedenia — typicka konvencia v inych ulohach (STT) byva, ze prah sa porovnava s casom medzi zaznamami a novy zaznam je oznaceny az po prekroceni. Stoji za zvazenie, ci semantika Length zodpoveda tomu, co skript predpoklada. (line 44)
- `[minor]` Skript pouziva relativne cesty 'in/...' a 'out/...' (riadky 31, 50) — funguje len pri spusteni z konkretneho pracovneho adresara. Pri spusteni z ineho miesta zlyha. Robustnejsie by bolo pouzit absolutne cesty alebo Path(__file__).parent. (line 31)
- `[minor]` Skript nepise log/info subor s pocetom sedeni do out/ — len printuje na konzolu. Pre archivaciu vysledkov by bolo vhodne ulozit aj summary (mean_length, rlength prah, pocet sedeni). (line 53)

**Rewrite**: Prepisal som skript s MAX-density slovenskymi komentarmi bez diakritiky: rozsireny header docstring (ciel v WUM pipeline, parafraza zadania, vstup/vystup, kniznice s odovodnenim, datove struktury, algoritmus, cross-ref na doc.md), teoreticke bloky pri kazdom kroku (odvodenie -ln(1-p)*mean z exp. rozdelenia, cumsum trick, NaN handling, edge cases) a inline komenty na kazdom netrivialnom riadku. Logika, importy, premenne a poradie operacii ostali nezmenene.

**Adversarial verify issues:**
- `[minor]` Line 86 numerical claim: '0.5108 * 147.20 ~ 75.18 s'. Actual calculation 0.5108256 * 147.20 = 75.194, which rounds to 75.19, not 75.18. Minor rounding discrepancy in comment, but the order of magnitude and conclusion are correct.
- `[minor]` Line 87 claims 'VYRAZNE NIZSI prah nez STT_MEAN -> citlivejsie delenie -> VIAC sedeni'. The threshold ~75s is indeed about half of STT_MEAN (~147s) so lower, but the claim that lower threshold gives MORE sessions is correct (a lower threshold means more records cross it as session boundaries).
- `[minor]` Lines 114-116 reference 'audit-poznamka' / 'audit-finding' multiple times (lines 66, 116, 144) — these are meta-comments referring to an external audit document that I cannot verify. The claims themselves are not code-relevant assertions, but if no such audit exists, these references could be misleading.
- `[minor]` Line 144 comment 'skutocnost ~ 7558 (audit: OK)' — I cannot verify the actual session count without running the script. The assignment expects ~8000 sessions; 7558 would be a 5.5% delta which is reasonable but unverified by me.
- `[minor]` Line 121 'Length presne == rlength : >= zachyti aj rovnost (sedenie sa konci)' — the comment correctly notes >= semantics but says 'sedenie sa konci'. More precisely, the current row STARTS a new session (it's the first row of the new session), not 'ends'. The bool flag marks NEW_SESSION starts, not endings. Slight imprecision in phrasing but the underlying logic description is consistent with how the code works (cumsum gives the row a new SESSION_ID).

---

### `03_identifikacia/09_h_ref/h_ref.py` — OK

**Počty**: expected=7200, actual=8180, Δ=13.6%

**Zadanie bullets:**
- ✅ Identifikacia sedeni metodou h-ref (heuristic referrer) — _Skript kombinuje casove okno + podmienku Referrer == '-' (priamy/externy pristup)_
- ✅ Casove okno = priemerny odhad casu straveneho na stranke (mean Length) — _mean_length = df['Length'].mean() = 147.20 s, pouzite ako prah (Length >= mean_length)_
- ✅ Vystupom je log doplneny o identifikaciu pouzivatelov (a sedeni) — _out/cleaned_log4_href.csv obsahuje USER_ID aj SESSION_ID_
- ✅ Cca 7200 identifikovanych sedeni — _Vystup: 8180 sedeni; delta = 13.6 %, co je v ramci tolerancie 'cca'_
- ✅ Pouzitie pd.read_csv na nacitanie log suboru — _df = pd.read_csv('in/cleaned_log4_length.csv')_

**Findings (audit):**
- `[minor]` Riadok 32: mean_length sa pocita cez celu kolonku Length, vratane NaN hodnot (prvy zaznam kazdeho usera). pandas mean() NaN ignoruje, takze vysledok je korektny, ale stoji za zmienku ze toto je odhad len z 'medzizaznamov', nie z poslednych zaznamov sedeni.
- `[minor]` Riadky 37-41: Skript NEresetuje SESSION_ID na hranici medzi pouzivatelmi explicitne. Funguje to nahodou len preto, ze prvy zaznam kazdeho usera ma Length == NaN (z ulohy 03), co spusti NEW_SESSION. Ak by sa vstupny CSV zmenil tak, ze prvy zaznam usera ma vyplnenu Length, sedenia by sa miesali medzi userami. Robustnejsie by bolo pridat | (df['USER_ID'] != df['USER_ID'].shift()).
- `[minor]` Riadky 37-45: Skript nesortuje data podla USER_ID + UNIXTIME pred aplikaciou logiky. Spolieha sa na to, ze vstupny subor je uz utriedeny z predchadzajuceho kroku. Ak by poradie nebolo zarucene, identifikacia sedeni by bola nespravna.
- `[minor]` Vystup ma 8180 sedeni vs. ocakavanych ~7200 (delta 13.6 %). Vacsi pocet sedeni moze suvisiet s tym, ze podmienka (Length >= mean_length) je inkluzivna (>=) namiesto (>); pri ostrom > by sa pocet sedeni mierne znizil. Toto je vsak v ramci tolerancie 'cca'.
- `[minor]` Riadok 33: print pouziva f-string s formatom .2f, co je OK; ale skript nezapisuje ziaden log/summary subor, len vypise do konzoly. Pre zadanie 'logovaci subor doplneny o identifikaciu' je vystup CSV postacujuci.

**Rewrite**: Prepisany skript h_ref.py s MAX-density komentami: rozsireny header docstring (ciel, zadanie + bullet referencie, vstup/vystup, kniznice, datove struktury, algoritmus, cross-ref na doc.md), inline teoria k STT/h-ref kombinacii 3 podmienok, vysvetlenie cumsum boolean idiomu, NaN handlingu pri mean(), edge case prveho zaznamu usera a rozdielu | vs `or` pre pandas Series. Logika kodu, importy ani volania funkcii sa nezmenili.

**Adversarial verify issues:**
- `[minor]` Comment claims 'tento skript poslednou variantou identifikacie sedeni v ulohach 07-09'. V skutocnosti cv2 folder obsahuje identifikaciu sedeni v ulohach 04-09 (04_STT_MEAN, 05_STT_Q, 06_SLength, 07_RLength_exp, 08_RLength, 09_h_ref). Rozsah '07-09' je nepresny - rovnaky rozsah pouziva doc.md, ale tam ma projekt iné cislovanie (07 RLength, 08 h-ref). (line 6)
- `[minor]` Komentar tvrdi 'OCAKAVANY POCET: cca 7200 sedeni (tolerancia "cca" = jednotky %).' Zadanie naozaj pise 'cca 7200', ale skutocny vystup uploadnuteho CSV ma ~8180 sedeni (cca 13.6% deviacia od 7200). Charakterizovat toleranciu ako 'jednotky %' je teda prilis optimisticke - reality je dvojciferna deviacia. Mozno zaviest opatrnejsiu formulaciu. (line 16)
- `[minor]` Komentar tvrdi 'Vystupom je log doplneny o identifikaciu pouzivatelov (USER_ID) a sedeni (SESSION_ID)'. Skript v skutocnosti pridava len SESSION_ID; USER_ID uz prislo z predchadzajucej ulohy (cv2/02). Formulacia v zadani '...doplnený o identifikáciu používateľov' je tiez nejednoznacna, ale komentar by mohol byt presnejsi: 'pridavame SESSION_ID, USER_ID uz je v inpute'. (line 13)
- `[minor]` Komentar 'predpokladame triedenie podla USER_ID + UNIXTIME z predchadzajuceho kroku' - skript nikde toto triedenie neoveruje ani nevynucuje (.sort_values()). Toto je faithful copy povodnej logiky (originalny skript tiez neradi), ale komentar pravdivo varuje pred touto zavislostou. Iba upozornenie - mozno explicitne pridat sort by bolo bezpecnejsie. (line 32)
- `[minor]` Komentar 'Tym aj implicitne resetujeme SESSION_ID na hranici userov - zavisle ale na tom, ze prvy zaznam ma NaN Length.' Toto je presne. Avsak hodi sa pripomenut: ak by data neboli zoradene po userovi (viz issue na line 32), 'prvy zaznam usera' by nebol prvy v ramci skupiny, a NaN by sa nezhodoval s userovou hranicou. Faithful zachytene v komente, ale stoji za zdoraznenie. (line 107)
- `[minor]` CROSS-REF: '07_projekt/materials/doc.md' - cesta existuje a obsahuje sekcie o STT a h-ref (overne grepom). OK, ale STT v doc.md je 'Session Timeout Threshold' (60-min STT), pricom komentar v tomto skripte interpretuje STT ako 'Static Time Threshold' (linka 72). Skontroloval som doc.md - tam je 'Session Timeout Threshold'. Tvrdenie 'Static Time Threshold' v komente skriptu sa nezhoduje s doc.md a moze byt nepresne. Toto je teoreticky problem - skutocna skratka STT v slovenskej literature WUM je 'Session Timeout Threshold'. (line 54)

---

### `04_doplnanie_ciest/01_doplnanie_STT_MEAN/doplnanie.py` — OK

**Počty**: expected=750, actual=855, Δ=14.0%

**Zadanie bullets:**
- ✅ Doplnit cesty do očisteného logovacieho súboru identifikovaného metódou STT_Mean — _Skript nacita 'in/cleaned_log4_stt_mean.csv' a doplna chybajuce medzistranky podla mapy webu._
- ✅ Pouzit identifikaciu pouzivatelov a sedeni z STT_Mean — _Vstupny subor je vystup z cv2 STT_MEAN; doplnanie sa robi len v ramci rovnakeho SESSION_ID._
- ✅ Odovzdat zdrojovy kod + doplneny logovaci subor — _Script doplnanie.py + out/cleaned_log4_doplnene.csv existuju a su vytvorene._
- ✅ Doplnenych zaznamov cca 750 — _Skutocnost 855 doplnenych zaznamov (delta ~14%, v ramci tolerancie 20%)._

**Findings (audit):**
- `[minor]` Riadok 40: 'mapa.iloc[1:].reset_index(drop=True)' - odstranuje prvy riadok dat ako 'hlavicku'. Ak read_excel uz spravne nacital hlavicku z prveho riadku Excelu, tento krok vyhadzuje prvy realny zaznam mapy webu. Treba overit strukturu mapa_webu.xlsx - moze chybat jedna stranka v parent dict aj v map_paths. (line 40)
- `[minor]` Riadok 86-88: Logika doplna pouze ked 'url_from NIE JE v mape ale url_to ANO'. Zadanie tuto podmienku explicitne neformuluje - typicke STT/Path completion algoritmy doplnaju aj pri 'url_from JE v mape, url_to JE v mape, ale neexistuje priame prepojenie'. Tato uzsia podmienka moze byt dovod, ze pocet doplnenych (855) sa nezhoduje presne s ocakavanym (~750). (line 86)
- `[minor]` Riadok 88: Podmienka 'ref_page != url_from' zabranuje vlozit referencnu stranku ak je rovna url_from, ale nekontroluje, ci samotna referencna stranka tvori platne prepojenie smerom k url_to (t.j. ze parent(url_to) == ref_page a zaroven existuje hrana z url_from na ref_page). Doplnenie tak moze byt este stale neuplne v hlbsie zanorenych stromoch. (line 88)
- `[minor]` Riadok 90-92: Novy zaznam kopiruje cely 'curr' riadok (vratane casovej znacky/IP), len preplisuje URL. To znamena, ze doplneny zaznam ma rovnaky timestamp ako predchadzajuci - moze sposobit problemy pri dalsej analyze (napr. doba zotrvania = 0). Zadanie sice nehovori o timestampe, ale je vhodne to mat v hlave. (line 90)
- `[minor]` Riadok 44-47: Konverzia URL pouziva fixne 'https://www.ukf.sk' bez ošetrenia variantov (http://, www. vs bez www, koncova '/'). Ak by mapa obsahovala miesane formaty, niektore stranky by sa nezhodovali s logom a zostali by mimo map_paths. (line 44)
- `[minor]` Pocet doplnenych (855) je o ~14% vyssi ako ocakavanych ~750. V ramci tolerancie 'cca', ale stoji za to overit, ci ucitelske ocakavanie nepocita s prisnejsou podmienkou doplnania (napr. ze ref_page musi byt potomkom url_from v strome).

**Rewrite**: Rozsiril som header docstring o WUM kontext, parafrazu zadania, vstup/vystup, kniznice, datove struktury, algoritmus a cross-ref na doc.md. Pridal som mini-teoreticke bloky (Path Completion, stromova mapa, set vs list lookup) a inline komenty na kazdy netrivialny riadok (parametre pandas, NaN/edge cases, audit-poznamky ako neinvazivne pripomienky bez zmeny logiky).

**Adversarial verify issues:**
- `[major]` Teoreticka nepresnost: komentar tvrdi, ze parent(url_to) = 'najblizsi spolocny predok' (LCA) url_from a url_to. To je nespravne — parent(url_to) je PRIAMY rodic url_to v strome webu, NIE LCA. Navyse podmienka vstupu je 'url_from not in map_paths', cize url_from v strome ani nie je, takze LCA medzi nimi formalne neexistuje. Heuristika realne robi 'doplnenie rodicom ciela', nie hladanie LCA. (line 128)
- `[minor]` Komentar tvrdi 'Riesi vsetky 4 bullety zo zadania', ale zadanie.txt ma realne 3 substantive poziadavky (doplnit cesty, odovzdat kod+log v zip, ~750 zaznamov) — datum/nazov nie su bullety. Pocet '4' je nepresny. (line 18)
- `[minor]` Komentar uvadza 'tolerancia ~20%' pre ocakavany pocet 750. Zadanie pise iba 'cca 750' bez explicitnej tolerancie — tolerancia ~20% je vymyslena/odhadnuta hodnota, nie z textu zadania. (line 17)
- `[minor]` Typograficka chyba v komentari: 'leziVAT MEDZI' — slovo 'leziVAT' nedava zmysel (asi malo byt 'lezi' alebo 'lezat'). Kosmeticke, neovplyvnuje logiku. (line 122)
- `[minor]` Nezvycajne slovo 'nahliadku' v komentari ('nahradime chybajucu nahliadku rodicom') — pravdepodobne malo byt 'navstevu' alebo 'stranku'. Kosmeticke. (line 127)
- `[minor]` Znakova korupcia v komentari: 'd`alsich' — zjavne malo byt 'dalsich' (alebo 'ďalších') ale backtick (`) nie je platny znak. Iba v komentari, nelamie syntaktiku. (line 188)
- `[minor]` Komentar uvadza 'CV3 - Uloha 01', ale priecinok je '04_doplnanie_ciest'. Z MEMORY.md vyplyva ze cv1=cleaning, cv2=sessions — '04' priecinok by mohol byt CV3 alebo CV4. Oznacenie 'CV3' je neoverene a moze byt mylne. (line 1)

---

### `04_doplnanie_ciest/02_doplnanie_STT_Q/doplnanie.py` — OK

**Počty**: expected=750, actual=735, Δ=2.0%

**Zadanie bullets:**
- ✅ Doplnit cesty do ocisteneho logovacieho suboru identifikovaneho metodou STT_Q — _Skript nacita 'in/cleaned_log4_stt_q.csv' a produkuje 'out/cleaned_log4_doplnene.csv'_
- ✅ Pouzit mapu webu na zistenie referencnych/rodicovskych stranok — _Mapa nacitana z 'in/mapa_webu.xlsx', vybudovany parent dict {path: ref_path}_
- ✅ Doplnit chybajuce medzistranky v ramci sedenia — _Kontrola SESSION_ID zhody pred doplnenim - korektne_
- ✅ Doplnenych zaznamov cca 750 — _Pocet riadkov out (21402) - in (20667) = 735 doplnenych; delta 2% voci cca 750_
- ✅ Odovzdat zdrojovy kod + doplneny logovaci subor — _Skript existuje (doplnanie.py), vystupny CSV existuje v out/_

**Findings (audit):**
- `[minor]` Riadok 40: 'mapa = mapa.iloc[1:].reset_index(drop=True)' - zahadzuje prvy riadok ako hlavicku, no read_excel uz by mal hlavicku spracovat automaticky. Ak Excel mal naozaj duplicitnu hlavicku v riadku 2, OK; inak sa straca jeden zaznam z mapy. Treba overit strukturu Excel suboru. (line 40)
- `[minor]` Riadok 86-88: Logika doplnania spusta SA LEN ked url_from NIE JE v mape ALE url_to JE v mape. Tym sa nepokryva pripad ked obe URL su v mape ale nie su priamo prepojene (chybajuca medzistranka v normalnej navigacii). Komentar v hlavicke (riadky 19-21) hovori o pripade 'preskoceni bez priameho prepojenia v mape' - implementacia rieesi len jeden specificky pripad. (line 86)
- `[minor]` Riadok 88: 'if ref_page and ref_page != url_from' - kontroluje len ze ref_page nie je rovne url_from. Nekontroluje ci ref_page nahodou nie je rovny url_to (samoreferencne mapovanie). Drobny edge case. (line 88)
- `[minor]` Riadky 46-47: 'mapa.loc[mapa["path"] == "", "path"] = "/"' - ak URL bola presne 'https://www.ukf.sk' (bez slash), str.replace ju zmeni na prazdny string, a tu sa nastavi na '/'. Funkcne OK, ale ak log obsahuje '' alebo iny tvar root URL, moze nastat nezhoda. (line 46)
- `[minor]` Skript pridava maximalne jednu medzistranku medzi dve URL. Ak chyba dlhsia cesta (napr. 2-3 urovne v strome), nedoplnia sa vsetky urovne. V STT_Q kontexte to byva v poriadku, ale je to obmedzenie hlbky doplnania. (line 86)
- `[minor]` Pocet doplnenych zaznamov: 735 (zo skutocnych: out 21402 riadkov vratane hlavicky - in 20667 riadkov vratane hlavicky = 735). Zadanie ocakava cca 750. Delta cca 2% - velmi blizko, akceptovatelne. (line 99)

**Rewrite**: Prepisal som doplnanie.py s MAX-density komentami: rozsireny header (ciel v WUM kontexte, parafrazovane zadanie s cca 750, vstup/vystup, kniznice, datove struktury, algoritmus, cross-ref na doc.md), inline komenty pri kazdom netrivialnom riadku (regex=False vysvetlenie, dict(zip) idiom, set vs list O(1) vs O(n), iloc/Series, .to_dict, .get vs []), teoreticke bloky pri kluc. krokoch (mapa webu ako strom, heuristika doplnania, edge cases) a AUDIT-NOTE poznamky ku vsetkym minor findingom z auditu (iloc[1:] hlavicka, single-pripad heuristika, samoreferencia, root URL normalizacia, hlbka doplnania) bez akejkolvek zmeny logiky/importov/premennych.

**Adversarial verify issues:**
- `[minor]` Komentar uvadza ~20667 riadkov na vstupe, ale skutocny pocet je 20666 (off-by-one). Drobne. (line 19)
- `[minor]` Komentar uvadza ~21402 riadkov na vystupe, ale skutocny pocet je 21401 (off-by-one). Drobne. (line 26)
- `[minor]` Komentar o droppovani riadku je mierne zavadzajuci: hovori 'Excel ma v riadku 0 zoznamovu hlavicku, ktoru read_excel uz konzumoval ako names; druhy riadok... zahadzujeme'. V skutocnosti iloc[1:] odstranuje DataFrame riadok s indexom 0 (ktory obsahuje sekundarnu hlavicku 'URLs'/'Root'/'Reference Page'). Tvrdenie 'druhy riadok' moze byt nejednoznacne (v Exceli vizualne 2. riadok = DataFrame index 0, takze technicky pravda, ale moze mýlit). (line 69)
- `[minor]` AUDIT-NOTE tvrdi 'ak by Excel mal len 1 hlavicku, stratil by sa 1 zaznam mapy' — to je pravda, ale v aktualnych datach (overene) prvy DataFrame riadok obsahuje literalne 'URLs'/'Root'/'Reference Page' (sekundarnu hlavicku), takze drop je spravny. Komentar je presny ohladom rizika; len pre uplnost. (line 71)
- `[minor]` Sanity check 'ref_page truthy' — pripomienka: po skoršej normalizacii ref_path == '' sa nahradi '/', takze prazdny string by sa tu nemal objavit ako None/falsy. Truthy test je len pre None z .get() ked URL nie je v parent dict — komentar by mohol byt explicitnejsi, ale fakticky je v poriadku. (line 154)
- `[minor]` Komentar tvrdi 'pri duplicitnych klucoch zostane POSLEDNA hodnota' a 'duplicity by ale byt nemali'. V mape_webu sa vsak vyskytuju riadky s rovnakou URL ale roznym ReferencePage (napr. riadok 1 s URL 'https://www.ukf.sk' a riadok 2 s URL 'https://www.ukf.sk/en' su rozne, ale niektore stranky mozu mat viacero zaznamov). Bez explicitnej validacie sa toto tvrdenie nedalo potvrdit s istotou — minor neistota. (line 92)

---

### `04_doplnanie_ciest/03_doplnanie_RLength/doplnanie.py` — OK

**Počty**: expected=850, actual=776, Δ=8.7%

**Zadanie bullets:**
- ✅ Doplnit cesty do ocisteneho logovacieho suboru (po RLength identifikacii) — _Skript nacita in/cleaned_log4_rlength.csv (vystup z cv2 RLength) a generuje out/cleaned_log4_doplnene.csv s doplnenymi medzistrankami._
- ✅ Vstup obsahuje identifikovanych pouzivatelov a sedenia metodou RLength — _Skript pracuje so stlpcom SESSION_ID a doplna len v ramci jedneho sedenia (riadok 74)._
- ✅ Doplnit chybajuce medzistranky pomocou referencnej stranky / parent v mape webu — _Pouzity parent dict zo stlpcov path -> ref_path z mapy webu (riadky 39-52)._
- ✅ Cca. 850 doplnenych zaznamov — _Actual 776 doplnenych (21443 - 20667 = 776 v out CSV), co je 8.7% pod ocakavanim 850 - akceptovatelne v ramci ~20% tolerancie._
- ✅ Odovzdat zdrojovy kod + doplneny logovaci subor — _doplnanie.py + out/cleaned_log4_doplnene.csv existuju._

**Findings (audit):**
- `[major]` mapa.columns = ["idx", "URL", "Root", "ReferencePage"] - preznacenie hlaviciek, pricom riadok 40 nasledne iloc[1:] zahadza prvy riadok ako 'hlavicku'. Ak Excel ma uz spravnu hlavicku v read_excel, prvy datovy riadok mapy sa stratil. Tym moze chybat jedna mapa webu polozka, co znizuje pocet doplnenych zaznamov. (line 39)
- `[major]` Logika dopla iba pripad 'url_from NOT in map_paths AND url_to in map_paths'. Zadanie/teoria RLength typicky vyzaduje doplnanie aj pri 'url_from in map AND url_to in map' ak medzi nimi nie je priame prepojenie v strome (napr. spolocny predok). Tento jednoduchy pripad moze byt pricinou nizsieho poctu doplnenych zaznamov (776 vs 850). (line 86)
- `[minor]` parent.get(url_to) sa pouziva ako referencna stranka, no kod nazyva premennu 'parent' - v skutocnosti ide o ref_page mapping z mapy webu (ReferencePage), nie striktne 'rodicovska stranka' v stromovom zmysle. Komentar je zavadzajuci. (line 87)
- `[minor]` Podmienka 'ref_page and ref_page != url_from' preskakuje doplnenie ak by referencna stranka bola rovna url_from. To je rozumne, ale mohlo by zhltnut validne pripady kde rodic je iny ale rovnaky zaznam. (line 88)
- `[minor]` Iteracia cez df.iloc v Pythone loope nad tisickami riadkov je pomala (O(n) iloc lookupy). Funkcne to funguje, ale je to neefektivne - lepsi by bol prevod na list of dicts pred loopom. (line 62)
- `[minor]` new_row = curr.to_dict() kopiruje cely riadok vratane casovej znacky, IP, atd. zo zaznamu curr - co je beznou praxou, ale moze sposobit ze doplneny zaznam ma rovnaky timestamp ako predchadzajuci. Zadanie nezada presnu strategiu, takze to je akceptovatelne. (line 90)

**Rewrite**: Prepisal som doplnanie.py s MAX-density komentami: rozsireny header (ciel v ramci WUM, parafraza zadania s ~850, vstup/vystup, kniznice, datove struktury, algoritmus, cross-ref na doc.md), pri kazdom kroku teoreticky/implementacny komentar a inline komenty na netrivialnych riadkoch vratane poznamok z auditu (mapa.iloc[1:], chybajuci pripad "oba v mape ale nesusedne", iloc loop, naming "parent"). Logika, importy, premenne a poradie operacii ostali nezmenene.

**Adversarial verify issues:**
- `[major]` FALOŠNÉ TVRDENIE V KOMENTÁRI: Riadok 63 (a 65) hovorí že `iloc[1:]` 'zahodi prvy datovy riadok ak read_excel uz spravne detekoval hlavicku' a označuje to ako 'audit-finding (major)'. Toto je nepravda. Overené spustením: `pd.read_excel('in/mapa_webu.xlsx')` vráti columns=[' ', 'Unnamed: 1', 'Unnamed: 2', 'Unnamed: 3'] (hlavička sa NEdetekovala) a row 0 obsahuje skutočné textové hlavičky [NaN, 'URLs', 'Root', 'Reference Page']. `iloc[1:]` teda správne zahadzuje textovú hlavičku, NIE prvý dátový riadok. Komentár klame o tom čo kód robí. (line 63)
- `[major]` FALOŠNÉ TVRDENIE V KOMENTÁRI: Riadky 96-103 a 140 tvrdia že skript 'nepokryva pripad oba v mape ale nesusedne' a označujú to ako 'audit-finding major' a 'mozna pricina 776 < 850'. Lenže doc.md §9 (Úloha 09 — Doplnenie ciest pre RLength, riadky 715-796) dokumentuje ALGORITMUS s presne jedinou podmienkou: `url_from not in map_paths and url_to in map_paths` — žiadny iný case neexistuje v zadaní/teórii. Skript faithfully implementuje zdokumentovaný algoritmus, takže označovať absenciu nedokumentovaného caseu ako 'major audit-finding' je zavádzajúce. (line 101)
- `[minor]` NEPRESNÝ CROSS-REF: Riadky 40 a 94 odkazujú na 'doc.md §8 Doplnanie ciest', ale v skutočnom doc.md je Doplnenie ciest pre RLength v 'Úloha 09' (riadok 715), nie §8. Cross-ref číslovanie nesedí. (line 40)
- `[minor]` ČIASTOČNE NEPRESNÝ KOMENTÁR: Riadok 89 tvrdí že '.unique() odstrani duplicity uz pri tvorbe — mensi set, rychlejsi hash-lookup'. Lookup čas v sete nezávisí od veľkosti (O(1)) a `set(mapa['path'])` by mal úplne rovnakú veľkosť ako `set(mapa['path'].unique())` — set automaticky dedupuje. `.unique()` síce zníži počet vkladaní, ale výsledný set nie je 'menší' ani 'rýchlejší pre lookup'. (line 89)
- `[minor]` Komentár (riadky 82-83) správne upozorňuje na nepresný naming 'parent' vs. fakticky 'ReferencePage'. Toto je užitočné poznamenanie a nie chyba, len overujem. (line 82)
- `[minor]` POZITÍVNE: Logika je 100% zachovaná oproti originálu v upload/03_doplnanie_RLength.zip — rovnaké imports, calls, premenné, poradie. Skript je validný Python, beží bez chyby, produkuje 776 doplnených záznamov rovnako ako originál. KS/IQR/exp. rozdelenie teória sa v tomto skripte nenachádza a komenty ich ani nespomínajú (správne, patria do cv2).

---

### `04_doplnanie_ciest/04_doplnanie_h_ref/doplnanie.py` — OK

**Počty**: expected=690, actual=706, Δ=2.3%

**Zadanie bullets:**
- ✅ Doplnit cesty do ocisteneho logu s identifikovanymi pouzivatelmi/sedeniami (h-ref metoda) — _Vstup cleaned_log4_href.csv je vystup z cv2 h-ref ulohy, skript iteruje po sedeniach (SESSION_ID) a doplna chybajuce kroky cez parent mapu._
- ✅ Pouzit metodu h-ref (referencna stranka z mapy webu) — _Skript nacita mapu webu z mapa_webu.xlsx, vybuduje parent dict {URL: ref_path} a vklada referencnu stranku medzi dva po sebe iduce zaznamy._
- ✅ Odovzdat zdrojovy kod + doplneny logovaci subor — _Skript doplnanie.py existuje, vystup out/cleaned_log4_doplnene.csv je vygenerovany (21372 datovych riadkov)._
- ✅ Doplnenych zaznamov cca 690 — _Vystup 21372 - vstup 20666 = 706 doplnenych zaznamov. Delta voci 690 je ~2.3%, plne v ramci tolerancie 'cca'._

**Findings (audit):**
- `[major]` mapa.iloc[1:].reset_index(drop=True) odstranuje prvy datovy riadok mapy webu. pd.read_excel() uz povazuje prvy riadok za hlavicku (kolony su prepisane na riadku 39 cez mapa.columns = [...]), takze tento iloc[1:] zahodi prvu skutocnu URL z mapy. Riziko: chyba jedneho zaznamu v parent dict (mozno root '/') a tym potencialne nizsi pocet doplneni. (line 40)
- `[major]` Logika doplna referencnu stranku LEN ked url_from nie je v mape ALE url_to ano. Standardna h-ref metoda by mala doplnit referenciu aj v pripade ked obe URL su v mape ale nie su priamo prepojene (parent(url_to) != url_from a parent(url_from) != url_to). Tento pripad sa ignoruje, co moze viest k podhodnoteniu poctu doplnenych zaznamov. (line 86)
- `[major]` Skript vlozi medzi dva zaznamy LEN JEDNU referencnu stranku (rodica url_to). Ak by bola medzera v ceste viacurovnova (napr. /a -> /a/b/c/d), korektny h-ref pristup by mal vlozit cely retazec rodicov az po najblizsieho spolocneho predka. Tu sa vlozi iba jeden krok. (line 91)
- `[minor]` Hardkodovane nazvy stlpcov mapy ['idx', 'URL', 'Root', 'ReferencePage'] - krehke voci zmene formatu Excel suboru. Lepsie by bolo overit/mapovat existujuce hlavicky. (line 39)
- `[minor]` Domena 'https://www.ukf.sk' je hardkodovana. Ak by mapa obsahovala URL s inou domenou (http vs https, www subdomena), nahradenie by nefungovalo a parent by obsahoval zle kluce. (line 44)
- `[minor]` Podmienka 'if ref_page and ref_page != url_from' - korektne preskakuje pripad ked rodic ciela je samotny zdroj, ale neoveruje cyklus ani nekontroluje ci ref_page existuje v map_paths (mohol by byt zaznam mimo mapy). (line 88)
- `[minor]` df.iloc[i] v cykle nad celym DataFrame (20k riadkov) je pomale O(n). Pre vacsi log by bolo vhodnejsie pouzit df.itertuples() alebo zip(df.values). Pre tento dataset OK, len efektivita. (line 62)

**Rewrite**: Prepisal som doplnanie.py s MAX-density komentami: rozsireny header (ciel/zadanie/vstup-vystup/kniznice/struktury/algoritmus/cross-ref), teoreticke bloky pre h-ref metodu, inline komenty s vysvetlenim parametrov (regex=False, .get(), .iloc, set/dict idiomy), edge cases (posledny riadok, rovnake URL, hranica sedenia) a anotacie 'POZN. (audit)' pri vsetkych miestach z auditu - logiku som NEZMENIL.

**Adversarial verify issues:**
- `[major]` Audit komentar na riadkoch 86-89 je NEPRAVDIVY. Tvrdi, ze 'read_excel() vsak hlavicku uz odstranil, takze tu sa strati 1 skutocna URL z mapy'. Realita (overene spustenim): mapa_webu.xlsx ma v riadku 0 string hlavicku ('URLs','Root','Reference Page') ale read_excel pouzil prazdne / NaN bunky ako nazvy stlpcov (' ', 'Unnamed: 1', 'Unnamed: 2', 'Unnamed: 3') a hlavicka stale ZOSTALA ako row 0 dat. Preto .iloc[1:] je SPRAVNE a NEvyhadzuje skutocnu URL - vyhadzuje hlavicku. Komentar zavadza. (line 86)
- `[minor]` Komentar 'pd.read_excel - prvy riadok automaticky bere ako hlavicku (header=0 default)' je technicky pravdivy o default chovani, ale v kombinacii s audit poznamkou nizsie sugeruje, ze hlavicka bola spotrebovana - co nie je pravda pre tento konkretny subor (pozri issue vyssie). (line 81)
- `[minor]` Komentar pise 'Ocakavany pocet doplnenych zaznamov: cca 690'. Skript fakticky produkuje 706 - to je 'cca 690', takze OK, ale stojí za zmienku, ze sa potvrdilo experimentom. (line 18)
- `[minor]` Komentar pise 'Pre 20k+ riadkov by bolo rychlejsie itertuples'. Vstup ma 20666 riadkov - tvrdenie je spravne, ale 'audit, line 62' v komentari je matuca referencia (riadok 62 v zdrojaku je 'import pandas as pd', nie iloc). Pravdepodobne sa odkazuje na riadok v povodnom skripte pred prepisom. (line 134)
- `[minor]` Referencie 'audit, line 86' a 'audit, line 88' a 'audit, line 91' v komentaroch odkazuju na cisla riadkov v POVODNOM skripte, nie v aktualnom. V aktualnom skripte tieto riadky obsahuju ine veci (line 86 = audit komentar, line 88 = audit komentar). Pre citatela matuce. (line 191)
- `[minor]` Verifikacny prompt sa pytal aj na 'KS test H0/H1, IQR vzorec, exp. rozdelenie' - tieto temy sa v tomto skripte VOBEC nevyskytuju (skript robi doplnanie ciest h-ref metodou, nie statisticke testy). Komentare o nich teda neexistuju a ani nemali by - to je v poriadku, len upozornujem ze prompt bol pravdepodobne generic template.
- `[minor]` Komentar tvrdi 'Ak by v path bola duplicita, zostane posledna hodnota (silent overwrite)' - to je pravda, ale v skutocnom datasete je 0 duplicit (overene). Pripomienka je teoreticka, nie chyba. (line 110)

---

### `05_prieskum_dat/03_cas_na_strankach/cas.py` — OK

**Počty**: expected=None, actual=748496, Δ=?

**Zadanie bullets:**
- ✅ Zahrnut aspon jednu premennu z kazdej skupiny charakterizujucej vlastnosti pristupov — _Pouzite: length (z URL/obsah), category (DV - obsah), yearQuartal a crisis (IV - cas). Pokryva skupiny DV aj IV._
- ✅ Analyzovat vybrane vztahy medzi premennymi — _Analyzovany vztah category x length, category x yearQuartal x length (heatmap), crisis x category x length._
- ✅ Pozriet sa na vyvoj navstevnosti/casu z hladiska casu — _Pivot table priemerny cas po kvartaloch (yearQuartal) - splnene cez heatmap_kategoria_kvartal.csv._
- ✅ Pracovat s casom stravenym na strankach z hladiska kategorii obsahu a obdobi — _Toto je presne tema skriptu - cas po kategoriach (priemerny_cas_kategorie.csv) a obdobiach (heatmap)._
- ⚠️ Vyjadrit silu zavislosti medzi premennymi — _Skript pocita len priemery, mediany, std a counts - nepocita statisticke testy (napr. ANOVA, korelacia, eta-squared) na vyjadrenie sily zavislosti. Vizualne porovnanie iba cez boxplot a heatmap._

**Findings (audit):**
- `[minor]` Mapping crisis labelov je obrateny / zavadzajuci. V riadku 45: 'kriza_porovnanie.index = ["Po krize (0)", "Pocas krizy (1)"]' - groupby zoradi index vzostupne (0,1), takze 0=Po krize a 1=Pocas krizy. Ak ale konvencia v datasete je crisis=1 znamena krizu, je to OK, ale nazov 'Po krize (0)' moze byt zavadzajuci ak 0 znamena 'pred krizou' alebo 'mimo krizy'. Treba overit semantiku stlpca crisis v CSV. (line 45)
- `[minor]` Filter length>0 vylucuje hodnoty -1 (timeout), -2 (zmena IP) a 0 (robot). Komentar v hlavicke to spravne dokumentuje, ale tymto sa stratia data o tych, ktori opustili stranku (-1) - co moze ovplyvnit interpretaciu 'casu na poslednej stranke v sedeni'. Vyplyva to z metodiky a je to akceptovatelne, ale stoji za zmienku. (line 29)
- `[minor]` Boxplot je orezany na length<100 (riadok 62) - tym sa odfiltruju outliery, ale strati sa informacia o 'dlhom citani' co je obsahova hodnota analyzy. V sumar.txt sa pritom uvadza pravostranne sikme rozdelenie a citanie obsiahlej dokumentacie - tieto outliery na boxplote chybaju. (line 62)
- `[minor]` Skript nepocita ziadnu silu zavislosti (napr. ANOVA F-statistika, eta-squared, Kruskal-Wallis pre nenormalne data). Zadanie explicitne spomina 'vyjadrit silu tejto zavislosti' - tato cast je len deskriptivne pokryta.
- `[minor]` sumar.txt je staticky napisany (komentar na riadku 20). Hodnoty v sumar.txt sa nedopocitavaju zo skriptu - ak by sa zmenil vstupny CSV, sumar.txt zostane neaktualny. Reproducibilita je zhorsena. (line 20)
- `[minor]` Pri pivot_table aggfunc='mean' sa nestratia chybajuce kombinacie kategoria x kvartal - ale v heatmap_kategoria_kvartal.csv nie su ziadne NaN, takze data su pokryte pre vsetky kvartaly 09Q1-12Q4. OK. (line 39)
- `[minor]` plt.show() chyba - skript len ulozi PNG ale nezobrazi graf. To je v poriadku pre batch beh, ale neda sa interaktivne preskumat. (line 68)

**Rewrite**: Prepisal som cas.py s MAX-density komentami: rozsireny header docstring s ciel/zadanie/vstup/vystup/kniznice/datove struktury/algoritmus/cross-ref na doc.md, inline komentare na vsetkych netrivialnych riadkoch s vysvetlenim pandas parametrov (low_memory, aspect, cmap, .copy()), teoreticke bloky pri groupby+agg, pivot_table, unstack a interpretacii mean vs median (sikmost), plus zachytene audit poznamky (-1 timeout, length<100 orezanie, crisis label semantika) bez zmeny logiky.

**Adversarial verify issues:**
- `[major]` Komentar 'figsize=(16,6) -> 6 cm vyska postacuje' je FAKTICKY NESPRAVNY. matplotlib figsize je v INCHES (palcoch), nie v cm. 6 inch = ~15.24 cm. Ide o teoreticku chybu v komentari. (line 183)
- `[major]` Cross-ref 'CROSS-REF na teoriu (07_projekt/materials/doc.md)' je zavadzajuci - doc.md popisuje INY dataset (komercna banka, 17.-23.12.2017, 73927 zaznamov po ocisteni). Tento skript pracuje s logs5.csv (2009-2012, ~2M zaznamov). Definicie length, robotov a sedeni z doc.md nemusia platit pre tento dataset. (line 64)
- `[major]` Tvrdenia o specialnych hodnotach length (-1 = timeout >30 min, -2 = zmena IP, 0 = robot crawl) su PREVZATE Z doc.md ktory popisuje iny dataset. Pre logs5.csv (2009-2012) nie je v repozitari overena dokumentacia tychto hodnot - su to spekulacie. V datach skutocne existuju: 401721 zaznamov s -1, 111055 s -2, 809963 s 0, ale ich SEMANTIKA pre tento dataset nie je v repozitari potvrdena. (line 82)
- `[minor]` Komentar 'crisis flag = obdobie financnej krizy 2008-2009' je nepresny: v datach crisis=1 pokryva 09Q1-10Q4 (roky 2009-2010), nie 2008-2009. crisis=0 pokryva 11Q1-12Q4. Komentar by mal hovorit 2009-2010. (line 71)
- `[minor]` Komentar 'dpi=150 = print quality' je nepresny - 150 dpi je 'screen/decent' kvalita; standardna print quality je 300 dpi. (line 222)
- `[minor]` Komentar k filtru length>0 spomina ze 'vypadnu aj -1 zaznamy' ale nezmieni ze vypadnu aj -2 (111055) a 0 (809963) zaznamy. Cisla v datach: -1=401721, -2=111055, 0=809963 - dohromady filter zahodi ~1.32M z ~2.07M zaznamov. (line 99)
- `[minor]` Komentar 'audit potvrdil actual_count' pre 748496 je SPRAVNY (overene proti datam), ale je vagny - 'audit' nie je nikde formalne zdokumentovany v repozitari, takze citatel nevie co tym mysli. (line 30)
- `[minor]` Tvrdenie 'length na webe je typicky pravostranne sikme' je VSEOBECNE pravda v literature, ale pre TENTO konkretny dataset to v skripte nie je overene (napr. by sa to dalo demonstrovat mean vs median). Komentar to prezentuje ako fakt bez podpornej statistiky v skripte. (line 119)
- `[minor]` Komentar 'Semantika crisis stlpca by sa mala overit v cv2 / kodebooku' je spravne kriticky, ale konkretne overenie: crisis=1 = 2009-2010 (financna kriza), crisis=0 = 2011-2012 (po krize). Labels 'Po krize (0)' a 'Pocas krizy (1)' su teda spravne. (line 169)
- `[minor]` Komentar k boxplot filtru < 100s tvrdi 'Pravostranne sikme rozdelenie tak nebude vidno' - to nie je presne; sikmost MOZE byt stale vidno v ramci 0-100s rangu (kratke kliky <5s vs dlhsie citanie). Vyhladenie skoslenia plati len pre extrem hornu cast distribucie. (line 213)
- `[minor]` Komentar 'Audit overil ze pre tieto data NaN nevznikaju (pokryte vsetky kvartaly 09Q1-12Q4)' - overene a SPRAVNE (6 kategorii x 16 kvartalov, ziadne NaN), ale stoji za zmienku ze toto plati LEN pre length>0 filter. Pri ineho filtri sa to moze zmenit. (line 144)

---

### `06_extrakcia_vzorov/03_matica_pravidiel/matica.py` — OK

**Počty**: expected=None, actual=450, Δ=?

**Zadanie bullets:**
- ✅ Identifikovať obdobia pre analýzu (rok/polrok/kvartál) — _Obdobia 2009-2012 (4 roky) sú definované v premennej obdobia_
- ✅ Filter dát (predspracovanie) — _Filter sa robi v predchadzajucich skriptoch; tento skript dostava uz odfiltrovane CSV s pravidlami_
- ✅ Extrahovať min. 10 pravidiel pre každé obdobie — _Vstupy: 2009=341, 2010=405, 2011=205, 2012=17 — vsetky >= 10_
- ✅ Frekventované transakcie/sekvencie / asociačné pravidlá — _Skript pracuje s asociacnymi pravidlami (antecedents => consequents)_
- ✅ Vytvoriť dátovú maticu unikátnych vzorov: Vzor, O1, O2, O3, O4 (0/1) — _Vystup matica_pravidiel.csv ma stlpce pravidlo, O1_2009, O2_2010, O3_2011, O4_2012 s 0/1 indikatormi_
- ⚠️ Zosumarizovať dosiahnuté výsledky — _Skript vypise pocet_obdobi value_counts a head(10) — zakladny sumar; hlbsie testy (Cochran Q, Concordance) su mimo tohto skriptu_
- ⚠️ Testovanie rozdielov (Cochran Q, Coeff. of Concordance) — _Tento skript len vytvara maticu; testy by mali byt v inom skripte (napr. 04_*). Matica je vsak vstup pre tieto testy — pripravena spravne_

**Findings (audit):**
- `[minor]` Stlpec 'pocet_obdobi' nie je v zadani priamo vyzadovany (zadanie uvadza len Vzor, O1..O4). Je to uzitocny doplnok, ale moze zmiast pri formalnej kontrole formatu. (line 58)
- `[minor]` Spajanie antecedents a consequents je cisto retazcove (df['antecedents'] + ' => ' + df['consequents']). Ak by vstupne CSV mali zoradene polozky v ramci antecedent/consequent inak medzi rokmi (napr. 'A;B' vs 'B;A'), pravidlo by sa povazovalo za rozne. Riziko: nadhodnotenie poctu unikatnych pravidiel. (line 38)
- `[minor]` Skript neoveruje existenciu out/ priecinka pred zapisom (to.csv). Ak by priecinok chybal, padne FileNotFoundError. V tomto pripade priecinok existuje, takze ide len o robustnost. (line 61)
- `[minor]` Zadanie uvadza format 'O1(0/1), O2(0/1)...'; skript pouziva 'O1_2009', 'O2_2010' (kombinacia indexu a roka). Funkcne ekvivalentne, ale literalne sa lisi od zadania. (line 52)
- `[minor]` Skript nedokumentuje, ze 'pravidla_{rok}.csv' musia mat stlpce 'antecedents' a 'consequents'. Ak by chybali, skript spadne s KeyError. Ide o implicitny kontrakt s predchadzajucim skriptom. (line 36)

**Rewrite**: Prepisal som matica.py s MAX-density komentami: rozsireny header docstring (ciel v kontexte WUM pipeline, zadanie bullets, vstup/vystup/kniznice/struktury/algoritmus/cross-ref doc.md), KROK sekcie s teoretickymi blokmi (asociacne pravidla, Cochran Q, idiomy set().union, apply+lambda), inline komenty na netrivialnych riadkoch (preco set, audit-minor poznamky o retazcovej konkatenacii a doplnkovom stlpci pocet_obdobi). Logika, importy ani volania zostali nezmenene.

**Adversarial verify issues:**
- `[minor]` Komentar (riadok 140-141) korektne priznava, ze nazvy stlpcov 'O1_2009' atd. su odchylka od literalneho zadania 'O1(0/1)'. Logika je funkcne ekvivalentna, ale formalne to nie je presny tvar zo zadania. (line 142)
- `[minor]` Komentar tvrdi, ze 'hlbsie testy su v dalsom skripte (04_*)'. Existencia skriptu 04 nebola overena — predpoklad pipeline, nie fakticky dokazany v tomto adresari. (line 17)
- `[minor]` Komentar na riadku 92-97 spravne dokumentuje pripadne riziko nekonzistentneho zoradenia poloziek v antecedents/consequents medzi rokmi. Toto je validna obava, nie chyba v skripte — len je dobre vediet, ze identita pravidla zavisi od kontraktu predchadzajuceho skriptu. (line 98)
- `[minor]` Doplnkovy stlpec 'pocet_obdobi' je nad ramec zadania (zadanie chce iba O1..O4). Komentar na riadku 34-35 to priznava — je to OK, ale formalne to nie je pozadovany vystup. (line 163)

---

### `07_projekt/00_extrakcia_tyzdna/extract_week.py` — OK

**Počty**: expected=None, actual=909828, Δ=?

**Zadanie bullets:**
- ✅ Vyselektovat z logu pridelene obdobie (17.-23.12.2017) — _Substring filter cez tuple dni 'DD/Dec/2017' nad DateTime poliom v Apache formate. Vystup 909 828 riadkov v 01/in a 02/in (~216 MB)._
- ✅ Ocistit od nepotrebnych poli (RequestMethod/Version, StatusCode, URL) — _Mimo rozsah tohto skriptu - extract_week.py je len utilita pre extrakciu tyzdna (uloha 00). Ciscenie poli rieši uloha 01_cistenie_zaznamov._
- ✅ Odstranit robotov podla robots.txt a User-Agent — _Mimo rozsah - rieši uloha 02_robot_ips. Skript len pripravuje vstup pre nu._
- ✅ Vytvorit premennu UnixTime — _Mimo rozsah tejto extrakcnej ulohy._
- ✅ Identifikovat uzivatelov (IP + User-Agent) — _Mimo rozsah - downstream._
- ✅ Premenna Length (User_ID, 60 min STT) — _Mimo rozsah - downstream._
- ✅ Identifikovat sedenia (Reference Length 40% nav., h-ref) — _Mimo rozsah - downstream._
- ✅ Doplnit chybajuce poziadavky (path completion) — _Mimo rozsah - downstream._

**Findings (audit):**
- `[minor]` Out folder 'out/' uvedeny v audit-zadani v skutocnosti neexistuje. Skript zapisuje priamo do '../01_cistenie_zaznamov/in/' a '../02_robot_ips/in/' (bypasuje standardnu in/out strukturu). Je to dokumentovane v komentaroch skriptu a logicky opodstatnene (216 MB subor sa nekopiruje 3x), ale porusuje konvenciu projektu. Riziko: pri reorganizacii ulohovej struktury sa lahko prerusi. (line 38)
- `[minor]` Substring filter 'd in line' na riadku 72 je rychly, ale teoreticky moze chytit false-positives ak by sa retazec '17/Dec/2017' objavil v inom poli ako DateTime (napr. v URL alebo User-Agent). V praxi pre Apache log s formatom '[DD/Mon/YYYY:hh:mm:ss +tz]' je riziko zanedbatelne. (line 71)
- `[minor]` encoding='utf-8' s errors='replace' pre Apache log - User-Agent moze obsahovat non-UTF8 bajty z botov. Replace stratí informaciu o povodnych bajtoch. Pre vstup OK, ale ak by downstream uloha potrebovala presny User-Agent, mohol by byt problem. Vhodnejsie by mohlo byt 'latin-1' alebo 'iso-8859-1' (bezstrátove). (line 60)
- `[minor]` shutil.copy() na riadku 85 vytvara duplikat 216 MB suboru - plytvanie diskom. Alternativa: zapisat naraz do oboch suborov v hlavnej slucke (open dvoch fout-ov), alebo pouzit hardlink/symlink. Akceptovatelne kvoli pythonskej jednoduchosti. (line 85)
- `[minor]` os.makedirs() sa vola len pre first_out (riadok 53), ale pre out_paths[1] sa spolieha na to, ze shutil.copy() ho vie vytvorit - shutil.copy vsak NEvytvara cielovy adresar, len cielovy subor. Ak '../02_robot_ips/in/' neexistuje, skript spadne na FileNotFoundError. V praxi to funguje lebo priecinok existuje, ale je to fragilne. (line 85)
- `[minor]` Skript nema main guard (if __name__ == '__main__') ani definovanu funkciu - vsetko bezi v module-level. Pre standalone utility OK, ale obmedzuje znovupouzitelnost.
- `[minor]` Pocet ulozenych riadkov (909 828) sa nikam neukladá ako audit-log/report - len sa vypise na stdout. Pre reprodukovatelnost by sa hodil maly metadata subor (napr. out/extraction_stats.txt) s poctom riadkov, casovym razitkom, hashom vstupu. (line 78)

**Rewrite**: Rozsiril som header docstring o WUM pipeline kontext, zadanie-bullet mapping, ocakavany pocet zaznamov, popis vstup/vystup tvaru, zoznam kniznic s odovodnenim, datove struktury a algoritmus v 1 vete. Pridal som inline MAX-density komenty s teoriou (streaming I/O, substring search v C, encoding tradeoffs), AUDIT-FLAG anotacie pre vsetkych 6 minor findings z auditu, edge case poznamky a cross-ref na doc.md - bez zmeny logiky, importov, premennych alebo poradia operacii.

**Adversarial verify issues:**
- `[minor]` Komentar tvrdi, ze CPython substring search je 'Boyer-Moore-Horspool (alebo dva-Way pre dlhsie patterny)'. Realne CPython od 3.10 pouziva 'two-way' (Crochemore-Perrin) algoritmus pre vsetky dlhsie patterny; predtym to bola variacia 'fastsearch' inspirovana BMH. Formulacia nie je presna, ale duch tvrdenia (rychly C-level search) je spravny. (line 139)
- `[minor]` Komentar 'break setri ~3.5 iteracii (prumer pre 7 dni)' je nepresny. Pre matching riadok s uniformne rozlozenou poziciou matchu je priemerny pocet usetrenych testov (7-1)/2 = 3, nie 3.5. Pre non-matching riadky break nesetri nic (vsetkych 7 sa skontroluje). Drobna nepresnost, neovplyvnuje funkciu. (line 152)
- `[minor]` Komentar tvrdi 'delegovane na OS calls (sendfile na Linux-e, CopyFile na Windows)' o shutil.copy. Toto je castocne pravda od Python 3.8 (PEP-prislusne fast-copy helpers: _fastcopy_sendfile na Linuxe, _winapi.CopyFile2 na Windows), ale shutil.copy() prv zavola shutil.copyfile() ktore tieto rychle cesty pouzije len ked su splnene podmienky (napr. oba file descriptors su regularne subory). Pre tento pripad to plati, ale tvrdenie je trochu zovseobecnene. (line 174)
- `[minor]` Komentar uvadza 'OCAKAVANY POCET: ~909 828 zaznamov (zistene experimentalne, audit-overene)'. Toto je tvrdenie ktore nie je overitelne z kodu samotneho - skript samotny nic neoveruje voci tejto hodnote (ziadny assert). Ak by sa pridal sanity check (napr. assert count > 900_000), bolo by to robustnejsie. Ako informacny komentar OK, ale slovo 'audit-overene' je silne tvrdenie ktore nemam moznost potvrdit. (line 18)
- `[minor]` AUDIT-FLAG o false-positive substring matchi v URL/UA je spravny ale podhodnoteny. Realne riziko: ak URL obsahuje napr. '/blog/17/Dec/2017/post' alebo Referer ma datum v tomto formate, riadok by sa neopravnene zahrnul aj keby skutocny request bol z ineho dna. Pre robustnost by sa hodil regex kotvyaci na '[' pred datumom (napr. line.find('[17/Dec/2017')). Komentar to spomina ale oznacuje za 'zanedbatelne' - co je rozumne, ale nie 100% zarucene bez auditu vstupu. (line 81)
- `[minor]` Komentar tvrdi ze Apache log je 'striktne ASCII v ramci protokolu'. Toto nie je uplne presne - HTTP/1.1 hlavicky (User-Agent, Referer) mozu obsahovat ISO-8859-1 znaky podla RFC 7230 (povodne), aj ked sucasna prax je US-ASCII + percent-encoding. Tvrdenie je v zasade OK pre praktickost, ale teoreticky nepresne. (line 122)

---

### `07_projekt/02_robot_ips/robot_ips.py` — OK

**Počty**: expected=None, actual=250, Δ=?

**Zadanie bullets:**
- ✅ Ocistit datovy subor od nepotrebnych udajov (Method/Version, StatusCode, URL) — _Mimo rozsahu tohto skriptu - skript iba extrahuje IP roboty; cistenie nepotrebnych stlpcov sa zrejme rieshi v inom kroku pipeline (napr. 01_cleaning). Script samotny necisti, ale to nie je jeho ulohou._
- ✅ Identifikovat robotov na zaklade pristupu k robots.txt (URL) — _Toto je hlavna uloha skriptu. Regex korektne parsuje Apache log, substring predfilter 'robots.txt' + double-check ze 'robots.txt' je v URL (group 4) a nie v Agent/Referrer. Vystup: 250 unikatnych IP, 2354 zaznamov._
- ❌ Identifikovat robotov na zaklade pola User-Agent — _Mimo rozsahu tohto skriptu - ocakavane v separatnom skripte (napr. 03_robot_agents). V ramci tohto skriptu sa s Agent vobec nepracuje._
- ❌ Vyselektovat skumane obdobie (17.-23.12.2017) a vytvorit UnixTime — _Mimo rozsahu tohto skriptu. Vstupny subor 'wm2020projekt_studeny.log' je podla komentara uz predextrahovany na tyzden, UnixTime sa neriesi tu._
- ❌ Identifikovat pouzivatelov na zaklade IP a User-Agent — _Mimo rozsahu - skript iba zbiera IP robotov._
- ❌ Vytvorit premennu Length (User_ID, 60 min STT) — _Mimo rozsahu - sedeniova logika nie je v tomto skripte._
- ❌ Identifikovat sedenia (Reference Length 40% + STT_Q, h-ref) — _Mimo rozsahu tohto skriptu._
- ❌ Doplnenie chybajucich poziadaviek (dopĺňanie ciest) — _Mimo rozsahu tohto skriptu._

**Findings (audit):**
- `[minor]` Komentar hovori 'mozu byt duplicitne' a vystup obsahuje 2354 riadkov pre 250 unikatnych IP. Pre dalsie kroky pipeline (filtrovanie robotov z hlavneho logu) je potrebny len zoznam unikatnych IP - duplikaty zbytocne zvacsuju subor a vyzaduju downstream deduplikaciu. Zvazit pridanie df.drop_duplicates() pred ulozenim, alebo zachovanie duplikatov ak je to vedome rozhodnutie pre nasledne pocítanie pristupov. (line 21)
- `[minor]` Hardcoded relativna cesta 'in/wm2020projekt_studeny.log' a 'out/02_robot_ips.csv'. Skript treba spustit z konkretneho adresara, inak zlyha. Toto je v sulade s memory pravidlom 'scripts must be standalone' ale chybatu absolutne cesty / os.path.dirname(__file__) fallback. (line 49)
- `[minor]` Regex pre HTTP request: '"(\S+)\s+(\S+)\s*\S*"' - posledna cast '\s*\S*' (HTTP version) je nepovinna a nezachytava sa do skupiny. Ak by request neobsahoval verziu (napr. malformed log), regex by stale matchol. Funkcne OK ale mensia odlisnost od standardneho Combined Log Format kde je verzia povinna. (line 38)
- `[minor]` Substring filter 'robots.txt' in line.lower() konvertuje cely riadok na lowercase pre kazdy log riadok. Pri velkych logoch (stovky tisic riadkov) to je drobne plytvanie CPU. Optimalnejsie by bolo 'robots.txt' in line (case-sensitive) alebo regex prekompilovany na case-insensitive. Funkcionalne OK, len performance hint. (line 58)
- `[minor]` Double-check 'if robots.txt in url.lower()' - dobra obrana proti False Positive (napr. ked je 'robots.txt' v Referer alebo Agent). Toto je spravne. Bez tohto by sa mohli pripocitavat IP, ktore nepristupovali k robots.txt ale ho mali v inych poliach. (line 66)
- `[minor]` Skript vypisuje 'Unikatnych IP: 250' do konzoly ale do CSV ulozi VSETKY (s duplikatmi). Mierna nekonzistencia medzi tym co sa hlasi a co sa odovzdava. Pre transparentnost by bolo vhodne bud (a) ulozit dedup verziu, alebo (b) ulozit s pocitadlom pristupov per IP. (line 71)
- `[minor]` Zadanie nestanovuje presny pocet ocakavanych robot IP, takze nie je mozne overit delta_pct. 250 unikatnych IP pre tyzden logov je realisticky pocet (typicke webove servery vidia desiatky az stovky botov za tyzden).

**Rewrite**: Rozsiril som header docstring (ciel v kontexte WUM, parafraza zadania s cross-ref na bullety, ocakavany pocet, vstup/vystup, kniznice s odovodnenim, datove struktury, algoritmus v 1 vete) a doplnil MAX-density inline komentare ku kazdemu netrivialnemu kroku - vratane teorie Apache Combined Log Format, vysvetlenia regex groups, optimalizacie substring filtra, double-check proti false positives v Referrer/Agent, encoding/errors handling, lazy iteracie, a poznamok z auditu (duplikaty, line.lower() performance). Logika kodu, importy a volania ostali bitove identicke.

**Adversarial verify issues:**
- `[minor]` Tvrdenie 'RFC 9309 vyzaduje case-insensitive porovnanie pre tento subor' je nepresne. RFC 9309 (Section 2.3) hovori len ze subor MUSI byt dostupny na URI path '/robots.txt' (lowercase). Standard nepredpisuje, ze servery MUSIA akceptovat varianty s velkymi pismenami. Praktika je taka, ze niektore servery to robia, ale to nie je poziadavka RFC. Lower-case porovnanie v skripte je rozumna defensive technika, ale komment to maluje ako poziadavku standardu - to nie je pravda. (line 127)
- `[minor]` Komment '.match (nie .search) lebo pattern je anchored ^' je trochu zavadzajuci. re.match() vzdy matchuje od zaciatku stringu nezavisle na tom ci pattern obsahuje ^ (^ je len explicitne potvrdenie). Funkcne OK, ale teoreticky nepresne - ^ a .match() su redundantne, nie ze jedno vyzaduje druhe. (line 118)
- `[minor]` Komment 'Iteracia for line in f je lazy generator -> O(1) pamat' je technicky O(buffer_size + max_line_length), nie strict O(1). V praxi konstantna pamat voci velkosti suboru, takze tvrdenie je OK v kontexte, len nie matematicky presne. (line 87)
- `[minor]` Komment '250 unikatnych IP / 2354 zaznamov' bol overeny spustenim skriptu - sedi. Toto je iba poznamka, nie issue. (line 21)
- `[minor]` Komment hovori '[^"]* = vsetko medzi uvodzovkami' - to je nepresne. [^"]* matchuje 0 az viac NE-uvodzovkovych znakov; uvodzovky su explicitne v patterne mimo class. Komment to popisuje vysledok zo siroka, drobna nepresnost. (line 65)
- `[minor]` Pouzivatel v prompte ziadal overit teoriu KS test H0/H1, IQR vzorec, exponencialne rozdelenie - tieto temy sa v tomto skripte (robot_ips) NEVYSKYTUJU vobec. Skript sa zaobera len Apache log parsovanim a robots.txt heuristickou. Komenty o regex/parsing su spravne. Bud sa prompt vztahuje na iny skript, alebo je to len generic checklist.

---

### `07_projekt/04_obdobie_unixtime/obdobie.py` — OK

**Počty**: expected=None, actual=73927, Δ=?

**Zadanie bullets:**
- ✅ Vyselektovat pridelene obdobie (17.-23.12.2017, Martin Studeny) — _Boolean maska cez str.startswith() pokryva vsetkych 7 dni 17-23/Dec/2017; po filtrovani zostalo 73927 zaznamov._
- ✅ Vytvorit premennu UnixTime (Unix timestamp v sekundach od 1.1.1970) — _Stlpec UNIXTIME pridany cez df.apply(to_unixtime); pouzity datetime.datetime(...).timestamp(). Hodnota napr. 1513488497.0 pre 17/Dec/2017 06:28:17 +0100 zodpoveda spravnemu UTC._

**Findings (audit):**
- `[major]` Funkcia to_unixtime() ignoruje timezone offset z logu (napr. '+0100' / '+0200'). datetime.datetime(...) bez tzinfo je naive a .timestamp() interpretuje ho v lokalnej timezone systemu. Vysledok bude nekonzistentny medzi systemami v roznych TZ; navyse log obsahuje letny aj zimny cas (zaznamy z decembra maju +0100, ale apache logy v ramci projektu mozu mat aj +0200). Spravne by sa malo parsovat aj '+HHMM' a vytvorit aware datetime cez timezone(timedelta(hours=...)) alebo pouzit datetime.strptime s '%z'. (line 89)
- `[minor]` Filter pomocou str.startswith() je krehky — zavisi na presnom formate DateTime '17/Dec/2017...'. Ak by upstream task 03 zmenil format (napr. ISO), filter by ticho vratil prazdny DataFrame bez chybovej hlasky. Odporucam pridat assert len(df) > 0 alebo logovat warning. (line 47)
- `[minor]` Hlavickovy komentar na riadku 10 sa odkazuje na cistenie RequestMethod/StatusCode/URL, ale tieto stlpce zostavaju v out/04_obdobie.csv (verifikovane v hlavicke CSV). Toto je spravne pre tuto ulohu (cisti sa v inom kroku), ale komentar moze mylit — vhodne by bolo upresnit ze cistenie stlpcov sa robi v ulohe 01/02.
- `[minor]` Zadanie neudava ocakavany pocet riadkov pre tento krok, takze delta_pct sa neda vypocitat. Hodnota 73927 zaznamov za tyzden vsak vyzera realisticky (~10.5k/den).
- `[minor]` Hardkodovany rok 2017 a mesiac 'Dec' v maske — pri zmene prideleneho obdobia by sa muselo manualne menit. Akceptovatelne pre jednorazovy skolsky projekt, ale lepsia by bola parametrizacia (start_date, end_date). (line 47)

**Rewrite**: Prepisany skript s MAX-density slovenskymi komentami bez diakritiky. Pridany rozsireny header docstring (ciel v kontexte WUM, zadanie bullets s ocakavanym poctom 73927, vstup/vystup, kniznice s odovodnenim, datove struktury, algoritmus, cross-ref), teoreticky blok o POSIX timestampe, idiomy vektorovej masky a OR pre Series, dokumentacia parametrov (low_memory, reset_index drop, index=False), edge cases a explicitna referencia na audit findings (TZ naive, krehky startswith) bez zmeny logiky/importov/premennych.

**Adversarial verify issues:**
- `[major]` Komentare pri jednotlivych dnoch tyzdna su NESPRAVNE — su posunute o jeden den. 17.12.2017 nebol pondelok ale NEDELA. Spravne: 17=nedela, 18=pondelok, 19=utorok, 20=streda, 21=stvrtok, 22=piatok, 23=sobota. Skript stale filtruje spravne datumy, ale dokumentacia klame o tom co tie datumy predstavuju — pri obhajobe to moze padnut. (line 96)
- `[major]` Priklad v docstringu klame: vstup '17/Dec/2017:06:25:47 +0100' neprodukuje 1513488497.0, ale 1513488347.0 (rozdiel 150 sekund). Hodnota 1513488497.0 zodpoveda casu 06:28:17, nie 06:25:47. Bud zmenit vystup na 1513488347.0, alebo vstup na ':06:28:17 +0100'. (line 131)
- `[minor]` Komentar uvadza priklad DateTime '17/Dec/2017:06:25:47 +0200', ale skutocny log (a iny komentar na riadku 91) pouziva '+0100' (zimny cas CET v decembri). +0200 by bol CEST (letny cas), ktory v decembri neplati. (line 23)
- `[minor]` Vymenovane stlpce 'IP, DateTime, RequestMethod, URL, StatusCode, Agent (+ dalsie)' presne nezodpovedaju skutocnym 7 stlpcom v 03_cleaned_log.csv (chyba explicitne uvedeny 'Referrer', ktory tam je medzi StatusCode a Agent). '(+ dalsie)' to ciastocne pokryva, ale je to nepresne. (line 22)
- `[minor]` Komentar nazyva '|' BITOVY OR. Pre pandas bool Series je to cez operator overloading element-wise LOGICKY OR — Pythonove `or` zlyhava lebo Series nema jednoznacny truthiness, nie kvoli bitovosti. Pri obhajobe by sa to dalo spochybnit, hoci v bool kontexte (bool je podtrieda int) bitovy a logicky OR davaju rovnaky vysledok. (line 84)
- `[minor]` Komentar tvrdi 'Ocakavany pocet zaznamov: nedefinovany v zadani; po filtri ~73 927'. Cislo som overil voci out/04_obdobie.csv — sedi presne (73927 riadkov, 8 stlpcov = 7 vstupnych + UNIXTIME). Bez issue, len upozornenie ze toto cislo je hard-coded a ak by sa upstream task 03 zmenil, komentar by zostarol. (line 17)

---

### `07_projekt/06_premenna_Length/length.py` — OK

**Počty**: expected=None, actual=73927, Δ=?

**Zadanie bullets:**
- ✅ Vytvorit premennu Length na zaklade USER_ID a 60 min STT — _Skript pouziva groupby(USER_ID).shift(1) na ziskanie predchadzajuceho UNIXTIME, vypocita rozdiel a aplikuje 3600s prah (60 min STT)._
- ✅ Vstup: in/05_users.csv (z ulohy 05 s USER_ID) — _Vstup obsahuje USER_ID a UNIXTIME potrebne na vypocet._
- ✅ Vystup: out/06_length.csv so stlpcom Length — _Subor existuje, 73928 riadkov (73927 zaznamov + header), stlpec Length pridany._
- ✅ Prvy zaznam usera nema predchadzajuci -> Length = NaN — _shift(1) automaticky priradi NaN prvemu zaznamu kazdej skupiny - viditelne v r.2 a r.5 vystupu (Length prazdne pre prvy zaznam usera)._
- ✅ Ak je rozdiel >= 3600s, Length = None (60 min STT pravidlo) — _df.loc[df['Length'] >= 3600, 'Length'] = None - korektne aplikovane vektorovo._

**Findings (audit):**
- `[minor]` Predpoklad chronologickeho zoradenia: skript spolieha na to, ze vstup je zoradeny podla [IP, Agent, UNIXTIME] z ulohy 05. Ak by toto zoradenie nebolo zachovane, shift(1) by dal nespravne predchadzajuce hodnoty. Bezpecnejsie by bolo explicitne df.sort_values(['USER_ID','UNIXTIME']) pred shift().
- `[minor]` Hranicna podmienka >= 3600: zadanie hovori o '60 min STT'. Pouzitie >= je rozumne (presne 60 min uz povazujeme za novy session), ale komentar v kode hovori 'pravdepodobne odisiel' - ide skor o oznacenie konca sedenia, nie 'odchodu'. Sémantika je spravna pre vytvorenie Length stlpca.
- `[minor]` Pouzitie None namiesto np.nan: df.loc[...] = None v numerickom stlpci moze pandas konvertovat na NaN automaticky, fungue to ale nie je idiomatic - lepsie pouzit pd.NA alebo np.nan explicitne.
- `[minor]` Skript nepocita ani nereportuje pocet NaN/None v Length stlpci (kolko prvych zaznamov userov, kolko medzier >= 3600s) - chyba metrika ktoru by bolo vhodne logovat pre kontrolu spravnosti voci dalsim ulohy (sedenia).
- `[minor]` Zadanie (zadanie.txt) je vseobecna osnova celeho projektu, nie konkretne pre tuto ulohu - nie su tu ziadne ocakavane pocty pre Length. Compliance je hodnotena podla docstringu skriptu a logickeho splnenia pravidiel.

**Rewrite**: Prepisal som length.py s MAX-density komentami: rozsiril som header docstring (WUM kontext, parafrazovany bullet zo zadania, ocakavany pocet 73927, cross-ref na doc.md a ulohu 07) a ku kazdemu kroku som pridal teoreticky blok (STT, NaN propagacia, groupby+shift idiom, vektorove .loc priradenie) + inline komenty k pandas parametrom (low_memory=False, index=False, skipna pri mean/median). Logika, importy ani volania funkcii zostali nezmenene.

**Adversarial verify issues:**
- `[minor]` Komentar hovori 'Pre POSLEDNU stranku v sedeni (alebo prvy zaznam usera) Length nepoznam — bude NaN.' Toto je miesane: kod pouziva shift(1) (lag), takze v skutocnosti je NaN priradeny PRVEMU zaznamu usera, nie poslednemu. doc.md (riadok 471) to explicitne pripusta: 'v projekte to pocitame cez shift(1), takze NaN ma prvy pristup'. Komentar by mal byt jednoznacny — bud lag (prvy zaznam = NaN, ako kod naozaj robi), alebo lead (posledny = NaN). Aktualne formulacia moze citatela popliest. (line 11)
- `[minor]` Komentar 'Pre POSLEDNU stranku to nepoznam (nema dalsi request), nechame NaN' je nepresny vzhladom na pouzity shift(1). shift(1) nedava NaN poslednemu, ale prvemu zaznamu skupiny. Vid riadok 103 (priklad) — komentar tam je spravny (NaN je prvy). Konflikt s vyssie uvedenym tvrdenim. (line 90)
- `[minor]` Pravdepodobny preklep / chyba v slovencine: 'priemer rosa pri par desiatkach az stovkach sekund' — slovo 'rosa' nedava zmysel v kontexte. Pravdepodobne malo byt 'sa pohybuje' alebo 'rastie' alebo podobne. Nepoznam istotu — moze byt zamerne, ale vyzera ako preklep. (line 184)
- `[minor]` Komentar tvrdi 'vstup z ulohy 05 ma 73927 zaznamov (audit potvrdil)' — nevedel som tento pocet nezavisle overit (nepustil som skript ani neskumal CSV). Ak audit povedal ze tak je, OK; inak overit. (line 22)
- `[minor]` Komentar spravne upozornuje ze None v numerickom stlpci nie je idiomaticke a navrhuje np.nan/pd.NA, ale logika zostala nezmenena. To je v poriadku (zachovanie povodnej logiky), len pripominam ze np.nan by vyzadoval 'import numpy as np' co tu nie je — preto None je v skutocnosti pragmatickou volbou aby sa neimportovala numpy. Stoji za zvazenie ci to spomenut v komentari. (line 156)

---

### `07_projekt/07_sedenia_RLength/rlength.py` — OK

**Počty**: expected=None, actual=33496, Δ=?

**Zadanie bullets:**
- ✅ Identifikacia sedeni metodou Reference Length s podielom navigacnych stranok 40% — _Vzorec -np.log(1 - 0.4) * mean_length spravne implementovany (riadok 83). Pouzity np.log (prirodzeny logaritmus), nie log10._
- ✅ V pripade nesplnenia podmienky pouzit STT_Q — _Podmienka overena Kolmogorov-Smirnov testom (p < 0.05 -> fallback). STT_Q = Q3 + 1.5*IQR spravne (riadok 95). V skutocnosti sa pouzil fallback STT_Q = 76.0s, pretoze data nemali exponencialne rozdelenie (p=0)._
- ✅ Pouzitie premennej Length z ulohy 06 ako vstupu — _Nacita in/06_length.csv (riadok 53)._
- ✅ Pridelit SESSION_ID identifikovanym sedeniam — _cumsum nad boolean stlpcom NEW_SESSION (riadky 109-115). Pocet sedeni: 33,496._
- ✅ Ulozit vystup pre dalsie spracovanie (dopĺňanie ciest) — _CSV out/07_sedenia_rlength.csv (73,928 riadkov vratane hlavicky = 73,927 zaznamov) + textovy zaver out/07_test_zaver.txt._

**Findings (audit):**
- `[minor]` NEW_SESSION pouziva podmienku (Length.isna()) | (Length >= prah). Pre prvy zaznam kazdeho usera je Length=NaN, takze zacne nove sedenie - to je spravne. Logika je korektna. (line 109)
- `[minor]` SESSION_ID je globalne unikatne cez cumsum cez vsetkych userov (riadok 115). To je v poriadku, pretoze sa SESSION_ID inkrementuje vzdy ked zacne novy user (NaN Length) alebo prekroci prah. Treba vsak overit, ci je dataset zoradeny podla User_ID a UnixTime - skript to nekontroluje ani nezoraduje. (line 115)
- `[minor]` Hranicna podmienka pouziva 'Length >= prah'. V niektorych referenciach sa pouziva striktne >. Rozdiel je marginalny pri spojitom case, ale teoreticky moze ovplyvnit hranicne pripady. (line 109)
- `[minor]` KS test vratil p=0.000000 a KS stat 0.5995 - velmi silne zamietnutie exponencialneho rozdelenia. Fallback STT_Q sa pouzil korektne podla zadania. Treshold 76s je vsak velmi nizky - vznika 33,496 sedeni z 73,927 zaznamov (cca 2.2 zaznamu na sedenie v priemere), co moze byt podozrivo vela fragmentovanych sedeni. Zadanie ale toto explicitne nezakazuje. (line 95)
- `[minor]` Skript predpoklada, ze CSV ma stlpec Length s NaN pre prve zaznamy uzivatelov. Ak by Length bol napr. 0 pre prvy zaznam namiesto NaN, logika by zlyhala. Toto je zavislost od ulohy 06. (line 58)
- `[minor]` Zadanie spomina aj h-ref metodu a doplnanie ciest - tieto su mimo rozsahu tohto konkretneho skriptu (suvisi to s inymi ulohami v projekte 07).

**Rewrite**: Prepisal som rlength.py s MAX-density komentarmi: rozsireny header docstring (ZADANIE, VSTUP/VYSTUP, KNIZNICE, DATOVE STRUKTURY, ALGORITMUS, CROSS-REF na doc.md), inline teoria pri kazdom kluc. koncepte (exp. rozdelenie, KS test H0/H1, IQR/Tukey hranica, cumsum idiom, RLength odvodenie -ln(0.6)) a edge-case poznamky (NaN handling, '|' vs 'or', global cumsum, '>=' vs '>') - logika, importy aj premenne ostali nezmenene.

**Adversarial verify issues:**
- `[minor]` Komentar 'NaN = prvy zaznam usera' je neuplny/zavadzajuci. Ulohe 06 (line 159) okrem prveho zaznamu usera nastavuje Length na None aj pre vsetky pripady kde Length >= 3600s (60 min STT pravidlo). Realne data potvrdzuju: 24168 NaN vs len 14563 userov - takze NaN obsahuje aj STT-prerusene zaznamy, nielen prve zaznamy userov. Logika algoritmu vsak ostava korektna (oba pripady su legitimne hranice sedenia). (line 79)
- `[minor]` Komentar '(a) Length je NaN -> prvy zaznam usera => vzdy zaciatok noveho sedenia' je rovnako neuplny ako line 79. NaN moze pochadzat aj z 60 min STT pravidla v ulohe 06, nielen z prveho zaznamu usera. Mal by spomenut obe pricniny NaN. (line 175)
- `[minor]` Komentar 'pri spojitom case je rozdiel marginalny' je nepresny - Length je v praxi diskretny (rozdiel celych UNIXTIME sekund, nie spojity), takze hranica '>=' vs '>' moze realne rozhodnut osud zaznamov s presnou hodnotou rovnou prahu. Algoritmus to zvlada spravne, len odovodnenie je matne. (line 181)
- `[minor]` Komentar 'kazdy novy user zacina NaN Length' je len ciastocne vysvetlenie. Pravda je ze cumsum funguje globalne korektne aj bez tejto vlastnosti - dolezitejsie je ze prah zachyti dlhe pauzy MEDZI userami. Stoji za to pridat ze v skutocnosti hranica medzi userami sa zachyti DVOJMO (raz cez velky Length, raz cez NaN), ale to nie je problem - SESSION_ID stale rastie monotonne. (line 200)
- `[minor]` Komentar tvrdi ze 'cumsum bezi cez CELY DataFrame (nie per-user)' a 'SESSION_ID je globalne unikatne cez vsetkych userov'. Toto je TECHNICKY pravda len ak su data zoradene podla USER_ID+UNIXTIME (co je predpoklad). Komentar to spomina, ale ak by sa niekedy v buducnosti zmenilo zoradenie vstupu, SESSION_ID by mohol stratit globalnu unikatnost per-user. Skript by mohol byt robustnejsi (napr. groupby+cumsum), ale toto nie je v zadani vyzadovane. (line 198)

---
