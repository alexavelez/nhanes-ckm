# Phenotyping Early Cardiometabolic Risk in Reproductive-Age Women Using NHANES

**Author:** Alexandra Velez, OB-GYN (Colombia) | Data Science  
**Data:** NHANES 2017–March 2020 Pre-Pandemic Public Use Files  
**Repository:** `github.com/alexavelez/nhanes-ckm`

---

Objective: To determine whether reproductive-age women (aged 20–44) with a history of adverse pregnancy outcomes (APOs)—specifically gestational diabetes mellitus (GDM)—exhibit distinct, early-stage cardiometabolic-kidney-metabolic (CKM) biomarker profiles compared to those with uncomplicated pregnancies.

Methodological Approach: This study applies unsupervised $k$-means clustering to six cardiometabolic-kidney-metabolic (CKM) biomarkers — HbA1c, BMI, systolic blood pressure, eGFR, HDL, and fasting glucose — in a cohort of $N = 1{,}338$ reproductive-age women from the National Health and Nutrition Examination Survey (NHANES). Reproductive history and APO status are deliberately withheld from the clustering algorithm and introduced only afterward, to test whether the biomarker-defined phenotypes it finds are enriched for GDM and macrosomia history. That ordering is the whole point: an earlier pass at this analysis clustered on a mix of biomarkers and reproductive features — including the variable encoding GDM and macrosomia directly — then tested whether GDM was "enriched" in clusters that had already been built partly from GDM. That test was circular and couldn't fail. It's documented below as a first pass rather than deleted from the project history, because catching and fixing it is part of what this project demonstrates.

Clinical Justification: Rather than examining established pathology, this analysis targets subclinical physiological dysregulation. Identifying these phenotypes in a young cohort provides a critical window for targeted preventive clinical interventions.

## The Question

Among reproductive-age women aged 20–44, do those with adverse pregnancy
outcomes (APOs) — particularly gestational diabetes — already show distinct
early cardiometabolic biomarker profiles compared to women without APOs?

This project clusters 1,338 reproductive-age women into phenotypes using six
cardiometabolic-kidney-metabolic (CKM) biomarkers alone, then tests —
strictly after clustering, using reproductive history the algorithm never
saw — whether those phenotypes track with GDM and macrosomia history. The
framing is intentional in two ways: first, not established cardiovascular
disease, but early dysregulation in a population young enough to benefit
most from preventive intervention; second, a clustering step and an
enrichment test that are genuinely independent of each other, so a positive
result actually means something.

---

## The Answer

Yes for GDM, with real nuance — and a materially weaker signal for
macrosomia.

A distinct metabolic risk phenotype emerges in 9.0% of the main clustering
sample (n=121 of 1,338), characterized by prediabetic-range glycemia (HbA1c
median 6.1%, IQR 5.8–6.5), central obesity (BMI median 39.2, IQR 32.8–46.1),
elevated fasting glucose (108 mg/dL, IQR 101–118), and higher blood pressure
(SBP 115.7 mmHg) than the Low Risk and Lowest Risk phenotypes. Among the
1,266 women with known APO status, GDM history is significantly enriched in
this cluster — 26.4% versus 10.9% in the combined lower-risk groups
(OR=2.93, 95% CI 1.75–4.91, p<0.001). That pattern is corroborated by
fasting lipid data the clustering algorithm never had access to
(triglycerides H=82.46, LDL H=26.98, both p<0.001).

Macrosomia is a different story. The direction is the same — 19.8% versus
12.4% in the Metabolic Risk cluster (OR=1.74, 95% CI 1.00–3.04) — but it's
only borderline significant (p=0.072) and the confidence interval touches
1.0. I'd rather report that honestly than fold it into the GDM finding as
if the two carried equal weight.

A separate outlier phenotype (n=20, excluded from the main clustering)
represents the far end of the spectrum — overt, often severe hyperglycemia
(HbA1c median 9.4%, glucose median 212 mg/dL) that dominated the clustering
metrics enough to obscure the subtler structure in the rest of the sample
when left in. These 20 women share the same adiposity profile as the
Metabolic Risk cluster (BMI median 35.7) and have the highest GDM rate of
any group in the dataset — 37% among the 19 with known status — separated
from the main Metabolic Risk phenotype by disease progression rather than
body size.

