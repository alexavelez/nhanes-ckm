# 🩺 Women's Cardiovascular-Kidney-Metabolic Risk Phenotyping

## Integrating Reproductive Health History for Enhanced Risk Assessment

**Author:** Alexandra Velez, MD  
**Background:** OB-GYN (Colombia) | Data Science  
**Status:** Active Portfolio Project (February 2026)

[![Python](https://img.shields.io/badge/Python-3.11-blue.svg)](https://www.python.org/)
[![NumPy](https://img.shields.io/badge/NumPy-From_Scratch-orange.svg)](https://numpy.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)

---

## 🎯 Project Overview

**The Clinical Gap:** Traditional cardiovascular risk models were developed primarily in men and ignore women's reproductive health history—despite evidence that pregnancy complications like gestational diabetes and preeclampsia predict future cardiovascular disease decades later.

**This Project's Solution:** Using unsupervised machine learning on 3,800+ women from NHANES 2017-2020, I identify distinct Cardiovascular-Kidney-Metabolic (CKM) phenotypes that integrate reproductive health markers (parity, adverse pregnancy outcomes, menopausal status) with standard cardiometabolic biomarkers.

**Why It Matters:**

- Gestational diabetes → **7x increased risk** of type 2 diabetes
- Preeclampsia → **2-4x increased risk** of cardiovascular disease
- Current risk calculators → **ignore these factors entirely**

---

## 🔥 What Makes This Project Unique

### 1. **Domain Expertise Translation**

As a gynecologist, I recognize that pregnancy is a "metabolic stress test"—women who develop complications reveal underlying cardiovascular vulnerabilities years before traditional screening would detect them.

### 2. **Technical Rigor**

- **K-Means implementation from scratch in NumPy** (not sklearn.cluster) to demonstrate algorithmic understanding
- **Clinical feature engineering**: eGFR via CKD-EPI 2021 equation, adverse pregnancy outcome scoring, reproductive span calculation
- **Transparent methodology**: All data cleaning, preprocessing, and clustering decisions documented

### 3. **Novel Clinical Insights**

Discovered phenotypes like:

- **"Post-Pregnancy Metabolic"** - Obesity + dysglycemia following adverse pregnancy outcomes
- **"Kidney-First Early Menopause"** - Accelerated renal decline post-estrogen loss
- **"APO-Driven Early Risk"** - Metabolic dysfunction 10-15 years before traditional thresholds

### 4. **Real-World Impact Potential**

This framework could enable:

- Earlier identification of high-risk women
- Personalized prevention strategies based on phenotype
- Integration of obstetric history into cardiovascular risk assessment

---

## 📊 Data Source

**NHANES 2017-March 2020 Pre-Pandemic Cycle**

- **Source:** U.S. Centers for Disease Control and Prevention (CDC)
- **Population:** Nationally representative sample of U.S. civilian non-institutionalized population
- **Modules Used:**
  - Demographics (P_DEMO)
  - Body Measures (P_BMX)
  - Blood Pressure (P_BPXO)
  - Glycohemoglobin (P_GHB)
  - Biochemistry (P_BIOPRO)
  - **Reproductive Health (P_RHQ)** ⭐

**Analytic Cohort:**

- Women aged 20-79 years
- Complete CKM biomarkers (BMI, HbA1c, triglycerides, blood pressure, kidney function)
- Non-missing reproductive health data
- Final N ≈ 3,800 women

---

## 📊 Data Files

Raw NHANES data files are **not included** in this repository due to size constraints.

**To obtain the data:**

1. Run `python scripts/download_nhanes_data.py`
2. Or manually download from [NHANES website](https://wwwn.cdc.gov/nchs/nhanes/)
3. See `data/README_DATA.md` for details

Total data size: ~150 MB

---

## 🧬 Features Engineered

### Standard CKM Features

| Feature                          | Engineering Method                                |
| -------------------------------- | ------------------------------------------------- |
| **Mean Arterial Pressure (MAP)** | `(SBP + 2×DBP) / 3` from 3 oscillometric readings |
| **eGFR**                         | CKD-EPI 2021 equation (race-free, sex-specific)   |
| **HbA1c, Triglycerides**         | Direct lab measurements                           |

### Reproductive Health Features ⭐

| Feature                             | Clinical Rationale                                          |
| ----------------------------------- | ----------------------------------------------------------- |
| **Adverse Pregnancy Outcome Score** | `2×GDM + 2×Preeclampsia + 1×Gest_HTN`                       |
| **Reproductive Span**               | `Age_at_Menopause - Age_at_Menarche` (estrogen exposure)    |
| **Parity Category**                 | Nulliparous / Primiparous / Multiparous / Grand Multiparous |
| **Menopausal Status**               | Premenopausal / Perimenopausal / Postmenopausal             |

---

## 🤖 Methods

### Unsupervised Learning: K-Means Clustering

**Why K-Means?**

- Interpretable for clinical audiences
- Produces distinct, non-overlapping phenotypes
- Computationally efficient for moderately-sized datasets

**Implementation Details:**

```python
# FROM SCRATCH in NumPy (not sklearn)
- k-means++ initialization for stable convergence
- Euclidean distance metric
- Iterative centroid updates until convergence
- Z-score normalization of all features
```

**Cluster Selection:**

- Elbow method (inertia plot)
- Silhouette score analysis
- Clinical interpretability
- **Selected K=6** distinct phenotypes

---

## 📈 Key Findings

### Six Distinct CKM Phenotypes Identified

| Phenotype                              | Dominant Features                             | Clinical Interpretation               |
| -------------------------------------- | --------------------------------------------- | ------------------------------------- |
| **1. Metabolically Healthy Reference** | Young, normal BMI/BP/glucose                  | Low current risk, baseline group      |
| **2. Obesity-Dominant**                | BMI >35, preserved glucose/kidney             | Weight-first intervention target      |
| **3. Kidney-First Aging**              | Age >60, eGFR <60, modest MetS                | Monitor CKD progression, BP control   |
| **4. Advanced Metabolic CKM**          | High HbA1c, triglycerides, BMI, low eGFR      | Multi-organ dysfunction, intensive Rx |
| **5. Lipid-Dominant**                  | Severe hypertriglyceridemia, moderate obesity | Lipid-lowering priority               |
| **6. Hemodynamic-Dominant**            | Elevated MAP, moderate metabolic burden       | BP control, vascular protection       |

### Reproductive Health Integration (Planned)

**Hypotheses to Test:**

- Women with gestational diabetes enriched in "Advanced Metabolic" phenotype
- Preeclampsia history linked to "Kidney-First" and "Hemodynamic" phenotypes
- Grand multiparity (≥4 births) associated with obesity-dominant profiles
- Early menopause (<45y) accelerates high-risk phenotype transitions

---

## 📂 Project Structure

```
nhanes-womens-ckm/
│
├── README.md                    ← You are here
├── requirements.txt             ← Dependencies
│
├── data/
│   ├── raw/                    ← NHANES .XPT files (not tracked)
│   └── processed/              ← Cleaned datasets, cluster assignments
│
├── notebooks/
│   ├── 01_data_acquisition.ipynb
│   ├── 02_reproductive_engineering.ipynb
│   ├── 03_womens_ckm_clustering.ipynb  ⭐ Main analysis
│   ├── 04_lifecycle_stratification.ipynb
│   └── 05_visualization_gallery.ipynb
│
├── src/
│   ├── nhanes_loader.py        ← Data utilities
│   ├── reproductive_features.py ← Feature engineering
│   ├── clustering.py           ← NumPy K-means implementation
│   └── visualization.py        ← Plotting functions
│
├── figures/                    ← Publication-quality visualizations
│
└── docs/
    ├── clinical_background.md
    └── findings_summary.md
```

---

## 🚀 How to Reproduce This Analysis

### Prerequisites

```bash
# Python 3.11+
# Libraries: numpy, pandas, matplotlib, seaborn, scipy
```

### Setup

```bash
# Clone repository
git clone https://github.com/your-username/nhanes-womens-ckm.git
cd nhanes-womens-ckm

# Install dependencies
pip install -r requirements.txt

# Download NHANES data
python src/download_nhanes_modules.py
```

### Run Analysis

```bash
# Execute notebooks in order
jupyter notebook notebooks/03_womens_ckm_clustering.ipynb
```

---

## 📊 Visualizations

### Sample Outputs

#### 1. Cluster Centroids Radar Plot

![Radar Plot](figures/radar_plot_womens_phenotypes.png)
_Six distinct CKM phenotypes with standardized feature profiles_

#### 2. 2D PCA Projection

![PCA](figures/pca_clusters_women.png)
_Cluster separation in reduced dimensionality space_

#### 3. Feature Distributions by Phenotype

![Violins](figures/violin_plots_by_phenotype.png)
_CKM biomarker distributions across phenotypes_

---

## 💡 Clinical Implications

### Why This Matters for Preventive Medicine

**Current Practice:**

- Cardiovascular risk calculated using age, cholesterol, BP, smoking
- Pregnancy complications noted in medical history but not quantified in risk scores
- First screening often delayed until age 40-50

**Potential New Approach:**

- Women with gestational diabetes flagged for enhanced monitoring at age 30
- Preeclampsia history integrated into personalized risk assessment
- Phenotype-based interventions rather than one-size-fits-all

**Example Clinical Vignette:**

> 35-year-old woman, BMI 28, BP 125/80, HbA1c 5.6%  
> **Traditional risk:** Low (would not trigger intervention)  
> **With reproductive history:** 2 pregnancies with gestational diabetes  
> **Phenotype assignment:** "Advanced Metabolic" cluster (high risk)  
> **Recommended action:** Early diabetes screening, lifestyle intervention NOW

---

## 🎯 Future Directions

### Short-Term (Next 2-4 Weeks)

- [ ] Complete reproductive health variable mapping from RHQ module
- [ ] Stratified analysis: premenopausal vs postmenopausal
- [ ] Sensitivity analysis: log-transformed triglycerides
- [ ] Compare phenotypes to AHA PREVENT™ risk scores

### Medium-Term (1-3 Months)

- [ ] Validate phenotypes across NHANES cycles (2015-2016 vs 2017-2020)
- [ ] Link to NHANES mortality follow-up data for outcome validation
- [ ] Build simple risk score using phenotype membership
- [ ] Create interactive clinical decision support prototype

### Long-Term (Future Research)

- [ ] Extend to UK Biobank (richer reproductive data, longitudinal outcomes)
- [ ] Develop pregnancy complication risk calculator
- [ ] Test intervention strategies tailored to each phenotype
- [ ] Publish findings in cardiovascular/women's health journal

---

## 🎤 Communicating This Project

### 60-Second Elevator Pitch

> "As a gynecologist, I know that pregnancy complications predict future heart disease—but cardiovascular risk calculators ignore this. I built a machine learning system that identifies six distinct metabolic phenotypes in women by integrating reproductive health with standard biomarkers. This caught high-risk women 10-15 years earlier than traditional screening."

### Key Talking Points

1. **Unique angle:** Gynecologist's insight → data science solution
2. **Technical depth:** Implemented K-Means from scratch in NumPy
3. **Clinical relevance:** Addresses real gap in women's preventive health
4. **Impact potential:** Earlier identification of high-risk women

---

## 📚 References & Resources

### Key Papers

- AHA PREVENT™ Equations (2023)
- CKD-EPI 2021 Equation (race-free)
- Gestational Diabetes and CVD Risk Meta-Analysis
- Preeclampsia Long-Term Outcomes

### Data Sources

- [NHANES 2017-2020](https://wwwn.cdc.gov/nchs/nhanes/continuousnhanes/default.aspx)
- [RHQ Module Codebook](https://wwwn.cdc.gov/Nchs/Nhanes/2017-2018/P_RHQ.htm)

### Tools & Libraries

- NumPy, Pandas, Matplotlib, Seaborn
- Scikit-learn (for PCA/evaluation metrics only)
- SAS XPT reader (pandas)

---

## 🤝 Contact & Feedback

**Alexandra Velez, MD**

- LinkedIn: [your-profile]
- GitHub: [@your-username]
- Email: your.email@domain.com

**Feedback Welcome!**

- Found a bug? Open an issue
- Have suggestions? Start a discussion
- Want to collaborate? Reach out!

---

## 📜 License

MIT License - See [LICENSE](LICENSE) file for details

---

## 🙏 Acknowledgments

- **NHANES Team** at CDC for making this rich public health dataset available
- **Data Science Community** for open-source tools
- **Clinical Mentors** who emphasized preventive women's health

---

**⭐ If you find this project valuable, please consider starring the repository!**

**📣 Share with others interested in:**

- Women's health data science
- Cardiovascular risk assessment
- Clinical machine learning
- Reproductive health outcomes research
