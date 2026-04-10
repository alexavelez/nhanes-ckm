## 📓 Notebooks

Analysis notebooks are numbered by execution order:

1. **01_reproductive_feature_engineering.ipynb**
   - Explores raw NHANES reproductive health data
   - Engineers pregnancy outcome features (APO score, parity, etc.)
   - Output: `reproductive_features.csv`

2. **02_ckm_integration_and_cohorts.ipynb**
   - Integrates CKM biomarkers with reproductive features
   - Defines analysis cohorts (population-level and pregnancy-informed)
   - Output: `cohort1_population.csv`, `cohort2_pregnancy.csv`

3. **03_population_ckm_clustering.ipynb**
   - K-Means clustering on all women (Cohort 1)
   - Identifies 6 CKM phenotypes
   - Examines APO distribution across phenotypes

4. **04_pregnancy_ckm_clustering.ipynb**
   - K-Means clustering on parous women (Cohort 2)
   - Pregnancy-informed phenotypes
   - APO as clustering feature

Run notebooks in order for reproducibility.