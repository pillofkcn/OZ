# AUDIT — `index_prednasky.html`

QA audit cez 4 dimenzie (vhodnosť task type, chronológia, učiteľnosť, kvalita otázok). Generované Workflow-om s 10 audit agentmi + 10 adversarial verify agentmi.

## Súhrn

| Metrika | Hodnota |
|---|---|
| Total prednášok | 10 |
| Total taskov | 301 |
| Total findings | **118** (59 major · 59 minor) |
| Task-type fit (priemer) | **84.0%** |
| Learnability (priemer) | **6.4/10** |
| Question quality (priemer) | **7.2/10** |

**Verdikty:** 🟢 GOOD: **5** · 🟡 NEEDS_WORK: **5**

**Chronológia:** 🟡 MIXED: **6** · 🟢 GOOD: **4**

## Rýchla tabuľka

| # | Prednáška | Tasks | Type fit | Chronológia | Learn | Quality | Findings | Verdict |
|---|---|---|---|---|---|---|---|---|
| P1 | Úvod do získavania znalostí | 30 | 90% | 🟢 GOOD | 7/10 | 8/10 | 8 (2 major) | 🟢 GOOD |
| P2 | Zdroje dát I — DB, text, web | 28 | 82% | 🟡 MIXED | 6/10 | 7/10 | 13 (4 major) | 🟡 NEEDS_WORK |
| P3 | Zdroje dát II — reprezentácia textu, log súbory | 32 | 78% | 🟡 MIXED | 5/10 | 7/10 | 21 (17 major) | 🟡 NEEDS_WORK |
| P4 | Proces objavovania znalostí — metodiky (CRISP-DM intro) | 27 | 78% | 🟢 GOOD | 7/10 | 7/10 | 9 (5 major) | 🟢 GOOD |
| P5 | CRISP-DM I — Porozumenie problematike a dátam | 30 | 88% | 🟢 GOOD | 7/10 | 7/10 | 10 | 🟢 GOOD |
| P6 | CRISP-DM II — Príprava dát (čistenie, roboti) | 30 | 90% | 🟡 MIXED | 7/10 | 8/10 | 8 (4 major) | 🟢 GOOD |
| P7 | CRISP-DM III — Príprava dát (UNIXTIME, používatelia, Le | 39 | 87% | 🟢 GOOD | 8/10 | 7/10 | 9 (1 major) | 🟢 GOOD |
| P8 | CRISP-DM IV — Sedenia + Doplnenie ciest | 32 | 84% | 🟡 MIXED | 6/10 | 7/10 | 13 (4 major) | 🟡 NEEDS_WORK |
| P9 | CRISP-DM V — Modelovanie | 27 | 78% | 🟡 MIXED | 5/10 | 7/10 | 16 (14 major) | 🟡 NEEDS_WORK |
| P10 | CRISP-DM VI — Evaluácia a deployment | 26 | 85% | 🟡 MIXED | 6/10 | 7/10 | 11 (8 major) | 🟡 NEEDS_WORK |

## Findings podľa typu

| Issue | Počet |
|---|---|
| `out-of-order` (Mimo poradia) | 47 |
| `duplicate` (Duplikát) | 19 |
| `ambiguous-answer` (Nejednoznačná odpoveď) | 18 |
| `broken` (Pokazené) | 13 |
| `trivial` (Triviálne) | 12 |
| `unclear` (Nejasné) | 6 |
| `wrong-type` (Zlý typ úlohy) | 3 |

**Postihnuté typy úloh:** `flash`: 27 · `quiz`: 23 · `fill`: 19 · `cat`: 17 · `match`: 16 · `order`: 16

## 🔴 Major findings (treba opraviť)

### P1 · task #8 · `cat` · Pokazené

**Aktuálne:** Roztried výroky podľa toho, ku ktorej vetve Web Miningu patria (PageRank, autority/huby, sentiment...)

**Problém:** Príklady ako PageRank, autority/huby, PrefixSpan, sentiment analýza a 'extrakcia sedení z access logu' nie sú v prednáške 1 vôbec spomenuté – prednáška len vymenuje 3 vetvy bez príkladov. Učiteľnosť: vyžaduje externé znalosti.

**Návrh opravy:** Nahradiť príklady iba pojmami z lecture 1: 'obsah stránok' / 'HTML' pre Content; 'odkazy medzi stránkami' / 'hyperlinky' pre Structure; 'logy návštev' / 'správanie používateľov' pre Usage. Alebo presunúť tento task neskôr (po prednáške, kde sa PageRank vysvetlí).

### P1 · task #18 · `match` · Nejasné

**Aktuálne:** Priraď fázu KDD k tomu, čo sa v nej deje (Predspracovanie = čistenie...)

**Problém:** Prednáška 1 iba vymenuje názvy 5 fáz, neuvádza ich popis. Detailné popisy (čistenie, doplnenie chýbajúcich hodnôt, odstránenie šumu) sú prevzaté z neskorších prednášok – pri samoštúdiu z prednášky 1 nie sú vysvetliteľné.

**Návrh opravy:** Buď preformulovať popisy na úroveň, ktorá je obsiahnutá v slide 2 (napr. 'Výber dát = identifikácia zdroja', 'Predspracovanie = úprava dát pred analýzou'), alebo presunúť task až za prednášku, kde sa fázy detailne preberajú.

### P2 · task #11 · `cat` · Pokazené

**Aktuálne:** Roztrieď zdroje dát z webu podľa toho, či ide o obsah, štruktúru alebo používanie

**Problém:** Lecture 2 listuje pod 'Web' iba Obsah, Mapa, Logovacie súbory — nešpecifikuje 'Sitemap', 'Hyperlinky', 'Záznamy klikov', 'Referrer a User-Agent'. Task vkladá P3 obsah a očakáva ho ako P2 znalosť.

**Návrh opravy:** Zjednodušiť na cat s 3 skupinami a iba 1 reprezentantom za každú (napr. 'Webové stránky','Mapa webu','Logovací súbor') — alebo zmeniť na match: kategória ↔ názov

### P2 · task #20 · `order` · Mimo poradia

**Aktuálne:** Usporiadaj kroky tvorby vektorovej reprezentácie textu od textu k TF-IDF vektoru

**Problém:** Tokenizácia a stemming sú obsahom prednášky 3 (preprocessing textu), nie P2. P2 hovorí len o vzorcoch wf/binary/log/IDF. Task predpokladá P3 znalosť.

**Návrh opravy:** Buď zúžiť kroky na P2 obsah: 'wf → binary alebo 1+log(wf) → df → IDF → kombinovaná váha'; alebo task presunúť do P3 a v P2 dať jednoduchší order 'wf → log frekvencia → df → IDF'

### P2 · task #24 · `fill` · Zlý typ úlohy

**Aktuálne:** Pri stemming-u (kmeňovaní) sa rôzne tvary slova zredukujú na spoločný ___

**Problém:** Stemming nie je obsahom prednášky 2 — je súčasťou P3 (techniky normalizácie). Učeň P2 nemá ako vedieť, čo je stemming.

**Návrh opravy:** Odstrániť task z P2 (presunúť do P3) alebo nahradiť za fill o vzorci wf/IDF — napr. 'IDF = log(N / ___)' → df

### P2 · task #27 · `quiz` · Zlý typ úlohy

**Aktuálne:** Prečo je pri výpočte word frequency (wf) potrebné najprv aplikovať stemming?

**Problém:** Stemming nie je v P2 — patrí do P3. Otázka preto presahuje obsah prednášky 2 a vyžaduje vedomosti z P3.

**Návrh opravy:** Presunúť do P3; nahradiť napr. quizom 'Prečo binary frequency môže byť výhodnejšie než wf?' alebo 'Čo je výhoda log frequency oproti wf?'

### P3 · task #2 · `match` · Mimo poradia

**Aktuálne:** Priraď techniku normalizácie slov (Stemming/Lematizácia/POS/Tokenizácia)

**Problém:** Stemming a lematizácia ako techniky nie sú v slidoch P3 vysvetlené - prednáška ukazuje len výslednú anotovanú tabuľku. Predpokladá externé znalosti.

**Návrh opravy:** Pridať flash s definíciami techník PRED tento match, alebo presunúť do prednášky o text preprocessing

### P3 · task #5 · `fill` · Mimo poradia

**Aktuálne:** Apache ___ Log Format (Combined)

**Problém:** P3 nezavádza termín 'Apache Combined Log Format' - slide ukáže príklad logu, ale neoznačuje formát. Patrí do P5/P6.

**Návrh opravy:** Presunúť do P5/P6 alebo pridať intro flash 'Apache Combined Log Format' do P3

### P3 · task #6 · `order` · Mimo poradia

**Aktuálne:** Usporiadaj polia Apache Combined Log riadku

**Problém:** Vyžaduje presnú znalosť štruktúry formátu, ktorú P3 nezavedie konceptuálne - len ukáže príklad bez popisu polí.

**Návrh opravy:** Pridať flash so štruktúrou polí Combined Log Format PRED order; alebo presunúť do P5/P6

### P3 · task #7 · `match` · Mimo poradia

**Aktuálne:** Priraď pole Apache Combined Log (IP/Method/Status/Bytes/User-Agent)

**Problém:** Polia Apache log nie sú v P3 vysvetlené ako koncepty - duplikuje obsah P5/P6.

**Návrh opravy:** Presunúť do P5/P6 kde je téma logu rozpracovaná

### P3 · task #9 · `cat` · Mimo poradia

**Aktuálne:** Roztried HTTP metódy: navigácia vs technické (filtrujú sa)

**Problém:** Filtrovanie HTTP metód pre WUM nie je v P3. Duplikuje P6 task 3.

**Návrh opravy:** Odstrániť z P3 (duplikuje P6)

### P3 · task #13 · `flash` · Mimo poradia

**Aktuálne:** Mapa webu - externá vs vybudovaná z logu, doplnenie chýbajúcich stránok

**Problém:** P3 slide 'Mapa webu' ukazuje strom + tabuľku URL/koreň/odkazujúca stránka. Flash však zachádza do path completion (Pattern Discovery) z P5/P6.

**Návrh opravy:** Preformulovať flash na obsah slide (strom + tabuľka URL/koreň/odkazujúca), path completion presunúť do P5

### P3 · task #14 · `fill` · Duplikát

**Aktuálne:** robots___.txt v koreni domény

**Problém:** robots.txt nie je v P3 slidoch. Duplikuje sa s P5 task 14 a P6 task 9.

**Návrh opravy:** Odstrániť z P3

### P3 · task #15 · `quiz` · Duplikát

**Aktuálne:** Prečo robots.txt indikuje robota

**Problém:** Téma nie je v P3. Duplikuje quiz v P5 (task 9) a P6 (task 9).

**Návrh opravy:** Odstrániť z P3

### P3 · task #16 · `order` · Mimo poradia

**Aktuálne:** Kroky čistenia Apache logu pre WUM

**Problém:** Celý WUM preprocessing pipeline - patrí do P6 (kde je takmer identický). P3 to nepokrýva.

**Návrh opravy:** Odstrániť z P3 (duplikuje P6 task 1)

### P3 · task #17 · `cat` · Mimo poradia

**Aktuálne:** Roztried záznamy: šum vs užitočná navigácia

**Problém:** WUM cleaning - patrí do P5/P6. Duplikuje sa s P5 task 14 a P6 task 6.

**Návrh opravy:** Odstrániť z P3

### P3 · task #18 · `flash` · Mimo poradia

**Aktuálne:** Techniky anonymizácie IP (hash, mask, pseudo, k-anonymita)

**Problém:** Anonymizácia nie je v P3 vôbec. K-anonymita je pokročilý koncept bez intro a nepatrí do P3.

**Návrh opravy:** Odstrániť alebo presunúť do prednášky o GDPR/etike

### P3 · task #20 · `match` · Mimo poradia

**Aktuálne:** Spôsob identifikácie užívateľa k presnosti (IP/IP+UA/Cookies/Login)

**Problém:** Identifikácia užívateľa je explicitne v P5 (task 21). P3 to nepokrýva ako koncept.

**Návrh opravy:** Presunúť do P5 alebo odstrániť (duplikuje P5)

### P3 · task #21 · `fill` · Mimo poradia

**Aktuálne:** TF-IDF penalizuje slová v ___ dokumentoch

**Problém:** TF-IDF, TF, DF, IDF NIE SÚ v slidoch P3 - prednáška spomína iba 'transakčný/sekvenčný model'. Bez definície TF-IDF sa fill nedá pochopiť.

**Návrh opravy:** Pridať flash s definíciou TF-IDF PRED tento fill; alebo odstrániť

### P3 · task #22 · `quiz` · Mimo poradia

**Aktuálne:** Prečo regex namiesto pd.read_csv pri parsovaní Apache log

**Problém:** Implementačný detail (Python/pandas) - nie je v teoretickej prednáške 3. Patrí do cvičenia.

**Návrh opravy:** Odstrániť z P3 - patrí do cv2 materiálov

### P3 · task #24 · `flash` · Duplikát

**Aktuálne:** Pasívnosť Apache logu - obmedzenie pre WUM

**Problém:** Téma pasívnosti logu nie je v P3. Duplikuje sa s P6 task 22.

**Návrh opravy:** Odstrániť z P3

### P3 · task #25 · `order` · Mimo poradia

**Aktuálne:** Fázy spracovania textu (tokenizácia → vektor)

**Problém:** Pipeline text mining nie je v slidoch P3 - lecture ukazuje len výstup (anotovaná tabuľka), nie fázy. Stop-words, vektorizácia nie sú v P3.

**Návrh opravy:** Pridať flash 'Pipeline spracovania textu' PRED order, alebo presunúť

### P3 · task #29 · `match` · Pokazené

**Aktuálne:** Priraď stĺpec tabuľky (Word/Lemma/Tag/POS/Order)

**Problém:** Lecture tabuľka má stĺpce: ID, Word, Tag, Lemma, Order, Tag_type, Post-Edit, MT@EC. Stĺpec 'POS' v tabuľke prednášky NIE JE. Používateľ sa učí nesprávne.

**Návrh opravy:** Nahradiť 'POS' za 'Tag_type' alebo 'Post-Edit' podľa skutočnej tabuľky lecture

### P4 · task #16 · `cat` · Pokazené

**Aktuálne:** Roztrieď fázy CRISP-DM časovo vs. analyticky náročné — len DP / Modeling+Evaluation

**Problém:** Cat má len 3 položky (1+2), zvyšné 3 fázy CRISP-DM (BU, DU, Deployment) chýbajú. Skupina 'Casovo narocne' s jednou položkou je tiež nešťastná — kategorizácia s 1 itemom je málo zmysluplná.

**Návrh opravy:** Premeniť na quiz 'Ktorá fáza CRISP-DM je v prednáške označená ako časovo náročná?' s odpoveďou Data Preparation, alebo pridať tretiu skupinu 'Ostatné fázy' s BU, DU, Deployment.

### P4 · task #22 · `match` · Nejasné

**Aktuálne:** Priraď oblasť KD k jej vstupu (WUM, WCM, WSM, TM, KDD)

**Problém:** Prednáška 4 uvádza WCM, WSM len ako skratky bez ich definície. Bez externej znalosti (P6) sa študent nedokáže naučiť, že WCM = obsah a WSM = štruktúra. Learnability gap.

**Návrh opravy:** Buď pridať pred tento match flash karty definujúce WCM a WSM (čo znamenajú skratky), alebo zredukovať match len na WUM + TM + KDD, ktoré sú lepšie pokryté v prednáške 4.

### P4 · task #23 · `fill` · Pokazené

**Aktuálne:** Fáza ___ ___ je časovo najnáročnejšia, 60-80 %

**Problém:** Dva blanky ('___ ___') s viacslovnou odpoveďou 'data preparation' — fill matching s viacslovnou frázou je nespoľahlivé (medzery, diakritika, EN/SK). Navyše 60-80 % nie je explicitne v prednáške 4.

**Návrh opravy:** Zmeniť na quiz s 4 možnosťami (Data Preparation/Modeling/BU/DU) alebo na flash. Vyhnúť sa fill s viacslovnou anglickou frázou.

### P4 · task #25 · `flash` · Nejednoznačná odpoveď

**Aktuálne:** Ktoré 3 fázy CRISP-DM tvoria analytické jadro?

**Problém:** Otázka pýta 'analytické jadro', odpoveď zahŕňa Data Preparation, ale samotná odpoveď vzápätí hovorí 'Data Preparation je časovo náročná, Modeling a Evaluation sú analyticky náročné' — vnútorná protirečivosť. Analytické jadro by malo byť Modeling+Evaluation.

**Návrh opravy:** Zmeniť otázku na 'Ktoré dve fázy CRISP-DM sú analyticky najnáročnejšie?' s odpoveďou 'Modeling, Evaluation', alebo preformulovať na 'Ktoré tri fázy CRISP-DM tvoria jadro procesu po porozumení dátam?'

### P4 · task #26 · `order` · Nejednoznačná odpoveď

**Aktuálne:** Usporiadaj: Validné dáta → Proces → Analytické metódy → Znalosti

**Problém:** Prednáška uvádza 'Validné dáta, Proces, Analytické metódy' ako spoločný menovateľ VP aj KD (zoznam = atribúty), NIE ako sekvenčný tok. 'Znalosti' do tohto zoznamu prednáška nepridáva — je to interpretačná konštrukcia. Kanonické poradie nie je v prednáške definované.

**Návrh opravy:** Premeniť na cat alebo flash 'Aký je spoločný menovateľ VP a KD? Validné dáta, Proces, Analytické metódy' (duplikát task 21, takže možno radšej odstrániť alebo nahradiť iným poradím — napr. usporiadaj 6 fáz CRISP-DM s WUM-mapovaním).

### P6 · task #17 · `match` · Mimo poradia

**Aktuálne:** Priraď oblasti web miningu k ich vstupom (Content/Structure/Usage)

**Problém:** Toto je úvodný koncept (Web Mining oblasti) ktorý sa logicky zaraduje na začiatok celej prednášky 6 — patrí pred všetky tasky o čistení logu a robotech, nie až ako 18. task po detailoch.

**Návrh opravy:** Presunúť pred task 0 (úvodný flash o 60-80%) ako úvodný kontext WUM.

### P6 · task #18 · `order` · Mimo poradia

**Aktuálne:** Usporiadaj 3 fázy procesu Web Usage Miningu (Data prep, Pattern discovery, Pattern analysis)

**Problém:** Toto je úplný top-level overview procesu WUM — prednáška ho zavádza ako prvé (lines 7-8). Tu sa však objavuje až po 17 detailných úlohách o čistení a sedeniach, čo bráni hierarchickému pochopeniu.

**Návrh opravy:** Presunúť hneď za task 0 alebo task 17 — pred ostatné detailné úlohy o data prep.

### P6 · task #19 · `cat` · Mimo poradia

**Aktuálne:** Roztriedi aktivity podľa fázy WUM (príprava / objavovanie vzorov / analýza vzorov)

**Problém:** Závisí od chápania troch fáz WUM (task 18). Mal by nasledovať hneď po úvodných úlohách o WUM oblastiach a fázach, nie až po polovici prednášky.

**Návrh opravy:** Presunúť ihneď za task 18 (3 fázy WUM) — vytvoriť úvodný blok 17→18→19.

### P6 · task #24 · `fill` · Pokazené

**Aktuálne:** ...platí t_i − t_{i−1} ___ τ (vložte symbol porovnania, napr. <=, >=, <)

**Problém:** Prompt obsahuje samotnú odpoveď ako hint ('napr. <=, >=, <') — to jednak prezrádza dva nesprávne odpovede a jednak odhaluje že správna je '<='. Triviálna úloha s prezradeným riešením.

**Návrh opravy:** Odstrániť '<=' z hintov a ponechať len 'symbol porovnania (≤, <, ≥, >, =)' alebo pred quiz preformulovať na quiz so 4 nerovnosťami.

### P7 · task #6 · `fill` · Nejednoznačná odpoveď

**Aktuálne:** Pri NAT môže jednu verejnú IP adresu zdieľať aj ___ a viac ľudí.

**Problém:** Číslo 100 je arbitrárne — prednáška presný počet neuvádza, mohlo by byť 50, 200, 'desiatky'. Answer matching zlyhá pri rozumných alternatívach.

**Návrh opravy:** Preformuluj na quiz s možnosťami (1-2, 10, 100+, neobmedzene), alebo vymeň na všeobecnejší fill o NAT bez konkrétneho čísla.

### P8 · task #26 · `flash` · Mimo poradia

**Aktuálne:** Aká je formálna definícia WALS (Web Access Log Set)?

**Problém:** Základná definícia WALS by mala byť úvodom — je to vstup celého procesu spomenutý v lekcii ako prvé, ale tu je až na pozícii 26 po pokročilých STT vzorcoch a doplňaní ciest.

**Návrh opravy:** Presunúť na začiatok (pred task 0) — WALS je predpoklad pre pochopenie sedení.

### P8 · task #28 · `flash` · Mimo poradia

**Aktuálne:** Aké tri zdroje informácií slúžia na identifikáciu používateľa

**Problém:** Identifikácia používateľa je v lekcii pred identifikáciou sedení a doplňaním ciest. Tu je až na konci po sedeniach a path completion — porušuje slide flow.

**Návrh opravy:** Presunúť pred tasks o sedeniach (pred task 0 alebo hneď po WALS).

### P8 · task #8 · `quiz` · Pokazené

**Aktuálne:** KS test (Kolmogorov-Smirnov) v projekte slúži na: ...

**Problém:** Otázka explicitne odkazuje na „projekt", ale lekcia 8 KS test menom nespomína (iba hovorí „ak premenná Length nemá exponenciálne rozdelenie"). Predpokladá externé znalosti z cvičení.