---

## Participant flow diagram

![Participant flow diagram: from the full P_RHQ sample (n=5,314) through age restrictions and CDC disclosure suppression to the analytical sample (n=1,603), then split by pregnancy history](figures/participant_flow.png)

---

## Pipeline

| Notebook                                    | Status      | Description                                                                                                                                                                                  |
| -------------------------------------------- | ----------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `01_data_exploration.ipynb`                 | ✅ Complete | Data loading, SAS artifact detection, encoding documentation, skip logic mapping, analytical sample definition (n=1,603), weighted prevalence estimates                                      |
| `02_reproductive_feature_engineering.ipynb` | ✅ Complete | Feature engineering across four reproductive domains: pregnancy history, adverse pregnancy outcomes, surgical history, hormone therapy. 19 features derived; 4 (Age_Menarche, Parity, Pregnancy_Loss, APO_Score) carried forward as descriptive/exposure variables, not clustering inputs |
| `03_ckm_integration.ipynb`                  | ✅ Complete | CKM biomarker integration from 6 NHANES modules, eGFR calculation, medication flags from P_RXQ_RX. 6-feature CKM biomarker set established for clustering                                    |
| `04_exploratory_analysis.ipynb`             | ✅ Complete | Descriptive analysis, biomarker distributions by APO status, Spearman correlation analysis, collinearity decisions, missingness strategy, medication confounder assessment                   |
| `05_preprocessing.ipynb`                    | ✅ Complete | Biomarker-only clustering matrix (6 features, RobustScaler). Reproductive/exposure variables coded separately and held out of clustering entirely. Never-pregnant zero-imputation, median imputation for residual Parity/Pregnancy_Loss, Age_Menarche left unimputed (no longer a clustering input), 72-woman unknown-APO subset flagged (not excluded) for notebook 07  |
| `06_clustering.ipynb`                       | ✅ Complete | K-means k=2–8 on 6 CKM biomarkers. Full-sample k=2 isolates a 20-woman extreme-glycemia outlier phenotype; excluding it defines the n=1,338 main sample. Silhouette, Calinski-Harabasz, and gap statistic all favor k=2 on the main sample, but k=3 is selected for clinical specificity — a disclosed, documented tradeoff. Bootstrap stability (100 iter., mean ARI=0.760), hierarchical Ward sensitivity (ARI=0.272), StandardScaler sensitivity (ARI=0.255) |
| `07_clinical_interpretation.ipynb`          | ✅ Complete | Cluster phenotype characterization, non-circular GDM/macrosomia enrichment test (excludes 72 women with unknown APO status), outlier phenotype characterization, APO-unknown group comparison, Stage 2 fasting lipid validation, clinical implications |

---

## Key Analytical Decisions

**Sample:** 1,603 women aged 20–44 from NHANES 2017–March 2020.
**Clustering sample:** 1,358 complete cases on all 6 CKM biomarkers (245
excluded for missing at least one biomarker — mostly incomplete
examination-module participation, led by Mean_SBP at 9.5% missing), then a
further 20 excluded as an extreme-glycemia outlier phenotype (identified at
k=2 on the full complete-case sample), leaving a **main clustering sample of
1,338**.

**Features:** 6 clustering features — HbA1c, BMI, Mean_SBP, eGFR, HDL,
Glucose. (Waist dropped — collinear with BMI, r=0.95; Mean_DBP dropped —
collinear with Mean_SBP, r=0.79.) Age_Menarche, Parity, Pregnancy_Loss, and
APO_Score are coded and carried forward as descriptive/exposure variables
but are **not** clustering inputs — they're the variables notebook 07 tests
against the biomarker-defined clusters, and keeping them out of the
algorithm is what makes that test non-circular.

