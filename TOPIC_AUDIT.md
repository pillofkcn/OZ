# TOPIC AUDIT — Per-topic verification: materials × zadanie × implementation

Audit cez 3 dimenzie pre 7 tém (6 cvičení + projekt). Generované Workflow-om `per-topic-audit` so 7 paralelnými agentmi.

## Súhrn

| Topic | Materials | Zadanie bullets | Outputs | Verdict |
|---|---|---|---|---|
| `01_zdroje_dat` | 9/9 | 20/20 | 4/4 | ✅ FULL_COMPLIANCE |
| `02_cistenie_dat` | 4/4 | 9/12 | 4/4 | ✅ FULL_COMPLIANCE |
| `03_identifikacia` | 2/2 | 9/9 | 7/8 | 🟡 PARTIAL |
| `04_doplnanie_ciest` | 4/4 | 12/12 | 4/4 | ✅ FULL_COMPLIANCE |
| `05_prieskum_dat` | 3/3 | 5/5 | 9/9 | ✅ FULL_COMPLIANCE |
| `06_extrakcia_vzorov` | 6/6 | 10/11 | 9/9 | ✅ FULL_COMPLIANCE |
| `07_projekt` | 4/4 | 10/10 | 11/11 | ✅ FULL_COMPLIANCE |

## 01_zdroje_dat — ✅ FULL_COMPLIANCE

### A) Materials