**Návrh opravy:** Preformulovať aby otázka necitovala „projekt" a vysvetlila prepojenie v explain: „Ak premenná Length nemá exp. rozdelenie, použijeme fallback STT_Q. Aký test overuje tento predpoklad?" + uviesť KS test ako odpoveď.

### P8 · task #16 · `order` · Nejednoznačná odpoveď

**Aktuálne:** Usporiadaj kroky výpočtu RLength s fallbackom na STT_Q

**Problém:** Položky „Ak H0 platí: ..." a „Ak H0 neplatí: ..." sú vetvy (alternatívy), nie sekvenčné kroky. V skutočnej procedúre sa vykoná iba jedna z nich, takže ich „poradie" nie je kanonické.

**Návrh opravy:** Rozdeliť na 2 menšie order tasky (jeden pre exp. cestu, jeden pre fallback) alebo premeniť na cat (parametrická vetva vs. neparametrická vetva).

### P9 · task #9 · `flash` · Mimo poradia

**Aktuálne:** Čo je asociačné pravidlo? X → Y, príklad pivo/plienky

**Problém:** Asociačné pravidlá ako pojem nie sú v prednáške 9 vôbec vysvetlené — prednáška iba uvádza 'Asociačné pravidlá' v zozname metód pre analýzu závislostí. Definícia + príklad pivo/plienky nepatrí do P9.

**Návrh opravy:** Buď presunúť do prednášky, ktorá AR skutočne preberá, alebo si overiť, či nemá byť celá AR-séria (tasks 9-20) v inej prednáške.

### P9 · task #10 · `flash` · Mimo poradia

**Aktuálne:** Vzorec pre support asociačného pravidla

**Problém:** Vzorec support v prednáške 9 vôbec nie je — prednáška AR len menuje. Student nemá z čoho sa to naučiť.

**Návrh opravy:** Presunúť mimo P9 alebo doplniť do prednášky úvodný slide o AR so vzorcami.

### P9 · task #11 · `flash` · Mimo poradia

**Aktuálne:** Vzorec pre confidence asociačného pravidla

**Problém:** Vzorec confidence v prednáške 9 nie je. Predpokladá externú znalosť.

**Návrh opravy:** Presunúť mimo P9 alebo doplniť teóriu AR do prednášky.

### P9 · task #12 · `flash` · Mimo poradia

**Aktuálne:** Vzorec pre lift a interpretácia

**Problém:** Lift v prednáške 9 vôbec nie je definovaný. Pojem je natoľko špecifický, že bez explicitnej teórie sa nedá deduktovať.

**Návrh opravy:** Presunúť mimo P9 alebo doplniť slide o miere lift do prednášky.

### P9 · task #13 · `fill` · Mimo poradia

**Aktuálne:** Miera ... obsahuje obe strany pravidla = support

**Problém:** Pojem support nie je v prednáške 9 vysvetlený. Duplikuje task 10.

**Návrh opravy:** Presunúť mimo P9; ak ostane, sankcionovať na duplicitu so 10.

### P9 · task #14 · `fill` · Mimo poradia

**Aktuálne:** Algoritmus ... využíva anti-monotónnu vlastnosť = Apriori

**Problém:** Apriori algoritmus, anti-monotónnosť, frekventované itemsety — nič z toho nie je v prednáške 9.

**Návrh opravy:** Presunúť mimo P9 do prednášky, ktorá pokrýva Apriori, alebo doplniť teóriu.

### P9 · task #15 · `quiz` · Mimo poradia

**Aktuálne:** Čo hovorí Apriori vlastnosť (anti-monotónnosť)?

**Problém:** Anti-monotónna vlastnosť nie je v prednáške 9. Učiteľnosť 0 — bez externého zdroja nemožno odpovedať.

**Návrh opravy:** Presunúť do prednášky o Apriori.

### P9 · task #16 · `order` · Mimo poradia

**Aktuálne:** Usporiadaj kroky algoritmu Apriori (načítaj, L1, kandidáti...)

**Problém:** Kroky Apriori nie sú v prednáške 9 vôbec spomínané. Predpokladá hlbokú externú znalosť.

**Návrh opravy:** Presunúť mimo P9.

### P9 · task #17 · `quiz` · Mimo poradia

**Aktuálne:** Rozdiel medzi asociačnými a sekvenčnými pravidlami

**Problém:** Sekvenčné pravidlá v prednáške 9 nie sú vôbec.

**Návrh opravy:** Presunúť do prednášky o sekvenčných vzoroch (P8 sa tomu venuje).

### P9 · task #18 · `fill` · Mimo poradia

**Aktuálne:** Algoritmus pre frekventované sekvencie = PrefixSpan

**Problém:** PrefixSpan v prednáške 9 nie je. Veľmi špecifický pojem bez kontextu.

**Návrh opravy:** Presunúť do prednášky o sekvenčných vzoroch.

### P9 · task #19 · `match` · Mimo poradia

**Aktuálne:** Priraď pojem AR (transakcia/itemset/minsup/minconf) k významu

**Problém:** Žiadny z týchto pojmov nie je v prednáške 9 zavedený.

**Návrh opravy:** Presunúť do prednášky o AR.

### P9 · task #20 · `quiz` · Mimo poradia

**Aktuálne:** Pravidlo pivo→plienky s support 0,1 a confidence 0,8

**Problém:** Príklad sa opiera o pojmy support/confidence, ktoré P9 neuvádza.

**Návrh opravy:** Presunúť spolu s ostatnými AR-úlohami.

### P9 · task #22 · `cat` · Mimo poradia

**Aktuálne:** Roztrieď: analógické (instance-based) vs modelové (eager learners)

**Problém:** Prednáška 9 spomína k-NN/CBR ako 'metódy založené na analógii', ale rozdelenie instance-based vs eager learners (lazy vs eager) nezavádza. Pojmy 'eager learners', 'modelové' nie sú v texte.

**Návrh opravy:** Buď preformulovať bez pojmov instance-based/eager (napr. 'metódy založené na analógii vs ostatné'), alebo doplniť teóriu, alebo presunúť mimo P9.

### P9 · task #26 · `quiz` · Mimo poradia

**Aktuálne:** Ktoré tvrdenie o lifte je správne?

**Problém:** Lift v prednáške 9 nie je. Druhá otázka o lifte (po task 12) duplikuje tému, ktorá tu nepatrí.

**Návrh opravy:** Presunúť mimo P9 alebo doplniť teóriu lift.

### P10 · task #3 · `flash` · Pokazené

**Aktuálne:** Aký je účel Cochranovho Q testu?

**Problém:** Cochranov Q test vôbec nie je spomenutý v prednáške 10 (ani v žiadnej skoršej) — task zavádza pojem bez akéhokoľvek úvodu zo slidov, predpokladá externé znalosti.

**Návrh opravy:** Pridať pred flash krátky intro/context task vysvetľujúci 'neparametrické alternatívy testov' s odkazom, že tieto špecifické testy sú rozšírenie nad rámec slidov. Alebo zmeniť na všeobecnejšiu otázku o neparametrických alternatívach.

### P10 · task #4 · `flash` · Pokazené

**Aktuálne:** Čo meria Kendallov koeficient konkordancie W?

**Problém:** Kendallov W nie je v texte prednášky 10 — len pojem 'neparametrické alternatívy'. Pre študenta učiaceho sa zo slidov neexistuje žiadny zdroj pre tento pojem.

**Návrh opravy:** Buď odstrániť, alebo presunúť do separátnej sekcie 'rozšírenie' s jasným označením, že nejde o učivo prednášky.

### P10 · task #5 · `flash` · Pokazené

**Aktuálne:** Na čo slúži Friedmanov test?

**Problém:** Friedmanov test nie je v texte prednášky 10. Tasks 3-10 zavádzajú konkrétne testy mimo skopu prednášky.

**Návrh opravy:** Odstrániť alebo zhrnúť všetky tri (Cochran/Friedman/Kendall) do jedného súhrnného flash 'príklady neparametrických alternatív' bez detailov.

### P10 · task #7 · `fill` · Nejednoznačná odpoveď

**Aktuálne:** Friedmanov test je neparametrická alternatíva ___ ANOVA (opakovaných meraní).

**Problém:** Veta tvrdí 'parametrickej ANOVA' — ale ANOVA je inherentne parametrická, takže slovo 'parametrickej' je redundantné a študent by skôr napísal 'klasickej' alebo 'opakovaných meraní'. Tieto sú legitímne ale answer matching ich odmietne.

**Návrh opravy:** Preformulovať na: 'Friedmanov test je neparametrická alternatíva ___ meraní ANOVA.' s answer 'opakovaných'. Konkrétne a jednoznačné.

### P10 · task #10 · `cat` · Pokazené

**Aktuálne:** Roztried metódy podľa toho, či sú parametrické alebo neparametrické.

**Problém:** Obsahuje 'Wilcoxonov test' a 'Bartlettov test' ktoré neboli vôbec nikde predtým predstavené v prednáške ani v predchádzajúcich tasks — študent ich nemá ako vedieť.

**Návrh opravy:** Odstrániť Wilcoxon a Bartlett, alebo pridať flash/intro pre ne pred týmto cat. Alternatívne nahradiť ich už zavedenými metódami z prednášky.

### P10 · task #17 · `cat` · Nejasné

**Aktuálne:** Roztried do 5 kategórií aplikácií web log miningu podľa prednášky.

**Problém:** Štruktúra groups je nekonzistentná — niektoré položky sú popisné vety ('Odporúčanie obsahu...'), iné sú zoznamy techník ('Segmentácia + Klasifikácia + Analýza závislostí'), iné chýbajú ('Business intelligence' má len abstraktnú vetu). Niektoré kategórie majú len 1 položku, čo cat task nepotrebuje klasifikovať.

**Návrh opravy:** Buď zmeniť na match (kategória ↔ príklad aplikácie + technika), alebo zjednotiť: každá skupina ≥2 konkrétne príklady aplikácií rovnakého typu.

