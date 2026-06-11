# Objavovanie znalosti - Navod a vysledky

## Ako rozbehat programy

### 1. Rozbalit ZIP subory

Rozbal cv1, cv2, cv3, cv4, cv5 do jedneho priecinka, napr. `C:\Objavovanie znalosti\`.

### 2. Vytvorit virtualne prostredie

Otvor terminal (PowerShell/CMD) v hlavnom priecinku a spusti:

```
py -m venv .venv
.venv\Scripts\activate
```

### 3. Nainstalovat kniznice

```
pip install pandas numpy nltk requests beautifulsoup4 openpyxl matplotlib scipy mlxtend statsmodels
```

### 4. Spustanie programov

Kazdy program sa spusta z JEHO priecinka. Napr.:

```
cd cv2\scripts\01_UNIXTIME
python unixtime.py
```

Kazdy priecinok ma:
- `in/` - vstupne subory (NEPREPISOVAT)
- `out/` - sem sa ulozia vysledky
- `.py` - skript na spustenie

### 5. Poradie spustania

CV1 → CV2 → CV3 (pipeline, vystupy zavisia na sebe).
CV4 a CV5 su nezavisle (oba pouzivaju logs5.csv).

**CV1** (ulohy 05-08 su pipeline, 01-04 su nezavisle):
```
cd cv1\scripts\05_cistenie_dat_I       && python clean.py
cd cv1\scripts\06_cistenie_dat_II      && python clean2.py
cd cv1\scripts\07_cistenie_dat_III     && python clean3.py
cd cv1\scripts\08_cistenie_dat_IV      && python clean4.py
```

**CV2** (spustat postupne 01 az 09):
```
cd cv2\scripts\01_UNIXTIME                    && python unixtime.py
cd cv2\scripts\02_identifikacia_pouzivatelov  && python identifikacia.py
cd cv2\scripts\03_premenna_Length              && python length.py
cd cv2\scripts\04_STT_MEAN                    && python stt_mean.py
cd cv2\scripts\05_STT_Q                       && python stt_q.py
cd cv2\scripts\06_SLength                     && python slength.py
cd cv2\scripts\07_RLength_exp                 && python rlength_exp.py
cd cv2\scripts\08_RLength                     && python rlength.py
cd cv2\scripts\09_h_ref                       && python h_ref.py
```

**CV3** (spustat po CV2, ulohy su nezavisle):
```
cd cv3\scripts\01_doplnanie_STT_MEAN  && python doplnanie.py
cd cv3\scripts\02_doplnanie_STT_Q     && python doplnanie.py
cd cv3\scripts\03_doplnanie_RLength   && python doplnanie.py
cd cv3\scripts\04_doplnanie_h_ref     && python doplnanie.py
```

**CV4** - Prieskum dat (ulohy nezavisle, kazda nacita logs5.csv):
```
cd cv4\scripts\01_popisne_statistiky    && python popisne.py
cd cv4\scripts\02_navstevnost_v_case    && python navstevnost.py
cd cv4\scripts\03_cas_na_strankach      && python cas.py
cd cv4\scripts\04_vztahy_premennych     && python vztahy.py
```

**CV5** - Asociacne pravidla (pipeline 01 → 02 → 03 → 04):
```
cd cv5\scripts\01_priprava_dat          && python priprava.py
cd cv5\scripts\02_asociacne_pravidla    && python pravidla.py
cd cv5\scripts\03_matica_pravidiel      && python matica.py
cd cv5\scripts\04_statisticka_analyza   && python analyza.py
```

### Poznamky

- Vstupy su uz pripravene v `in/` priecinkoch, netreba nic kopirovat
- Ak `python` nefunguje, skus `py` alebo `python3`
- Ak NLTK hlasi chybu, spusti: `python -c "import nltk; nltk.download('all')"`

---

## Vyhodnotenie presnosti vysledkov

### CV1 - Cistenie dat

| Uloha | Popis | Nase | Ocakavane | Odchylka |
|-------|-------|------|-----------|----------|
| 05 | Cistenie dat I - zaznamy | 57650 | ~56500 | +2.0% |
| 06 | Cistenie dat II - zaznamy | 31980 | ~31500 | +1.5% |
| 07 | Cistenie dat III - robot IPs | **333** | 333 | **presne** |
| 08 | Cistenie dat IV - zaznamy | 20666 | (neuvedene) | - |

### CV2 - Identifikacia sedeni

| Uloha | Popis | Nase | Ocakavane | Odchylka |
|-------|-------|------|-----------|----------|
| 02 | Identifikacia pouzivatelov | 4096 | ~4040 | +1.4% |
| 03 | Priemer Length | 147.20 | ~150 | -1.9% |
| 04 | STT_MEAN - pocet sedeni | 7097 | ~7500 | -5.4% |
| 05 | STT_Q - pocet sedeni | 7873 | ~7500 | +5.0% |
| 06 | SLength - pocet sedeni | 6515 | ~6700 | -2.8% |
| 07 | KS test - p-hodnota | p < 0.05 | - | NEMAJU exp. rozdelenie |
| 08 | RLength - pocet sedeni | 7558 | ~8000 | -5.5% |
| 09 | h-ref - pocet sedeni | 8180 | ~7200 | +13.6% |

### CV3 - Doplnanie ciest

| Uloha | Popis | Nase | Ocakavane | Odchylka |
|-------|-------|------|-----------|----------|
| 01 | Doplnanie STT_MEAN | 855 | ~750 | +14.0% |
| 02 | Doplnanie STT_Q | 735 | ~750 | -2.0% |
| 03 | Doplnanie RLength | 776 | ~850 | -8.7% |
| 04 | Doplnanie h-ref | 706 | ~690 | +2.3% |

### CV4 - Prieskum dat (banka 2009-2012)

Volne zadanie - analyticky prieskum, hlavne zistenia:

| Uloha | Hlavne zistenie |
|-------|-----------------|
| 01 Popisne statistiky | 2M zaznamov, 6 kategorii, 6912 userov, top "Pricing List" (33% pristupov) |
| 02 Navstevnost v case | **Po krize +29.8% pristupov/mesiac** vs pocas krizy |
| 03 Cas na strankach | Najdlhsie citanie "Reputation" (25s), najkratsie "We support.." (10s) |
| 04 Vztahy premennych | Vsetky chi-square testy vyznamne (p<0.001), Cramerovo V do 0.37 |

### CV5 - Asociacne pravidla a metaanalyza

Extrakcia pravidiel z transakcii pre kazdy rok + Cochranov Q test:

| Uloha | Vysledok |
|-------|----------|
| 01 Priprava transakcii | 2009: 37734, 2010: 18996, 2011: 21473, 2012: 24278 transakcii |
| 02 Asociacne pravidla (apriori) | 2009: 341, 2010: 405, 2011: 205, 2012: 17 pravidiel |
| 03 Matica unikatnych pravidiel | 450 unikatnych pravidiel × 4 obdobia |
| 04 Cochranov Q test | Q=724.3, p<0.001 → **rozdiely medzi obdobiami su vyznamne** |

Z 450 unikatnych pravidiel:
- **15** je vo vsetkych 4 obdobiach (stabilne jadro)
- 157 v 3 obdobiach
- 159 v 2 obdobiach
- **119** unikatne pre 1 obdobie

### Poznamky k odchylkam

- Vsetky ocakavane hodnoty su **priblizne** ("cca", "priblizne") - nie su to presne cisla
- Odchylky do ~5% su normalne a vyplyvaju z mierne odlisneho sposobu cistenia dat v cv1
- **h-ref (cv2/09)** ma vyssiu odchylku (+13.6%) pretoze je citlivy na pocet zaznamov s prazdnym referrerom ("-")
- **cv3/01 STT_MEAN** ma vyssiu odchylku (+14%) pretoze STT_MEAN ma menej sedeni nez ocakavane -> dlhsie sedenia -> viac parov na doplnenie
- Cisla cv2 a cv3 priamo zavisia na cisteni v cv1 - mala zmena v cv1 sa propaguje do vsetkych dalsich uloh
- CV4 a CV5 pouzivaju iny dataset (logs5.csv - banka), nie su prepojene s cv1-cv3