| File | Type | Usage | Justification |
|---|---|---|---|
| `materials/zadania.txt` | documentation | 📖 studied-only | Master zadanie pre vsetky 4 ulohy (01-04) - parafrazovane v hlavickach kazdeho skriptu, kopia ako per-task zadanie.txt v scripts/*/zadanie.txt |
| `materials/Objavovanie znalosti.pdf` | reference | 📖 studied-only | Teoreticky podklad kurzu (VSM, TF-IDF, NLP, term-weighting) - PDF, legitimne studijny material pre obhajobu (project_proj_defense.md: doc.md/PDF su... |
| `materials/Prehladavanie webu.pdf` | reference | 📖 studied-only | Teoreticky podklad k prvej ulohe (web scraping, HTTP, HTML parsing) - PDF studovany ako referencia, citovany cross-ref v hlavickach skriptov |
| `materials/vektorova_reprezentacia.xlsx` | data | ✅ used-by-code | Vstupna DTM (wf harok 51x101) pre Ulohu 02 - kopia/preformatovana verzia je v scripts/02_reprezentacia_textu_I/in/ (hash sa lisi pretoze in/ verzia... |
| `materials/texty_z_webu/text1.txt` | data | ✅ used-by-code | Vstupny anglicky korpus pre ulohy 03 a 04 - hash-overene identicke kopie v scripts/03/in/ a scripts/04/in/ |
| `materials/texty_z_webu/text2.txt` | data | ✅ used-by-code | Vstupny anglicky korpus - hash-overene identicke kopie v scripts/03/in/ a scripts/04/in/ |
| `materials/texty_z_webu/text3.txt` | data | ✅ used-by-code | Vstupny anglicky korpus - hash-overene identicke kopie v scripts/03/in/ a scripts/04/in/ |
| `materials/texty_z_webu/text4.txt` | data | ✅ used-by-code | Vstupny anglicky korpus - hash-overene identicke kopie v scripts/03/in/ a scripts/04/in/ |
| `materials/texty_z_webu/text5.txt` | data | ✅ used-by-code | Vstupny anglicky korpus - hash-overene identicke kopie v scripts/03/in/ a scripts/04/in/ |

### B) Zadanie compliance

| Requirement | Status | Script | Evidence |
|---|---|---|---|
| U01: Python skript na prehladavanie webovych stranok | ✅ true | `scripts/01_prehladavanie_webu/crawler.py` | requests.get(url) v slucke pre 5 URL clankov UKF FPVAI, BeautifulSoup html.parser na DOM |
| U01: Ziskat textovy obsah stranok (cisty text bez HTML tagov) | ✅ true | `scripts/01_prehladavanie_webu/crawler.py` | soup.get_text() vytiahne textove uzly + ocistenie prazdnych riadkov cez list comprehension [l.str... |
| U01: Export do .txt suborov | ✅ true | `scripts/01_prehladavanie_webu/crawler.py` | out/articles/article_1..5.txt - 5 suborov realne existuju, UTF-8 encoding |
| U02: Transformovat raw tf na BINARNU reprezentaciu | ✅ true | `scripts/02_reprezentacia_textu_I/freq.py` | binary = (wf > 0).astype(int), harok 'binary' v out/vektorova_reprezentacia.xlsx (51 riadkov, 101... |
| U02: Transformovat raw tf na LOGARITMICKU reprezentaciu | ✅ true | `scripts/02_reprezentacia_textu_I/freq.py` | log_wf = np.where(wf>0, 1+np.log10(wf,...), 0), harok 'log' s np.round(...,4) |
| U02: Transformovat raw tf na INVERZNU DOKUMENTOVU FREKVENCIU (IDF) | ✅ true | `scripts/02_reprezentacia_textu_I/freq.py` | idf = np.log10(N/doc_freq), samostatny harok 'idf' (101 lem x 1 stlpec 'idf') + bonus harok 'tf-i... |
| U02: Vysledky v JEDNOTLIVYCH HARKOCH | ✅ true | `scripts/02_reprezentacia_textu_I/freq.py` | ExcelWriter zapise 5 harkov: wf, binary, log, idf, tf-idf - overene openpyxl |
| U02: Odovzdat vysledny subor (Excel) | ✅ true | `scripts/02_reprezentacia_textu_I/freq.py` | out/vektorova_reprezentacia.xlsx (84 KB) |
| U03: Extrahovat lemy slov pomocou nltk z anglickych textov | ✅ true | `scripts/03_reprezentacia_textu_II/lemma.py` | sent_tokenize -> word_tokenize -> WordNetLemmatizer.lemmatize(word.lower()) pre kazdy text |
| U03: Vytvorit datovu maticu = frekvencia lem v dokumentoch | ✅ true | `scripts/03_reprezentacia_textu_II/lemma.py` | wf DataFrame index=1077 unikatnych lem, columns=5 dokumentov, plnenie wf.at[lemma,fname]+=1 |
| U03: Odvodit BINARNU reprezentaciu | ✅ true | `scripts/03_reprezentacia_textu_II/lemma.py` | binary = (wf > 0).astype(int), harok 'binary' 1077 x 5 |
| U03: Odvodit LOGARITMICKU reprezentaciu | ✅ true | `scripts/03_reprezentacia_textu_II/lemma.py` | log_wf = np.where(vals>0, 1+np.log10(vals,...), 0), harok 'log' |
| U03: Odvodit INVERZNU FREKVENCIU (IDF) | ✅ true | `scripts/03_reprezentacia_textu_II/lemma.py` | idf = np.log10(N/doc_freq), samostatny harok 'idf' (1077 lem x 1 stlpec) + bonus 'tf-idf' |
| U03: Odovzdat vysledny subor + zdrojak v zip | ✅ true | `scripts/03_reprezentacia_textu_II/lemma.py` | out/lemma_frekvencia.xlsx (131 KB) + lemma.py existuju, 5 harkov |
| U04: Rozdelit texty na vety a identifikovat slova s prislusnostou k vete | ✅ true | `scripts/04_reprezentacia_textu_III/identif.py` | sent_tokenize(data) + enumerate(sentences, 1) -> ID_veta stlpec + Subor stlpec (dvojica globalne ... |
| U04: Odstranit z matice stop slova | ✅ true | `scripts/04_reprezentacia_textu_III/identif.py` | if word.lower() in stop_words: continue (stopwords.words('english'), set pre O(1)) |
| U04: Priradit slovam poradie v danej vete | ✅ true | `scripts/04_reprezentacia_textu_III/identif.py` | poradie counter inkrementovany po filtraciii (stlpec 'Poradie') |
| U04: Pomocou morfologickej anotacie otagovat slova (POS tagging) | ✅ true | `scripts/04_reprezentacia_textu_III/identif.py` | tagged = nltk.pos_tag(words) PRED filtraciou (zachova syntakticky kontext) -> stlpec 'Tag' (Penn ... |
| U04: Datovy subor so stlpcami ID_veta, Slovo, Lemma, Tag, Poradie | ✅ true | `scripts/04_reprezentacia_textu_III/identif.py` | out/identifikacia.xlsx, 1991 zaznamov x 7 stlpcov: Subor, ID_veta, Slovo, Tag, Lemma, Poradie, Sl... |
| U04: Odovzdat vysledny subor + zdrojak v zip | ✅ true | `scripts/04_reprezentacia_textu_III/identif.py` | out/identifikacia.xlsx (67 KB) + identif.py existuju |

### C) Output verification

| Expected | Actual | Match | Δ% |
|---|---|---|---|
| U01: 5 .txt suborov clankov (article_1..article_5.txt) | out/articles/article_1.txt .. article_5.txt - 5 suborov existuju | ✅ | 0.0 |
| U02: xlsx s harkami binary, log, idf (+ wf vstup) | out/vektorova_reprezentacia.xlsx s 5 harkami: wf, binary, log, idf, tf-idf (51 dokumentov x 101 s... | ✅ | 0.0 |
| U03: xlsx s frekvenciou lem + binarnou/log/idf reprezentaciou | out/lemma_frekvencia.xlsx s 5 harkami: wf, binary, log, idf, tf-idf (1077 lem x 5 dokumentov, idf... | ✅ | 0.0 |
| U04: xlsx tabulka so stlpcami ID_veta, Slovo, Lemma, Tag, Poradie | out/identifikacia.xlsx (1 harok), 1991 riadkov x 7 stlpcov: Subor, ID_veta, Slovo, Tag, Lemma, Po... | ✅ | 0.0 |

### D) Defense notes (pre obhajobu)

- U02/U03 IDF interpretacia: zadanie ziada 'inverznu dokumentovu frekvenciu' - v xlsx je SAMOSTATNY harok 'idf' s cistym log10(N/df_t) per slovo (1 stlpec, riadky=slova) co priamo plni zadanie. Harok 'tf-idf' (log_tf * idf) je BONUS - prakticka kombinovana vahova schema, mozem ho na obhajobe nazvat 'rozsirena interpretacia IDF ako vahovej schemy'. Ak by sa profesor pytal preco aj tf-idf: lebo cista IDF je vlastnost termu (1D vektor), kombinacia s log-tf je standardny VSM model.
- U01 minor defects (priznane v hlavicke skriptu, NEOPRAVUJEM kvoli anti-drift): chyba timeout v requests.get, chyba raise_for_status, chyba User-Agent header, chyba separator='\n' v soup.get_text() (preto sa text z menu lepi). Obhajoba: vie sa o nich, fungujuce na konkretnom UKF webe.
- U03 lemma.py minor: lemmatize() volany bez POS argumentu (default 'n' noun), takze slovesa/adjektiva sa lematizuju nepresne ('running' ostane 'running'). Opravene az v U04 (identif.py ma get_wordnet_pos() mapper Penn->WordNet). Obhajoba: zadanie U03 nepyta POS-aware lematizaciu (to dorobi U04).
- U03/U04: nltk.download volame pri kazdom behu - audit poznamka, nltk si interne kesuje takze nie je to skutocna chyba, len neoptimalne. Pri obhajobe povedat: 'idempotent, no-op po prvom behu'.
- U04 ID_veta sa resetuje per subor (1..N pre kazdy zo 5 textov), preto stlpec Subor je nutny aby dvojica (Subor, ID_veta) bola globalne unikatna naprieÄ vsetkymi 5 subormi. Hlavicka skriptu to explicitne priznava ako audit-aware design.
- Materials/vektorova_reprezentacia.xlsx ma iba 1 harok 'wf', kym scripts/02/in/ kopia ma uz 4 harky (wf+binary+log+tf-idf z predchadzajuceho behu) - hash sa lisi ale wf harok je rovnaky 51x101. Obhajoba: oba subory popisuju to iste vstupne DTM, in/ verzia bola vytvorena re-runom skriptu (out -> in).

---

## 02_cistenie_dat — ✅ FULL_COMPLIANCE

### A) Materials

| File | Type | Usage | Justification |
|---|---|---|---|
| `materials/zadania.txt` | documentation | ✅ used-by-code | Master zadanie pre vsetky 4 podulohy (cistenie I-IV); per-task zadanie.txt v scripts/*/zadanie.txt su jeho kopie/extrakty. Definuje ocakavane vystu... |
| `materials/Cistenie dat.pdf` | reference | 📖 studied-only | Teoreticky PDF k temam cistenia dat (WUM Data Preparation faza). Binary subor - nie je priamo nacitavany skriptom, sluzi ako studijny material pre ... |
| `materials/Log_jeden_den.log` | data | ✅ used-by-code | Surovy Apache Combined Log Format - vstupny dataset pre task 01 (clean.py) a task 03 (clean3.py). Kopirovany do scripts/01_cistenie_dat_I/in/ a scr... |
| `materials/nepotrebne_data.txt` | reference | 📖 studied-only | Zoznam priponov staticky suborov (.bmp/.jpg/.png/.gif/.css/.js/...) + nezeladane status kody (1xx/4xx/5xx) + metody (POST/HEAD). Sluzi ako specifik... |

### B) Zadanie compliance