### P10 · task #19 · `match` · Duplikát

**Aktuálne:** Priraď aplikáciu web log miningu k použitej dolovacej technike.

**Problém:** Obsahovo prekrýva task 17 (cat) — tie isté páry aplikácia→technika sú v oboch taskoch. Študent rieši dvakrát to isté.

**Návrh opravy:** Odstrániť task 17 (cat má slabú štruktúru) a ponechať len match task 19, ktorý je jasnejší. Alebo odstrániť task 19 a opraviť cat.

### P10 · task #25 · `cat` · Duplikát

**Aktuálne:** Roztried výroky o štatistických testoch pre závislé vzorky.

**Problém:** Duplikuje obsah tasks 3-6, 10 — opäť Cochran/Friedman/Kendall fakty. Navyše je úplne na konci, po deployment/summary tasks, čo je out-of-order.

**Návrh opravy:** Buď odstrániť ako duplikát, alebo ak má slúžiť ako záverečný review, presunúť hneď za task 10 a označiť ako 'kontrolný cat'.

---

## Per-prednáška detail

### P1 — Úvod do získavania znalostí 🟢 **GOOD**

**Skóre:** Type-fit 90% · Chronológia GOOD · Learn 7/10 · Quality 8/10

**Summary:** Prednáška 1 (úvod do KD) má 30 taskov s prevažne dobre zvolenými typmi a slušnou pokrytosťou všetkých 5 slidov. Hlavné problémy: (1) task 8 zavádza pojmy ako PageRank, autority/huby, sentiment analýzu, ktoré v prednáške 1 nie sú, čo blokuje samoštúdium; (2) task 18 popisuje fázy KDD detailne, hoci slide 2 ich len menuje — predpoklad externej znalosti; (3) task 12 spomína Apache log, ktorý patrí do prednášky 3; (4) tasks 22 a 23 sú obsahové duplicity s 3 a 4. Chronológia je rozumná, ale pyramída je rozhodená cez 4 nesúsediace pozície (6, 13, 20). Kvalita formulácií je dobrá, distraktory v kvízoch sú zmysluplné. Po opravách 3-4 problémových taskov bude prednáška veľmi učiteľná.

**Findings:**

- 🔴 **task #8** (`cat`, Pokazené)
  - _Roztried výroky podľa toho, ku ktorej vetve Web Miningu patria (PageRank, autority/huby, sentiment...)_
  - Problém: Príklady ako PageRank, autority/huby, PrefixSpan, sentiment analýza a 'extrakcia sedení z access logu' nie sú v prednáške 1 vôbec spomenuté – prednáška len vymenuje 3 vetvy bez príkladov. Učiteľnosť: vyžaduje externé znalosti.
  - Návrh: Nahradiť príklady iba pojmami z lecture 1: 'obsah stránok' / 'HTML' pre Content; 'odkazy medzi stránkami' / 'hyperlinky' pre Structure; 'logy návštev' / 'správanie používateľov' pre Usage. Alebo presunúť tento task neskôr (po prednáške, kde sa PageRank vysvetlí).
- 🟡 **task #12** (`flash`, Mimo poradia)
  - _Vstup pre Web Log Mining: logy webového servera (napr. Apache access log)..._
  - Problém: Apache access log a konkrétny formát sa preberajú až v prednáške 3. Pre prednášku 1 stačí 'logy webového servera' bez konkrétneho mena. Predpoklad externej znalosti.
  - Návrh: Odstrániť konkrétnu zmienku 'Apache access log' a 'kategorizácia návštevníkov' – ponechať len 'logy webového servera (web logs)' a 'správanie používateľov, typické navigačné cesty'.
- 🔴 **task #18** (`match`, Nejasné)
  - _Priraď fázu KDD k tomu, čo sa v nej deje (Predspracovanie = čistenie...)_
  - Problém: Prednáška 1 iba vymenuje názvy 5 fáz, neuvádza ich popis. Detailné popisy (čistenie, doplnenie chýbajúcich hodnôt, odstránenie šumu) sú prevzaté z neskorších prednášok – pri samoštúdiu z prednášky 1 nie sú vysvetliteľné.
  - Návrh: Buď preformulovať popisy na úroveň, ktorá je obsiahnutá v slide 2 (napr. 'Výber dát = identifikácia zdroja', 'Predspracovanie = úprava dát pred analýzou'), alebo presunúť task až za prednášku, kde sa fázy detailne preberajú.
- 🟡 **task #26** (`flash`, Duplikát)
  - _Na koľko základných častí sa rozdeľuje proces objavovania znalostí na základe používania webu..._
  - Problém: Tento flash sa prakticky úplne prekrýva s task 27 (order), ktorý tie isté tri fázy usporiada. Učenec dostane rovnakú informáciu dvakrát za sebou.
  - Návrh: Buď zlúčiť do jedného (ponechať len order, alebo ponechať len flash s popisom čo každá fáza robí), alebo preformulovať flash na 'Vysvetli, čo robí fáza Pattern Discovery vs. Pattern Analysis' – aby šiel hlbšie, nie širšie.
- 🟡 **task #22** (`flash`, Duplikát)
  - _Vymenuj tri základné vetvy objavovania znalostí podľa typu zdroja._
  - Problém: Úplne sa kryje obsahovo s task 3 (match s tými istými 3 vetvami). Task 3 už nielen vymenuje, ale aj priradí k typu dát – tento flash je len menší podmnožinou.
  - Návrh: Odstrániť, alebo preformulovať na otázku 'Prečo sa zaviedli práve tieto tri vetvy a čím sa líšia ich vstupy?'
- 🟡 **task #23** (`flash`, Duplikát)
  - _Vymenuj tri vetvy Web Miningu._
  - Problém: Prekrýva sa s task 4 (match tých istých 3 vetiev). Recall vetiev je už pokrytý v matchi.
  - Návrh: Odstrániť, alebo preformulovať na 'Ktorá z troch vetiev Web Miningu sa zaoberá výlučne dátami zo servera (nie zo strany klienta) a prečo?'
- 🟡 **task #15** (`cat`, Nejasné)
  - _Roztried podľa toho, či ide o vstup alebo výstup procesu objavovania znalostí (asociačné pravidlá, akčné odporúčania...)_
  - Problém: 'Asociačné pravidlá' nie sú v prednáške 1 nikde spomenuté (len 'sekvenčné pravidlá' v pyramíde). Zaradiť ich do výstupu KD vyžaduje predznalosť.
  - Návrh: Nahradiť 'asociačné pravidlá' za 'sekvenčné pravidlá' (čo je v prednáške) alebo za 'znalosti' a 'akčné znalosti' (úrovne pyramídy zo slide 4).
- 🟡 **task #7** (`order`, Mimo poradia)
  - _Usporiadaj pyramídu hodnoty od základne po vrchol._
  - Problém: Task 6 = pyramid order, task 13 = pyramid match, task 20 = pyramid cat – pyramída je rozhodená cez 4 nesúsediace pozície (6, 13, 20). Slide 4 sa preberá raz, učiteľnosť by bola lepšia, keby boli súvisiace tasks pri sebe.
  - Návrh: Presunúť task 13 (match pyramídy s príkladmi) hneď za task 7 (fill akčné), pred prechod na ďalšie témy. Task 20 (cat pyramídy) môže ostať ako neskorší 'check', alebo zlúčiť s task 13.

**Chýba pre učiteľnosť:**

- Krátke vysvetlenie čo robí každá z 5 fáz KDD procesu (slide 2 ich len menuje, task 18 ich ale testuje s detailnými popismi)
- Pred task 8 (cat s PageRank/autority/sentiment): základná definícia týchto pojmov, ktorá v prednáške 1 chýba — alebo presunúť task neskôr
- Vysvetlenie čo je 'Príprava dát' vs 'Objavovanie vzorov' vs 'Analýza vzorov' (rozdiel medzi 3-fázovým WLM procesom a 6-fázovým CRISP-DM)

**Adversarial verify:** ✅ audit_ok=True

Audit prehliadol:
  - task #21 (`unclear`): Quiz na vzťah KDD a Web Miningu má terminologickú nezrovnalosť: správna odpoveď tvrdí 'Web Mining je jednou z troch hlavných vetiev KDD' a vysvetlenie hovorí 'KDD má tri hlavné vetvy: KDD in Databases, KD from Texts, KD from Web' — to je vnútorne rozporné (KDD obsahuje KDD?). Podľa zdrojového textu prednášky 1 sú tieto tri vetvy podoblastami 'objavovania znalostí' (Knowledge Discovery) ako zastrešujúceho pojmu, pričom KDD = Knowledge Discovery in Databases je iba jednou z troch vetiev. Mal by sa nahradiť 'KDD' za 'objavovanie znalostí' / 'Knowledge Discovery'.

---

### P2 — Zdroje dát I — DB, text, web 🟡 **NEEDS_WORK**

**Skóre:** Type-fit 82% · Chronológia MIXED · Learn 6/10 · Quality 7/10

**Summary:** Sekcia P2 má 28 taskov s dobrým pokrytím databáz a vektorovej reprezentácie textu, no trpí dvomi systémovými problémami. Po prvé, posledných cca 8 taskov (indexy 20–27) miesi P2 obsah s P3 znalosťami (stemming, tokenizácia, sitemap.xml, robots.txt štruktúry) — niektoré flash karty samé priznávajú 'detailne v P3'. Pre samostatné učenie z P2 sú tieto tasks blokujúce, lebo predpokladajú znalosti, ktoré učeň ešte nemá. Po druhé, chronológia je porušená: tasks o databázach (21–23) a fill o stemmingu (24) sa objavujú AŽ ZA vektorovou reprezentáciou textu, hoci v slidoch prednášky idú DB → text → web → vektor. Tasks 25 a 26 sú navyše triviálne (jednoslovné položky zo zoznamu rozšírené na flash). Task 11 (cat web sources) extrapoluje P3 podpoložky. Kvalita ostatných taskov (0–19) je dobrá — správne typy, dobré quizy s netriviálnymi distractormi, vzorce sú podporené intuíciou (task 19). Odporúčam: presunúť tasks 21–23 hneď za task 5; tasks 24, 27 do P3; zlúčiť 25+26 do jedného match; obmedziť task 20 na P2 vzorce.

**Findings:**

- 🔴 **task #11** (`cat`, Pokazené)
  - _Roztrieď zdroje dát z webu podľa toho, či ide o obsah, štruktúru alebo používanie_
  - Problém: Lecture 2 listuje pod 'Web' iba Obsah, Mapa, Logovacie súbory — nešpecifikuje 'Sitemap', 'Hyperlinky', 'Záznamy klikov', 'Referrer a User-Agent'. Task vkladá P3 obsah a očakáva ho ako P2 znalosť.
  - Návrh: Zjednodušiť na cat s 3 skupinami a iba 1 reprezentantom za každú (napr. 'Webové stránky','Mapa webu','Logovací súbor') — alebo zmeniť na match: kategória ↔ názov
- 🟡 **task #18** (`quiz`, Nejednoznačná odpoveď)
  - _Aký je intuitívny zmysel TF-IDF váhy pre slovo?_
  - Problém: Pojem 'TF-IDF' nie je v texte prednášky 2 explicitne uvedený (len wf, df, IDF). Otázka predpokladá znalosť skratky/intuitívneho zmyslu odinakiaľ.
  - Návrh: Pred quizom doplniť flash 'Čo je TF-IDF? = súčin TF · IDF...'; alebo preformulovať quiz: 'Akú intuíciu má IDF — log(N/df)?'
- 🔴 **task #20** (`order`, Mimo poradia)
  - _Usporiadaj kroky tvorby vektorovej reprezentácie textu od textu k TF-IDF vektoru_
  - Problém: Tokenizácia a stemming sú obsahom prednášky 3 (preprocessing textu), nie P2. P2 hovorí len o vzorcoch wf/binary/log/IDF. Task predpokladá P3 znalosť.
  - Návrh: Buď zúžiť kroky na P2 obsah: 'wf → binary alebo 1+log(wf) → df → IDF → kombinovaná váha'; alebo task presunúť do P3 a v P2 dať jednoduchší order 'wf → log frekvencia → df → IDF'
- 🟡 **task #21** (`cat`, Mimo poradia)
  - _Roztrieď tvrdenia podľa toho, či popisujú produkčnú databázu alebo dátový sklad_
  - Problém: Tematicky patrí k tasks 1–5 (vlastnosti DB/DW), ale je až za vektorovou reprezentáciou textu. Chronológia slidov: DB → text → web → vektor; tento task by mal nasledovať hneď za task 5.
  - Návrh: Presunúť pred task 6 (fill 'trojvrstvova') — tematicky dokončí porovnanie OLTP vs OLAP
- 🟡 **task #21** (`cat`, Pokazené)
  - _'Normalizovaná schéma', 'Optimalizovaná pre rýchly zápis a update'_
  - Problém: Položky ako 'Normalizovaná schéma' alebo 'Optimalizovaná pre rýchly zápis' v prednáške 2 nie sú spomínané — task predpokladá externú DB znalosť mimo slidov.
  - Návrh: Nahradiť položky tými, ktoré sú v slidoch: 'Subjektovo orientovaný','Integrovaný','Časovo premenný','Nemenný' do DW; 'každodenné transakcie' do OLTP. Ostatné odstrániť.
- 🟡 **task #22** (`match`, Mimo poradia)
  - _Priraď konkrétnu verejnú databázu k jej krátkemu popisu (DATAcube, RegDat, STATdat, Eurostat)_
  - Problém: Tematicky duplicitný s task 8 (cat verejné DB) a task 9 (flash 3 DB). Ide o DB obsah, no je až na pozícii 22 — za vektorovou reprezentáciou textu.
  - Návrh: Presunúť pred task 10 (match textový zdroj) alebo zlúčiť s task 9
- 🟡 **task #23** (`quiz`, Mimo poradia)
  - _Prečo prednáška uvádza príklad „databáza banky + RegDat"..._
  - Problém: Slide 'DATABÁZA BANKY + RegDat' v lecture je medzi DB sekciou a TEXT sekciou. Task je až za vektor textu — mimo chronológie.
  - Návrh: Presunúť hneď za task 8 (cat verejné DB) — tam je prirodzená pointa kombinácie interných a verejných dát
- 🔴 **task #24** (`fill`, Zlý typ úlohy)
  - _Pri stemming-u (kmeňovaní) sa rôzne tvary slova zredukujú na spoločný ____
  - Problém: Stemming nie je obsahom prednášky 2 — je súčasťou P3 (techniky normalizácie). Učeň P2 nemá ako vedieť, čo je stemming.
  - Návrh: Odstrániť task z P2 (presunúť do P3) alebo nahradiť za fill o vzorci wf/IDF — napr. 'IDF = log(N / ___)' → df
- 🟡 **task #25** (`flash`, Triviálne)
  - _Čo je mapa webu ako zdroj dát spomenutý v prednáške 2?_
  - Problém: Karta sama priznáva 'Detailne sa rieši v prednáške 3'. V P2 je 'Mapa webu' iba jednoslovná položka v zozname — k tomu netreba flash.
  - Návrh: Buď zlúčiť mapu+logy do jedného match 'Web → 3 zdroje (obsah, mapa, logy)', alebo odstrániť a presunúť do P3
- 🟡 **task #26** (`flash`, Triviálne)
  - _Čo sú logovacie súbory webu ako zdroj dát podľa prednášky 2?_
  - Problém: Rovnako ako task 25 — karta priznáva detail v P3. Pre P2 ide len o triviálne 'logy = záznamy aktivity'.
  - Návrh: Odstrániť alebo zlúčiť s task 25 do jedného match/cat o 3 typoch webových zdrojov