**A note on methodology:** the original version of this pipeline clustered
on 10 features — the 6 biomarkers above plus the 4 reproductive variables,
including APO_Score, which directly encodes GDM and macrosomia history.
Testing whether GDM was "enriched" in clusters built partly from GDM is not
a real test; it can't fail. That circularity is fixed throughout the
current pipeline: clustering runs on biomarkers only, and every number in
this README describing GDM or macrosomia enrichment comes from a test the
algorithm had no way to see coming.

**Scaling:** RobustScaler (median/IQR) — chosen over StandardScaler because
skewed clinical distributions with meaningful outliers inflate standard
deviation and distort z-score scaling. A StandardScaler sensitivity check
confirmed this wasn't an arbitrary choice: agreement between the two
scalers' k=3 solutions is low (ARI=0.255), and StandardScaler's most-elevated
cluster is more than twice the size of RobustScaler's Metabolic Risk cluster
while being less extreme on every biomarker — exactly the dilution pattern
mean/SD scaling produces on skewed data.

**Missing data:** Never-pregnant women zero-imputed on pregnancy features
(clinical definition, not statistical imputation). Small residual item
non-response in Parity (15 women) and Pregnancy_Loss (50 women) among
ever-pregnant women median-imputed. Age_Menarche (78 missing) is left
unimputed in this version — the previous pipeline filled it via KNN using
the same biomarkers that were also clustering inputs at the time, which
would have manufactured part of the cluster-level difference notebook 07
later measures. Since Age_Menarche is descriptive-only now, imputing it
that way is no longer defensible, so it's left as missing and excluded only
from analyses that use it directly. APO_Score is left unknown for 89
women — clinical events cannot be statistically estimated — of whom 72 fall
within the biomarker-complete clustering sample and are excluded only from
notebook 07's enrichment test, not from clustering itself.

**K selection:** k=3 is chosen despite every standard internal validity
metric favoring k=2 — silhouette peaks at k=2 (0.2760) and drops to 0.1677
at k=3; Calinski-Harabasz is highest at k=2 (406.49) and declines
monotonically; the gap statistic satisfies the Tibshirani, Walther & Hastie
(2001) criterion at k=2; there's no sharp elbow distinguishing k=2 from
k=3. The reason for choosing k=3 anyway is clinical, not statistical: k=2
gives a coarse split into higher- and lower-metabolic-burden groups (GDM
rate 17.0% vs. 9.5%, χ²=10.10, p=0.0015), while k=3 peels a small, sharply
defined Metabolic Risk cluster (n=121, 9.0%) out of that coarser split,
producing a cleaner and clinically more interpretable phenotype. This is
presented as a disclosed, deliberate choice rather than an objectively
optimal partition — see Known Limitations.

---

## Results Summary

| Group             | N   | %     | HbA1c (median) | BMI (median) | GDM history |
| ----------------- | --- | ----- | --------------- | ------------- | ----------- |
| Metabolic Risk    | 121 | 9.0%  | 6.1%            | 39.2          | 25.0%       |
| Low Risk          | 584 | 43.6% | 5.4%            | 32.8          | 12.2%       |
| Lowest Risk       | 633 | 47.3% | 5.1%            | 23.8          | 7.9%        |
| Outlier phenotype | 20  | —     | 9.4%            | 35.7          | 37.0%*      |

*Among the 19 outlier-phenotype women with known APO status (1 unknown).
GDM history figures for the three main phenotypes are self-reported GDM
rate within each cluster (n=1,266 women with known APO status); the formal
enrichment test in the next line uses the odds-ratio framing below.

GDM OR (Metabolic Risk vs. combined Low Risk + Lowest Risk, n=1,266):
**2.93 (95% CI 1.75–4.91, p<0.001)**
Macrosomia OR (same comparison): **1.74 (95% CI 1.00–3.04, p=0.072)** —
directionally consistent, not conventionally significant
Fasting triglycerides across phenotypes (n=661, Kruskal-Wallis): **H=82.46,
p<0.001**

---

## Known Limitations

- **No temporality** — cross-sectional design cannot establish whether
  GDM preceded cardiometabolic dysregulation or vice versa
- **Hypertensive disorders of pregnancy absent** — preeclampsia and
  gestational hypertension are not available in the NHANES 2017–March
  2020 public use file; the enrichment test covers GDM and macrosomia only
