# NHANES Data Files

## Source

National Health and Nutrition Examination Survey (NHANES)  
Cycle: 2017-March 2020 Pre-Pandemic  
Source: https://wwwn.cdc.gov/nchs/nhanes/

## Files Required

| File         | Module                            | URL                                                     |
| ------------ | --------------------------------- | ------------------------------------------------------- |
| P_DEMO.XPT   | Demographics                      | https://wwwn.cdc.gov/Nchs/Nhanes/2017-2018/P_DEMO.XPT   |
| P_BMX.XPT    | Body Measures                     | https://wwwn.cdc.gov/Nchs/Nhanes/2017-2018/P_BMX.XPT    |
| P_BPXO.XPT   | Blood Pressure (Oscillometric)    | https://wwwn.cdc.gov/Nchs/Nhanes/2017-2018/P_BPXO.XPT   |
| P_GHB.XPT    | Glycohemoglobin                   | https://wwwn.cdc.gov/Nchs/Nhanes/2017-2018/P_GHB.XPT    |
| P_BIOPRO.XPT | Biochemistry Profile              | https://wwwn.cdc.gov/Nchs/Nhanes/2017-2018/P_BIOPRO.XPT |
| P_RHQ.XPT    | Reproductive Health Questionnaire | https://wwwn.cdc.gov/Nchs/Nhanes/2017-2018/P_RHQ.XPT    |

## How to Obtain

### Option 1: Automated Download (Recommended for Reproduction)

```bash
python scripts/download_nhanes_data.py
```

### Option 2: Manual Download (What I Did)

1. Visit URLs above
2. Save .XPT files to `data/raw/`
3. Files are not included in repository due to size

## Data Not Included in Repository

Raw .XPT files are excluded from version control (see .gitignore).
Total size: ~150MB

## Last Updated

February 2026