- 🔴 **task #27** (`quiz`, Zlý typ úlohy)
  - _Prečo je pri výpočte word frequency (wf) potrebné najprv aplikovať stemming?_
  - Problém: Stemming nie je v P2 — patrí do P3. Otázka preto presahuje obsah prednášky 2 a vyžaduje vedomosti z P3.
  - Návrh: Presunúť do P3; nahradiť napr. quizom 'Prečo binary frequency môže byť výhodnejšie než wf?' alebo 'Čo je výhoda log frequency oproti wf?'
- 🟡 **task #9** (`flash`, Duplikát)
  - _Aké tri verejné databázy spomína prednáška ako zdroje dát?_
  - Problém: Tematicky duplikát s task 8 (cat verejných DB) a task 22 (match k popisom). Tri tasks o tých istých štyroch názvoch.
  - Návrh: Zlúčiť task 8+9, ponechať task 22 ako overovacie match
- 🟡 **task #3** (`flash`, Duplikát)
  - _Aké sú 4 charakteristické vlastnosti dátového skladu?_
  - Problém: Tesne za task 1 (match s identickými 4 vlastnosťami) a task 2 (quiz na 4 vlastnosti). Tri tasks v rade testujú tú istú znalosť.
  - Návrh: Odstrániť task 3 alebo nahradiť za order/flash s príkladom (napr. 'Dajte príklad subjektovo orientovaného')

**Chýba pre učiteľnosť:**

- Definícia stemming-u a kmenového slova — task 24 a 27 ho používajú, ale prednáška 2 ho nezavádza
- Tokenizácia ako predspracovanie — task 20 (order) ho používa ako krok, no v P2 sa nezavádza
- Skratka a definícia TF-IDF — task 18 a názov task 20 pracuje s 'TF-IDF', no v slidoch P2 je len IDF a wf/log frequency
- Intuícia 1+log(wf) — task 19 ju vysvetľuje sám, no flash by mal byť po prezentácii vzorca v task 14
- Význam toho, prečo sa robí inverse document frequency (motivácia) — IDF formula je v task 15/16/17, no nikde nie je flash 'IDF penalizuje slová časté v celej kolekcii — preto inverse'

**Adversarial verify:** ✅ audit_ok=True

Audit false positives (problém v skutočnosti nie je):
  - task #21: Druhý finding pre task 21 ('Normalizovaná schéma', 'Optimalizovaná pre rýchly zápis') je príliš striktný. Sú to bežné OLTP/DW charakteristiky implicitne pokryté slidom 'Produkčné databázy' vs DW so 4 vlastnosťami. Učeň, ktorý porozumel slidom (DW = subjektovo orientovaný, integrovaný, časovo premenný, nemenný, OLAP), vie ľahko odvodiť že OLTP/produkčná DB je opak - aktuálne dáta, optimalizovaná pre transakcie. Tieto distractory sú legitímne rozšírenie, nie 'broken' content. Audit sám priznáva minor severity.

Audit prehliadol:
  - task #7 (`out-of-scope-content`): Order task 'Usporiadaj typické vrstvy trojvrstvovej architektúry' vyžaduje znalosť 5 konkrétnych vrstiev (Zdrojové DB, ETL, Dátový sklad, OLAP server, Klient/prezentačná). Prednáška 2 však uvádza len titul slidu 'TROJVRSTVOVÁ ARCHITEKTÚRA DÁTOVÉHO SKLADU' bez detailov o vrstvách. ETL ani OLAP server nie sú v texte zavedené ako pojmy. Task predpokladá externú znalosť architektúry DW. Severity: minor (lebo slide v originále má pravdepodobne diagram, ktorý sa nevypäl do textu).
  - task #15 (`minor-typo`): V match pre IDF: 'log(N / df), penalizuje slová častô v celej kolekcii' - preklep 'častô' namiesto 'často'. Nie je obsahový problém, len kvalitatívny.

---

### P3 — Zdroje dát II — reprezentácia textu, log súbory 🟡 **NEEDS_WORK**

**Skóre:** Type-fit 78% · Chronológia MIXED · Learn 5/10 · Quality 7/10

**Summary:** P3 obsahuje 32 taskov, ale prednáška 3 má iba 8 slidov: titulná, transakčný/sekvenčný model (anotovaná tabuľka), substantíva 5-pozičné kódovanie, príklad Apache logu, 3 diagramy pripojení (priame/proxy/load balancer), mapa webu (strom + tabuľka). Veľká časť taskov (cca 12) je out-of-order: testujú témy z P5/P6 (Apache log cleaning pipeline, robots.txt identifikácia, anonymizácia IP, path completion, identifikácia užívateľov cez IP+UA, TF-IDF, stemming/lematizácia, parsovanie regex vs pandas). Mnohé tasks sú duplikáty s P5 a P6. Pozitívne: tasks na pozície substantív, rod, paradigma sa zhodujú s lecture tabuľkou. Task 29 (match stĺpcov) obsahuje stĺpec 'POS', ktorý v lecture tabuľke nie je - learner si zapamätá nesprávne. Chronologicky: TF-IDF testované bez definície, doplnenie ciest spomenuté pred jeho zavedením v P5/P6. Question quality je solídna (jasné formulácie, dobré distractory), no learnability trpí kvôli množstvu predpokladov externých znalostí.

**Findings:**

- 🔴 **task #2** (`match`, Mimo poradia)
  - _Priraď techniku normalizácie slov (Stemming/Lematizácia/POS/Tokenizácia)_
  - Problém: Stemming a lematizácia ako techniky nie sú v slidoch P3 vysvetlené - prednáška ukazuje len výslednú anotovanú tabuľku. Predpokladá externé znalosti.
  - Návrh: Pridať flash s definíciami techník PRED tento match, alebo presunúť do prednášky o text preprocessing
- 🔴 **task #5** (`fill`, Mimo poradia)
  - _Apache ___ Log Format (Combined)_
  - Problém: P3 nezavádza termín 'Apache Combined Log Format' - slide ukáže príklad logu, ale neoznačuje formát. Patrí do P5/P6.
  - Návrh: Presunúť do P5/P6 alebo pridať intro flash 'Apache Combined Log Format' do P3
- 🔴 **task #6** (`order`, Mimo poradia)
  - _Usporiadaj polia Apache Combined Log riadku_
  - Problém: Vyžaduje presnú znalosť štruktúry formátu, ktorú P3 nezavedie konceptuálne - len ukáže príklad bez popisu polí.
  - Návrh: Pridať flash so štruktúrou polí Combined Log Format PRED order; alebo presunúť do P5/P6
- 🔴 **task #7** (`match`, Mimo poradia)
  - _Priraď pole Apache Combined Log (IP/Method/Status/Bytes/User-Agent)_
  - Problém: Polia Apache log nie sú v P3 vysvetlené ako koncepty - duplikuje obsah P5/P6.
  - Návrh: Presunúť do P5/P6 kde je téma logu rozpracovaná
- 🔴 **task #9** (`cat`, Mimo poradia)
  - _Roztried HTTP metódy: navigácia vs technické (filtrujú sa)_
  - Problém: Filtrovanie HTTP metód pre WUM nie je v P3. Duplikuje P6 task 3.
  - Návrh: Odstrániť z P3 (duplikuje P6)
- 🟡 **task #11** (`quiz`, Triviálne)
  - _Prečo je proxy server problém pre identifikáciu užívateľa_
  - Problém: 3 zo 4 distraktorov sú zjavne nezmysly (proxy maže UA, mení timestamp, nezapisuje GET) - quiz je triviálny.
  - Návrh: Pridať plauzibilnejšie distraktory; alebo preformulovať na flash
- 🔴 **task #13** (`flash`, Mimo poradia)
  - _Mapa webu - externá vs vybudovaná z logu, doplnenie chýbajúcich stránok_
  - Problém: P3 slide 'Mapa webu' ukazuje strom + tabuľku URL/koreň/odkazujúca stránka. Flash však zachádza do path completion (Pattern Discovery) z P5/P6.
  - Návrh: Preformulovať flash na obsah slide (strom + tabuľka URL/koreň/odkazujúca), path completion presunúť do P5
- 🔴 **task #14** (`fill`, Duplikát)
  - _robots___.txt v koreni domény_
  - Problém: robots.txt nie je v P3 slidoch. Duplikuje sa s P5 task 14 a P6 task 9.
  - Návrh: Odstrániť z P3
- 🔴 **task #15** (`quiz`, Duplikát)
  - _Prečo robots.txt indikuje robota_
  - Problém: Téma nie je v P3. Duplikuje quiz v P5 (task 9) a P6 (task 9).
  - Návrh: Odstrániť z P3
- 🔴 **task #16** (`order`, Mimo poradia)
  - _Kroky čistenia Apache logu pre WUM_
  - Problém: Celý WUM preprocessing pipeline - patrí do P6 (kde je takmer identický). P3 to nepokrýva.
  - Návrh: Odstrániť z P3 (duplikuje P6 task 1)
- 🔴 **task #17** (`cat`, Mimo poradia)
  - _Roztried záznamy: šum vs užitočná navigácia_
  - Problém: WUM cleaning - patrí do P5/P6. Duplikuje sa s P5 task 14 a P6 task 6.
  - Návrh: Odstrániť z P3
- 🔴 **task #18** (`flash`, Mimo poradia)
  - _Techniky anonymizácie IP (hash, mask, pseudo, k-anonymita)_
  - Problém: Anonymizácia nie je v P3 vôbec. K-anonymita je pokročilý koncept bez intro a nepatrí do P3.
  - Návrh: Odstrániť alebo presunúť do prednášky o GDPR/etike
- 🟡 **task #19** (`quiz`, Mimo poradia)
  - _Prečo NEMÔŽEME odstrániť IP pred WUM_
  - Problém: Identifikácia užívateľa cez IP je téma P5/P6, nie P3. P3 obsahuje len diagramy pripojení.
  - Návrh: Presunúť do P5
- 🔴 **task #20** (`match`, Mimo poradia)
  - _Spôsob identifikácie užívateľa k presnosti (IP/IP+UA/Cookies/Login)_
  - Problém: Identifikácia užívateľa je explicitne v P5 (task 21). P3 to nepokrýva ako koncept.
  - Návrh: Presunúť do P5 alebo odstrániť (duplikuje P5)
- 🔴 **task #21** (`fill`, Mimo poradia)
  - _TF-IDF penalizuje slová v ___ dokumentoch_
  - Problém: TF-IDF, TF, DF, IDF NIE SÚ v slidoch P3 - prednáška spomína iba 'transakčný/sekvenčný model'. Bez definície TF-IDF sa fill nedá pochopiť.
  - Návrh: Pridať flash s definíciou TF-IDF PRED tento fill; alebo odstrániť
- 🔴 **task #22** (`quiz`, Mimo poradia)
  - _Prečo regex namiesto pd.read_csv pri parsovaní Apache log_
  - Problém: Implementačný detail (Python/pandas) - nie je v teoretickej prednáške 3. Patrí do cvičenia.
  - Návrh: Odstrániť z P3 - patrí do cv2 materiálov
- 🔴 **task #24** (`flash`, Duplikát)
  - _Pasívnosť Apache logu - obmedzenie pre WUM_
  - Problém: Téma pasívnosti logu nie je v P3. Duplikuje sa s P6 task 22.
  - Návrh: Odstrániť z P3
- 🔴 **task #25** (`order`, Mimo poradia)
  - _Fázy spracovania textu (tokenizácia → vektor)_
  - Problém: Pipeline text mining nie je v slidoch P3 - lecture ukazuje len výstup (anotovaná tabuľka), nie fázy. Stop-words, vektorizácia nie sú v P3.
  - Návrh: Pridať flash 'Pipeline spracovania textu' PRED order, alebo presunúť
- 🟡 **task #28** (`order`, Nejednoznačná odpoveď)
  - _Usporiadaj prvých 6 pádov slovenčiny_
  - Problém: Slovenčina má 7 pádov; výber práve 6 (vynechanie inštrumentálu) je arbitrárny. Lecture tabuľka ukazuje všetkých 7.
  - Návrh: Rozšíriť na 7 pádov podľa lecture tabuľky, alebo zdôvodniť výber 6
- 🔴 **task #29** (`match`, Pokazené)
  - _Priraď stĺpec tabuľky (Word/Lemma/Tag/POS/Order)_
  - Problém: Lecture tabuľka má stĺpce: ID, Word, Tag, Lemma, Order, Tag_type, Post-Edit, MT@EC. Stĺpec 'POS' v tabuľke prednášky NIE JE. Používateľ sa učí nesprávne.
  - Návrh: Nahradiť 'POS' za 'Tag_type' alebo 'Post-Edit' podľa skutočnej tabuľky lecture
- 🟡 **task #4** (`quiz`, Mimo poradia)
  - _Prečo sa používajú LEN SUBSTANTÍVA pri reprezentácii textu_
  - Problém: P3 má slide 'Substantíva' s tabuľkou pozícií, ale NEVYSVETĽUJE prečo práve substantíva (obsahové slová). Predpoklad externej znalosti.
  - Návrh: Pridať flash 'Substantíva nesú obsah textu' PRED tento quiz

**Chýba pre učiteľnosť:**

- Definícia bag-of-words / transakčného a sekvenčného modelu pred match/quiz/cat (task 0, 1, 23)
- Intro k stemmingu, lematizácii, tokenizácii ako technikám pred match task 2
- Štruktúra Apache Combined Log Format (zoznam polí v poradí) pred task 5-7, 10
- Definícia TF-IDF (TF, DF, IDF zložky) pred fill task 21
- Pipeline spracovania textu (tokenizácia → stop-words → POS → lema → substantíva → vektor) pred order task 25
- Prečo substantíva nesú obsah (vs slovesá/stop-words) pred quiz task 4
- Explicit zoznam 7 pádov slovenčiny pred order task 28
- Definícia robots.txt (ak má byť v P3) - inak presunúť do P5/P6

**Adversarial verify:** ✅ audit_ok=True

Audit prehliadol:
  - task #0 (`out-of-order`): Match task 0 obsahuje dvojice 'Vektorová reprezentácia' (TF, TF-IDF, binary) a 'n-gram model', pričom P3 slide 'REPREZENTÁCIA TEXTU: TRANSAKČNÝ/SEKVENČNÝ MODEL' zavádza len transakčný a sekvenčný model. TF-IDF a n-gramy nie sú v P3 slidoch, učenec sa s nimi stretne až neskôr (P5/P6 alebo iné). Konzistentné so zvyškom auditu, ktorý flagol task 21 (TF-IDF fill) — ten istý problém je už v task 0.
  - task #3 (`out-of-order`): Flash 'Čo je tokenizácia a prečo je netriviálna pre slovenčinu' uvádza konkrétne príklady (skratky, spojovníky, desatinné čiarky, dátumy) ktoré v P3 slidoch NIE SÚ — slide 'SUBSTANTÍVA' len odkazuje na Garabík paper bez vysvetlenia. Učenec musí externý paper čítať. Konzistentné s findingom o task 2 (stemming/lematizácia).
  - task #26 (`out-of-order`): Flash o 5-pozičnom kódovaní tagu substantíva (S, paradigma, rod, číslo, pád) je hutný technický obsah, ktorý P3 slide 'SUBSTANTÍVA' explicitne neuvádza — len ukazuje tabuľku zo zdrojového papera. Bez tohto flashu sa nedajú zodpovedať tasks 27, 30, 31. Audit nezaznačil že tieto detaily nie sú v P3 slide texte (sú len v externom referencovanom paperi). Minor — borderline ak pripustíme že linkovaný paper = súčasť materiálu.

---

### P4 — Proces objavovania znalostí — metodiky (CRISP-DM intro) 🟢 **GOOD**

**Skóre:** Type-fit 78% · Chronológia GOOD · Learn 7/10 · Quality 7/10