- **Medication attenuation** — medicated women retained (exclusion would
  bias against the highest-risk group); biomarker values likely
  underestimate true underlying disease burden
- **K selection is a disclosed clinical judgment call, not a statistically
  optimal partition** — silhouette, Calinski-Harabasz, and the gap
  statistic all favor k=2 on the main sample; k=3 is chosen because it
  isolates a clinically distinct Metabolic Risk phenotype that k=2's
  coarser split blends into a larger, less specific cluster
- **Cluster boundary sensitivity** — bootstrap stability across 100
  resamples is moderate (mean ARI=0.760, median=0.818; 85/100 iterations
  above the 0.6 stability threshold, but a real low-stability tail
  remains); agreement with an independent hierarchical (Ward) clustering
  is modest (ARI=0.272); agreement with a StandardScaler-based refit is
  also modest (ARI=0.255) — the GDM enrichment signal survives all three
  checks but with softer edges than a single clean cluster boundary would
  suggest
- **Macrosomia signal is underpowered relative to GDM** — directionally
  consistent (OR=1.74) but the 3-way comparison doesn't reach conventional
  significance (p=0.072); this should be read as inconclusive, not
  negative
- **Fasting lipids in subsample only** — Stage 2 independent-validation
  analysis is limited to 661 of 1,338 women (49.4%) with fasting lipid
  panels

---

## Repository Structure

nhanes-ckm/
├── notebooks/
│ ├── 01_data_exploration.ipynb
│ ├── 02_reproductive_feature_engineering.ipynb
│ ├── 03_ckm_integration.ipynb
│ ├── 04_exploratory_analysis.ipynb
│ ├── 05_preprocessing.ipynb
│ ├── 06_clustering.ipynb
│ └── 07_clinical_interpretation.ipynb
├── data/
│ ├── raw/ # NHANES .XPT files (not tracked — see below)
│ └── processed/ # Pipeline outputs (tracked)
│ ├── reproductive_features.csv
│ ├── feature_classification.csv
│ ├── ckm_features.csv
│ ├── clustering_ready.csv
│ ├── clustering_prescale.csv
│ ├── cluster_assignments.csv
│ ├── cluster_summary_table.csv
│ ├── outlier_phenotype.csv
│ └── apo_unknown_reference.csv
├── figures/ # All visualizations
└── scripts/
└── download_nhanes_data.py

---

## Reproducing the Analysis

### 1. Clone the repository

```bash
git clone https://github.com/alexavelez/nhanes-ckm.git
cd nhanes-ckm
```

### 2. Create the environment

```bash
conda create -n nhanes-ckm python=3.11
conda activate nhanes-ckm
pip install pandas numpy matplotlib seaborn scikit-learn scipy jupyter
```

### 3. Download NHANES data

```bash
python scripts/download_nhanes_data.py
```

This downloads all required modules from CDC to `data/raw/`.
Total size ~9MB. Files are excluded from version control —
they are publicly available and reproducible.

### 4. Run notebooks in order

Execute notebooks 01 through 07 sequentially. Each notebook
validates its input files with assertions before proceeding.

---

## Technical Notes

**SAS XPT artifacts:** True zeros in several NHANES variables are
stored as near-zero floats (~5.4e-79) due to SAS floating point
encoding. Resolved via a reusable `scan_sas_artifacts()` function
in notebook 01.

**SEQN index:** All processed files use SEQN as the index. Float64
vs int64 type mismatches caused silent boolean mask failures during
development — resolved by consistently using `.isin()` on indices.

**Survey weights:** Clustering uses the unweighted analytical sample.
Weighted prevalence estimates for population-level claims were
established in notebook 01 using WTMECPRP.

---

## Environment

- Python 3.11
- pandas, numpy, scipy, matplotlib, seaborn, scikit-learn
- NHANES 2017–March 2020 Pre-Pandemic Public Use Files

---

**NHANES 2017–March 2020 Pre-Pandemic | Women aged 20–44**  
**Unsupervised CKM phenotyping | Reproductive history linkage**
**Alexandra Velez, OB-GYN (Colombia) | Data Science**
