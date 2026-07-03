# NHANES Women's CKM Phenotyping

### Early Cardiometabolic-Kidney-Metabolic Risk in Reproductive-Age Women

**Author:** Alexandra Velez, MD  
**Data:** NHANES 2017–March 2020 Pre-Pandemic Public Use Files  
**Repository:** `github.com/alexavelez/nhanes-ckm`

---

## The Question

Among reproductive-age women aged 20–44, do those with adverse pregnancy
outcomes — particularly gestational diabetes — already show distinct early
cardiometabolic biomarker profiles compared to women without APOs?

This project uses unsupervised clustering to phenotype early
cardiometabolic-kidney-metabolic (CKM) risk in 1,603 reproductive-age
women, linking reproductive history features to cardiometabolic biomarkers
through k-means clustering. The framing is intentional: not established
cardiovascular disease, but early dysregulation in a population young
enough to benefit most from preventive intervention.

---

## The Answer

Yes — with important nuance.

A distinct metabolic risk phenotype emerges in 19.2% of the analytical
sample (n=243), characterized by prediabetic glycemia (HbA1c 5.8%),
central obesity (BMI 36.5, waist 113 cm), low HDL (46 mg/dL), elevated
triglycerides (93 mg/dL), and elevated blood pressure (SBP 115.7 mmHg).
Women with GDM history are 2.45 times more likely to be in this cluster
than in the combined low-risk groups (OR=2.45, p=0.001). The pattern
holds across eight independent biomarkers and is confirmed by fasting
lipid data the clustering algorithm never accessed.

An additional outlier phenotype (n=19) represents the far end of the
spectrum — severely uncontrolled diabetes (HbA1c 9.4%, glucose 218 mg/dL)
with 37% GDM history. These women share the same adiposity profile as
the metabolic risk cluster, separated by disease progression rather than
body size.

---

## Pipeline

| Notebook                                    | Status      | Description                                                                                                                                                                                  |
| ------------------------------------------- | ----------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `01_data_exploration.ipynb`                 | ✅ Complete | Data loading, SAS artifact detection, encoding documentation, skip logic mapping, analytical sample definition (n=1,603), weighted prevalence estimates                                      |
| `02_reproductive_feature_engineering.ipynb` | ✅ Complete | Feature engineering across four reproductive domains: pregnancy history, adverse pregnancy outcomes, surgical history, hormone therapy. 19 features derived, 4 designated for clustering     |
| `03_ckm_integration.ipynb`                  | ✅ Complete | CKM biomarker integration from 6 NHANES modules, eGFR calculation, medication flags from P_RXQ_RX. 12-feature Stage 1 clustering set established                                             |
| `04_exploratory_analysis.ipynb`             | ✅ Complete | Descriptive analysis, biomarker distributions by APO status, Spearman correlation analysis, collinearity decisions, missingness strategy, medication confounder assessment                   |
| `05_preprocessing.ipynb`                    | ✅ Complete | Zero-imputation for never-pregnant women, KNN imputation for Age_Menarche, median imputation for residual missingness, APO unknown exclusion, RobustScaler application                       |
| `06_clustering.ipynb`                       | ✅ Complete | K-means k=2–8, gap statistic, silhouette, Calinski-Harabasz, bootstrap stability (ARI=0.876 median), hierarchical sensitivity, StandardScaler sensitivity, APO_Score sensitivity (ARI=0.969) |
| `07_clinical_interpretation.ipynb`          | ✅ Complete | Cluster phenotype characterization, central question answered, outlier phenotype, APO unknown group, Stage 2 fasting lipids, clinical implications                                           |

---

## Key Analytical Decisions

**Sample:** 1,603 women aged 20–44 from NHANES 2017–March 2020  
**Clustering sample:** 1,266 after exclusions (unknown pregnancy status n=2,
unknown APO status n=89, incomplete biomarker data n=227, outlier
phenotype excluded n=19 after preliminary clustering)

**Features:** 10 clustering features — Age_Menarche, Parity,
Pregnancy_Loss, APO_Score, HbA1c, BMI, Mean_SBP, eGFR, HDL, Glucose  
(Waist dropped — collinear with BMI r=0.95; Mean_DBP dropped — collinear
with Mean_SBP r=0.79)

**Scaling:** RobustScaler (median/IQR) — chosen over StandardScaler
because skewed clinical distributions with meaningful outliers inflate
standard deviation and distort z-score scaling. StandardScaler
sensitivity confirmed choice was not arbitrary — it destroyed the
metabolic signal entirely.

**Missing data:** Never-pregnant women zero-imputed on pregnancy features
(clinical definition, not statistical imputation). Age_Menarche imputed
via KNN (k=5) leveraging known BMI-menarche associations. APO_Score
unknowns excluded — clinical events cannot be statistically estimated.

**K selection:** k=3 selected on convergence of silhouette peak (0.1813),
gap statistic Tibshirani criterion, and inertia elbow. Calinski-Harabasz
favored k=2 which inspection confirmed was not clinically meaningful.

---

## Results Summary

| Group             | N   | %     | HbA1c | BMI  | GDM history |
| ----------------- | --- | ----- | ----- | ---- | ----------- |
| Metabolic Risk    | 243 | 19.2% | 5.8%  | 36.5 | 15.6%       |
| Low Risk          | 273 | 21.6% | 5.3%  | 25.5 | 8.1%        |
| Lowest Risk       | 750 | 59.2% | 5.2%  | 27.7 | 6.7%        |
| Outlier phenotype | 19  | —     | 9.4%  | 36.1 | 37.0%       |

GDM OR (Metabolic Risk vs combined low-risk): **2.45 (p=0.001)**  
Triglycerides ≥150 mg/dL: **22.1%** Metabolic Risk vs **2.8%** Low Risk

---

## Known Limitations

- **No temporality** — cross-sectional design cannot establish whether
  GDM preceded cardiometabolic dysregulation or vice versa
- **Hypertensive disorders of pregnancy absent** — preeclampsia and
  gestational hypertension are not available in the NHANES 2017–March
  2020 public use file; APO_Score captures metabolic APOs only
- **Medication attenuation** — medicated women retained (exclusion would
  bias against highest-risk APO-positive group); biomarker values
  underestimate true underlying disease burden
- **Cluster boundary uncertainty** — bootstrap stability (mean ARI=0.777)
  confirmed the metabolic risk cluster is stable; the boundary between
  the two low-risk clusters is less certain
- **Fasting lipids in subsample only** — Stage 2 analysis limited to
  49.4% of clustering sample

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
│ └── apo_unknown.csv
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
**Alexandra Velez, MD — Health Data Science Portfolio**