**Summary:** Prednáška 4 obsahuje 27 taskov pokrývajúcich 4 metodiky procesu KD (CRISP-DM, 5A, SEMMA, DMAIC), WUM proces, VP vs. KD a spoločné prvky. Chronológia je dobrá — pre každú metodiku sa najprv predstaví (flash), potom usporiada (order) a priradí (match). Hlavné problémy: (1) tri tasks (3, 23) sa opierajú o 60-80 % údaj, ktorý prednáška 4 nemá explicitne; (2) task 16 (cat) má nesymetrické skupiny (1 vs. 2 položky) a vynecháva 3 fázy CRISP-DM; (3) task 22 (match KD oblastí) predpokladá definície WCM a WSM, ktoré v prednáške nie sú; (4) task 25 (flash) má vnútorný rozpor — pýta analytické jadro vrátane Data Preparation, ale sama odpoveď hovorí, že DP je časovo a nie analyticky náročná; (5) tasks 13, 17, 24 majú slabé distractors (zjavne nezmyselné možnosti). Kvalita pokrytia látky je dobrá, ale niektoré tasks treba precízne formulovať a vyhnúť sa externým znalostiam.

**Findings:**

- 🟡 **task #3** (`quiz`, Pokazené)
  - _Akú % času zaberá Data Preparation v CRISP-DM (60-80 %)_
  - Problém: Prednáška 4 text uvádza len 'Časovo náročné' bez konkrétneho percenta — 60-80 % je externá znalosť, ktorá v prednáške 4 nie je explicitne uvedená.
  - Návrh: Buď preformulovať na 'Ktorá fáza CRISP-DM je označená ako časovo náročná?' (jednoznačne v slide) alebo presunúť do P6 kde sa 60-80 % spomína.
- 🟡 **task #13** (`quiz`, Triviálne)
  - _Ktorá metodika pochádza z riadenia kvality? CRISP-DM/SEMMA/Six Sigma/5A_
  - Problém: Tri zo štyroch možností sú zjavne DM metodiky, Six Sigma je z kvality — výber je triviálny aj bez učenia (najmä keď názov Six Sigma je všeobecne známy z manažmentu).
  - Návrh: Lepšie ako flash 'Ktorá metodika z prednášky 4 pochádza z riadenia kvality?' alebo posilniť distractors (napr. pridať WUM, KDD, DMAIC ako možnosti).
- 🔴 **task #16** (`cat`, Pokazené)
  - _Roztrieď fázy CRISP-DM časovo vs. analyticky náročné — len DP / Modeling+Evaluation_
  - Problém: Cat má len 3 položky (1+2), zvyšné 3 fázy CRISP-DM (BU, DU, Deployment) chýbajú. Skupina 'Casovo narocne' s jednou položkou je tiež nešťastná — kategorizácia s 1 itemom je málo zmysluplná.
  - Návrh: Premeniť na quiz 'Ktorá fáza CRISP-DM je v prednáške označená ako časovo náročná?' s odpoveďou Data Preparation, alebo pridať tretiu skupinu 'Ostatné fázy' s BU, DU, Deployment.
- 🟡 **task #17** (`quiz`, Triviálne)
  - _Hranice medzi oblasťami KD sú... prelínajúce/ostré/neexistujúce/formálne_
  - Problém: Možnosti 'neexistujúce — všetko je to to isté' a 'len formálne, prakticky nepodstatné' sú zjavné absurdity. Distractors testujú schopnosť eliminovať nezmysly, nie pochopenie.
  - Návrh: Zmeniť na flash 'Ako sú v prednáške znázornené hranice medzi oblasťami KD?' s odpoveďou 'fuzzy / prelínajúce sa, zapisuje sa <>'.
- 🔴 **task #22** (`match`, Nejasné)
  - _Priraď oblasť KD k jej vstupu (WUM, WCM, WSM, TM, KDD)_
  - Problém: Prednáška 4 uvádza WCM, WSM len ako skratky bez ich definície. Bez externej znalosti (P6) sa študent nedokáže naučiť, že WCM = obsah a WSM = štruktúra. Learnability gap.
  - Návrh: Buď pridať pred tento match flash karty definujúce WCM a WSM (čo znamenajú skratky), alebo zredukovať match len na WUM + TM + KDD, ktoré sú lepšie pokryté v prednáške 4.
- 🔴 **task #23** (`fill`, Pokazené)
  - _Fáza ___ ___ je časovo najnáročnejšia, 60-80 %_
  - Problém: Dva blanky ('___ ___') s viacslovnou odpoveďou 'data preparation' — fill matching s viacslovnou frázou je nespoľahlivé (medzery, diakritika, EN/SK). Navyše 60-80 % nie je explicitne v prednáške 4.
  - Návrh: Zmeniť na quiz s 4 možnosťami (Data Preparation/Modeling/BU/DU) alebo na flash. Vyhnúť sa fill s viacslovnou anglickou frázou.
- 🟡 **task #24** (`quiz`, Triviálne)
  - _Ktorá metodika NEPATRÍ medzi spomenuté? KDD-Waterfall_
  - Problém: Distractor 'KDD-Waterfall' je vymyslený a študent ho vyfiltruje aj bez pochopenia — recall typu 'čo nie je v texte' s vymysleným menom je trivialný gotcha trik.
  - Návrh: Buď nahradiť skutočnými konkurenčnými metodikami (napr. KDD process model od Fayyada, ASUM-DM) alebo zmeniť na flash 'Vymenuj 4 metodiky procesu KD z prednášky 4'.
- 🔴 **task #25** (`flash`, Nejednoznačná odpoveď)
  - _Ktoré 3 fázy CRISP-DM tvoria analytické jadro?_
  - Problém: Otázka pýta 'analytické jadro', odpoveď zahŕňa Data Preparation, ale samotná odpoveď vzápätí hovorí 'Data Preparation je časovo náročná, Modeling a Evaluation sú analyticky náročné' — vnútorná protirečivosť. Analytické jadro by malo byť Modeling+Evaluation.
  - Návrh: Zmeniť otázku na 'Ktoré dve fázy CRISP-DM sú analyticky najnáročnejšie?' s odpoveďou 'Modeling, Evaluation', alebo preformulovať na 'Ktoré tri fázy CRISP-DM tvoria jadro procesu po porozumení dátam?'
- 🔴 **task #26** (`order`, Nejednoznačná odpoveď)
  - _Usporiadaj: Validné dáta → Proces → Analytické metódy → Znalosti_
  - Problém: Prednáška uvádza 'Validné dáta, Proces, Analytické metódy' ako spoločný menovateľ VP aj KD (zoznam = atribúty), NIE ako sekvenčný tok. 'Znalosti' do tohto zoznamu prednáška nepridáva — je to interpretačná konštrukcia. Kanonické poradie nie je v prednáške definované.
  - Návrh: Premeniť na cat alebo flash 'Aký je spoločný menovateľ VP a KD? Validné dáta, Proces, Analytické metódy' (duplikát task 21, takže možno radšej odstrániť alebo nahradiť iným poradím — napr. usporiadaj 6 fáz CRISP-DM s WUM-mapovaním).

**Chýba pre učiteľnosť:**

- Definícia/význam skratiek WCM (Web Content Mining) a WSM (Web Structure Mining) — používané v match task 22, ale nikde v prednáške 4 ani na učenie HTML nie sú vysvetlené pred touto úlohou
- Explicitné zaradenie 60-80 % času pre Data Preparation (používané v task 3 a 23) — v slide texte prednášky 4 je len 'Časovo náročné' bez percentuálneho údaju
- Význam zápisu <> medzi oblasťami KD (task 17) — symbol je v texte, ale jeho interpretácia ako 'prelínanie/fuzzy hranice' chýba ako úvodný koncept

**Adversarial verify:** ✅ audit_ok=True

Audit false positives (problém v skutočnosti nie je):
  - task #16: Audit claims BU, DU, Deployment 'chýbajú' v cat — ale prednáška 4 (riadok 38-40) sama explicitne zobrazuje LEN tri fázy (Data Preparation, Modeling, Evaluation) v kontexte časovo/analyticky náročné, s '..' na oboch stranách. Task verne reflektuje slide. Asymetrické skupiny 1 vs. 2 sú slabší dizajn, ale nie 'major broken' — severity je nadhodnotená. Issue je skôr minor (kategorizácia s 1 itemom je suboptimálna), nie major broken.

Audit prehliadol:
  - task #2 (`learnability`): Match CRISP-DM fáza → činnosť (BU=definícia cieľov, DU=zber/prieskum, DP=čistenie). Tieto popisy NIE SÚ v prednáške 4 — slide uvádza len 6 názvov fáz. Študent sa to musí naučiť z externej znalosti, nie zo slide. Minor learnability gap pre prvý match v poradí — bez kontextu v slide. Podobne task 3 (druhá polovica match).
  - task #6 (`learnability`): Match 5A → význam (Assess=posúdenie problému, Access=získanie prístupu k dátam, ...). Prednáška 4 (riadok 13-18) uvádza len anglické slová bez ich interpretácie/popisu. Slovenské popisy sú interpretačné. Minor learnability gap.
  - task #9 (`learnability`): Match SEMMA → popis (Sample=výber reprezentatívnej vzorky, Explore=prieskum dát atď.). Prednáška 4 uvádza len 5 anglických slov; popisy v match sú externé štandardné definície. Minor learnability gap.
  - task #12 (`learnability`): Match DMAIC → účel. Prednáška uvádza len 5 anglických slov Define/Measure/Analyze/Improve/Control bez ich vysvetlenia. Popisy sú externá štandardná znalosť, nie zo slide. Minor learnability gap.

---

### P5 — CRISP-DM I — Porozumenie problematike a dátam 🟢 **GOOD**

**Skóre:** Type-fit 88% · Chronológia GOOD · Learn 7/10 · Quality 7/10

**Summary:** P5 má 30 taskov pokrývajúcich tri témy slidov (CRISP-DM fázy, typy DM úloh, príprava log dát) s rozumnou variabilitou typov (8 quiz, 6 match, 5 flash, 5 fill, 4 order/cat). Chronológia v zásade sleduje slide-flow (problematika → dáta → príprava → roboti → sessions → path completion). Hlavné slabiny: niekoľko duplicitných dvojíc (task 6/7 fill, task 12/13 order, task 24/2 match, task 28/29 flash+quiz, task 25/26 flash+quiz), niektoré trivialne quizy s nezmyselnými distraktormi (task 21), a zavlečené externé fakty (STT = 30 min v task 22, '(mimo P5)' fázy v task 0). Žiadny task nie je broken alebo má nesprávny typ — všetky issues sú minor.

**Findings:**

- 🟡 **task #0** (`order`, Nejasné)
  - _Usporiadaj fázy CRISP-DM... vrátane položiek označených '(mimo P5)'_
  - Problém: Items 'Modelovanie (mimo P5)', 'Vyhodnotenie (mimo P5)', 'Nasadenie (mimo P5)' nie sú v prednáške 5 — prednáška spomína iba prvé tri fázy. Zaradenie 'mimo P5' do orderu núti študenta poznať externe celý CRISP-DM, čo P5 priamo neučí.
  - Návrh: Obmedziť items na 3 fázy z P5 (Porozumenie problematike, Porozumenie dátam, Príprava dát) alebo doplniť do learning material úvod, ktorý všetkých 6 fáz CRISP-DM vysvetľuje.
- 🟡 **task #6** (`fill`, Triviálne)
  - _Web/proxy servery ukladajú dáta v spoločnej ___ štruktúre v textovom formáte._
  - Problém: Doslovná rekonštrukcia vety zo slidu, jedno adjektívum. Testuje len pamäť konkrétneho slova bez konceptuálneho významu.
  - Návrh: Zlúčiť s task 5 (match) alebo nahradiť konceptuálnejším quizom o rozdiele medzi IS a web/proxy zdrojom dát.
- 🟡 **task #7** (`fill`, Duplikát)
  - _Informačné systémy obsahujú dáta vo vlastnej štruktúre, organizované v ___._
  - Problém: Skoro identický fill ako task 6, len druhá veta z toho istého slidu. Spolu s task 6 testujú výhradne mechanickú reprodukciu slidu.
  - Návrh: Odstrániť jeden z dvojice fillov (6 alebo 7) alebo nahradiť konceptuálnym quizom (porovnaj IS vs Web log dáta).
- 🟡 **task #13** (`order`, Duplikát)
  - _Usporiadaj transformácie log súboru (Hrubé dáta → Bez robotov → ...)_
  - Problém: Veľmi blízky duplikát task 12 (order krokov prípravy dát). Obe testujú v podstate to isté chronologické poradie filtrácie logu, len v inom slovníku ('kroky' vs 'transformácie').
  - Návrh: Ponechať len jeden z dvoch order taskov; druhý prerobiť napr. na match (krok → výstup transformácie) alebo cat.
- 🟡 **task #17** (`match`, Triviálne)
  - _Priraď IP adresu robota k hostname (msnbot-65-55..., crawl.yahoo, spider27.yandex...)_
  - Problém: Hostname obsahuje doslovne IP alebo názov vyhľadávača (msnbot-65-55-110-205 obsahuje 65.55.110.205; yandex obsahuje yandex). Priradenie sa dá vyriešiť bez akéhokoľvek konceptuálneho pochopenia, len stringovým rozpoznávaním.
  - Návrh: Buď zmeniť na flash s explikáciou 'ako z hostname spoznáme crawler', alebo nahradiť quizom o tom, prečo reverse-DNS na hostname je silnejší signál než User-Agent.
- 🟡 **task #21** (`quiz`, Triviálne)
  - _Identifikácia používateľov v prednáške 5 je založená na: ... Telefónnom čísle / Iba na cookies / Iba na IP / User-Agent_
  - Problém: Distraktory sú zjavné nezmysly (telefónne číslo, iba cookies pri Apache logu). Quiz tu netestuje pochopenie — 3 zo 4 možností sú zjavne mimo.
  - Návrh: Prerobiť na flash, alebo nahradiť kvalitnejším quizom porovnávajúcim IP-only vs IP+User-Agent vs cookies podľa presnosti.
- 🟡 **task #22** (`flash`, Nejednoznačná odpoveď)
  - _DVA spôsoby identifikácie sedení... STT 30 min, štruktúra (Referrer)_
  - Problém: Odpoveď uvádza 'STT 30 min ako štandard', ale prednáška 5 (skuska/_txt/prednaska_5.txt) konkrétnu hodnotu 30 min nespomína — slide píše len 'na základe casu/strukt.'. Zavádza externý fakt ako súčasť P5 obsahu.
  - Návrh: Odstrániť tvrdenie '30 min štandard' z odpovede, alebo presunúť tento detail do P6/P7 kde sa STT objavuje explicitne.
- 🟡 **task #24** (`match`, Duplikát)
  - _Priraď úlohu data miningu k typickému príkladu vo web log miningu_
  - Problém: Obsahovo prekrýva task 2 (match: úloha → popis). Task 2 už mapuje úlohu na definíciu; task 24 mapuje tú istú úlohu na konkrétny príklad, ale princíp testovania je identický (poznanie 6 typov úloh).
  - Návrh: Ponechať tento task (príklady sú pedagogicky cennejšie ako definície), ale odstrániť task 2 — alebo redukovať task 2 na 3 položky a zachovať task 24 ako rozšírenie.
- 🟡 **task #28** (`flash`, Duplikát)
  - _Čo robí krok 'Doplnenie ciest' a prečo je potrebný? (cache, Späť/Vpred)_
  - Problém: Task 29 (quiz hneď za ním) testuje úplne ten istý obsah a uvádza tie isté dôvody (cache, Späť/Vpred). Dvojica flash + quiz tesne vedľa seba s identickým obsahom.
  - Návrh: Ponechať len jeden z dvojice (preferenčne flash 28, lebo má bohatšiu explikáciu), alebo prerobiť quiz 29 na otázku skúmajúcu mechanizmus path completion (mapa webu, Referrer → URL).