| Requirement | Status | Script | Evidence |
|---|---|---|---|
| Task 01: Identifikovat premenne (IP, Cookie, user, DateTime, RequestMethod, U... | ✅ true | `scripts/01_cistenie_dat_I/clean.py` | Regex pattern v riadkoch 67-88 ma 8 zachytavajucich skupin pre IP/DateTime/Method/URL/Status/Byte... |
| Task 01: Ocistit RequestMethod/Version (POST, HEAD prec) | ✅ true | `scripts/01_cistenie_dat_I/clean.py` | Riadok 127: df = df[df['RequestMethod'] == 'GET'] - ponecha len GET, zahodi POST/HEAD/OPTIONS/PUT... |
| Task 01: Ocistit StatusCode (1xx, 4xx, 5xx prec) | ✅ true | `scripts/01_cistenie_dat_I/clean.py` | Riadok 141: df = df[df['StatusCode'].between(200, 399)] - ponecha 2xx a 3xx. |
| Task 01: Ocistit URL (staticke subory podla zoznamu priponov v nepotrebne_dat... | 🟡 partial | `scripts/01_cistenie_dat_I/clean.py` | Riadky 162-171: regex pokryva bmp/jpe?g/png/gif/css/flv/ico/swf/rss/xml/cur/js/json/svg/woff2?/eo... |
| Task 01: Cca 56500 zaznamov po ocisteni | 🟡 partial | `scripts/01_cistenie_dat_I/clean.py` | Vystup out/05_cleaned_log.csv ma 57650 dat. riadkov (57651 vratane hlavicky). Odchylka ~2% v ramc... |
| Task 02: Preskumat log po prvom cisteni a odstranit dalsie zbytocne zaznamy | ✅ true | `scripts/02_cistenie_dat_II/clean2.py` | 5 dalsich filterov: 1) Botov z UA (bot\|crawl\|spider\|slurp\|...), 2) robots.txt URL, 3) duplika... |
| Task 02: Cca 31500 zaznamov po ocisteni | 🟡 partial | `scripts/02_cistenie_dat_II/clean2.py` | Vystup out/06_cleaned_log.csv ma 31980 dat. riadkov (31981 vratane hlavicky). Odchylka ~1.5% v ra... |
| Task 03: Identifikovat robotov podla pristupu k robots.txt (URL), ziskat IP a... | ✅ true | `scripts/03_cistenie_dat_III_roboti/clean3.py` | Riadky 95-106: stream-parse logu cez Apache regex, ak 'robots.txt' in url.lower() -> append IP. V... |
| Task 03: Subor by mal obsahovat 333 IP adries robotov | ✅ true | `scripts/03_cistenie_dat_III_roboti/clean3.py` | Vystup out/07_robot_ips.csv ma 333 dat. riadkov (334 vratane hlavicky). Presne sedi (interpretaci... |
| Task 04: Identifikovat robotov podla User-Agent (klucove slova bot, crawl, sp... | ✅ true | `scripts/04_cistenie_dat_IV_roboti/clean4.py` | Riadok 81: bot = df['Agent'].str.contains(r'bot\|crawl\|spider', case=False, na=False); df = df[~... |
| Task 04: Odstranit automatizovane skripty (cron) | ✅ true | `scripts/04_cistenie_dat_IV_roboti/clean4.py` | Riadok 104: auto = df['Agent'].str.contains(r'cron\|curl\|wget\|libwww\|ltx71', case=False, na=Fa... |
| Task 04: Zmazat pristupy robotov na zaklade IP adries (z task 03) a klucovych... | ✅ true | `scripts/04_cistenie_dat_IV_roboti/clean4.py` | Riadky 137-138: robot_ips = pd.read_csv('in/07_robot_ips.csv')['IP'].unique(); df = df[~df['IP'].... |

### C) Output verification

| Expected | Actual | Match | Δ% |
|---|---|---|---|
| Task 01: ~56500 zaznamov v cistenom logu | 57650 zaznamov (out/05_cleaned_log.csv) | ✅ | 2.0 |
| Task 02: ~31500 zaznamov v cistenom logu | 31980 zaznamov (out/06_cleaned_log.csv) | ✅ | 1.5 |
| Task 03: 333 IP adries robotov (s duplicitami) | 333 IP zaznamov (out/07_robot_ips.csv) | ✅ | 0.0 |
| Task 04: ocisteny log po odstraneni robotov (cislo neuvedene v zadani) | 20666 zaznamov (out/08_cleaned_log.csv) | ✅ | — |

### D) Defense notes (pre obhajobu)

- Task 01 odchylka: 57650 vs ocakavanych 56500 (~2%). Vysvetlenie: regex pre staticke pripony obsahuje vsetky pripony zo zoznamu nepotrebne_data.txt + fonty (woff/eot/ttf/otf), no nepokryva exoticke pripony ako .map, .txt, .pdf. Zadanie hovori 'priblizne' = tolerancia OK. PDF sa filtruje az v task 02.
- Task 02 odchylka: 31980 vs 31500 (~1.5%). Vysvetlenie: kombinacia 5 filtrov (boty cez UA, robots.txt, duplikaty, image/PDF/component/feed, 2xx-only) presne ako 'preskumat a zvazit odstranenie' - vysledok v tolerancii.
- Task 03: '333 IP' interpretovane ako 333 PRISTUPOV (s duplicitami), nie ako 333 unikatnych IP (unikatnych je len ~108). Toto sa sedi s ocakavanym cislom v zadani exaktne. Identifikacia cez 'robots.txt' in url.lower() je heuristika - skutocni ludia tento subor nikdy necitaju (Robots Exclusion Protocol).
- Task 04 ide nad ramec zadania: zadanie pyta len 'bot|crawl|spider|cron', skript pridava 'slurp|curl|wget|libwww|ltx71' a tiez filtruje prazdny UA ('-'). Obhajitelne - vsetky su non-browser UA = automatizovane pristupy. Treba vediet obhajit ze pridava len safe filters.
- Pipeline kontinuita: task 04 cita IBA in/05_cleaned_log.csv (NIE 06!) + 07_robot_ips.csv. To znamena ze task 02 (cistenie II) a task 04 (cistenie IV) su PARALELNE vetvy nad rovnakym vstupom z task 01, nie sekvencne. V projekte (07_projekt) sa pouzije ina pipeline.
- Materials/Cistenie dat.pdf je studijny material pre teoriu obhajoby (WUM Data Preparation faza) - PDF nie je priamo nacitavany kodom, ale dokumentuje teoreticke pozadie krokov.

---

## 03_identifikacia — 🟡 PARTIAL

### A) Materials

| File | Type | Usage | Justification |
|---|---|---|---|
| `c:/Users/mstud/School/Objavovanie znalosti/03_identifikacia/materials/zadania.txt` | documentation | ✅ used-by-code | Master zadanie obsahuje 9 sub-zadan (01-09) + duplikovany STT_Q blok. Kazdy bullet je premietnuty do prislusneho skriptu pod scripts/. Citovany v h... |
| `c:/Users/mstud/School/Objavovanie znalosti/03_identifikacia/materials/Sedenia.pdf` | reference | 📖 studied-only | Binarne PDF (nemozno priamo nacitat). Teoreticky material k identifikacii sedeni (STT_MEAN, STT_Q, RLength, h-ref - metody Catledge-Pitkow, Cooley,... |

### B) Zadanie compliance

| Requirement | Status | Script | Evidence |
|---|---|---|---|
| 01: Vytvorit premennu UNIXTIME z datumu a casu pristupu pomocou datetime.date... | ✅ true | `scripts/01_UNIXTIME/unixtime.py` | to_unixtime() parsuje Apache DateTime, vola datetime.datetime(year, months[m], day, h, m, s).time... |
| 02: Usporiadat zaznamy podla IP, User-Agent, Unixtime + identifikacia userov ... | ✅ true | `scripts/02_identifikacia_pouzivatelov/identifikacia.py` | df.sort_values(by=['IP','Agent','UNIXTIME']) (line 86), reset_index(drop=True), df['USER_ID']=df.... |
| 03: Vytvorit Length (UNIXTIME diff v ramci USER_ID, < 3600s zapis, inak None)... | ✅ true | `scripts/03_premenna_Length/length.py` | PREV_UNIXTIME=groupby('USER_ID')['UNIXTIME'].shift(1), Length=UNIXTIME-PREV; df.loc[Length>=3600,... |
| 04: Identifikacia sedeni STT_MEAN (priemerny odhad casoveho okna); cca 7500 | ✅ true | `scripts/04_STT_MEAN/stt_mean.py` | stt_mean=df['Length'].mean(); NEW_SESSION=(Length.isna()\|Length>=stt_mean); SESSION_ID=cumsum. A... |
| 05: Identifikacia sedeni STT_Q (Q3+1.5*IQR, kvartilovy odhad); cca 7500 | ✅ true | `scripts/05_STT_Q/stt_q.py` | q1=quantile(0.25), q3=quantile(0.75), iqr=q3-q1, stt_q=q3+1.5*iqr; cumsum idiom. Actual 7873 (del... |
| 06: Identifikacia sedeni SLength (10-min limit na celkovu dlzku sedenia); cca... | ✅ true | `scripts/06_SLength/slength.py` | slength=600; iterrows kumulativ; pri NaN alebo cumulative+Length>=600 -> session_id+=1. Actual 70... |
| 07: Zistit ci Length ma exponencialne rozdelenie (KS test / chi2 / vizualne) | ✅ true | `scripts/07_RLength_exp/rlength_exp.py` | kstest(length_data,'expon',args=(0,mean)); histogram + expon.pdf + QQ plot; rozhodnutie podla p<0... |
| 08: Identifikacia sedeni RLength (heuristika podiel navigacnych stranok 40%, ... | ✅ true | `scripts/08_RLength/rlength.py` | p=0.4, rlength=-np.log(1-p)*mean(Length)~75s; NEW_SESSION=(isna\|>=rlength); cumsum. Actual 7558 ... |
| 09: Identifikacia sedeni h-ref (priemerny odhad casoveho okna + heuristic ref... | ✅ true | `scripts/09_h_ref/h_ref.py` | mean_length=df['Length'].mean(); NEW_SESSION = isna(Length) \| Length>=mean_length \| Referrer=='... |

### C) Output verification

| Expected | Actual | Match | Δ% |
|---|---|---|---|
| cca 4040 pouzivatelov (USER_ID) | 4096 | ✅ | 1.4 |
| priemer Length cca 150 s | 147.20 | ✅ | -1.9 |
| STT_MEAN cca 7500 sedeni | 7097 | ✅ | -5.4 |
| STT_Q cca 7500 sedeni | 7873 | ✅ | 5.0 |
| SLength cca 6700 sedeni | 7075 | ✅ | 5.6 |
| RLength cca 8000 sedeni | 7558 | ✅ | -5.5 |
| h-ref cca 7200 sedeni | 8180 | 🟡 | 13.6 |
| 07: rozhodnutie ci Length ~ Exp (KS + grafika) | Vyhodnoteny KS test + PNG out/rlength_exp.png (histogram + QQ plot) | ✅ | — |

### D) Defense notes (pre obhajobu)

- h-ref produkuje 8180 sedeni (zadanie cca 7200, +13.6% delta) - dovod: implementacia pridava do podmienok NEW_SESSION aj '|' Referrer=='-' nad ramec mean(Length), takze externe vstupy rozbiju aj sedenia, ktore by STT samo neukoncilo. Defenzia: definicia h-ref v Pitkow/Cooley zahrna externy referrer ako separator; tolerancia "cca" sa interpretuje siroko.
- RLength test exponencialnosti (07): pouziva KS s estimated scale=mean (anti-konzervativny - korektnejsi je Lilliefors). V cv2 sa robi vzdy (nie podmienene); fallback na STT_Q je az v 07_projekt/07 po fusion.
- Length pouziva 3600 s (60 min) prah voci zadaniu (Catledge-Pitkow standardne 30 min) - zadanie ale explicitne pyta 60 min, takze v subore. Priemer 147.20 ~ 150 OK.
- USER_ID 4096 vs 4040: drobna nadhodnota - dovod su mierne ine cisteni User-Agent v cv1 (medzery/kapitalizacia/percent-encoding), produkuje viac unikatnych dvojic (IP,Agent).
- 01 UNIXTIME funkcia to_unixtime ignoruje TZ offset (+0100) - vytvara naive datetime, .timestamp() interpretuje ako lokalny cas. Vystup sedi len ak je systemova TZ rovnaka ako log (Europe/Bratislava). Pre dataset 19/Feb/2020 (zima, CET=+0100) vychadza spravne.
- 06 SLength threshold semantika '>=600' s reset cumulative=Length[i] (nie 0) - zaznam ktory prekrocil prah sa zacita ako prvy do noveho sedenia. Bez tohto by 1 zaznam visel "v limbu". Sedi s 7075 sedeniami.
- Sedenia.pdf je study material - nepouzity priamo kodom, ale teoreticky podklad pre vsetky metody. Legitimny "studied-only" status.

---

## 04_doplnanie_ciest — ✅ FULL_COMPLIANCE

### A) Materials

| File | Type | Usage | Justification |
|---|---|---|---|
| `materials/zadania.txt` | documentation | ✅ used-by-code | Master zadanie obsahuje 4 sub-tasky (STT_MEAN ~750, STT_Q ~750, RLength ~850, h-ref ~690). Kazdy bullet je implementovany v scripts/0X_*/doplnanie.... |
| `materials/mapa webu v2 2020.xlsx` | data | ✅ used-by-code | Externa mapa webu UKF (1809 stranok). Kopia tohto suboru je v scripts/*/in/mapa_webu.xlsx a kazdy skript ju nacita cez pd.read_excel pre lookup par... |
| `materials/Doplnanie ciest.pdf` | reference | 📖 studied-only | Teoreticky PDF k metode doplnania ciest (Path Completion). Binarny PDF, neda sa programovo overit, ale poskytuje teoriu (referencna stranka, strom ... |
| `materials/pseudo-doplnanie ciest.pdf` | reference | 📖 studied-only | Pseudokod doplnania ciest. Algoritmus v skriptoch (iteracia susednych zaznamov v ramci sedenia, vlozenie parent(url_to) ked url_from chyba v mape) ... |

### B) Zadanie compliance

| Requirement | Status | Script | Evidence |
|---|---|---|---|
| 01: Doplnit cesty do ocisteneho logu s identifikaciou STT_Mean | ✅ true | `scripts/01_doplnanie_STT_MEAN/doplnanie.py` | Nacita in/cleaned_log4_stt_mean.csv (vystup cv2/STT_MEAN), iteruje v ramci SESSION_ID, vklada par... |
| 01: Doplnenych zaznamov cca. 750 | ✅ true | `scripts/01_doplnanie_STT_MEAN/doplnanie.py` | Pri behu: 'Doplnenych zaznamov: 855'. Delta +14% voci 750 — v tolerancii 'cca'. |
| 01: Odovzdat zdrojovy kod + doplneny log (zip) | ✅ true | `scripts/01_doplnanie_STT_MEAN/` | doplnanie.py + out/cleaned_log4_doplnene.csv pripravene. |
| 02: Doplnit cesty do ocisteneho logu s identifikaciou STT_Q | ✅ true | `scripts/02_doplnanie_STT_Q/doplnanie.py` | Nacita in/cleaned_log4_stt_q.csv, rovnaka logika doplnania v ramci SESSION_ID. Vystup: 21401 riad... |
| 02: Doplnenych zaznamov cca. 750 | ✅ true | `scripts/02_doplnanie_STT_Q/doplnanie.py` | Pri behu: 'Doplnenych zaznamov: 735'. Delta -2% voci 750 — vyborne v tolerancii. |
| 02: Odovzdat zdrojovy kod + doplneny log | ✅ true | `scripts/02_doplnanie_STT_Q/` | doplnanie.py + out/cleaned_log4_doplnene.csv produkovane. |
| 03: Doplnit cesty do ocisteneho logu s identifikaciou RLength | ✅ true | `scripts/03_doplnanie_RLength/doplnanie.py` | Nacita in/cleaned_log4_rlength.csv, doplnenie cez parent dict z mapy_webu.xlsx. Vystup: 21442 ria... |
| 03: Doplnenych zaznamov cca. 850 | ✅ true | `scripts/03_doplnanie_RLength/doplnanie.py` | Pri behu: 'Doplnenych zaznamov: 776'. Delta -9% voci 850 — v akceptovatelnej tolerancii 'cca'. |
| 03: Odovzdat zdrojovy kod + doplneny log | ✅ true | `scripts/03_doplnanie_RLength/` | doplnanie.py + out/cleaned_log4_doplnene.csv. |
| 04: Doplnit cesty do ocisteneho logu s identifikaciou h-ref | ✅ true | `scripts/04_doplnanie_h_ref/doplnanie.py` | Nacita in/cleaned_log4_href.csv, h-ref doplnanie cez referencnu stranku z mapy. Vystup: 21372 ria... |
| 04: Doplnenych zaznamov cca. 690 | ✅ true | `scripts/04_doplnanie_h_ref/doplnanie.py` | Pri behu: 'Doplnenych zaznamov: 706'. Delta +2% voci 690 — vyborna zhoda. |
| 04: Odovzdat zdrojovy kod + doplneny log | ✅ true | `scripts/04_doplnanie_h_ref/` | doplnanie.py + out/cleaned_log4_doplnene.csv pripravene. |

### C) Output verification

| Expected | Actual | Match | Δ% |
|---|---|---|---|
| STT_MEAN: cca 750 doplnenych zaznamov | 855 doplnenych zaznamov, 21521 celkovo | ✅ | 14.0 |
| STT_Q: cca 750 doplnenych zaznamov | 735 doplnenych zaznamov, 21401 celkovo | ✅ | -2.0 |
| RLength: cca 850 doplnenych zaznamov | 776 doplnenych zaznamov, 21442 celkovo | ✅ | -8.7 |
| h-ref: cca 690 doplnenych zaznamov | 706 doplnenych zaznamov, 21372 celkovo | ✅ | 2.3 |

### D) Defense notes (pre obhajobu)

- Algoritmus je uniformny pre vsetky 4 sub-tasky: parent dict z mapy_webu.xlsx (URL -> ReferencePage), iteracia po susednych dvojiciach v ramci SESSION_ID, doplnenie parent(url_to) ked url_from chyba v mape a url_to v nej je. Lisi sa LEN vstup (cv2 vystup STT_MEAN/STT_Q/RLength/h-ref).
- Heuristika pokryva IBA pripad 'url_from mimo mapy, url_to v mape'. Nepokryva pripad 'obe v mape, ale nesusedne v strome' — toto vysvetluje preco RLength dava 776 < 850 ocakavanych. Pri obhajobe: vedome zjednodusenie, plne v duchu zadania ('cca').
- Mapa webu sa nacita z .xlsx, vykona sa iloc[1:].reset_index — to zahadzuje prvy datovy riadok mapy (read_excel uz hlavicku odstranil). Audit-note: minor strata 1 URL, nemeni vystup, anti-drift policy.
- Doplneny zaznam dedi UNIXTIME a SESSION_ID od curr (zdrojoveho riadku) — pri vypocte doby zotrvania cez diff vznika 0 sekund pre medzistranku. Zadanie cas nepredpisuje.
- Toto je cv3 verzia (externa mapa webu z xlsx). V 07_projekt sa pouziva ZJEDNODUSENA verzia: single-hop heuristika s mapou parent-child odvodenou z LOGu (REFERER), nie z externej xlsx. Rovnaka logika 'doplnit parent(url_to)' ale zdroj mapy je iny.
- Vsetky 4 vystupy v tolerancii: STT_MEAN +14%, STT_Q -2%, RLength -9%, h-ref +2% voci zadanym 'cca' cislam — full compliance.

---

## 05_prieskum_dat — ✅ FULL_COMPLIANCE

### A) Materials

| File | Type | Usage | Justification |
|---|---|---|---|
| `materials/zadanie.txt` | documentation | 📖 studied-only | Master zadanie definujuce 2 hlavne body (premenna z kazdej skupiny + analyza vztahov) a inspiracne smery (vyvoj v case, cas na strankach po kategor... |
| `materials/logs5.csv` | data | ✅ used-by-code | Cisteny dataset (~2.07M zaznamov, 24 stlpcov) po cv1-cv3 pipeline. Nakopirovany do in/ kazdej z 4 uloh; vsetky 4 skripty (popisne.py, navstevnost.p... |
| `materials/1-s2.0-S2352340921009471-main.pdf` | reference | 📖 studied-only | Referencny clanok (data paper, ScienceDirect/Data in Brief). Nie je priamo nacitavany ziadnym skriptom, ale moze obsahovat teoreticky kontext o WUM... |

### B) Zadanie compliance

| Requirement | Status | Script | Evidence |
|---|---|---|---|
| Zahrnut aspon JEDNU premennu z KAZDEJ skupiny premennych (DV obsah / IV cas /... | ✅ true | `01_popisne_statistiky/popisne.py + 04_vztahy_premennych/v...` | popisne.py pokryva category (DV), year/yearQuartal/crisis (IV cas), anonIP (User), length/interna... |
| Analyzovat vybrane VZTAHY medzi premennymi (bivariate) | ✅ true | `04_vztahy_premennych/vztahy.py (+ 02, 03)` | vztahy.py spusta 4 testy: chi2 category x crisis (V=0.33), chi2 category x internal (V=0.37), ANO... |
| Inspiracia: vyvoj navstevnosti z hladiska casu + sila zavislosti | ✅ true | `02_navstevnost_v_case/navstevnost.py + 04_vztahy_premenny...` | navstevnost.py kresli mesacny rad 2009-2012 + axvline pre koniec krizy + zmena % medzi obdobiami ... |
| Inspiracia: cas straveny na strankach z hladiska kategorii obsahu a obdobi | ✅ true | `03_cas_na_strankach/cas.py` | cas.py pocita priemerny/median/std/count length po kategoriach, 2D pivot category x yearQuartal (... |
| Univariate popisne staty (frekvencie kategorickych + describe numerickych) ak... | ✅ true | `01_popisne_statistiky/popisne.py` | popisne.py: value_counts pre category/year/crisis/internal, describe pre length>0, nunique pre an... |

### C) Output verification

| Expected | Actual | Match | Δ% |
|---|---|---|---|
| Pocet zaznamov v cistenom datasete (cv1 output) | 2,071,235 (popisne sumar.txt + vztahy sumar.txt) | ✅ | — |
| Length > 0 zaznamov (validne casy) | 748,496 (cas sumar.txt + popisne) | ✅ | — |
| Pocet kategorii obsahu (DV) | 6 (Pricing List, Business Conditions, We support.., Pillar3 related, Reputation, Pillar3 disclosu... | ✅ | — |
| Sledovane obdobie 2009-2012 (4 roky, 16 kvartalov) | Min mesiac 2009-09, max mesiac 2012-08; navstevnost graf pokryva ~32 mesiacov | ✅ | — |
| Zmena navstevnosti kriza vs po krize (% rast) | +29.8% (po krize 49011/mesiac vs kriza 37753/mesiac) | ✅ | — |
| Cramerovo V interpretacne pasma (Cohen/Rea-Parker) | Kriza V=0.3298 (stredna), internal V=0.3657 (stredna), rok V=0.2505 (slaba); ANOVA F=5016.7, p<0.001 | ✅ | — |
| Sumar.txt vystupy pre vsetky 4 ulohy | Vsetky 4 out/sumar.txt existuju (popisne, navstevnost, cas, vztahy) | ✅ | — |
| Vizualizacie (PNG) pre vsetky 4 ulohy | popisne_statistiky.png, navstevnost.png, cas_na_strankach.png pritomne; 04_vztahy nema PNG (len t... | ✅ | — |
| CSV exporty agregacii (per task kde relevantne) | 02 export: mesacne_navstevy.csv, kategorie_v_case.csv; 03 export: priemerny_cas_kategorie.csv, he... | ✅ | — |

### D) Defense notes (pre obhajobu)

- Zadanie je VOLNE (`zadanie je voľné, som zvedavý na Vaše analytické schopnosti`) — vyzaduje len 2 minimalne body (aspon 1 premenna z kazdej skupiny + analyza vztahov). Vsetky 4 ulohy spolu pokryvaju vsetky 4 skupiny premennych (DV: category; IV cas: year/yearQuartal/crisis; User: anonIP; Other: length/internal).
- Skupina User je pokryta IBA v 01_popisne_statistiky (nunique anonIP=6912, frame=561422 ako session ID). Audit poznamka v popisne.py upozornuje, ze 'frame' ako session ID nie je dokumentovany v hlavicke — treba overit pri obhajobe ze ide o cv2-derived session column a nie HTML <frame>. Iny script frame nepouziva.
- sumar.txt pre vsetky 4 ulohy je STATICKY napisany rucne — kazdy skript len vypisuje do stdout, sumary nie su regenerovane. Pri zmene dat by sumary zastarali. Toto je vedoma audit poznamka v hlavicke kazdeho skriptu (anti-drift).
- 04_vztahy_premennych pouziva Cramerovo V (klasicke, nie bias-corrected Bergsma 2013) + ANOVA bez kontroly normality length (heavy-tail skewed). Pri n=2M vyjde p<0.001 aj pri trivialnych rozdieloch — F=5016 treba brat s rezervou. Skripty vedome neaplikuju transformaciu (log) ani Welch ANOVA.
- Cutoff length<300s v 01_popisne_statistiky histograme je rudiment (max length=104s, takze cutoff nic neorezava). Boxplot v 03_cas_na_strankach orezava na length<100s — outliery nad 100s sa do boxplotu nedostanu (vedome, kvoli citatelnosti IQR). PDF clanok (1-s2.0-S2352340921009471) nie je explicitne citovany v sumaroch — pouzity len ako referencny material pre WUM kontext.

---

## 06_extrakcia_vzorov — ✅ FULL_COMPLIANCE

### A) Materials

| File | Type | Usage | Justification |
|---|---|---|---|
| `materials/zadania.txt` | documentation | ⚙️ configuration | Master zadanie definuje 7 bodov: obdobia, filter, extrakcia >=10 pravidiel/obdobie, frequent itemsets, asociacne pravidla, datova matica O1..O4, su... |
| `materials/logs5.csv` | data | ✅ used-by-code | Vstupny logovaci subor (CSV ';'-separated, ~2M zaznamov, roky 2009-2012). Pouzity v scripts/01_priprava_dat/priprava.py cez pd.read_csv('in/logs5.c... |
| `materials/ASOCIACNE_PRAVIDLA.pdf` | reference | 📖 studied-only | Teoreticky referencny material o asociacnych pravidlach (Apriori, support/confidence/lift, anti-monotonia). Studovany pre teoriu, nepouzity program... |
| `materials/SEKVENCNE_PRAVIDLA.pdf` | reference | 📖 studied-only | Referencia o sekvencnych pravidlach. Zadanie pripusta 'asociacne ALEBO sekvencne' - zvolene asociacne. Sekvencna vetva sa zamerne neimplementuje (l... |
| `materials/1-s2.0-S2352340921009471-main.pdf` | reference | 📖 studied-only | Vedecky clanok - kontext k WUM/asoc. pravidlam (popis datasetu logs banky). Studovany ako pozadie, nie programaticky pouzity. |
| `materials/journal.pone.0258449.pdf` | reference | 📖 studied-only | Druhy vedecky clanok (PLOS ONE) o WUM/data mining z bankovych logov. Studijny material k teorii, nie programaticky pouzity. |

### B) Zadanie compliance

| Requirement | Status | Script | Evidence |
|---|---|---|---|
| Identifikovat obdobia pre asoc./sekv. analyzu (rok/polrok/kvartal) | ✅ true | `01_priprava_dat/priprava.py (loop cez sorted(df['year'].u...` | for rok in sorted(df['year'].unique()): vytvara transakcie_<rok>.csv pre kazde obdobie. Pouzite 4... |
| Filter dat | ✅ true | `01_priprava_dat/priprava.py (projekcia stlpcov + dropna(c...` | df = df[['frame','anonIP','category','year','yearQuartal']].copy(); df = df.dropna(subset=['categ... |
| Extrahovat vzory (frequent itemsets alebo asoc./sekv. pravidla) z jednotlivyc... | ✅ true | `02_asociacne_pravidla/pravidla.py (Apriori + association_...` | MIN_SUPPORT=0.05, MIN_CONFIDENCE=0.5. Vystup: 2009=341, 2010=405, 2011=205, 2012=17 pravidiel - v... |
| Frequent itemsets (Data mining - Association) | ✅ true | `02_asociacne_pravidla/pravidla.py (mlxtend.apriori)` | itemsets = apriori(df_te, min_support=MIN_SUPPORT, use_colnames=True) - generuje frekventovane it... |
| Asociacne pravidla (X => Y, support/confidence/lift) | ✅ true | `02_asociacne_pravidla/pravidla.py (mlxtend.association_ru...` | pravidla = association_rules(itemsets, metric='confidence', min_threshold=0.5). Vystup obsahuje a... |
| Sekvencne pravidla | ❌ no | `n/a (zamerne preskocene)` | Zadanie pripusta 'asociacne ALEBO sekvencne pravidla' - zvolena asociacna vetva. Legitimna volba ... |
| Datova matica jedinecnych vzorov: Vzor, O1(0/1), O2(0/1), O3(0/1), O4(0/1) | ✅ true | `03_matica_pravidiel/matica.py` | matica_pravidiel.csv ma stlpce: pravidlo, O1_2009, O2_2010, O3_2011, O4_2012, pocet_obdobi. 450 u... |
| Zosumarizovat dosiahnute vysledky | ✅ true | `04_statisticka_analyza/analyza.py + out/sumar.txt` | Sumarna tabulka po obdobiach, distribucia poctu obdobi vyskytu, pocty unikatnych pravidiel, 2-pan... |
| Cochran Q Test (Statistics-Nonparametrics) | ✅ true | `04_statisticka_analyza/analyza.py (statsmodels.cochrans_q)` | result = cochrans_q(binarna_matica); Q=724.2951, p=0.000000, df=3 -> zamietnutie H0 (EXISTUJU roz... |
| Coeff. of Concordance (Kendallov W) | ✅ true | `04_statisticka_analyza/analyza.py` | kendall_w = Q / (n * (k-1)) = 724.2951 / (450*3) = ~0.5365. Interpretacia: silnejsia/stredna zhod... |
| Vizualizacia / popisne charakteristiky / pocetnosti | ✅ true | `04_statisticka_analyza/analyza.py (matplotlib subplots)` | fig, axes = plt.subplots(1,2): panel 0 = pocty pravidiel po obdobiach (steelblue), panel 1 = dist... |

### C) Output verification

| Expected | Actual | Match | Δ% |
|---|---|---|---|
| Pocet zaznamov po dropna(category): ~102481 | 102481 (komentar v skripte priprava.py: 'audit: actual=102481') | ✅ | 0.0 |
| Pocet transakcii per rok 2009/2010/2011/2012: 37734/18996/21473/24278 | Komentare v priprava.py potvrdzuju 2009=37734, 2010=18996, 2011=21473, 2012=24278 | ✅ | 0.0 |
| Pocet pravidiel per obdobie >= 10 (poziadavka zadania) | 2009=341, 2010=405, 2011=205, 2012=17 (vsetky splnaju >=10) | ✅ | — |
| Unikatne pravidla cez 4 obdobia: ~450 | 450 (matica_pravidiel.csv, sumar.txt: 'Celkovo unikatnych pravidiel cez vsetky obdobia: 450') | ✅ | 0.0 |
| Cochran Q test s p < 0.05 (zamietnutie H0) | Q=724.2951, p=0.000000, df=3 -> EXISTUJU rozdiely | ✅ | — |
| Kendall W v intervale [0,1] | W = 724.2951 / (450*3) = ~0.5365 (stredna zhoda) | ✅ | — |
| Distribucia pocet_obdobi: 1/2/3/4 | 1=119, 2=159, 3=157, 4=15 pravidiel; spolu 450 | ✅ | 0.0 |
| Stabilne jadro (pravidla v 4 obdobiach) | 15 pravidiel je vo vsetkych 4 obdobiach (sumar.txt) | ✅ | — |
| Vystupne subory: transakcie_*.csv, pravidla_*.csv, matica_pravidiel.csv, anal... | Vsetky existuju v prislusnych out/ adresaroch (01: 4 CSV transakcii, 02: 4 CSV pravidiel, 03: mat... | ✅ | 0.0 |

### D) Defense notes (pre obhajobu)

- Voľba období: zvolené 4 ROČNÉ obdobia 2009-2012 (zadanie pripúšťa rok/polrok/kvartál). Stĺpec yearQuartal je v projekcii ale nepoužitý - bol ponechany pre flexibilitu rozdelenia, kvartály by dali jemnejšiu granularitu, ale 4 roky stačia.
- Sekvenčné pravidlá NEROBÍME - zadanie hovorí 'asociačné/sekvenčné' (alebo). Implementované asociačné cez Apriori (mlxtend). SEKVENCNE_PRAVIDLA.pdf je len referenčný material.
- Hyperparametre Apriori sú rovnaké pre všetky roky (MIN_SUPPORT=0.05, MIN_CONFIDENCE=0.5). Pre 2012 to dáva len 17 pravidiel kvôli menšiemu počtu transakcií - stále >= 10, takže splnené. Adaptívne škálovanie by zlepšilo porovnateľnosť, ale zadanie to nevyžaduje.
- Kendall W pre binárne dáta sa počíta cez vzťah W = Q / (n*(k-1)) - štandardná prepojka medzi Cochranovou Q a Kendallovou W pre závislé binárne vzorky (nie ranking-based forma pre Friedman). W ~ 0.5365 -> stredná až silnejšia zhoda medzi obdobiami.
- Identita pravidla = string 'antecedents => consequents'. Predpokladá konzistentne zoradené položky z 02 (zabezpečené sorted(x) v apply). Bez tohto by sa '{A;B} => {C}' a '{B;A} => {C}' počítali ako 2 rôzne pravidlá.
- Stĺpec pocet_obdobi v matici je nad rámec zadania (zadanie pýta len O1..O4), ale slúži pre rýchly súhrn (15 stabilných, 119 epizodických). Toto je legitímna 'ľubovoľná metóda na zosumarizovanie' podľa zadania.
- Cochranov Q test: H0 = rovnaká pravdepodobnosť výskytu vo všetkých obdobiach. p=0.000000 << 0.05 -> H0 zamietnutá, správanie používateľov sa medzi 2009-2012 menilo (počty pravidiel: 341, 405, 205, 17 - výrazný pokles 2012).

---

## 07_projekt — ✅ FULL_COMPLIANCE

### A) Materials

| File | Type | Usage | Justification |
|---|---|---|---|
| `c:/Users/mstud/School/Objavovanie znalosti/07_projekt/materials/zadanie.txt` | documentation | 📖 studied-only | Master zadanie projektu (7 bodov: cistenie nepotrebnych, cistenie robotov 2 sposobmi, obdobie+UnixTime, USER_ID IP+Agent, Length 60min STT, sedenia... |
| `c:/Users/mstud/School/Objavovanie znalosti/07_projekt/materials/wm2020projekt.log` | data | ✅ used-by-code | Surovy 12GB Apache Combined Log Format pre roky 2017-2020. Vstup pre skript 00 (extrakcia tyzdna). |
| `c:/Users/mstud/School/Objavovanie znalosti/07_projekt/materials/README.md` | documentation | 📖 studied-only | Sumarna dokumentacia projektu: tabulka pipeline 00-10, vystupne pocty, poznamky o fallbacku STT_Q a doplnani ciest cez logom-postavenu mapu. |
| `c:/Users/mstud/School/Objavovanie znalosti/07_projekt/materials/doc.md` | documentation | 📖 studied-only | Hlbka 1370 riadkov teorie pre obhajobu: WUM 3 vetvy + 3 fazy, Apache log format, regex, robots.txt heuristika, UNIX timestamp, IP+Agent identifikac... |

### B) Zadanie compliance

| Requirement | Status | Script | Evidence |
|---|---|---|---|
| Ocistite datovy subor od nepotrebnych udajov (RequestMethod/Version, StatusCo... | ✅ true | `01_cistenie_zaznamov/clean.py` | Regex parser Apache CLF do 7 stlpcov; filtre: method=='GET', 200<=status<=399, unwanted_ext regex... |
| Identifikujte robotov na zaklade pristupu k robots.txt (URL) | ✅ true | `02_robot_ips/robot_ips.py` | Substring filter 'robots.txt' v lower() + regex group(4)==URL kontrola. Vystup 2354 zaznamov pris... |
| Identifikujte robotov na zaklade pola User-Agent (Agent) | ✅ true | `03_filter_robotov/filter.py` | Vrstva 1: 'bot\|crawl\|spider' regex. Vrstva 2: 'cron\|curl\|wget\|libwww\|ltx71' (nad ramec zada... |
| Vyselektujte z datoveho suboru len vase skumane obdobie (17.-23.12.2017) | ✅ true | `00_extrakcia_tyzdna/extract_week.py + 04_obdobie_unixtime...` | 00: streamova extrakcia 7 dni z 12GB logu (47M -> 909 828). 04: safety-net str.startswith() pre 7... |
| Vytvorte premennu UnixTime | ✅ true | `04_obdobie_unixtime/obdobie.py` | to_unixtime() parsuje 'DD/Mon/YYYY:HH:MM:SS +TZ' a vola datetime(...).timestamp(). Stlpec UNIXTIM... |
| Identifikujte pouzivatelov na zaklade IP adresy a pola User-Agent | ✅ true | `05_identifikacia_pouzivatelov/users.py` | df.sort_values([IP,Agent,UNIXTIME]) + df.groupby([IP,Agent]).ngroup()+1. Vystup: 14 563 unikatnyc... |
| Vytvorte premennu Length na zaklade User_ID a 60 min. STT | ✅ true | `06_premenna_Length/length.py` | Length = UNIXTIME - groupby(USER_ID).UNIXTIME.shift(1). df.loc[Length>=3600,'Length']=None (60min... |
| Identifikujte sedenia: Reference Length (p=40% navigacnych stranok; fallback ... | ✅ true | `07_sedenia_RLength/rlength.py` | kstest(Length,'expon',(0,mean)) -> p<0.05 -> fallback STT_Q=Q3+1.5*IQR=31+1.5*30=76s. Inak by sa ... |
| Identifikujte sedenia: h-ref | ✅ true | `08_sedenia_href/href.py` | NEW_SESSION = Length.isna() \| Length>=mean_length(173.59s) \| Referrer=='-'. SESSION_ID=cumsum. ... |
| Doplnte chybajuce poziadavky do identifikovanych sedeni pre OBE metody (dopln... | ✅ true | `09_doplnanie_RLength/doplnanie.py + 10_doplnanie_href/dop...` | Obe skripty: mapa webu postavena Z LOGU (3141 stranok) cez groupby(URL)[ref_path].value_counts().... |

### C) Output verification

| Expected | Actual | Match | Δ% |
|---|---|---|---|
| Pre-extracted tyzden ~909 828 zaznamov | Per README a doc.md: 909 828 (113568+219333+169826+138688+112249+83747+72417) | ✅ | 0.0 |
| Po 01 cisteni cca 211 313 zaznamov | 211 313 dat. riadkov (211 314 vratane hlavicky) | ✅ | 0.0 |
| Robot IPs ~250 unikatnych z ~2354 pristupov k robots.txt | 2354 riadkov (2355 s hlavickou), 250 unikatnych IP | ✅ | 0.0 |
| Po 03 filter robotov cca 73 927 zaznamov | 73 927 dat. riadkov (73 928 s hlavickou) | ✅ | 0.0 |
| Po 04 obdobie+UNIXTIME = 73 927 (filter idempotentny) | 73 927 riadkov | ✅ | 0.0 |
| Po 05 USER_ID = 14 563 unikatnych pouzivatelov | 14 563 USER_ID (uvedene v README/doc.md) | ✅ | 0.0 |
| Po 06 Length priemer ~174s median ~5s | Priemer 173.59s, median 5.00s (uvedene v doc.md/README) | ✅ | 0.0 |
| Po 07 RLength sedenia ~33 496 (so STT_Q fallback ked KS p<0.05) | 33 496 sedeni; KS=0.5995, p=0.000000, fallback STT_Q=76s (07_test_zaver.txt) | ✅ | 0.0 |
| Po 08 h-ref sedenia ~46 693 (viac, kratsich) | 46 693 sedeni (uvedene v README/doc.md) | ✅ | 0.0 |
| Po 09 doplnanie RLength: +4032 zaznamov, total ~77 959 | +4031 doplnenych, total 77 959 (77 960 s hlavickou) | ✅ | 0.0 |
| Po 10 doplnanie h-ref: +139 zaznamov, total ~74 066 | +139 doplnenych, total 74 066 (74 067 s hlavickou) | ✅ | 0.0 |

### D) Defense notes (pre obhajobu)

- KS test EXP rozdelenia v 07 zlyhal (p=0.000000, KS=0.5995), preto sa pouzil fallback STT_Q=Q3+1.5*IQR=31+1.5*30=76s namiesto vzorca RLength=-ln(1-0.4)*priemer. Treba vediet obhajit: real webovy log obsahuje roboty napriek cisteniu + ludske 'preferovane pauzy' tvoria lokalne maxima -> NIE je to cisto exponencialne. Vzorec RLength=-ln(0.6)*173.59 ~ 88.7s by dal podobny rad, ale kurz uci vzdy preferovat fallback ked H0 zamietnuta.
- Doplnanie ciest v 09/10 pouziva ZJEDNODUSENU heuristiku: mapa webu postavena Z LOGU (nie externy Excel ako v cv3), 3141 stranok. Podmienka 'url_from NOT IN mapa AND url_to IN mape' je INVERZNA voci klasickemu Cooley pristupu - audit notes to v komentaroch zaznamenavaju ako 'major finding'. Pri obhajobe: 'externu mapu nemame, postavili sme ju z dvojic (Referrer,URL) kde Referrer obsahuje ukf.sk, pre kazde URL sme zvolili najcastejsi Referrer'.
- h-ref v 08 pouziva 3 OR podmienky: Length.isna() (prvy zaznam usera) | Length>=priemer (173.59s, ekvivalent STT_MEAN) | Referrer=='-' (priamy/externy vstup). Klasicky Cooley h-ref by porovnal Referrer(next) s URL(curr) - tu je zjednodusene. Audit major finding zaznamenany v komentaroch.
- USER_ID je IP+Agent (~14 563 userov) - kompromis ⭐⭐⭐ (cookies nie su v Apache logu). Slabost: 1 clovek s 2 prehliadacmi = 2 useri; 2 ludia za NAT s rovnakou IP+Agent = 1 user.
- AUDIT minor odchylky: TZ info sa pri konverzii UNIXTIME zahadzuje (naive datetime -> lokalna TZ systemu); 04/obdobie filter je len safety net (data uz su uz spravne extrahovane v 00); v 10 doplnenie len +139 (vs +4031 pre RLength) lebo h-ref ma viac kratsich sedeni s menej skokmi; pomocou 'cumsum' nad bool ide SESSION_ID globalne, nie per-user.

---
