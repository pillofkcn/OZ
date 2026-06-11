# PROJEKT — Web Usage Mining

**Autor:** Martin Studený
**Pridelené obdobie:** 17.12.2017 — 23.12.2017
**Dátum:** 2026-05-05

---

## Obsah

1. [Úvod pre nového čitateľa](#úvod-pre-nového-čitateľa)
2. [Zadanie projektu](#zadanie-projektu)
3. [Vstupné dáta](#vstupné-dáta)
4. [Použité knižnice](#použité-knižnice)
5. [Detailný popis úloh 00–10](#detailný-popis-úloh-0010)
6. [Metodológia — prehľad metód](#metodológia--prehľad-metód)
7. [Výsledky pipeline](#výsledky-pipeline)
8. [Diskusia a závery](#diskusia-a-závery)
9. [Najčastejšie otázky pri obhajobe](#najčastejšie-otázky-pri-obhajobe)

---

## Úvod pre nového čitateľa

Máme **server log z webu Univerzity Konštantína Filozofa** (`www.ukf.sk`) — textový súbor, kde každý riadok = jedno otvorenie stránky niekým na internete. Za 4 roky (2017–2020) je tam **47 miliónov takýchto klikov** (12 GB). Z toho mi bol pridelený **jeden týždeň** (17.–23.12.2017, ~910 tisíc klikov), ktorý mám spracovať.

**Cieľom projektu je dostať surový log do podoby, na ktorej sa dajú analyzovať vzory správania používateľov** (napr. nájsť, že kto otvoril stránku X, často otvorí aj Y — tzv. *asociačné pravidlá* z cv6). To zahŕňa:

1. **Vyčistiť** záznamy — odhodiť prístupy robotov (Google, Bing…), nepodstatné POST/error riadky, statické súbory (CSS, obrázky).
2. **Odhadnúť, kto je kto** — log nemá prihlásenia, takže používateľa odhadneme ako dvojicu `(IP adresa, prehliadač)`.
3. **Rozdeliť kliky na sedenia** — jedno sedenie = súvislá návšteva, kým človek nezatvoril prehliadač/neodišiel. Dve metódy: **RLength** (štatisticky odvodená hranica) a **h-ref** (porovnanie URL s Referrerom).
4. **Doplniť chýbajúce stránky** — niektoré stránky používateľ videl, ale server ich nezachytil (cache, tlačidlo Späť). Doplníme ich rekonštrukciou z mapy webu.

Výstupom je **vyčistený CSV** so stĺpcami `USER_ID`, `SESSION_ID`, `URL`, `UNIXTIME`…, ktorý by sa dal použiť napr. ako vstup pre **Apriori** algoritmus na hľadanie asociačných pravidiel (cv6).

**Metodologicky** ide o fázu *Data Preparation* z **CRISP-DM** (Cross-Industry Standard Process for Data Mining) aplikovanú na **Web Usage Mining (WUM)** = data mining nad záznamami o používaní webu. Detailný teoretický rámec je v sekcii [Detailný popis úloh 00–10](#detailný-popis-úloh-0010) a [Metodológia](#metodológia--prehľad-metód).

---

## Zadanie projektu

Z priloženého logovacieho súboru (Apache web server log) zopakovať celý postup naučený za semester:

- ✅ očistiť dáta od nepotrebných záznamov *(RequestMethod, Version, StatusCode, URL)*
- ✅ očistiť dáta od prístupov robotov vyhľadávacích služieb
  - identifikácia podľa prístupu k `robots.txt`
  - identifikácia podľa `User-Agent`
- ✅ vyselektovať pridelené obdobie + vytvoriť premennú `UNIXTIME`
- ✅ identifikovať používateľov podľa `IP + User-Agent`
- ✅ vytvoriť premennú `Length` na základe `User_ID` a 60-min STT
- ✅ identifikovať sedenia 2 metódami:
  - **Reference Length** (40% navigačných stránok, fallback `STT_Q`)
  - **h-ref**
- ✅ doplniť chýbajúce stránky pre obe metódy

---

## Vstupné dáta

| Vlastnosť | Hodnota |
|-----------|---------|
| Súbor | `materials/wm2020projekt.log` |
| Formát | Apache Combined Log Format |
| Veľkosť | **12 GB** |
| Počet riadkov | **47 215 218** (~47M) |
| Časové rozpätie | 2017 – 2020 |

### Formát riadku Apache logu

```
IP - - [DateTime] "Method URL HTTP/Version" StatusCode Bytes "Referrer" "Agent"
```

### Príklad riadku

```log
193.87.12.30 - - [17/Dec/2017:06:28:17 +0100] "GET /index.html HTTP/1.1" 200 12345 "https://www.ukf.sk/" "Mozilla/5.0..."
```

Pre pridelené obdobie 17.–23.12.2017 sa nájde **909 828** záznamov.

---

## Použité knižnice

### Externé (pip)

```bash
pip install pandas numpy scipy
```

| Knižnica | Účel |
|----------|------|
| `pandas` | Tabuľkové dáta, DataFrame, CSV I/O |
| `numpy` | Matematické operácie, `np.log` (prirodzený logaritmus) |
| `scipy` | Štatistické testy (`kstest`) |

### Štandardná knižnica

| Knižnica | Účel |
|----------|------|
| `re` | Regulárne výrazy (parsovanie Apache logu) |
| `datetime` | Konverzia dátumu na Unix timestamp |
| `os`, `shutil` | Práca so súborovým systémom |
| `urllib.parse` | Parsovanie URL adries |

---

## Detailný popis úloh 00–10

### Pipeline diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│  00 extrakcia týždňa  (12 GB → 216 MB)                              │
└──────┬───────────────────────────────────────────┬──────────────────┘
       ↓                                            ↓
┌──────────────────┐                  ┌────────────────────────────┐
│ 01 čistenie      │                  │ 02 robot IPs               │
│  parse + filter  │                  │  z prístupov k robots.txt  │
└────────┬─────────┘                  └────────────┬───────────────┘
         └────────────────┬──────────────────────┘
                          ↓
              ┌─────────────────────────┐
              │ 03 filter robotov       │
              │  Agent + IP             │
              └────────────┬────────────┘
                           ↓
              ┌─────────────────────────┐
              │ 04 obdobie + UNIXTIME   │
              └────────────┬────────────┘
                           ↓
              ┌─────────────────────────┐
              │ 05 USER_ID              │
              │  IP + Agent             │
              └────────────┬────────────┘
                           ↓
              ┌─────────────────────────┐
              │ 06 Length (60 min STT)  │
              └────┬───────────┬────────┘
                   ↓           ↓
        ┌──────────────────┐  ┌─────────────────────┐
        │ 07 RLength       │  │ 08 h-ref            │
        │  (STT_Q fallback)│  │                     │
        └──────────┬───────┘  └─────────┬───────────┘
                   ↓                    ↓
        ┌──────────────────┐  ┌─────────────────────┐
        │ 09 doplnenie     │  │ 10 doplnenie        │
        │  ciest RLength   │  │  ciest h-ref        │
        └──────────────────┘  └─────────────────────┘
```

---

> ### 📚 Teoretický rámec celého projektu
>
> **Data Mining** = hľadanie netriviálnych, doteraz neznámych a užitočných vzorov v dátach (klasika: „kto kúpi pivo, kúpi aj plienky").
>
> **Web Mining** = data mining aplikovaný na web. 3 vetvy:
> | Vetva | Vstup | Príklad |
> |-------|-------|---------|
> | Web Content Mining | obsah stránok (HTML, text) | analýza sentimentu |
> | Web Structure Mining | hyperlinkový graf | PageRank (Google) |
> | **Web Usage Mining (WUM)** | **logy návštev** | **náš projekt** |
>
> **WUM má 3 fázy:**
> | Fáza | Popis | Kde sme |
> |------|-------|---------|
> | 1. **Data preparation** | čistenie, USER_ID, SESSION_ID, doplnenie ciest | **úlohy 00–10 (celý projekt)** |
> | 2. Pattern discovery | asociačné a sekvenčné pravidlá | mimo projektu |
> | 3. Pattern analysis | štatistické testy, interpretácia | mimo projektu |
>
> Náš projekt = **iba fáza 1**. To nie je „len príprava" — typicky tvorí **60–80 % času** celého WUM procesu.

---

### Úloha 00 — Extrakcia týždňa

> **📚 Čo je Apache log?** Apache je webový server. Pri každej HTTP požiadavke (klient si pýta stránku/súbor) zapíše jeden riadok do textového súboru — tzv. **access log**. 12 GB súbor = záznam o **47 miliónoch požiadaviek** za roky 2017–2020.
>
> **Formát Apache Combined Log:**
> ```
> IP - - [DateTime] "Method URL HTTP/Version" StatusCode Bytes "Referrer" "Agent"
> ```
> | Pole | Význam |
> |------|--------|
> | IP | sieťová adresa klienta *(môže ju zdieľať viac ľudí cez NAT)* |
> | DateTime | kedy server prijal požiadavku |
> | Method | typ HTTP operácie: `GET` (čítanie), `POST` (formulár), `HEAD` (iba hlavičky) |
> | URL | čo si klient pýta |
> | StatusCode | `2xx` úspech, `3xx` presmerovanie, `4xx` chyba klienta, `5xx` chyba servera |
> | Referrer | z ktorej stránky klient prišiel *(odkiaľ klikol)* |
> | User-Agent | identifikácia prehliadača/zariadenia |
>
> **Dôležité:** Apache log je **pasívny záznam**. Server zapíše iba *„prišla požiadavka"*. **Nevidí**, čo používateľ na stránke skutočne robí (scrollovanie, čas čítania, kliky na nelinkované elementy). Toto je fundamentálne obmedzenie WUM zo serverového logu.

**Cieľ:** Z 12 GB pôvodného logu vytiahnuť ~910 000 riadkov pre pridelený týždeň.

**Vstup:** `materials/wm2020projekt.log` *(12 GB)*
**Výstup:**
- `01/in/wm2020projekt_studeny.log` *(216 MB)*
- `02/in/wm2020projekt_studeny.log` *(216 MB)*

#### Algoritmus

```python
dni = ("17/Dec/2017", "18/Dec/2017", "19/Dec/2017", "20/Dec/2017",
       "21/Dec/2017", "22/Dec/2017", "23/Dec/2017")

with open(src) as fin, open(out, "w") as fout:
    for line in fin:                # streamové čítanie
        for d in dni:
            if d in line:           # rýchly substring filter
                fout.write(line)
                break
```

**Prečo streamové čítanie:** 12 GB log nemôžeme nahrať do pamäte naraz. `for line in f` číta súbor riadok po riadku — iba jeden riadok je v pamäti.

#### Výsledok

```log
17/Dec/2017: 113 568    21/Dec/2017: 112 249
18/Dec/2017: 219 333    22/Dec/2017:  83 747
19/Dec/2017: 169 826    23/Dec/2017:  72 417
20/Dec/2017: 138 688
─────────────────────────────────────────
SPOLU:       909 828 záznamov
```

---

### Úloha 01 — Čistenie záznamov

> **📚 Prečo čistiť?** Apache log obsahuje veľa záznamov, ktoré nevypovedajú o navigácii ľudského užívateľa:
>
> 1. **Statické súbory.** Keď načítaš jednu HTML stránku, prehliadač automaticky vyžiada **všetky** obrázky, CSS, JS, fonty. Ak má stránka 30 obrázkov → 1 návšteva = 31 záznamov v logu. Keby sme to nezahodili, priemerný „počet stránok na sedenie" by bol 30× nadhodnotený.
> 2. **Neúspešné a technické požiadavky.** `4xx` (404 a pod.) a `5xx` nie sú reálnou navigáciou. `POST` je odoslanie formulára (nie navigácia). `HEAD` používajú prevažne skripty.
> 3. **Roboti** — riešime v úlohách 02–03.
>
> **Prečo regex namiesto `pd.read_csv`?** Apache Combined Log Format má polia oddelené medzerou, ALE niektoré sú v úvodzovkách (napr. `"GET /url HTTP/1.1"` je *jeden* stĺpec). `pd.read_csv(sep=' ')` to nezvládne — split by rozbil URL aj User-Agent. Regex umožní napasovať presný formát s rôznymi typmi oddeľovačov.

**Cieľ:** Parsovať Apache log a očistiť od nepotrebných záznamov.

**Vstup:** `in/wm2020projekt_studeny.log`
**Výstup:** `out/01_cleaned_log.csv`

#### Regex na parsovanie Apache Combined Log Format

```python
pattern = re.compile(
    r'^(\S+)\s+\S+\s+\S+\s+'      # IP (cookie + user preskočené)
    r'\[([^\]]+)\]\s+'              # DateTime
    r'"(\S+)\s+(\S+)\s*\S*"\s+'     # Method, URL
    r'(\d{3})\s+'                   # StatusCode
    r'(\S+)\s+'                     # Bytes
    r'"([^"]*)"\s+'                  # Referrer
    r'"([^"]*)"'                     # Agent
)
```

#### Aplikované filtre

1. **RequestMethod:** ponechať len `GET` *(POST, HEAD sú technické)*
2. **StatusCode:** ponechať `200–399` *(úspech + presmerovanie)*
3. **URL:** vyhodiť statické súbory:

```python
unwanted_ext = re.compile(
    r'\.(?:bmp|jpe?g|png|gif|css|flv|ico|swf|rss|xml|cur|js|json|svg|woff2?|eot|ttf|otf)(?:\?|$)',
    re.IGNORECASE
)
```

#### Výsledok

```log
Celkom prečítaných:     909 828
Po parsovaní + čistení: 211 313    (zníženie o 77%)
```

---

### Úloha 02 — Identifikácia IP robotov

> **📚 Čo sú roboti a prečo ich riešime?** Vyhľadávače (Google, Bing, Seznam) majú **crawlery** — programy, ktoré automaticky prechádzajú web a indexujú stránky. Pre WUM sú nežiaduce, lebo skreslia metriky („Googlebot navštívil 10 000 stránok za hodinu" nie je „návšteva" v ľudskom zmysle).
>
> **3 spôsoby, ako poznáme robota:**
>
> 1. **`robots.txt`** — súbor v koreni domény, ktorý hovorí robotom, kam smú a kam nie. **Bežný používateľ ho nikdy nevidí** — neexistuje naňho odkaz, prehliadač ho nestiahne. Preto: kto si stiahol `robots.txt` ≈ robot. *(Toto je presne podstata úlohy 02.)*
> 2. **User-Agent string** — roboti sa väčšinou identifikujú: `Googlebot`, `bingbot`, kľúčové slová `bot`/`crawl`/`spider`. *(Úloha 03.)*
> 3. **Automatizované nástroje** — `curl`, `wget`, `libwww`, prázdny User-Agent (`-`). Nie sú to klasické vyhľadávače, ale ani ľudia v prehliadači — typicky scrapery, monitorovacie skripty. *(Úloha 03.)*

**Cieľ:** Nájsť IP adresy robotov, ktorí pristúpili k `robots.txt`.

**Logika:** `robots.txt` je inštrukčný súbor pre vyhľadávacie roboty. Bežných používateľov tento súbor nezaujíma. Preto **každá IP, ktorá si stiahla `robots.txt`, je takmer určite robot**.

**Vstup:** `in/wm2020projekt_studeny.log`
**Výstup:** `out/02_robot_ips.csv`

#### Algoritmus

```python
for line in f:
    # rýchly substring filter (regex je drahší)
    if "robots.txt" not in line.lower():
        continue

    m = pattern.match(line)
    if m and "robots.txt" in m.group(4).lower():    # group 4 = URL
        rows.append({"IP": m.group(1)})
```

#### Výsledok

```log
Záznamy s robots.txt:    2 354
Unikátnych IP:             250
```

---

### Úloha 03 — Filter robotov

**Cieľ:** Z očisteného logu (úloha 01) odstrániť prístupy robotov.

**Vstup:** `in/01_cleaned_log.csv` + `in/02_robot_ips.csv`
**Výstup:** `out/03_cleaned_log.csv`

#### 4 filtre spustené postupne

```python
# 1. Boti podľa User-Agent
bot = df["Agent"].str.contains(r"bot|crawl|spider", case=False, na=False)
df = df[~bot]

# 2. Automatizované skripty
auto = df["Agent"].str.contains(r"cron|curl|wget|libwww|ltx71", case=False, na=False)
df = df[~auto]

# 3. Prázdne User-Agent
df = df[df["Agent"] != "-"]

# 4. Robot IP adresy z úlohy 02
df = df[~df["IP"].isin(robot_ips)]
```

#### Výsledok pri každom kroku

```log
Načítané:                                    211 313
Po odstránení botov (bot|crawl|spider):      154 333    (-27%)
Po odstránení automatizovaných skriptov:      95 096
Po odstránení prázdnych agentov:              78 592
Po odstránení robot IP:                       73 927    (-65% celkom)
```

---

### Úloha 04 — Obdobie + UNIXTIME

> **📚 Prečo UNIX timestamp?** Časový reťazec `"17/Dec/2017:06:28:17 +0100"` je čitateľný pre človeka, ale ťažko sa s ním počíta. Koľko sekúnd je medzi `06:28:17` a `06:30:42`? Treba parsovať dni, mesiace, časové zóny, riešiť polnoc/mesiace.
>
> **UNIX timestamp** rieši elegantne: **jediné celé číslo** = počet sekúnd od **1.1.1970 00:00:00 UTC** (tzv. „epoch" — arbitrárny štartovací bod, ktorý si zvolil UNIX).
>
> ```
> "17/Dec/2017:06:28:17 +0100"  →  1 513 488 497
> "17/Dec/2017:06:30:42 +0100"  →  1 513 488 642
>                                   ────────────────
>                                   rozdiel = 145 sekúnd
> ```
>
> **Výhody:**
> - jedno číslo, jednoduchá aritmetika (`t2 - t1` = rozdiel v sekundách)
> - nezávislé od časovej zóny *(vždy v UTC pod kapotou)*
> - menšie číslo = skorší čas → ľahké triedenie
>
> Bez UNIXTIME by sme úlohu 06 (`Length`) museli robiť cez `datetime` knižnicu pri každom rozdiele. S UNIXTIME je to obyčajné odčítanie.

**Cieľ:** Filter na pridelené obdobie + vytvorenie premennej `UNIXTIME`.

**Vstup:** `in/03_cleaned_log.csv`
**Výstup:** `out/04_obdobie.csv`

#### Filter

```python
mask = (
    df["DateTime"].str.startswith("17/Dec/2017") |
    df["DateTime"].str.startswith("18/Dec/2017") |
    df["DateTime"].str.startswith("19/Dec/2017") |
    df["DateTime"].str.startswith("20/Dec/2017") |
    df["DateTime"].str.startswith("21/Dec/2017") |
    df["DateTime"].str.startswith("22/Dec/2017") |
    df["DateTime"].str.startswith("23/Dec/2017")
)
df = df[mask]
```

#### Konverzia na UNIXTIME

```python
def to_unixtime(dt_str):
    # "17/Dec/2017:06:28:17 +0100"
    parts = dt_str.split(":")
    date_part = parts[0]
    hour, minute = int(parts[1]), int(parts[2])
    second = int(parts[3].split(" ")[0])
    day, month_str, year = date_part.split("/")
    return datetime.datetime(
        int(year), months[month_str], int(day), hour, minute, second
    ).timestamp()

df["UNIXTIME"] = df["DateTime"].apply(to_unixtime)
```

#### Výsledok

```log
Po filtrovaní na 17.-23.12.2017: 73 927 riadkov

Príklad:
                     DateTime      UNIXTIME
0  17/Dec/2017:06:28:17 +0100  1.513488e+09
1  17/Dec/2017:06:28:17 +0100  1.513488e+09
2  17/Dec/2017:06:28:19 +0100  1.513488e+09
```

---

### Úloha 05 — Identifikácia používateľov

> **📚 Fundamentálny problém:** HTTP je **bezstavový protokol** — server nevie, či 2 požiadavky prišli od toho istého človeka, alebo od dvoch rôznych. Toto rieši aj Facebook či Google, nielen my.
>
> **4 prístupy zoradené od najslabšieho po najsilnejší:**
>
> | Metóda | Presnosť | Slabina |
> |--------|----------|---------|
> | iba IP | ⭐ | NAT (firma/internát/hotspot) zdieľa jednu IP medzi 100+ ľuďmi; DHCP mení IP po reštarte routra |
> | **IP + User-Agent** | ⭐⭐⭐ | **náš prípad** — kompromis: dvaja ľudia za NAT zvyčajne nemajú úplne rovnaký prehliadač/OS |
> | Cookies | ⭐⭐⭐⭐ | funguje aj pri zmene IP, ale Apache log štandardne nelogovacuje cookies |
> | Login | ⭐⭐⭐⭐⭐ | najpresnejšie, ale len pre prihlásených |
>
> **Slabosti IP + Agent:**
> - jeden človek s viacerými prehliadačmi = **viac userov** *(Chrome aj Firefox)*
> - dvaja ľudia s úplne rovnakým prehliadačom za NAT = **jeden user**
>
> V Apache logu **nemáme cookies**, takže IP+Agent je maximum, ktoré z neho vieme dostať.

**Cieľ:** Prideliť `USER_ID` každej unikátnej kombinácii `(IP, Agent)`.

**Vstup:** `in/04_obdobie.csv`
**Výstup:** `out/05_users.csv`

#### Algoritmus

```python
# 1. Sort: záznamy jedného usera za sebou, chronologicky
df = df.sort_values(by=["IP", "Agent", "UNIXTIME"]).reset_index(drop=True)

# 2. groupby + ngroup: každá unikátna dvojica (IP, Agent) = USER_ID
df["USER_ID"] = df.groupby(["IP", "Agent"]).ngroup() + 1
```

#### Príklad

```log
IP=1.2.3.4, Agent=Chrome  →  ngroup=0  →  USER_ID=1
IP=1.2.3.4, Agent=Firefox →  ngroup=1  →  USER_ID=2  (iný prehliadač = iný user)
IP=5.6.7.8, Agent=Chrome  →  ngroup=2  →  USER_ID=3
```

#### Výsledok

```log
Počet identifikovaných používateľov: 14 563
```

---

### Úloha 06 — Premenná Length

> **📚 Length = aproximácia času na stránke.** Apache log neobsahuje „čas strávený na stránke" — server nevie, kedy užívateľ z nej odíde *(odíde, keď zavrie tab alebo klikne inde, server o tom nedostane signál)*. Aproximujeme to **rozdielom medzi 2 po sebe idúcimi prístupmi toho istého usera**:
>
> ```
> Length[i] = UNIXTIME[i] - UNIXTIME[i-1]   (predchádzajúci prístup toho istého USER_ID)
> ```
>
> Posledný prístup usera nemá nasledovníka → `Length` neznáme. *(V projekte to počítame cez `shift(1)`, takže `NaN` má prvý prístup, ale výsledok je ekvivalentný — jeden záznam na okraji.)*
>
> **60-minútové STT (Session Timeout Threshold)** je heuristika: ak je medzi 2 prístupmi viac ako 60 min, určite ide o iné sedenie a `Length` je neplatné *(`None`)*. Bez tohto by sme mali „stránku, na ktorej užívateľ strávil 8 hodín — od piatka do soboty rána".

**Cieľ:** Pre každý záznam vypočítať čas strávený na stránke.

**Vzorec:**
```
Length[i] = UNIXTIME[i] - UNIXTIME[i-1]   (v rámci toho istého usera)
```

**Pravidlá podľa zadania (60-min STT):**
- Prvý záznam usera nemá predchodcu → `Length = NaN`
- Ak `Length >= 3600s` (60 min) → `Length = None` *(user pravdepodobne odišiel)*

**Vstup:** `in/05_users.csv`
**Výstup:** `out/06_length.csv`

#### Algoritmus

```python
# predchádzajúci čas v rámci toho istého usera
df["PREV_UNIXTIME"] = df.groupby("USER_ID")["UNIXTIME"].shift(1)

# Length = aktuálny - predchádzajúci
df["Length"] = df["UNIXTIME"] - df["PREV_UNIXTIME"]

# 60-min STT
df.loc[df["Length"] >= 3600, "Length"] = None
```

#### Príklad výpočtu pre jedného usera

```log
UNIXTIME:      [100, 110, 125, 4000, 4030]
shift(1):      [NaN, 100, 110,  125, 4000]
                ─────────────────────────
Length:        [NaN,  10,  15, 3875,   30]
                                  ↓
                          >= 3600 → None
                ─────────────────────────
Final Length:  [NaN,  10,  15, None,   30]
```

#### Štatistiky

```log
Priemer Length:  173.59 s   (~3 minúty)
Median Length:     5.00 s
```

---

### Úloha 07 — Sedenia RLength (s STT_Q fallbackom)

> **📚 Sedenie (session)** = súvislá séria prístupov **jedného usera** v krátkom časovom okne, kde aktívne navigoval. Príklad jedného usera za týždeň:
> ```
> Po 09:00 — 5 stránok (10 min)        ← sedenie 1
> Po 14:00 — 3 stránky (5 min)         ← sedenie 2
> St 20:30 — 12 stránok (25 min)       ← sedenie 3
> ```
> 1 user, 3 sedenia. HTTP nedáva žiadny signál „sedenie skončilo" — musíme ho odhadnúť.

**Cieľ:** Identifikovať sedenia metódou Reference Length s `p = 40%`.

#### Teória RLength

> **📚 Predpoklad:** `Length` (čas medzi navigačnými klikmi) má **exponenciálne rozdelenie**.
>
> Predstav si, že stojíš na zastávke a meriaš čas medzi príchodmi autobusov. Ak prichádzajú náhodne a nezávisle, časy majú **exponenciálne rozdelenie**:
> ```
> f(t) = λ · e^(-λ·t)         pre t ≥ 0
> ```
> Vlastnosti:
> - `t = 0` má **najvyššiu hustotu** → krátke pauzy sú najčastejšie
> - hustota postupne klesá → dlhé pauzy sú zriedkavé
> - **priemer** = `1/λ`
>
> Pri navigácii to dáva zmysel: veľa krátkych pauz *(klikol, hneď klikol ďalej — preletel cez navigáciu)*, málo dlhých *(zastavil sa a čítal)*.
>
> **Vzorec RLength** = `p`-tý percentil exponenciálneho rozdelenia s priemerom `μ`:
> ```
> RLength = -ln(1 - p) · μ
> ```

```
RLength = -ln(1 - p) × mean(Length)
```

Pre `p = 0.4`:
```
-ln(1 - 0.4) = -ln(0.6) ≈ 0.5108
RLength ≈ 0.51 × priemer
```

> **📚 Význam:** ak `p = 0.4`:
> - 40 % záznamov má `Length < RLength` → **navigačné stránky** *(rýchlo preklikol)*
> - 60 % má `Length ≥ RLength` → **content stránky** *(zostal a čítal)*
>
> Predpoklad zadania: koniec sedenia = dlhá pauza → ak `Length ≥ RLength`, ide o nové sedenie.

#### KS test (Kolmogorov-Smirnov)

> **📚 Čo robí KS test?** Odpovedá na otázku: **„Sú tieto dáta z konkrétneho rozdelenia?"**
>
> Princíp: porovná **empirickú distribučnú funkciu** *(ako vyzerá histogram dát)* s **teoretickou** *(napr. exponenciálnou)*. Vypočíta **maximálnu vertikálnu vzdialenosť** medzi týmito dvoma krivkami → **KS štatistika `D`**.
>
> ```
> p-hodnota = pravdepodobnosť, že by sme videli také alebo extrémnejšie D,
>             keby H₀ bola pravda
> ```
>
> ak `p < 0.05` → **zamietame H₀** *(dáta z toho rozdelenia nie sú)*

| Hypotéza | Význam |
|----------|--------|
| **H₀** | Length má exponenciálne rozdelenie |
| **H₁** | Length nemá exponenciálne rozdelenie |

Ak `p_value < 0.05` → zamietame H₀ → **fallback na STT_Q**.

> **📚 Prečo zlyhal KS test v projekte?** Reálny webový log je „špinavý":
> - Roboti, ktorí zostali napriek čisteniu, klikajú **perfektne pravidelne** *(nie exponenciálne)*.
> - Ľudia majú „preferované" pauzy *(2–10 s pri scrollovaní článku)* — to tvorí **lokálne maximá** v histograme. Exp. rozdelenie má lokálne maximum **iba na nule**.

#### Fallback STT_Q (kvartilový)

> **📚 Kvartily** delia zoradené dáta na štvrtiny:
> - **Q1** (25. percentil) — pod ním je 25 % hodnôt
> - **Q2** (median, 50. percentil)
> - **Q3** (75. percentil) — pod ním je 75 % hodnôt
>
> **IQR (Inter-Quartile Range)** = `Q3 − Q1` = šírka strednej polovice dát.
>
> **Pravidlo `Q3 + 1.5 × IQR`** je tradičná hranica „miernych outlierov" v boxplote — nad ňou sa kreslia jednotlivé bodky. Empiricky sa zhoduje s tým, čo intuitívne nazveme „neobvykle veľká hodnota".
>
> V STT_Q to interpretujeme: **neobvykle dlhá pauza medzi 2 prístupmi → nové sedenie**.

```
STT_Q = Q3 + 1.5 × IQR
IQR = Q3 - Q1
```

Robustnejší voči outlierom, štandardná hranica miernych outlierov v boxplote.

> **📚 Prečo robustný?** Outlieri *(roboti s 3-hodinovými pauzami)* **nemenia Q1 a Q3** — menia iba „konce" rozdelenia, ktoré nie sú v kvartiloch. **Priemer** by tieto outlieri vychýlili smerom hore, takže metóda založená na priemere by bola voči nim citlivá.

#### Algoritmus

```python
# KS test
ks_stat, p_value = kstest(length_data, "expon", args=(0, mean_length))

if p_value >= 0.05:
    # data MAJÚ exp. rozdelenie
    prah = -np.log(1 - 0.4) * mean_length     # RLength
else:
    # fallback STT_Q
    q3 = length_data.quantile(0.75)
    iqr = q3 - length_data.quantile(0.25)
    prah = q3 + 1.5 * iqr                      # STT_Q

# označenie nových sedení
df["NEW_SESSION"] = (df["Length"].isna()) | (df["Length"] >= prah)

# globálne SESSION_ID pomocou cumsum na boolean
df["SESSION_ID"] = df["NEW_SESSION"].cumsum()
```

#### Výsledok v projekte

```log
KS štatistika:    0.5985
P-hodnota:        0.000000  (< 0.05)

→ data NEMAJÚ exponenciálne rozdelenie
→ POUŽILA SA METÓDA STT_Q
→ prah: Q3 + 1.5×IQR = 31.0 + 1.5×30.0 = 76.0 sekúnd

Počet sedení: 33 496
```

#### Vysvetlenie cumsum

`cumsum()` na boolean stĺpci treats `False=0, True=1` a kumulatívne sčíta:

```log
NEW_SESSION:  [True, False, False, True, False, True]
            =   1     0      0     1      0     1
cumsum:       [  1,    1,     1,    2,     2,    3]    ← SESSION_ID
```

---

### Úloha 08 — Sedenia h-ref

> **📚 h-ref (heuristic referrer)** používa **iný princíp** ako RLength. Zatiaľ čo RLength sa pozerá iba na čas, h-ref kombinuje **čas + odkiaľ user prišiel**.
>
> **3 podmienky pre nové sedenie** *(stačí jedna — OR)*:
> 1. **`Length` je NaN** — prvý záznam usera, nemá predchodcu
> 2. **`Length ≥ priemer`** — pauza dlhšia ako priemerná
> 3. **`Referrer = "-"`** — užívateľ otvoril stránku **priamo** *(napadol URL, otvoril záložku, prišiel z externého zdroja, ktorý nepošle Referrer)*
>
> **3. podmienka je kľúčová.** Aj keď čas nehovorí o novej návšteve, prázdny Referrer signalizuje „začiatok niečoho nového" — preto h-ref typicky tvorí **viac, kratších sedení** ako STT_MEAN/STT_Q/RLength.
>
> **Rozdiel vs. STT_MEAN:** STT_MEAN = iba čas (prah = priemer). h-ref = STT_MEAN **+ kontextová podmienka** na Referrer.

**Cieľ:** Identifikovať sedenia metódou h-ref (heuristic referrer).

**Vstup:** `in/06_length.csv`
**Výstup:** `out/08_sedenia_href.csv`

#### Logika h-ref

Časové okno = `priemer Length` *(rovnako ako STT_MEAN)*.

Nové sedenie ak (OR — stačí jedna podmienka):
- `Length` je `NaN` *(prvý záznam usera)*
- `Length >= priemer` *(prekročený časový limit)*
- `Referrer == "-"` *(priamy/externý prístup)*

#### Algoritmus

```python
mean_length = df["Length"].mean()

df["NEW_SESSION"] = (
    (df["Length"].isna())
    | (df["Length"] >= mean_length)
    | (df["Referrer"] == "-")
)
df["SESSION_ID"] = df["NEW_SESSION"].cumsum()
```

#### Výsledok

```log
Časové okno (priemer Length): 173.59 s

Počet sedení: 46 693    (viac než RLength — 3. podmienka rozdeľuje aj kratšie pauzy)
```

---

### Úloha 09 — Doplnenie ciest pre RLength

> **📚 Prečo v logu chýbajú stránky?** Apache log je **server-side** záznam. Niekedy sa stránka užívateľovi zobrazí **bez toho, aby server o tom vedel**:
>
> 1. **Browser cache.** Prehliadač si pamätá nedávno navštívené stránky. Keď klikneš „späť", prehliadač zobrazí stránku z lokálnej cache → **žiadny request → žiadny záznam v logu**.
> 2. **Sieťové problémy.** Request sa stratí, server log nezachytí, klient stránku nakoniec dostane *(z cache, retry…)*.
> 3. **Multi-tab navigácia.** User otvorí stránku v novom tabe (Ctrl+klik) — pôvodný tab zostane, log môže zachytiť požiadavky v zvláštnom poradí.
>
> **Dôsledok pre WUM:** v sekvencii prístupov sú „diery". Pravidlá ako „A → C" v skutočnosti znamenajú „A → B → C", kde B chýba. To skresľuje fázu 2 (asociačné/sekvenčné pravidlá).
>
> **Riešenie:** rekonštruujeme chýbajúce kroky pomocou **mapy webu** (graf `parent[B] = A`, ktorý hovorí „bežne sa na B chodí z A"). Pri „skoku" v sedení vložíme medzi `URL[i]` a `URL[i+1]` ich pravdepodobnú medzistránku `parent[URL[i+1]]`.

**Cieľ:** Doplniť chýbajúce medzistránky v navigačných cestách.

#### Princíp

Štandardná navigácia: prehliadač posiela `Referrer=A, URL=B` → mapa webu má `parent[B] = A`.

Niekedy v logu chýba *medzistránka* — user sa dostane z A na C bez logu pre B *(napr. cez browser cache)*.

#### Mapa webu

V projekte **nemáme** externú mapu (Excel ako v cv3). Vybudujeme ju **zo samotného logu**:

```python
# (a) všetky páry (Referrer, URL)
mapa_df = df[["Referrer", "URL"]].copy()
mapa_df["ref_path"] = mapa_df["Referrer"].apply(url_to_path)

# (b) iba interné odkazy (Referrer obsahuje "ukf.sk")
mapa_df = mapa_df[mapa_df["Referrer"].str.contains("ukf.sk", case=False, na=False)]

# (c) pre každé URL → najčastejší referrer = "kanonický" rodič
parent_series = mapa_df.groupby("URL")["ref_path"].agg(
    lambda x: x.value_counts().idxmax()
)
parent = parent_series.to_dict()
map_paths = set(parent.keys())
```

#### Algoritmus doplnenia

```python
for i, curr in enumerate(records):
    new_rows.append(curr)
    next_row = records[i + 1]

    if curr["SESSION_ID"] != next_row["SESSION_ID"]:
        continue

    url_from = curr["URL"]
    url_to = next_row["URL"]

    # KĽÚČOVÁ PODMIENKA: doplň ak url_from nie je v mape ale url_to je
    if url_from not in map_paths and url_to in map_paths:
        ref_page = parent.get(url_to)
        if ref_page and ref_page != url_from:
            doplneny = curr.copy()
            doplneny["URL"] = ref_page    # NOVÁ skutočná URL!
            new_rows.append(doplneny)
```

#### Príklad

```log
PRED:
  SESSION_ID=5, URL=/uvod        (Referrer: -)
  SESSION_ID=5, URL=/clanok-42   (Referrer: /blog)   ← /blog tu chýba!

PO doplnení:
  SESSION_ID=5, URL=/uvod
  SESSION_ID=5, URL=/blog        ← DOPLNENÉ (parent[/clanok-42] = /blog)
  SESSION_ID=5, URL=/clanok-42
```

#### Výsledok

```log
Stránok v mape webu (postavená z logu):  3 141
Doplnených záznamov:                      4 032
Celkový počet záznamov:                  77 959
```

---

### Úloha 10 — Doplnenie ciest pre h-ref

Logika identická s úlohou 09, len pracuje nad sedeniami h-ref.

#### Výsledok

```log
Doplnených záznamov:        139
Celkový počet záznamov:  74 066
```

**Prečo o toľko menej než pre RLength?**

h-ref má **viac sedení** (46k) ale **kratších**. Krátke sedenia majú **málo skokov** v navigácii, takže menej párov potrebuje doplnenie. RLength má naopak menej, ale dlhších sedení s viac skokmi.

---

## Metodológia — prehľad metód

> Hlbšiu teóriu (HTTP protokol, UNIX timestamp, identifikácia užívateľa, exponenciálne rozdelenie, KS test, IQR, doplnenie ciest) nájdeš **inline pri každej úlohe** v sekcii „Detailný popis úloh 00–10". Tu sú len súhrnné tabuľky pre rýchlu referenciu.

### Identifikácia používateľov — prehľad metód

| Metóda | Presnosť | Komentár |
|--------|----------|----------|
| Iba IP | ⭐ | NAT / DHCP / mobilné siete zdieľajú IP |
| **IP + User-Agent** | ⭐⭐⭐ | **kompromis — používame** |
| Cookies | ⭐⭐⭐⭐ | presné, ale Apache log ich nelogovacuje |
| Login | ⭐⭐⭐⭐⭐ | najpresnejšie, len pre prihlásených |

### Identifikácia sedení — prehľad metód

| Metóda | Vzorec / podmienka | Charakteristika |
|--------|-------------------|-----------------|
| STT_MEAN | prah = priemer Length | jednoduchá, na priemere |
| **STT_Q** | prah = `Q3 + 1.5×IQR` | **robustná, neparametrická, fallback** |
| SLength | prah = pevné 10 min | statická, bez prispôsobenia dátam |
| **RLength** | prah = `-ln(1-p) × priemer` | **štatistická, predpoklad exp. rozdelenia, p = 40 %** |
| **h-ref** | čas **+** `Referrer = "-"` | **heuristická, kombinuje čas a kontext** |

### Celý WUM rámec

```
SUROVÝ APACHE LOG (47 M riadkov)
   │
   │  fáza 1: Data preparation  ← NÁŠ PROJEKT
   │  ┌───────────────────────────────────────┐
   │  │  • čistenie šumu  (statika, neúspechy)│
   │  │  • odstránenie robotov                │
   │  │  • UNIX timestamp                     │
   │  │  • USER_ID  (IP + Agent)              │
   │  │  • Length  (60-min STT)               │
   │  │  • SESSION_ID  (RLength / h-ref)      │
   │  │  • doplnenie ciest                    │
   │  └───────────────────────────────────────┘
   │
   ↓
ČISTÝ DATASET S OZNAČENÝMI SEDENIAMI
   │
   │  fáza 2: Pattern discovery  (mimo projektu)
   │  • asociačné pravidlá  (FP-growth, Apriori)
   │  • sekvenčné pravidlá  (PrefixSpan)
   │
   ↓
NÁJDENÉ VZORY
   │
   │  fáza 3: Pattern analysis  (mimo projektu)
   │  • štatistické testy
   │  • interpretácia, vizualizácia
   │
   ↓
INSIGHT  (napr. „kto navštívi /admissions, často skončí na /tuition-fees")
```

Každý krok fázy 1 je **nutnou prípravou** pre fázy 2 a 3. Bez čistenia by vzory boli skreslené robotmi; bez sedení by sa hľadali cesty cez týždne; bez doplnenia ciest by mali pravidlá medzery.

<!-- BEGIN_REMOVED_DEEP_THEORY
Hlboký teoretický blok bol presunutý k jednotlivým úlohám 00–10 (sekcia „Detailný popis úloh"). Pôvodný text zostáva len v gite cez históriu commitov, aby tento dokument zostal kompaktnejší.
END_REMOVED_DEEP_THEORY -->

### Pôvodný hlboký teoretický blok (skrytý — kvôli kompaktnosti)

<details>
<summary>Rozkliknúť pre kompletnú samostatnú teóriu</summary>

#### 1. Od Data Mining k Web Usage Mining

**Data Mining** je proces hľadania netriviálnych, doteraz neznámych a potenciálne užitočných vzorov v dátach. Klasický príklad: supermarket analyzuje, ktoré produkty sa kupujú spolu — z toho vznikajú **asociačné pravidlá** typu *"kto kúpi pivo, kúpi aj plienky"*.

Keď sa Data Mining aplikuje na dáta z webu, hovoríme o **Web Mining**. Ten sa delí na 3 vetvy:

| Vetva | Vstup | Príklad |
|-------|-------|---------|
| **Web Content Mining** | obsah stránok (HTML, text) | analýza sentimentu, klasifikácia článkov |
| **Web Structure Mining** | hyperlinkový graf medzi stránkami | PageRank (Google), autority a huby |
| **Web Usage Mining (WUM)** | **logy návštev** | **náš projekt** |

**WUM študuje, ako sa ľudia po webe pohybujú** — nie *čo* je na stránkach, ale *ako* ich používajú. Otázky typu:
- Ktoré stránky vedú k nákupu / odchodu?
- Aké sú typické navigačné cesty?
- Ako kategorizovať návštevníkov podľa ich správania?

WUM sa formálne delí na **3 fázy**:

| Fáza | Popis | Naše úlohy |
|------|-------|------------|
| 1. **Data preparation** | čistenie, identifikácia userov a sedení, doplnenie ciest | **úlohy 01–10 (celý projekt)** |
| 2. Pattern discovery | hľadanie vzorov — asociačné a sekvenčné pravidlá | mimo projektu |
| 3. Pattern analysis | interpretácia, štatistické testy, sumarizácia | mimo projektu |

Náš projekt pokrýva **len fázu 1**. To nie je "iba prípravná práca" — typicky tvorí **60–80 % času** celého WUM procesu, lebo z chaotického surového logu treba vyrobiť čisté, dobre označkované dáta.

---

### 2. HTTP protokol — čo sa vlastne loguje

Keď v prehliadači klikneš na odkaz, prebehne tento dialóg medzi tvojím počítačom (klient) a serverom:

```
KLIENT → SERVER:  GET /index.html HTTP/1.1
                  Host: www.ukf.sk
                  User-Agent: Mozilla/5.0 (Windows NT 10.0; ...)
                  Referer: https://www.google.com/

SERVER → KLIENT:  HTTP/1.1 200 OK
                  Content-Type: text/html
                  Content-Length: 12345

                  <html>...</html>
```

**Apache** *(jeden z najrozšírenejších webových serverov)* zapisuje každý takýto dialóg do textového súboru — tzv. **prístupového logu (access log)**. **Jeden riadok = jedna HTTP požiadavka.**

#### Čo znamenajú jednotlivé polia

| Pole | Význam |
|------|--------|
| **IP** | sieťová adresa klienta *(môže ju zdieľať viac ľudí cez NAT)* |
| **DateTime** | kedy server prijal požiadavku |
| **Method** | typ HTTP operácie: `GET` (čítanie), `POST` (odoslanie formulára), `HEAD` (iba hlavičky) |
| **URL** | čo si klient pýta |
| **StatusCode** | ako server odpovedal: `2xx` úspech, `3xx` presmerovanie, `4xx` chyba klienta, `5xx` chyba servera |
| **Bytes** | koľko dát server poslal |
| **Referrer** | z ktorej stránky klient prišiel *(odkiaľ klikol)* |
| **User-Agent** | identifikácia prehliadača a zariadenia |

> **Dôležité:** Apache log je **pasívny záznam**. Server iba zapisuje, čo sa stalo. **Nevidí**, čo užívateľ na stránke skutočne robí — scrolling, čas čítania, kliky na nelinkované elementy. Vidí len **požiadavky o ďalšiu stránku alebo súbor**. Toto je fundamentálne obmedzenie WUM zo serverového logu.

---

### 3. Šum v logu — prečo musíme čistiť (úlohy 01–03)

Apache log obsahuje veľa záznamov, ktoré nevypovedajú o navigácii ľudského užívateľa:

#### a) Statické súbory
Keď načítaš HTML stránku, prehliadač automaticky vyžiada **všetky** obrázky, CSS, JS, fonty. Ak má stránka 30 obrázkov, **jedna návšteva = 31 záznamov v logu** (1 HTML + 30 obrázkov). Keby sme to nezahodili, štatistiky by boli skreslené (priemerný "počet stránok na sedenie" by bol 30× nadhodnotený).

#### b) Neúspešné a technické požiadavky
- `4xx` (napr. 404 — stránka neexistuje) a `5xx` (chyba servera) **nepatria** k reálnej navigácii.
- `POST` je odoslanie formulára *(nie navigácia, ale akcia)*.
- `HEAD` si vyžaduje iba metadáta — používajú prevažne skripty.

Ponechávame iba `GET` so statusom `2xx`/`3xx`.

#### c) Roboti
Vyhľadávacie služby (Google, Bing, Seznam) majú **crawlery** — programy, ktoré automaticky prechádzajú web a indexujú stránky. Pre WUM sú **nežiaduce**, lebo skreslia metriky *(„Googlebot navštívil 10 000 stránok za hodinu")*.

3 spôsoby, ako poznáme robota:

##### `robots.txt`
Súbor v koreni domény *(napr. `www.ukf.sk/robots.txt`)*, ktorý hovorí robotom, kam smú a kam nie. **Bežný používateľ tento súbor nikdy nevidí** — neexistuje naňho odkaz, prehliadač ho automaticky nestiahne. Preto: **kto si stiahol `robots.txt`, je takmer určite robot.** Toto je základ úlohy 02.

##### User-Agent string
Roboti sa zvyčajne *(ale nie vždy — pretvarujú sa)* identifikujú v User-Agent. Hľadáme kľúčové slová: `bot`, `crawl`, `spider`. Príklady:
```
Googlebot/2.1 (+http://www.google.com/bot.html)
Mozilla/5.0 (compatible; bingbot/2.0; +http://www.bing.com/bingbot.htm)
```

##### Automatizované nástroje
`curl`, `wget`, `libwww`, skripty s prázdnym Agentom *(`-`)* — nie sú to klasické vyhľadávače, ale ani ľudia v prehliadači. Ide o monitorovacie nástroje, scrapery, custom skripty.

---

### 4. Reprezentácia času — UNIX timestamp (úloha 04)

Časový reťazec `"17/Dec/2017:06:28:17 +0100"` je čitateľný pre človeka, ale **ťažko sa s ním počíta**. Koľko sekúnd je medzi `"17/Dec/2017:06:28:17"` a `"17/Dec/2017:06:30:42"`? Treba parsovanie, dní, mesiacov, časových zón…

**UNIX timestamp** problém rieši elegantne: **jediné celé číslo** = počet sekúnd od **1.1.1970 00:00:00 UTC** *(tzv. „epoch" — arbitrárny štartovací bod, ktorý si UNIX zvolil)*.

```
"17/Dec/2017:06:28:17 +0100"  →  1 513 488 497
"17/Dec/2017:06:30:42 +0100"  →  1 513 488 642
                                 ────────────────
                                 rozdiel = 145 sekúnd
```

Výhody:
- **jedno číslo, jednoduchá aritmetika** — `t2 - t1` je rozdiel v sekundách
- **nezávislé od časovej zóny** *(vždy v UTC)*
- **ľahko porovnateľné** — menšie číslo = skorší čas
- **vhodné pre databázy a triedenie**

Bez UNIXTIME by sme úlohu 06 (premenná `Length`) museli robiť cez `datetime` knižnicu pri každom rozdiele. S UNIXTIME je to jednoduchá `subtraction`.

---

### 5. Identifikácia používateľa — fundamentálny problém (úloha 05)

HTTP je **bezstavový protokol** — server nevie, či 2 požiadavky pochádzajú od toho istého človeka alebo od dvoch rôznych. Toto je problém aj pre Facebook/Google, nielen pre nás.

Riešenia, zoradené od najslabšieho po najsilnejšie:

#### a) Iba IP adresa
Najjednoduchšie, ale **nepresné**:
- **NAT (Network Address Translation):** celá firma / internát / WiFi hotspot **zdieľa jednu verejnú IP**. Možno 100+ ľudí.
- **DHCP:** doma sa IP mení po reštarte routra — jeden človek dostane viac IP za týždeň.
- **Mobilné siete:** carrier-grade NAT zdieľa IP medzi tisíckami zariadení.

#### b) IP + User-Agent (**náš prípad**)
Dvaja ľudia za jednou IP zvyčajne **nemajú úplne rovnaký User-Agent** (iný prehliadač, iná verzia, iný OS). Kompromis: **lepšie ako iba IP, horšie ako cookies.**

```
IP=147.175.1.5, Agent="Chrome 84.0 Win10"  → user A
IP=147.175.1.5, Agent="Firefox 78 macOS"   → user B  (iný človek)
```

Slabosti:
- jeden človek s viacerými prehliadačmi = **viac userov**
- dvaja ľudia s **úplne** rovnakým prehliadačom za NAT = **jeden user**

#### c) Cookies
Server pošle pri prvej návšteve unikátny token, prehliadač ho vracia s každou ďalšou požiadavkou. Funguje aj cez zmenu IP. Ale: užívateľ môže cookies vymazať alebo zakázať.

#### d) Prihlásenie
Najpresnejšie — server vie konkrétneho používateľa. Funguje ale len pre prihlásených.

| Metóda | Presnosť | Komentár |
|--------|----------|----------|
| Iba IP | ⭐ | NAT môže mať 100+ ľudí |
| **IP + User-Agent** | ⭐⭐⭐ | **kompromis — používame v projekte** |
| Cookies | ⭐⭐⭐⭐ | presné, ale nelogujú sa štandardne |
| Login | ⭐⭐⭐⭐⭐ | najpresnejšie, len pre prihlásených |

V Apache logu **nemáme cookies** *(štandardne sa nelogujú)*, takže IP+Agent je **maximum, čo z neho vieme dostať**.

---

### 6. Sedenie (session) — čo to vlastne je (úlohy 07–08)

**Sedenie** = súvislá séria prístupov **jedného užívateľa** v **krátkom časovom okne**, kde užívateľ aktívne navigoval.

Príklad jedného usera za týždeň:
```
Pondelok 09:00 — pozeral 5 stránok (10 minút)            ← sedenie 1
Pondelok 14:00 — pozeral 3 stránky (5 minút)             ← sedenie 2
Streda    20:30 — pozeral 12 stránok (25 minút)          ← sedenie 3
```

Jeden user, **3 rôzne sedenia**. Bez delenia by sme mali "dlhú nepretržitú cestu po webe" — to nereprezentuje skutočné správanie *(užívateľ medzitým spal, pracoval, žil)*.

#### Prečo je delenie sedení ťažké?
HTTP nedáva **žiadny signál** typu "sedenie skončilo". Musíme to **odhadnúť** podľa nepriamych znakov:
- veľká pauza medzi prístupmi → asi nové sedenie
- prístup priamou URL *(bez referrera)* → asi nové sedenie
- ...

Toto je presne to, čo robia metódy **STT_MEAN, STT_Q, SLength, RLength, h-ref**.

#### Prehľad metód identifikácie sedení

| Metóda | Vzorec / podmienka | Charakteristika |
|--------|-------------------|-----------------|
| STT_MEAN | prah = priemer Length | jednoduchá, na priemere |
| **STT_Q** | prah = `Q3 + 1.5×IQR` | **robustná, neparametrická, fallback v projekte** |
| SLength | prah = pevné 10 minút | statická, bez prispôsobenia dátam |
| **RLength** | prah = `-ln(1-p) × priemer` | **štatistická, predpoklad exp. rozdelenia, p = 40%** |
| **h-ref** | čas **+** `Referrer = "-"` | **heuristická, kombinuje čas a kontext** |

---

### 7. Length — čas strávený na stránke (úloha 06)

Apache log **neobsahuje** "čas strávený na stránke" — server nevie, kedy užívateľ z nej odíde *(odíde, keď zavrie tab alebo klikne inde)*. **Aproximujeme to** rozdielom medzi 2 po sebe idúcimi prístupmi toho istého usera:

```
Length[i] = UNIXTIME[i+1] - UNIXTIME[i]
```

V projekte to počítame "spätne" cez `shift(1)` (predchádzajúci čas mínus aktuálny zlyhá, takže robíme aktuálny mínus predchádzajúci) → **prvý prístup usera nemá `Length`** (NaN).

#### 60-minútové STT (Session Timeout Threshold)
Heuristika: ak je medzi 2 prístupmi **viac ako 60 minút**, určite ide o iné sedenie a `Length` je neplatné *(nastavíme `None`)*. Bez tohto by sme mali "stránku, na ktorej užívateľ strávil 8 hodín — od piatka do soboty rána".

---

### 8. Štatistický základ RLength (úloha 07)

#### a) Exponenciálne rozdelenie

Predstav si, že stojíš na zastávke MHD a meriaš **čas medzi príchodmi autobusov**. Ak prichádzajú náhodne a nezávisle (Poissonov proces), časy medzi nimi sú **exponenciálne rozdelené**:

```
Hustota:  f(t) = λ · e^(-λt)         pre t ≥ 0
```

Vlastnosti, ktoré treba rozumieť:
- Hodnota `t = 0` má **najvyššiu hustotu** → **krátke pauzy sú najčastejšie**.
- Hustota **postupne klesá** → dlhé pauzy sú zriedkavé.
- **Priemer** = `1/λ`.
- **Bezpamätová** vlastnosť: pravdepodobnosť ďalšieho čakania nezávisí od toho, koľko si už čakal.

V WUM sa očakáva, že **`Length` (čas medzi navigačnými klikmi)** má podobný tvar:
- veľa krátkych pauz *(klikol, hneď klikol ďalej — preletel cez navigáciu)*
- málo dlhých pauz *(zastavil sa a čítal)*

#### b) Percentil exponenciálneho rozdelenia

Pre danú pravdepodobnosť `p` *(napr. 40 %)* hľadáme prah `t` taký, aby `P(Length ≤ t) = p`. Pre exponenciálne rozdelenie s priemerom `μ` platí:

```
t = -ln(1 - p) · μ
```

**Význam pre WUM:** ak `p = 0.4`, prah `t ≈ 0.51 · μ`. To znamená:
- **40 %** záznamov má `Length < t` → **navigačné stránky** *(rýchlo preklikol)*
- **60 %** záznamov má `Length ≥ t` → **content stránky** *(zostal a čítal)*

**Predpoklad zadania:** koniec sedenia je **dlhá pauza**. Ak `Length` prekročí prah, ide o nové sedenie.

#### c) Kolmogorov–Smirnov test (KS test)

KS test odpovedá na otázku: **„Sú tieto dáta z konkrétneho rozdelenia?"**

Princíp: porovná **empirickú distribučnú funkciu** *(ako vyzerá histogram dát)* s **teoretickou** *(napr. exponenciálnou)*. Vypočíta **maximálnu vertikálnu vzdialenosť** medzi týmito dvoma krivkami → **KS štatistika `D`**.

```
H₀: dáta pochádzajú z exponenciálneho rozdelenia
H₁: nepochádzajú

p-hodnota = pravdepodobnosť, že by sme videli také alebo extrémnejšie D,
            keby H₀ bola pravda

ak p < 0.05  →  zamietame H₀
```

**Náš výsledok:**
```
KS štatistika:  D = 0.5985    (obrovská odchýlka)
p-hodnota:        0.000000    (mizivá)
→ zamietame H₀: dáta NIE SÚ exponenciálne
```

**Prečo?** Reálny webový log je „špinavý":
- Roboti, ktorí zostali napriek čisteniu, klikajú **perfektne pravidelne** *(nie exponenciálne)*.
- Ľudia majú „preferované" pauzy *(typicky 2–10 s pri scrollovaní článku)*, čo tvorí **lokálne maximá** v histograme — exp. rozdelenie má lokálne maximum **iba na nule**.

Preto **fallback** na inú metódu — **STT_Q**.

#### d) STT_Q a kvartily

Ak nedôverujeme tvaru rozdelenia, použijeme **neparametrickú** metódu (= **bez predpokladu** o tvare).

**Kvartily** delia zoradené dáta na štvrtiny:
- **Q1** *(25. percentil)* — pod ním je 25 % hodnôt
- **Q2** *(median, 50. percentil)*
- **Q3** *(75. percentil)* — pod ním je 75 % hodnôt

**IQR (Inter-Quartile Range)** = `Q3 − Q1`. **Šírka strednej polovice dát.**

**Pravidlo `Q3 + 1.5 × IQR`** je **tradičná hranica „miernych outlierov"** v boxplote — nad ňou sa kreslia jednotlivé bodky. Empiricky sa zhoduje s tým, čo intuitívne nazveme „neobvykle veľká hodnota". *(Pre normálne rozdelenie zachytáva ~99 % dát; v iných rozdeleniach je to robustný kompromis.)*

V STT_Q to interpretujeme: **neobvykle dlhá pauza** medzi 2 prístupmi → **nové sedenie**.

```
Q1  = 1 s
Q3  = 31 s
IQR = 30 s
prah = 31 + 1.5 · 30 = 76 s
```

**Prečo je STT_Q robustné** *(a teda dobrý fallback)*: outlieri *(napr. roboti s 3-hodinovými pauzami)* **nemenia Q1 a Q3** — menia len „konce" rozdelenia, ktoré nie sú v kvartiloch. **Priemer (`μ`) by tieto outlieri vychýlili** smerom hore, takže metóda založená na priemere by bola voči outlierom citlivá.

---

### 9. h-ref — heuristic referrer (úloha 08)

Iná logika sedení, založená **nielen na čase**, ale aj na **odkiaľ** užívateľ prišiel.

**3 podmienky pre nové sedenie** *(ľubovoľná z nich)*:

1. **`Length` nedostupné** — prvý záznam usera (nemá predchodcu).
2. **`Length ≥ priemer`** — pauza dlhšia ako priemerná.
3. **`Referrer = "-"`** *(prázdny)* — užívateľ otvoril stránku **priamo** *(napadol URL, otvoril záložku, prišiel z externého zdroja, ktorý nepošle Referrer)*.

**3. podmienka je kľúčová:** aj keď čas nehovorí o novej návšteve, **prázdny Referrer signalizuje „začiatok niečoho nového"**. Preto h-ref typicky tvorí **viac, kratších sedení** ako STT_MEAN/STT_Q/RLength.

#### Rozdiel vs. STT_MEAN
- **STT_MEAN** = iba čas *(prah = priemer)*.
- **h-ref** = STT_MEAN + **kontextová podmienka** na Referrer.

---

### 10. Doplnenie ciest — prečo chýbajú stránky (úlohy 09–10)

Apache log je **server-side** záznam. Niekedy sa stránka zobrazí užívateľovi **bez toho, aby server o tom vedel**:

#### a) Browser cache
Prehliadač si pamätá nedávno navštívené stránky. Keď klikneš „späť", prehliadač zobrazí stránku **z lokálnej cache** → **žiadny request → žiadny záznam v logu**.

#### b) Sieťové problémy
Request sa stratí, server log nezachytí, ale klient stránku nakoniec dostane *(z cache, retry, …)*

#### c) Multi-tab navigácia
User otvorí stránku v novom tabe (Ctrl+klik). Pôvodný tab zostane otvorený, log môže zachytiť požiadavky v rôznom poradí, niektoré sa „preplietnu".

#### Príklad chýbajúcej stránky

```
Skutočná navigácia užívateľa:  /úvod  →  /blog  →  /článok-42

Apache log:
  /úvod         (Referrer: -)
  /článok-42    (Referrer: /blog)         ← /blog v logu CHÝBA, ale Referrer
                                              prezrádza, že tam bol!
```

#### Ako to opravujeme

1. **Postavíme „mapu webu"** zo všetkých `(Referrer → URL)` párov v logu. Pre každú URL nájdeme **najčastejší referrer** = **„kanonický rodič"**. *(V projekte mapu staviame z toho istého logu, pretože nemáme externý zdroj.)*
2. Pre každý susedný pár `(URL[i], URL[i+1])` v rámci sedenia skontrolujeme: **bol prechod priamy?** *(t. j. existuje hrana z `URL[i]` do `URL[i+1]` v mape?)*
3. Ak nie *(typicky `URL[i]` nie je v mape, ale `URL[i+1]` áno)*, **vložíme medzi ne kanonického rodiča `URL[i+1]`** — rekonštruujeme chýbajúci medzikrok.

Doplnené stránky sú **rekonštrukciou pravdepodobne navštívenej stránky**. Zlepšujú kvalitu vstupu pre **fázu 2** WUM (asociačné a sekvenčné pravidlá), ktoré inak môžu mať „diery" v cestách *(napr. pravidlo „A → C" namiesto skutočného „A → B → C")*.

---

### 11. Zhrnutie — celý rámec

```
SUROVÝ APACHE LOG (47 M riadkov)
   │
   │  fáza 1: Data preparation  ← NÁŠ PROJEKT
   │  ┌───────────────────────────────────────┐
   │  │  • čistenie šumu  (statika, neúspechy)│
   │  │  • odstránenie robotov                │
   │  │  • UNIX timestamp                     │
   │  │  • USER_ID  (IP + Agent)              │
   │  │  • Length  (60-min STT)               │
   │  │  • SESSION_ID  (RLength / h-ref)      │
   │  │  • doplnenie ciest                    │
   │  └───────────────────────────────────────┘
   │
   ↓
ČISTÝ DATASET S OZNAČENÝMI SEDENIAMI
   │
   │  fáza 2: Pattern discovery  (mimo projektu)
   │  • asociačné pravidlá  (FP-growth, Apriori)
   │  • sekvenčné pravidlá  (PrefixSpan)
   │
   ↓
NÁJDENÉ VZORY
   │
   │  fáza 3: Pattern analysis  (mimo projektu)
   │  • štatistické testy
   │  • interpretácia, vizualizácia
   │
   ↓
INSIGHT  (např. "kto navštívi /admissions, často skončí na /tuition-fees")
```

Každý krok fázy 1 je **nutnou prípravou** pre fázy 2 a 3. Bez čistenia by vzory boli skreslené robotmi; bez sedení by sa hľadali cesty cez týždne; bez doplnenia ciest by mali pravidlá medzery.

</details>

---

## Výsledky pipeline

| Krok | Počet záznamov | Komentár |
|------|----------------|----------|
| Surový log | **47 215 218** | celých 4 rokov 2017–2020 |
| Predextrahovaný týždeň | 909 828 | len 17.–23.12.2017 |
| Po 01 (parse + clean) | 211 313 | -77% |
| Robot IP (02) | 250 unik. | z 2 354 prístupov |
| Po 03 (bez robotov) | 73 927 | -65% z 211k |
| Po 04 (UNIXTIME) | 73 927 | safety check |
| Po 05 (USER_ID) | 73 927 | **14 563 unikátnych userov** |
| Po 06 (Length) | 73 927 | priemer 174s, median 5s |
| **Sedenia RLength** | **33 496** | KS test → STT_Q |
| **Sedenia h-ref** | **46 693** | viac než RLength |
| Doplnenie RLength | +4 032 | spolu 77 959 |
| Doplnenie h-ref | +139 | spolu 74 066 |

---

## Diskusia a závery

### ✅ Silné stránky riešenia

- **Konzistentná `in`/`out` štruktúra** — každý task má vlastné priečinky, izolované testovanie
- **Detailné komentáre** v každom skripte
- **Streamové čítanie 12 GB logu** — memory efficient
- **RLength s automatickým fallbackom** na STT_Q (podľa zadania)
- **Mapa webu vybudovaná z logu** — netreba externý zdroj

### ⚠️ Obmedzenia

- **Mapa webu** je iba pre pridelené obdobie *(stránky mimo týždňa nie sú v nej)*
- **User identifikácia** podľa IP+Agent zlyháva pri NAT alebo VPN
- **60-min STT** je arbitrárne *(môže nezachytiť niektoré dlhé sedenia)*
- **Statické súbory:** filter pokrýva typické *(obrázky, css, js, fonty)*, ale **nezahŕňa PDF, DOC, ZIP** *(ak sa vyskytnú v logu)*

### Možné vylepšenia

- Asociačné pravidlá nad sedeniami *(rozšírenie projektu)*
- Klastering používateľov podľa navigačných vzorov
- Predikcia ďalšej návštevy podľa aktuálneho sedenia

---

## Najčastejšie otázky pri obhajobe

### Q: Prečo si použil regex namiesto `pd.read_csv` pre Apache log?

**A:** Apache Combined Log Format má stĺpcový oddeľovač kombinujúci medzeru a úvodzovky *(napr. `"GET /url HTTP/1.1"` je jeden stĺpec ohraničený `"..."`)*. `pd.read_csv` so `sep=' '` by to nezvládol. Regex zachytí presný formát.

### Q: Čo vyjadruje vzorec RLength: `-ln(1-p) × mean`?

**A:** Pri exp. rozdelení s priemerom `mean`, hodnota `-ln(1-p) × mean` je `p`-tý percentil. Pre `p=0.4` to znamená: 40% hodnôt je menších než RLength. Tieto hodnoty sú "navigačné" stránky *(krátke kliky)*, ostatné sú content.

### Q: Prečo prah `Q3 + 1.5×IQR` pre STT_Q?

**A:** Toto je štandardná definícia "miernych outlierov" v boxplote. Hodnoty nad týmto prahom sú štatisticky neobvyklé — takže ak je medzi 2 prístupmi taký čas, ide pravdepodobne o nové sedenie.

### Q: Ako sa líši h-ref od STT_MEAN?

**A:** STT_MEAN = iba časový prah (priemer). h-ref pridáva 3. podmienku: nové sedenie ak `Referrer="-"` *(priamy prístup zvonku)*. h-ref je teda STT_MEAN + extra rozdelenia kde user prišiel zvonku.

### Q: Prečo doplnenie ciest nájde viac záznamov pre RLength než pre h-ref?

**A:** RLength má menej sedení ale **dlhších**. Dlhé sedenia majú viac "skokov" v navigácii *(kde chýba medzistránka)*. h-ref má viac kratkých sedení — krátke sedenia majú málo skokov, takže menej čo doplniť.

### Q: Čo sa stane ak by data MALI exponenciálne rozdelenie?

**A:** Použila by sa metóda RLength s prahom `-ln(1-0.4) × priemer ≈ 89s`. Výsledok by bol pravdepodobne podobný STT_Q `(~76s)`, ale matematicky inak odôvodnený.

### Q: Prečo si extrahoval týždeň VOPRED (úloha 00) namiesto v úlohe 04?

**A:** Praktickosť — 12 GB log nemusíme spracovávať 2x *(raz pre čistenie a raz pre robot IPs)*. Zmenšením na 216 MB sa každá nasledujúca úloha urýchli. Logicky je to ekvivalentné *(filter všade je idempotentný)*.

### Q: Ako funguje `cumsum()` na boolean stĺpci?

**A:** Pandas `False=0, True=1`. Kumulatívny súčet rastie pri každom `True`:

```log
[True, False, False, True, False, True]
   1     0      0     1      0     1
   1     1      1     2      2     3      ← SESSION_ID
```

Každé nové sedenie *(True)* zvýši ID o 1. Globálny counter cez celý DataFrame.

### Q: Prečo si filter použil `(?:\?|$)` na konci priponov?

**A:** Aby sa nezachytávali pripony v strednej časti URL. `?` v URL znamená query string *(napr. `/api/data.json?id=5`)*, `$` koniec URL. Bez toho by sa zachytil aj `/some.css.html` *(content stránka)*.

---

**KONIEC DOKUMENTÁCIE**