- 🟡 **task #25** (`flash`, Duplikát)
  - _Čo je úloha Deskripcia konceptov v DM (P5)?_
  - Problém: Hneď nasledujúci task 26 (quiz) testuje 'aký je hlavný rozdiel medzi Klasifikáciou a Deskripciou konceptov' — obsah sa silne prekrýva s touto flash kartou (porovnanie K vs DK).
  - Návrh: Ponechať flash a zmeniť quiz na otázku skúmajúcu konkrétny príklad/metódu deskripcie konceptov (napr. rozhodovacie pravidlá vs klasifikačný strom), alebo flash zovšeobecniť a quiz odstrániť.

**Chýba pre učiteľnosť:**

- Vysvetlenie pojmu STT (Session Timeout Threshold) — task 22 ho používa, ale P5 text ho explicitne nedefinuje; ak má byť STT v učení P5, treba úvodný flash/quiz so štandardnou hodnotou.
- Stručný úvod k zvyšným fázam CRISP-DM (Modelovanie, Vyhodnotenie, Nasadenie) — task 0 ich žiada usporiadať, hoci P5 ich obsahovo neprejednáva.
- Stručný príklad rozkladu Apache combined log riadku (každé pole anotované) — task 15 (flash) iba vymenúva polia, ale chýba interaktívny prepojený materiál, na ktorom si študent overí kde je IP, kde Referrer atď. (predpoklad pre task 16 a 17).

**Adversarial verify:** ✅ audit_ok=True

Audit prehliadol:
  - task #5 (`scope-creep`): Match 'zdroj dát k charakteristike' obsahuje 4 páry, ale prednáška 5 v sekcii 'Porozumenie dátam' explicitne menuje iba 2 zdroje: Informačné systémy a Web/proxy servery. Páry 'Apache log → textový riadkový záznam' a 'Databázové tabuľky → štruktúrované dáta s definovanými stĺpcami' sú obohatenie mimo doslovného obsahu P5. Minor — nezavádza nesprávne info, ale rozširuje slovník, ktorý slide nedáva.
  - task #23 (`duplicate-cluster`): Spolu s task 28 (flash) a task 29 (quiz) je task 23 (fill 'doplnenie ___ ciest') tretí task v rade o tej istej téme path completion. Audit zachytil len dvojicu 28/29, ale 23 tvorí trio. Minor — fill 23 testuje názov, zvyšné dva mechanizmus, takže prekryv nie je úplný.

---

### P6 — CRISP-DM II — Príprava dát (čistenie, roboti) 🟢 **GOOD**

**Skóre:** Type-fit 90% · Chronológia MIXED · Learn 7/10 · Quality 8/10

**Summary:** Tasky pokrývajú prednášku 6 komplexne, typy úloh sú prevažne vhodne zvolené (90% fit). Hlavný problém je CHRONOLÓGIA: úvodné koncepty (3 oblasti web miningu, 3 fázy WUM) sú zaradené až ako tasky 17-19, po 17 detailných úlohách o čistení a robotech — to bráni hierarchickému pochopeniu. Tiež task 24 (fill so symbolom porovnania) prezrádza správnu odpoveď v hinte a tasky 23-24 sú redundantné. Vzorce a definície sú dobre rozdelené medzi flash/quiz/fill; match a cat úlohy sú vhodne navrhnuté. Po preusporiadaní úvodných taskov 17-19 a oprave task 24 by bola učiteľnosť výrazne lepšia.

**Findings:**

- 🔴 **task #17** (`match`, Mimo poradia)
  - _Priraď oblasti web miningu k ich vstupom (Content/Structure/Usage)_
  - Problém: Toto je úvodný koncept (Web Mining oblasti) ktorý sa logicky zaraduje na začiatok celej prednášky 6 — patrí pred všetky tasky o čistení logu a robotech, nie až ako 18. task po detailoch.
  - Návrh: Presunúť pred task 0 (úvodný flash o 60-80%) ako úvodný kontext WUM.
- 🔴 **task #18** (`order`, Mimo poradia)
  - _Usporiadaj 3 fázy procesu Web Usage Miningu (Data prep, Pattern discovery, Pattern analysis)_
  - Problém: Toto je úplný top-level overview procesu WUM — prednáška ho zavádza ako prvé (lines 7-8). Tu sa však objavuje až po 17 detailných úlohách o čistení a sedeniach, čo bráni hierarchickému pochopeniu.
  - Návrh: Presunúť hneď za task 0 alebo task 17 — pred ostatné detailné úlohy o data prep.
- 🔴 **task #19** (`cat`, Mimo poradia)
  - _Roztriedi aktivity podľa fázy WUM (príprava / objavovanie vzorov / analýza vzorov)_
  - Problém: Závisí od chápania troch fáz WUM (task 18). Mal by nasledovať hneď po úvodných úlohách o WUM oblastiach a fázach, nie až po polovici prednášky.
  - Návrh: Presunúť ihneď za task 18 (3 fázy WUM) — vytvoriť úvodný blok 17→18→19.
- 🟡 **task #23** (`flash`, Duplikát)
  - _Formálna definícia sedenia: t_i − t_{i−1} ≤ τ ... > τ začína nové sedenie_
  - Problém: Task 24 (fill) okamžite testuje rovnakú definíciu (vlož symbol ≤ do nerovnosti t_i − t_{i−1} ___ τ). Flash dáva odpoveď a fill ju potom testuje na rovnakej veci — redundantné.
  - Návrh: Buď zlúčiť flash+fill, alebo odstrániť fill (24) keďže flash 23 už obsahuje celú definíciu vrátane symbolu.
- 🟡 **task #12** (`order`, Nejednoznačná odpoveď)
  - _Usporiadaj 4 filtračné kroky odstránenia robotov (poradie podľa cv2/projektu)_
  - Problém: Prednáška neuvádza kanonické poradie 4 filtračných krokov pre robotov — toto poradie je 'podľa cv2/projektu', čo bez znalosti projektu môže pôsobiť arbitrárne (User-Agent kľúčové slová pred prázdnym agentom? alebo opačne?).
  - Návrh: Buď premeniť na 'cat' (rozdeliť kritériá na User-Agent based vs IP-based), alebo doplniť prompt o odôvodnenie poradia (od najľahšie identifikovateľných po najťažšie).
- 🟡 **task #16** (`fill`, Nejednoznačná odpoveď)
  - _Pri p=0.4 je hraničný čas ≈ ___ krát priemer Length_
  - Problém: Akceptované odpovede sú '0.51', '0,51', '0.5108'. Študent môže zadať '0.5', '0,5' alebo iné rozumné zaokrúhlenie — fill matching to nezachytí.
  - Návrh: Pridať '0.5', '0,5', '0.510', '0.511' do alts; alebo premeniť na quiz s 3-4 možnosťami (0.4, 0.51, 0.6, 0.92).
- 🟡 **task #14** (`fill`, Nejednoznačná odpoveď)
  - _MLE odhad lambda = 1 deleno ___ (priemer dĺžky návštev)_
  - Problém: Akceptuje 'priemer' / 'priemerom', ale logicky správne odpovede 'x̄', 'x bar', 'mean', 'priemer Length' nie sú v alts. Študent by mohol intuitívne napísať symbol z prednášky.
  - Návrh: Pridať alts: 'x̄', 'x bar', 'mean', 'priemer Length', 'aritmeticky priemer'.
- 🔴 **task #24** (`fill`, Pokazené)
  - _...platí t_i − t_{i−1} ___ τ (vložte symbol porovnania, napr. <=, >=, <)_
  - Problém: Prompt obsahuje samotnú odpoveď ako hint ('napr. <=, >=, <') — to jednak prezrádza dva nesprávne odpovede a jednak odhaluje že správna je '<='. Triviálna úloha s prezradeným riešením.
  - Návrh: Odstrániť '<=' z hintov a ponechať len 'symbol porovnania (≤, <, ≥, >, =)' alebo pred quiz preformulovať na quiz so 4 nerovnosťami.

**Chýba pre učiteľnosť:**

- Apache Combined Log Format — z čoho sa skladá riadok (atribúty IP, DateTime, Method, URL, StatusCode, Bytes, Referrer, User-Agent) — task 2 ich rozdeľuje bez úvodu
- HTTP StatusCode triedy (2xx-5xx) — task 5 ich testuje matchom ale prednáška a predchádzajúce tasky to nezavádzajú
- Definícia 'navigačnej' vs 'pomocnej' stránky — prednáška ich spomína v kontexte parametra p, ale interaktívne učenie ich nikde nevysvetľuje

**Adversarial verify:** ✅ audit_ok=True

Audit false positives (problém v skutočnosti nie je):
  - task #14: Task 14 alts už obsahuje 'priemer' a 'priemerom' — to sú najprirodzenejšie slovenské odpovede zodpovedajúce promptu ('priemer dĺžky návštev'). Symbol x̄ je v prednáške označený ako premenná v texte, ale prompt explicitne hovorí 'priemer dĺžky návštev', takže študent prirodzene napíše 'priemer'. Pridať 'x̄', 'mean' alebo 'aritmeticky priemer' je nice-to-have, ale chýbanie týchto alts nie je reálny problém — prompt jasne navádza na slovo 'priemer'.

Audit prehliadol:
  - task #0 (`content-not-in-lecture`): Task 0 (flash) tvrdí '60-80 % času celého WUM procesu' tvorí príprava dát. Túto konkrétnu štatistiku som v prednaska_6.txt nenašiel — prednáška spomína iba 'Príprava dát' ako fázu, ale bez konkrétneho percentuálneho odhadu. Toto je všeobecne známy WUM fakt z literatúry, ale nie z prednášky 6 — môže byť zavádzajúci pre študenta pri obhajobe (project_proj_defense.md: 'teóriu treba naspamäť').
  - task #27 (`duplicate-with-task-15`): Task 27 (order) usporiadava kroky odhadu hraničného času τ (Reference Length): priemer x̄ → λ=1/x̄ → p → kvantilová funkcia → prah. Toto sa veľmi prekrýva s tasks 13 (flash o exp. rozdelení), 14 (fill o MLE λ=1/priemer) a 15 (quiz o kvantilovej funkcii) — task 27 ich len zostavuje do sekvencie. Nie je to úplne redundantné (typ úlohy je iný, integrujúci), ale audit toto neoznačil ako potenciálny problém learnability/redundancie.

---

### P7 — CRISP-DM III — Príprava dát (UNIXTIME, používatelia, Length) 🟢 **GOOD**

**Skóre:** Type-fit 87% · Chronológia GOOD · Learn 8/10 · Quality 7/10

**Summary:** Prednáška 7 má 39 taskov, z ktorých väčšina je dobre formulovaných a kryje vhodne UNIXTIME, identifikáciu používateľov, Length výpočet a teoretické základy exponenciálneho rozdelenia. Pomer task type fit je vysoký (~87%), match a order tasks sú vhodne použité pre prirodzene viacpoložkové znalosti. Hlavné problémy: task_index 3 (flash so zoznamom 4 položiek by mal byť order), task_index 6 (arbitrárne číslo 100 v NAT), task_index 27 (duplicate quiz s flash 26), a niekoľko ambiguous answer matchings vo fill úlohách s matematickou notáciou. Chronológia je vcelku dobrá (úvod UNIXTIME → users → Length → matematické základy → formálne definície), drobný presun order task 37 by ju vylepšil. Učiteľnosť 8/10 — väčšina taskov má dostatočný kontext, ale pojem 'navigačné stránky' (premenná p) sa používa bez definície.

**Findings:**

- 🟡 **task #3** (`flash`, Zlý typ úlohy)
  - _Aké 4 metódy identifikácie používateľov sa používajú a v akom poradí podľa presnosti?_
  - Problém: Odpoveď je zoznam 4 položiek s poradím — typický kandidát na order task, kde sa študent učí aktívne usporiadať od najslabšej po najpresnejšiu metódu.
  - Návrh: Premeň na order task: items=['Iba IP','IP + User-Agent','Cookies','Login/prihlásenie'] s promptom 'Usporiadaj metódy identifikácie od najslabšej po najpresnejšiu'.
- 🔴 **task #6** (`fill`, Nejednoznačná odpoveď)
  - _Pri NAT môže jednu verejnú IP adresu zdieľať aj ___ a viac ľudí._
  - Problém: Číslo 100 je arbitrárne — prednáška presný počet neuvádza, mohlo by byť 50, 200, 'desiatky'. Answer matching zlyhá pri rozumných alternatívach.
  - Návrh: Preformuluj na quiz s možnosťami (1-2, 10, 100+, neobmedzene), alebo vymeň na všeobecnejší fill o NAT bez konkrétneho čísla.
- 🟡 **task #8** (`cat`, Triviálne)
  - _Roztrieď tvrdenia podľa správnosti pri identifikácii používateľov (Pravda/Nepravda)_
  - Problém: True/False kategorizácia s len 2 skupinami, kde Nepravda obsahuje očividne nesprávne tvrdenia ('Iba IP je najpresnejšia', 'Login je menej presný ako IP-only') — trivialne rozlišiteľné.
  - Návrh: Posilniť distractory v Nepravda alebo rozdeliť na 3-4 disjunktné kategórie (napr. 'IP-based limitácie' vs 'Cookies/Agent vlastnosti' vs 'HTTP vlastnosti').
- 🟡 **task #16** (`match`, Nejednoznačná odpoveď)
  - _Priraď konverziu časového reťazca na UNIXTIME (pairs s konkrétnymi číslami)_
  - Problém: Tretia dvojica 'Rozdiel medzi nimi → 145 sekúnd' je matematicky nesprávna: 1513488642 − 1513488497 = 145 — to sedí, ale match je trivial — keďže iba 3 páry a tretí sa dá vyčítať odčítaním zo zvyšných, match nepridáva pedagogickú hodnotu.
  - Návrh: Pridaj 4. pár (napr. iný čas+hodnota) alebo zmen na fill: 'Rozdiel medzi 18:16:26 a 18:19:47 v sekundách = ___' s answer 201.
- 🟡 **task #27** (`quiz`, Duplikát)
  - _Ako pomáha štruktúra stránok (referrer, topológia) pri identifikácii používateľov?_
  - Problém: Takmer doslovne duplikuje flash task_index 26 — quiz iba parafrázuje rovnakú odpoveď so správnou možnosťou ako reformulácia flash karty. Žiadne nové učenie.
  - Návrh: Zmaž quiz alebo preformuluj na konkrétny scenár (napr. 'User navštívi stránky A→B→C, potom skočí na X bez odkazu z A,B,C. Čo je pravdepodobné?').
- 🟡 **task #30** (`fill`, Nejednoznačná odpoveď)
  - _Hustota exponenciálneho rozdelenia má tvar f(t) = λ · e^(___)._
  - Problém: Akceptovateľné odpovede '-lambda*t', '-λt', '-λ·t', '-lambda t' — answer matching je v poriadku, ale 'správny' tvar v answer='-lambda*t' je s asteriskom, čo nie je intuitívne ani štandardné v matematike. Študent ľahko napíše '-λt' bez separátora.
  - Návrh: Posilniť alts: pridaj '-lambdat', '-lambda·t', '-λ*t'; alebo zmeň formuláciu na quiz so 4 tvarmi.
- 🟡 **task #33** (`fill`, Nejednoznačná odpoveď)
  - _MLE odhad parametra exponenciálneho rozdelenia: λ̂ = 1 / ___ (priemer Length)._
  - Problém: Answer='x' je zlomok matematickej notácie — študent skôr napíše 'priemer', 'x̄', 'μ' alebo 'mean'. Hoci sú v alts, primárna odpoveď 'x' je málo intuitívna a študent ľahko trafí mimo.
  - Návrh: Zmen primárnu odpoveď na 'x̄' alebo 'priemer'; alts ponechaj.
