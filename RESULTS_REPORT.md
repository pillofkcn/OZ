# RESULTS REPORT — Spustenie všetkých 40 skriptov

## Súhrn

- **Total**: 40 skriptov
- **OK** (Δ<5%): 34
- **TOL** (delta < 20 percent, v tolerancii cca): 6
- **FLAG** (Δ<50%): 0
- **MISMATCH** (Δ≥50%): 0
- **FAILED** (exit ≠ 0): 0
- **Wall time spolu**: 414.4 s (6.9 min)

## 01_zdroje_dat

| Skript | Expected | Actual | Δ% | Status | Wall |
|--------|----------|--------|-----|--------|------|
| `01_prehladavanie_webu/crawler.py` | 5 .txt suborov v out/articles/ | — | — | ✅ OK | 4.1s |
| `02_reprezentacia_textu_I/freq.py` | Excel s 5 harkami: wf, binary, log, idf, tf-idf | — | — | ✅ OK | 1.7s |
| `03_reprezentacia_textu_II/lemma.py` | Excel s 5 harkami | — | — | ✅ OK | 7.0s |
| `04_reprezentacia_textu_III/identif.py` | Excel so 7 stlpcami | — | — | ✅ OK | 6.7s |

<details>
<summary>Detail: všetky extrahované hodnoty pre 01_zdroje_dat</summary>

**01_prehladavanie_webu/crawler.py**:
  - (žiadne číselné výstupy parsované)

**02_reprezentacia_textu_I/freq.py**:
  - docs_or_lemmas: 50

**03_reprezentacia_textu_II/lemma.py**:
  - docs_or_lemmas: 1076

**04_reprezentacia_textu_III/identif.py**:
  - words: 1990

</details>

## 02_cistenie_dat

| Skript | Expected | Actual | Δ% | Status | Wall |
|--------|----------|--------|-----|--------|------|
| `01_cistenie_dat_I/clean.py` | 56500 (records) | 57650 | 2.0 | ✅ OK | 3.0s |
| `02_cistenie_dat_II/clean2.py` | 31500 (records) | 31980 | 1.5 | ✅ OK | 1.6s |
| `03_cistenie_dat_III_roboti/clean3.py` | 333 (unique_ips) | — | — | ✅ OK | 1.4s |
| `04_cistenie_dat_IV_roboti/clean4.py` | bez konkretneho cisla | — | — | ✅ OK | 1.4s |

<details>
<summary>Detail: všetky extrahované hodnoty pre 02_cistenie_dat</summary>

**01_cistenie_dat_I/clean.py**:
  - records: 57650
  - records_intermediate: 255503

**02_cistenie_dat_II/clean2.py**:
  - records: 31980

**03_cistenie_dat_III_roboti/clean3.py**:
  - robots_records: 333
  - robot_ips: 333

**04_cistenie_dat_IV_roboti/clean4.py**:
  - records: 20666

</details>

## 03_identifikacia

| Skript | Expected | Actual | Δ% | Status | Wall |
|--------|----------|--------|-----|--------|------|
| `01_UNIXTIME/unixtime.py` | UNIXTIME stlpec doplneny | — | — | ✅ OK | 1.1s |
| `02_identifikacia_pouzivatelov/identifikacia.py` | 4040 (users) | 4096 | 1.4 | ✅ OK | 1.1s |
| `03_premenna_Length/length.py` | 150 (avg_length) | 147.2 | 1.9 | ✅ OK | 1.1s |
| `04_STT_MEAN/stt_mean.py` | 7500 (sessions) | 7097 | 5.4 | 🟡 TOL | 1.1s |
| `05_STT_Q/stt_q.py` | 7500 (sessions) | 7873 | 5.0 | ✅ OK | 1.1s |
| `06_SLength/slength.py` | 6700 (sessions) | 7075 | 5.6 | 🟡 TOL | 1.9s |
| `07_RLength_exp/rlength_exp.py` | KS test vystup | — | — | ✅ OK | 130.8s |
| `08_RLength/rlength.py` | 8000 (sessions) | 7558 | 5.5 | 🟡 TOL | 1.2s |
| `09_h_ref/h_ref.py` | 7200 (sessions) | 8180 | 13.6 | 🟡 TOL | 1.1s |