- 🟡 **task #12** (`quiz`, Mimo poradia)
  - _Aký je STT (Session Timeout Threshold) podľa zadania pre výpočet Length?_
  - Problém: Pojem STT (60-min) je tu zavedený náhle bez predošlej definície/intuitívneho výkladu. Lekcia 8 STT definuje formálne — v lekcii 7 sa tu používa konkrétna hodnota bez teoretického zázemia.
  - Návrh: Pridaj pred tento task krátky flash 'Čo je STT a prečo 60 min' alebo upresni v otázke že STT je hyperparameter projektu.
- 🟡 **task #37** (`order`, Mimo poradia)
  - _Usporiadaj kroky odvodenia hraničného času δ z dát (matematicky)_
  - Problém: Tento order task je výborný zhrňujúci, ale prichádza až ako úplne posledný — pred ním už boli match a formal definitions sedení (tasks 34, 35, 36). Logicky by mal nasledovať hneď po MLE flash/fill (32, 33), pretože opisuje matematickú odvodbu.
  - Návrh: Presuň order task ihneď za task_index 33 (MLE fill), pred formálne definície sedení.

**Chýba pre učiteľnosť:**

- Pojem 'navigačná stránka' vs 'obsahová stránka' — premenná p (relatívna početnosť navigačných stránok) sa vo flash 30 a fill 31 používa bez vysvetlenia, čo navigačná stránka je (toto definuje až ďalšia prednáška).
- Intuitívny príklad výpočtu δ s konkrétnymi číslami — tasks 30-33 dávajú vzorce, ale chýba 'dosaď x̄ = 100s, p = 0.4, výsledok δ = ?' typu výpočet, ktorý by ukázal použitie vzorcov v praxi.
- Intro k STT pred jeho použitím v task 12-14 — hodnota 3600s (60 min) je arbitrárne zavedená; chýba motivácia 'prečo práve 60 min' alebo zmienka že je to project hyperparameter ladený KS testom (príde až v P8).

**Adversarial verify:** ✅ audit_ok=True

Audit prehliadol:
  - task #1 (`ambiguous-answer`): Fill task pre dátum 1.1.1970 nemá v alts ISO formát '1970-01-01' alebo '1970' — študent oboznámený s ISO 8601 (bežný v dátových vedách) môže napísať '1970-01-01' a dostane nesprávne. Pridať alt '1970-01-01'.
  - task #13 (`ambiguous-answer`): Fill 'Length väčšia alebo rovná ako ___ sekúnd' s answer='3600' a alts=['3600'] — chýba alt '3600s', '60*60', '3600 sekúnd'. Aj keď je primárna odpoveď jednoznačná, žiadne tolerancia pre alternatívne notácie.

---

### P8 — CRISP-DM IV — Sedenia + Doplnenie ciest 🟡 **NEEDS_WORK**

**Skóre:** Type-fit 84% · Chronológia MIXED · Learn 6/10 · Quality 7/10

**Summary:** Sekcia P8 má 32 taskov s dobrým mixom typov (flash/fill/quiz/match/order/cat). Najväčší problém je CHRONOLÓGIA: základné pojmy WALS a identifikácia používateľa (tasks 26-30) sú zaradené až na koniec, hoci v lekcii prichádzajú PRED sedeniami a doplňaním ciest. Druhým väčším problémom je task 8 (KS test) a task 16 (order s vetvami if-else), ktoré porušujú buď opieranie o text lekcie, alebo logiku order úlohy. Pár taskov sa obsahovo prekrýva (18-19-20 o h-ref a STT_Q vs STT_MEAN). Učiteľnosť je obmedzená predpokladmi externých znalostí (KS test, Cooley, mapa webu ako algoritmický pojem). Kvalita formulácií je inak slušná, vzorce sú správne, distractors väčšinou zmysluplné s výnimkou tasku 11 (trivial).

**Findings:**

- 🔴 **task #26** (`flash`, Mimo poradia)
  - _Aká je formálna definícia WALS (Web Access Log Set)?_
  - Problém: Základná definícia WALS by mala byť úvodom — je to vstup celého procesu spomenutý v lekcii ako prvé, ale tu je až na pozícii 26 po pokročilých STT vzorcoch a doplňaní ciest.
  - Návrh: Presunúť na začiatok (pred task 0) — WALS je predpoklad pre pochopenie sedení.
- 🟡 **task #27** (`fill`, Mimo poradia)
  - _WALS (Web Access Log Set) je množina ... zoradených podľa ___ známky._
  - Problém: Základný pojem WALS — patrí na úvod, nie na koniec po pokročilých témach.
  - Návrh: Presunúť k taskom o WALS na začiatok sekcie.
- 🔴 **task #28** (`flash`, Mimo poradia)
  - _Aké tri zdroje informácií slúžia na identifikáciu používateľa_
  - Problém: Identifikácia používateľa je v lekcii pred identifikáciou sedení a doplňaním ciest. Tu je až na konci po sedeniach a path completion — porušuje slide flow.
  - Návrh: Presunúť pred tasks o sedeniach (pred task 0 alebo hneď po WALS).
- 🟡 **task #29** (`match`, Mimo poradia)
  - _Priraď zdroj informácie k tomu, ako pomáha identifikovať používateľa_
  - Problém: Match o IP/Cookie/Agent patrí logicky pred identifikáciu sedení (rovnaký dôvod ako task 28).
  - Návrh: Presunúť spolu s ostatnými task o identifikácii používateľa pred sedenia.
- 🟡 **task #30** (`quiz`, Mimo poradia)
  - _Prečo samotná IP adresa nestačí na identifikáciu používateľa_
  - Problém: Téma identifikácie používateľa skončila tu (task 30) ale začína v lekcii pred sedeniami. Chronológia opačná.
  - Návrh: Presunúť do bloku s ostatnými tasks o identifikácii používateľa na začiatok sekcie.
- 🟡 **task #11** (`quiz`, Triviálne)
  - _Ktorý algoritmus / autor sa spomína v súvislosti s referrer-based identifikáciou sedení (h-ref)?_
  - Problém: Distractors Apriori, K-means, PageRank sú zjavne nezmysel — žiadny z nich nesúvisí so sedeniami. Odpoveď je triviálne identifikovateľná elimináciou. Navyše Cooley nie je explicitne v texte lekcie (h-ref je projektová terminológia).
  - Návrh: Premeniť na flash o tom kto je Cooley a aký bol jeho prínos, alebo nahradiť distractor relevantnejšími autormi (napr. Berendt, Spiliopoulou).
- 🔴 **task #8** (`quiz`, Pokazené)
  - _KS test (Kolmogorov-Smirnov) v projekte slúži na: ..._
  - Problém: Otázka explicitne odkazuje na „projekt", ale lekcia 8 KS test menom nespomína (iba hovorí „ak premenná Length nemá exponenciálne rozdelenie"). Predpokladá externé znalosti z cvičení.
  - Návrh: Preformulovať aby otázka necitovala „projekt" a vysvetlila prepojenie v explain: „Ak premenná Length nemá exp. rozdelenie, použijeme fallback STT_Q. Aký test overuje tento predpoklad?" + uviesť KS test ako odpoveď.
- 🔴 **task #16** (`order`, Nejednoznačná odpoveď)
  - _Usporiadaj kroky výpočtu RLength s fallbackom na STT_Q_
  - Problém: Položky „Ak H0 platí: ..." a „Ak H0 neplatí: ..." sú vetvy (alternatívy), nie sekvenčné kroky. V skutočnej procedúre sa vykoná iba jedna z nich, takže ich „poradie" nie je kanonické.
  - Návrh: Rozdeliť na 2 menšie order tasky (jeden pre exp. cestu, jeden pre fallback) alebo premeniť na cat (parametrická vetva vs. neparametrická vetva).
- 🟡 **task #5** (`fill`, Nejednoznačná odpoveď)
  - _...Referrer = "___" priamy/externý prístup..._
  - Problém: Odpoveď je jednoznakový pomlčka „-". Bez explicitného uvedenia v texte úlohy (napr. „znak") môže študent skúšať „prázdne", „null", „none". Answer matching je krehký.
  - Návrh: Upresniť úlohu „...signalizuje hodnotu Referrer rovná jednému znaku ___ priamy prístup" alebo pridať alts: ["-","prázdne","null","none"].
- 🟡 **task #18** (`cat`, Nejednoznačná odpoveď)
  - _Roztrieď: parametrické vs. neparametrické_
  - Problém: Kategorizácia „SLength — pevný limit dĺžky sedenia" ako Neparametrické je sporné — SLength žiadne rozdelenie nepredpokladá, ale ani nie je „štatistická metóda" v zmysle parametrickosti. Hraničný prípad.
  - Návrh: Upresniť skupiny na „Vyžaduje predpoklad o rozdelení" vs. „Bez predpokladu rozdelenia" — potom je SLength jasne v druhej skupine.
- 🟡 **task #20** (`cat`, Duplikát)
  - _Roztrieď výroky o STT_Q vs. STT_MEAN_
  - Problém: Veľký prekryv s taskom 6 (quiz Prečo je STT_Q robustný) a taskom 12 (match STT_MEAN/STT_Q → prah). Tretia formulácia tej istej myšlienky.
  - Návrh: Buď zlúčiť s taskom 6, alebo nahradiť výpočtovým príkladom (daná vzorka, vypočítaj STT_Q).
- 🟡 **task #19** (`cat`, Duplikát)
  - _Roztrieď: kedy ide o NOVÉ sedenie (h-ref) vs. pokračovanie_
  - Problém: Vysoký prekryv s taskom 14 (match podmienka → signalizuje v h-ref). Tie isté podmienky sú zaradené dvakrát do dvoch rôznych úloh.
  - Návrh: Vybrať len jednu z týchto dvoch (match alebo cat), druhú nahradiť tématickej dierou (napr. otázka na rozdiel time-only vs. h-ref hybridnej metódy).
- 🟡 **task #17** (`order`, Nejasné)
  - _Usporiadaj kroky dopĺňania ciest pre jedno sedenie_
  - Problém: Lekcia 8 popisuje doplnenie ciest len cez konkrétny príklad (A,B,C,D→X) bez explicitných algoritmických krokov ako „postav mapu webu", „urči kanonického rodiča". Predpokladá implementačnú znalosť z cvičení.
  - Návrh: Pridať buď flash s vysvetlením „mapa webu" pred tento order task, alebo zjednodušiť kroky na to, čo je v slide (z mapy A,B,C,D rekonštruuj cestu pri skoku z D na X).

**Chýba pre učiteľnosť:**

- Explicitné intro k pojmu USS (User Session Set) — formálna definícia, ktorá je v lekcii
- Vysvetlenie pojmu „Length" pred jeho použitím v STT taskoch (čas medzi po sebe idúcimi prístupmi)
- Pojem „referenčná dĺžka" / motivácia pre voľbu p=0,4 (podiel navigačných stránok)
- Explicitné prepojenie KS testu na lekciu (lekcia hovorí len o predpoklade exp. rozdelenia, nie o KS teste)
- Definícia „navigačná vs. obsahová stránka" — používa sa v RLength bez vysvetlenia
- Cooley / autor h-ref metódy — task 11 ho spomína, ale nikde inde nie je predstavený

**Adversarial verify:** ✅ audit_ok=True

Audit false positives (problém v skutočnosti nie je):
  - task #18: Auditor sám priznáva, že ide o hraničný prípad (severity minor). SLength bez predpokladu rozdelenia legitímne patrí do kategórie 'neparametrické / robustné', a názov skupiny v taske ('Neparametrické / robustné') je dostatočne široký. Nie je to skutočný problém s odpoveďou — žiak by rovnako triedil. Skôr terminologický nuans než ambiguous-answer.

Audit prehliadol:
  - task #12 (`inconsistent-definition`): Match definuje h-ref ako 'čas + podmienka Referrer = "-"' (2 podmienky), ale task 14 a 19 ho prezentujú s 3 podmienkami (vrátane 'Referrer neukazuje na žiadnu z navštívených stránok'). Nezhoda medzi taskmi o tej istej metóde.
  - task #13 (`pedagogically-confusing`): Pár 'μ (priemer Length)' → 'maximálne vierohodný odhad pre 1/λ exp. rozdelenia' je formálne korektný, ale matúci — bežnejšie sa hovorí, že λ̂ = 1/x̄ je MLE pre λ, nie že x̄ je MLE pre 1/λ. Bez vysvetlenia v explain (match ho nemá) môže žiak pojem prevrátiť.

---

### P9 — CRISP-DM V — Modelovanie 🟡 **NEEDS_WORK**

**Skóre:** Type-fit 78% · Chronológia MIXED · Learn 5/10 · Quality 7/10

**Summary:** Prednáška 9 (CRISP-DM V — Modelovanie) je obsahovo veľmi stručná — 10 slidov pokrýva iba: 6 typov úloh modelovania a zoznamy odporúčaných CRISP-DM metód pre každú úlohu. Sada 27 taskov má dva odlišné módy: tasks 0-8, 21, 23-24 sú dobre zarovnané so slide flow (vhodný type, jasné otázky, učiteľné). Tasks 9-20 a 22, 26 však obsahujú detaily o asociačných pravidlách (formuly support/confidence/lift, Apriori, anti-monotónnosť, PrefixSpan, sekvenčné pravidlá, instance-based vs eager learners), ktoré prednáška 9 vôbec neobsahuje — len menuje 'Asociačné pravidlá' v zozname metód pre analýzu závislostí. To je 14 taskov (~52 %), ktoré predpokladajú znalosti mimo prednášky, čo blokuje samostatnú učiteľnosť. Chronologicky je flow narušený: deep-dive do AR/Apriori v strede sady prerušuje slide-based líniu, ktorá sa vracia až pri taskoch 21-25. Typy taskov sú prevažne vhodne zvolené (správny mix flash/fill/quiz/match/order/cat), ale obsah tém je problém. Odporúčanie: presunúť AR/Apriori/PrefixSpan tasky do prednášky, ktorá tieto pojmy skutočne pokrýva, alebo doplniť prednášku 9 o úvodné slidy.

**Findings:**

- 🟡 **task #2** (`match`, Nejednoznačná odpoveď)
  - _Priraď typ úlohy k jej cieľu (Deskripcia/Segmentácia/Klasifikácia/Predikcia/Analýza závislostí)_
  - Problém: Prednáška 9 iba vymenováva typy úloh menom, neuvádza žiadne definície/ciele — študent nemá z prednášky odkiaľ vedieť, že 'Segmentácia = rozdelenie do homogénnych skupín'. Predpokladá externú znalosť.
  - Návrh: Buď doplniť do prednášky popisy (intro slide pre každú úlohu), alebo presunúť tento match do skoršej prednášky kde sa definície vysvetľujú; alebo preformulovať tak, aby cieľ bol odvoditeľný z mien.
- 🔴 **task #9** (`flash`, Mimo poradia)
  - _Čo je asociačné pravidlo? X → Y, príklad pivo/plienky_
  - Problém: Asociačné pravidlá ako pojem nie sú v prednáške 9 vôbec vysvetlené — prednáška iba uvádza 'Asociačné pravidlá' v zozname metód pre analýzu závislostí. Definícia + príklad pivo/plienky nepatrí do P9.
  - Návrh: Buď presunúť do prednášky, ktorá AR skutočne preberá, alebo si overiť, či nemá byť celá AR-séria (tasks 9-20) v inej prednáške.
- 🔴 **task #10** (`flash`, Mimo poradia)
  - _Vzorec pre support asociačného pravidla_
  - Problém: Vzorec support v prednáške 9 vôbec nie je — prednáška AR len menuje. Student nemá z čoho sa to naučiť.
  - Návrh: Presunúť mimo P9 alebo doplniť do prednášky úvodný slide o AR so vzorcami.
- 🔴 **task #11** (`flash`, Mimo poradia)
  - _Vzorec pre confidence asociačného pravidla_
  - Problém: Vzorec confidence v prednáške 9 nie je. Predpokladá externú znalosť.
  - Návrh: Presunúť mimo P9 alebo doplniť teóriu AR do prednášky.
- 🔴 **task #12** (`flash`, Mimo poradia)
  - _Vzorec pre lift a interpretácia_
  - Problém: Lift v prednáške 9 vôbec nie je definovaný. Pojem je natoľko špecifický, že bez explicitnej teórie sa nedá deduktovať.
  - Návrh: Presunúť mimo P9 alebo doplniť slide o miere lift do prednášky.
- 🔴 **task #13** (`fill`, Mimo poradia)
  - _Miera ... obsahuje obe strany pravidla = support_
  - Problém: Pojem support nie je v prednáške 9 vysvetlený. Duplikuje task 10.
  - Návrh: Presunúť mimo P9; ak ostane, sankcionovať na duplicitu so 10.
- 🔴 **task #14** (`fill`, Mimo poradia)
  - _Algoritmus ... využíva anti-monotónnu vlastnosť = Apriori_
  - Problém: Apriori algoritmus, anti-monotónnosť, frekventované itemsety — nič z toho nie je v prednáške 9.
  - Návrh: Presunúť mimo P9 do prednášky, ktorá pokrýva Apriori, alebo doplniť teóriu.
- 🔴 **task #15** (`quiz`, Mimo poradia)
  - _Čo hovorí Apriori vlastnosť (anti-monotónnosť)?_
  - Problém: Anti-monotónna vlastnosť nie je v prednáške 9. Učiteľnosť 0 — bez externého zdroja nemožno odpovedať.
  - Návrh: Presunúť do prednášky o Apriori.
- 🔴 **task #16** (`order`, Mimo poradia)
  - _Usporiadaj kroky algoritmu Apriori (načítaj, L1, kandidáti...)_
  - Problém: Kroky Apriori nie sú v prednáške 9 vôbec spomínané. Predpokladá hlbokú externú znalosť.
  - Návrh: Presunúť mimo P9.
- 🔴 **task #17** (`quiz`, Mimo poradia)
  - _Rozdiel medzi asociačnými a sekvenčnými pravidlami_
  - Problém: Sekvenčné pravidlá v prednáške 9 nie sú vôbec.
  - Návrh: Presunúť do prednášky o sekvenčných vzoroch (P8 sa tomu venuje).
- 🔴 **task #18** (`fill`, Mimo poradia)
  - _Algoritmus pre frekventované sekvencie = PrefixSpan_
  - Problém: PrefixSpan v prednáške 9 nie je. Veľmi špecifický pojem bez kontextu.
  - Návrh: Presunúť do prednášky o sekvenčných vzoroch.
- 🔴 **task #19** (`match`, Mimo poradia)
  - _Priraď pojem AR (transakcia/itemset/minsup/minconf) k významu_
  - Problém: Žiadny z týchto pojmov nie je v prednáške 9 zavedený.
  - Návrh: Presunúť do prednášky o AR.
- 🔴 **task #20** (`quiz`, Mimo poradia)
  - _Pravidlo pivo→plienky s support 0,1 a confidence 0,8_
  - Problém: Príklad sa opiera o pojmy support/confidence, ktoré P9 neuvádza.
  - Návrh: Presunúť spolu s ostatnými AR-úlohami.
- 🔴 **task #22** (`cat`, Mimo poradia)
  - _Roztrieď: analógické (instance-based) vs modelové (eager learners)_
  - Problém: Prednáška 9 spomína k-NN/CBR ako 'metódy založené na analógii', ale rozdelenie instance-based vs eager learners (lazy vs eager) nezavádza. Pojmy 'eager learners', 'modelové' nie sú v texte.
  - Návrh: Buď preformulovať bez pojmov instance-based/eager (napr. 'metódy založené na analógii vs ostatné'), alebo doplniť teóriu, alebo presunúť mimo P9.
- 🟡 **task #25** (`match`, Nejednoznačná odpoveď)
  - _Priraď príklad úlohy (byt, spam, zákazníci) k typu CRISP-DM_
  - Problém: Príklady (cena bytu, spam, košíky) nepochádzajú z prednášky — sú generické. Učiteľnosť nízka, pretože prednáška neuvádza definície úloh ani príklady. Avšak ak študent vie definície z iných predmetov, je to OK.
  - Návrh: Doplniť do prednášky príklady/definície úloh, alebo zachovať ako 'bonus' s explicitným vysvetlením v hint.
- 🔴 **task #26** (`quiz`, Mimo poradia)
  - _Ktoré tvrdenie o lifte je správne?_
  - Problém: Lift v prednáške 9 nie je. Druhá otázka o lifte (po task 12) duplikuje tému, ktorá tu nepatrí.
  - Návrh: Presunúť mimo P9 alebo doplniť teóriu lift.

**Chýba pre učiteľnosť:**

- Definície/ciele typov úloh modelovania (Segmentácia = rozdelenie do skupín atď.) — bez nich tasks 2, 7, 25 predpokladajú externú znalosť
- Úvodný slide o asociačných pravidlách: pojem AR, support, confidence, lift — bez toho je 12 taskov (9-20, 26) bez učebnej opory
- Apriori algoritmus a anti-monotónna vlastnosť — tasks 14-16 ich vyžadujú
- Sekvenčné pravidlá a PrefixSpan — tasks 17-18 ich vyžadujú
- Rozlíšenie analógické (lazy/instance-based) vs modelové (eager learners) — task 22 ich vyžaduje, prednáška len uvádza 'metódy založené na analógii'

**Adversarial verify:** ✅ audit_ok=True

Audit prehliadol:
  - task #7 (`minor-ambiguity`): Task 7 (match metóda k typu úlohy) priraďuje 'Zhlukovanie konceptov' → 'deskripcia konceptov' a 'OLAP analýza' → 'deskripcia dát a sumarizácia' — tieto sú priamo zo slidov a OK. Avšak pár 'Regresné stromy → predikcia' vs 'Rozhodovacie stromy → klasifikácia' funguje len vďaka tomu, že študent vie rozlíšiť regresné/rozhodovacie. Z prednášky odvoditeľné (regresné stromy sú v zozname pre predikciu, rozhodovacie stromy v zozname pre klasifikáciu), takže OK. Minor — nie je to skutočný miss.

---

### P10 — CRISP-DM VI — Evaluácia a deployment 🟡 **NEEDS_WORK**

**Skóre:** Type-fit 85% · Chronológia MIXED · Learn 6/10 · Quality 7/10

**Summary:** Prednáška 10 v ucenie/index_prednasky.html má 26 taskov, ktoré pokrývajú evaluáciu (overenie predpokladov, porovnanie, vizualizácia) a deployment (5 kategórií aplikácií). Hlavné silné stránky: dobrý mix typov (flash/fill/quiz/match/cat/order), zmysluplné explainy. Hlavné slabiny: (1) tasks 3-10 zavádzajú konkrétne neparametrické testy (Cochranov Q, Friedman, Kendall W, Wilcoxon, Bartlett), ktoré v texte prednášky 10 vôbec nie sú — len pojem 'neparametrické alternatívy' — čo porušuje learnability bez externého zdroja; (2) chronológia je MIXED — order kroky evaluácie (task 11) prichádza až po deep dive, vizualizačné tasks (12-13) sú medzi testami, a task 25 (cat o Cochran/Friedman) je úplne na konci po deployment; (3) duplikácie: task 19 (match) prekrýva task 17 (cat) o aplikáciách a task 25 prekrýva tasks 3-6, 10 o testoch; (4) task 17 cat má nekonzistentnú štruktúru groups (mix popisných viet a zoznamov techník). Verdict: NEEDS_WORK — funkčné jadro, ale rozšírenia mimo slidov a štrukturálne duplikáty vyžadujú prepracovanie.

**Findings:**

- 🔴 **task #3** (`flash`, Pokazené)
  - _Aký je účel Cochranovho Q testu?_
  - Problém: Cochranov Q test vôbec nie je spomenutý v prednáške 10 (ani v žiadnej skoršej) — task zavádza pojem bez akéhokoľvek úvodu zo slidov, predpokladá externé znalosti.
  - Návrh: Pridať pred flash krátky intro/context task vysvetľujúci 'neparametrické alternatívy testov' s odkazom, že tieto špecifické testy sú rozšírenie nad rámec slidov. Alebo zmeniť na všeobecnejšiu otázku o neparametrických alternatívach.
- 🔴 **task #4** (`flash`, Pokazené)
  - _Čo meria Kendallov koeficient konkordancie W?_
  - Problém: Kendallov W nie je v texte prednášky 10 — len pojem 'neparametrické alternatívy'. Pre študenta učiaceho sa zo slidov neexistuje žiadny zdroj pre tento pojem.
  - Návrh: Buď odstrániť, alebo presunúť do separátnej sekcie 'rozšírenie' s jasným označením, že nejde o učivo prednášky.
- 🔴 **task #5** (`flash`, Pokazené)
  - _Na čo slúži Friedmanov test?_
  - Problém: Friedmanov test nie je v texte prednášky 10. Tasks 3-10 zavádzajú konkrétne testy mimo skopu prednášky.
  - Návrh: Odstrániť alebo zhrnúť všetky tri (Cochran/Friedman/Kendall) do jedného súhrnného flash 'príklady neparametrických alternatív' bez detailov.
- 🔴 **task #7** (`fill`, Nejednoznačná odpoveď)
  - _Friedmanov test je neparametrická alternatíva ___ ANOVA (opakovaných meraní)._
  - Problém: Veta tvrdí 'parametrickej ANOVA' — ale ANOVA je inherentne parametrická, takže slovo 'parametrickej' je redundantné a študent by skôr napísal 'klasickej' alebo 'opakovaných meraní'. Tieto sú legitímne ale answer matching ich odmietne.
  - Návrh: Preformulovať na: 'Friedmanov test je neparametrická alternatíva ___ meraní ANOVA.' s answer 'opakovaných'. Konkrétne a jednoznačné.
- 🔴 **task #10** (`cat`, Pokazené)
  - _Roztried metódy podľa toho, či sú parametrické alebo neparametrické._
  - Problém: Obsahuje 'Wilcoxonov test' a 'Bartlettov test' ktoré neboli vôbec nikde predtým predstavené v prednáške ani v predchádzajúcich tasks — študent ich nemá ako vedieť.
  - Návrh: Odstrániť Wilcoxon a Bartlett, alebo pridať flash/intro pre ne pred týmto cat. Alternatívne nahradiť ich už zavedenými metódami z prednášky.
- 🟡 **task #11** (`order`, Mimo poradia)
  - _Usporiadaj kroky vo fáze vyhodnotenia výsledkov (CRISP-DM)._
  - Problém: Tento order o krokoch fázy by mal byť hneď za task 0/1 ako prehľad fázy, nie až po 8 detailných tasks o konkrétnych testoch. Učenie ide od konkrétneho k všeobecnému namiesto naopak.
  - Návrh: Presunúť pred task 3 (pred deep dive do konkrétnych testov), ideálne na pozíciu task 2.
- 🟡 **task #12** (`flash`, Mimo poradia)
  - _Čo je logit a prečo sa vizualizuje?_
  - Problém: Logit patrí k 'Vizualizácia' kategórii z prednášky, ale je tu zaradený medzi testy a porovnaniami. Mal by byť pri tasks o vizualizácii.
  - Návrh: Presunúť bližšie k task 1 (cat o overení/porovnaní/vizualizácii), alebo zoskupiť všetky vizualizačné tasks (12, 13) s task 1.
- 🟡 **task #14** (`quiz`, Triviálne)
  - _Porovnanie rozdelenia pravdepodobnosti empirických... a odhadnutých pravdepodobností výberu webovej časti j v čase i sa robí pomocou:_
  - Problém: Distraktory 'Asociačné pravidlá', 'PageRank algoritmus', 'K-means klastrovania' sú zjavne mimo kontextu — 3 zo 4 sú zjavné nezmysly, čo robí quiz trivial.
  - Návrh: Nahradiť distraktory podobnými testami: 'Testy rozdelenia (chí-kvadrát dobrej zhody)', 'Testy o rozptyle', 'Testy nezávislosti'. Tak otázka testuje reálne pochopenie.
- 🔴 **task #17** (`cat`, Nejasné)
  - _Roztried do 5 kategórií aplikácií web log miningu podľa prednášky._
  - Problém: Štruktúra groups je nekonzistentná — niektoré položky sú popisné vety ('Odporúčanie obsahu...'), iné sú zoznamy techník ('Segmentácia + Klasifikácia + Analýza závislostí'), iné chýbajú ('Business intelligence' má len abstraktnú vetu). Niektoré kategórie majú len 1 položku, čo cat task nepotrebuje klasifikovať.
  - Návrh: Buď zmeniť na match (kategória ↔ príklad aplikácie + technika), alebo zjednotiť: každá skupina ≥2 konkrétne príklady aplikácií rovnakého typu.
- 🔴 **task #19** (`match`, Duplikát)
  - _Priraď aplikáciu web log miningu k použitej dolovacej technike._
  - Problém: Obsahovo prekrýva task 17 (cat) — tie isté páry aplikácia→technika sú v oboch taskoch. Študent rieši dvakrát to isté.
  - Návrh: Odstrániť task 17 (cat má slabú štruktúru) a ponechať len match task 19, ktorý je jasnejší. Alebo odstrániť task 19 a opraviť cat.
- 🔴 **task #25** (`cat`, Duplikát)
  - _Roztried výroky o štatistických testoch pre závislé vzorky._
  - Problém: Duplikuje obsah tasks 3-6, 10 — opäť Cochran/Friedman/Kendall fakty. Navyše je úplne na konci, po deployment/summary tasks, čo je out-of-order.
  - Návrh: Buď odstrániť ako duplikát, alebo ak má slúžiť ako záverečný review, presunúť hneď za task 10 a označiť ako 'kontrolný cat'.

**Chýba pre učiteľnosť:**

- Úvodný kontext o tom, že konkrétne neparametrické testy (Cochranov Q, Friedman, Kendall W, Wilcoxon, Bartlett) nie sú menované v slidoch prednášky 10 — sú to rozšírenia. Bez tejto poznámky študent stráca orientáciu, čo je 'učivo' a čo 'rozšírenie'.
- Stručná definícia pojmu 'empirické vs. teoretické početnosti/pravdepodobnosti' pred tasks 14-15, ktoré pojem používajú bez vysvetlenia.
- Vysvetlenie 'webovej časti j v čase i' a 'referenčnej webovej časti' — používa sa v taskoch 13, 14, ale prednáška to nevysvetľuje, predpoklad z predchádzajúcich prednášok.
- Intro k pojmu 'multivariačné testy o rozptyle' a 'variančno-kovariančné matice' — používa sa v taskoch 1, 16, ale chýba intuitívne vysvetlenie.

**Adversarial verify:** ✅ audit_ok=True

Audit prehliadol:
  - task #2 (`out-of-scope-names-in-explain`): Task 2 (quiz o rovnosti rozptylov) má v explain text 'Univariačné testy o rozptyle (napr. Levene, Bartlett)...' — Levene a Bartlett nie sú v texte prednášky 10 (text uvádza len 'testy o rozptyle a ich neparametrické alternatívy'). Podobný problém ako audit identifikoval pre tasks 3-10, hoci tu je menej závažný, lebo mená sú len v post-answer explain, nie v otázke.
  - task #15 (`out-of-scope-name`): Task 15 (quiz o porovnaní teoretických a empirických početností) má v správnej odpovedi 'Testov rozdelenia (napr. chí-kvadrát test dobrej zhody)' — chí-kvadrát test dobrej zhody nie je explicitne menovaný v texte prednášky 10 (text hovorí len 'testy rozdelenia'). Borderline, lebo je to bežná konkretizácia, ale formálne extension.

---