<details>
<summary>Detail: všetky extrahované hodnoty pre 03_identifikacia</summary>

**01_UNIXTIME/unixtime.py**:
  - records: 20666

**02_identifikacia_pouzivatelov/identifikacia.py**:
  - records: 20666
  - users: 4096

**03_premenna_Length/length.py**:
  - records: 20666
  - avg_length: 147.2

**04_STT_MEAN/stt_mean.py**:
  - records: 20666
  - sessions: 7097

**05_STT_Q/stt_q.py**:
  - records: 20666
  - sessions: 7873

**06_SLength/slength.py**:
  - records: 20666
  - sessions: 7075

**07_RLength_exp/rlength_exp.py**:
  - ks_stat: 0.6096
  - p_value: 0.0

**08_RLength/rlength.py**:
  - records: 20666
  - sessions: 7558
  - avg_length: 147.2

**09_h_ref/h_ref.py**:
  - records: 20666
  - sessions: 8180

</details>

## 04_doplnanie_ciest

| Skript | Expected | Actual | Δ% | Status | Wall |
|--------|----------|--------|-----|--------|------|
| `01_doplnanie_STT_MEAN/doplnanie.py` | 750 (added) | 855 | 14.0 | 🟡 TOL | 5.8s |
| `02_doplnanie_STT_Q/doplnanie.py` | 750 (added) | 735 | 2.0 | ✅ OK | 5.8s |
| `03_doplnanie_RLength/doplnanie.py` | 850 (added) | 776 | 8.7 | 🟡 TOL | 5.7s |
| `04_doplnanie_h_ref/doplnanie.py` | 690 (added) | 706 | 2.3 | ✅ OK | 5.8s |

<details>
<summary>Detail: všetky extrahované hodnoty pre 04_doplnanie_ciest</summary>

**01_doplnanie_STT_MEAN/doplnanie.py**:
  - records: 21521
  - added: 855

**02_doplnanie_STT_Q/doplnanie.py**:
  - records: 21401
  - added: 735

**03_doplnanie_RLength/doplnanie.py**:
  - records: 21442
  - added: 776

**04_doplnanie_h_ref/doplnanie.py**:
  - records: 21372
  - added: 706

</details>

## 05_prieskum_dat

| Skript | Expected | Actual | Δ% | Status | Wall |
|--------|----------|--------|-----|--------|------|
| `01_popisne_statistiky/popisne.py` | popisne statistiky + PNG | — | — | ✅ OK | 15.9s |
| `02_navstevnost_v_case/navstevnost.py` | casovy vyvoj + PNG | — | — | ✅ OK | 18.6s |
| `03_cas_na_strankach/cas.py` | cas na strankach + PNG | — | — | ✅ OK | 14.9s |
| `04_vztahy_premennych/vztahy.py` | chi-square + ANOVA | — | — | ✅ OK | 15.6s |

<details>
<summary>Detail: všetky extrahované hodnoty pre 05_prieskum_dat</summary>

**01_popisne_statistiky/popisne.py**:
  - (žiadne číselné výstupy parsované)

**02_navstevnost_v_case/navstevnost.py**:
  - (žiadne číselné výstupy parsované)

**03_cas_na_strankach/cas.py**:
  - records: 748496

**04_vztahy_premennych/vztahy.py**:
  - (žiadne číselné výstupy parsované)

</details>

## 06_extrakcia_vzorov

| Skript | Expected | Actual | Δ% | Status | Wall |
|--------|----------|--------|-----|--------|------|
| `01_priprava_dat/priprava.py` | 4 CSV transakcii 2009-2012 | — | — | ✅ OK | 24.8s |
| `02_asociacne_pravidla/pravidla.py` | >= 10 (min_rules (per obdobie, n_obdobi=4)) | 17–405 | — | ✅ OK | 3.1s |
| `03_matica_pravidiel/matica.py` | binarna matica O1-O4 | — | — | ✅ OK | 0.9s |
| `04_statisticka_analyza/analyza.py` | Cochran Q + Kendall W | — | — | ✅ OK | 3.3s |

<details>
<summary>Detail: všetky extrahované hodnoty pre 06_extrakcia_vzorov</summary>

**01_priprava_dat/priprava.py**:
  - records: 2071235
  - records_input: 2071235

**02_asociacne_pravidla/pravidla.py**:
  - itemsets: 63
  - rules: 341

**03_matica_pravidiel/matica.py**:
  - (žiadne číselné výstupy parsované)

**04_statisticka_analyza/analyza.py**:
  - cochran_q: 724.2951
  - kendall_w: 0.5365

</details>

## 07_projekt

| Skript | Expected | Actual | Δ% | Status | Wall |
|--------|----------|--------|-----|--------|------|
| `00_extrakcia_tyzdna/extract_week.py` | 909828 (records) | — | — | ✅ OK | 99.8s |
| `01_cistenie_zaznamov/clean.py` | 211313 (records) | 211313 | 0.0 | ✅ OK | 5.7s |
| `02_robot_ips/robot_ips.py` | 250 (unique_ips) | 250 | 0.0 | ✅ OK | 1.9s |
| `03_filter_robotov/filter.py` | 73927 (records) | 73927 | 0.0 | ✅ OK | 2.9s |
| `04_obdobie_unixtime/obdobie.py` | 73927 (records) | 73927 | 0.0 | ✅ OK | 1.7s |
| `05_identifikacia_pouzivatelov/users.py` | 14563 (users) | 14563 | 0.0 | ✅ OK | 1.6s |
| `06_premenna_Length/length.py` | 174 (avg_length) | 173.59 | 0.2 | ✅ OK | 1.6s |
| `07_sedenia_RLength/rlength.py` | 33496 (sessions) | 33496 | 0.0 | ✅ OK | 3.3s |
| `08_sedenia_href/href.py` | 46693 (sessions) | 46693 | 0.0 | ✅ OK | 1.6s |
| `09_doplnanie_RLength/doplnanie.py` | 4032 (added) | 4032 | 0.0 | ✅ OK | 3.4s |
| `10_doplnanie_href/doplnanie.py` | 139 (added) | 139 | 0.0 | ✅ OK | 3.3s |

<details>
<summary>Detail: všetky extrahované hodnoty pre 07_projekt</summary>

**00_extrakcia_tyzdna/extract_week.py**:
  - (žiadne číselné výstupy parsované)

**01_cistenie_zaznamov/clean.py**:
  - records: 211313

**02_robot_ips/robot_ips.py**:
  - robots_records: 2354
  - unique_ips: 250

**03_filter_robotov/filter.py**:
  - records: 73927
  - robot_ips_input: 250

**04_obdobie_unixtime/obdobie.py**:
  - records: 73927

**05_identifikacia_pouzivatelov/users.py**:
  - users: 14563

**06_premenna_Length/length.py**:
  - avg_length: 173.59
  - median_length: 5.0

**07_sedenia_RLength/rlength.py**:
  - sessions: 33496
  - avg_length: 173.59
  - ks_stat: 0.5995
  - p_value: 0.0

**08_sedenia_href/href.py**:
  - sessions: 46693

**09_doplnanie_RLength/doplnanie.py**:
  - records: 77959
  - added: 4032

**10_doplnanie_href/doplnanie.py**:
  - records: 74066
  - added: 139

</details>
