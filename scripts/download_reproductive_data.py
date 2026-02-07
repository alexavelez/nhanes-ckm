#!/usr/bin/env python3
"""
NHANES Reproductive Health Data Acquisition Script
Downloads and explores the RHQ (Reproductive Health Questionnaire) module
"""

import pandas as pd
import requests
from pathlib import Path

def download_nhanes_module(url, save_path):
    """Download NHANES .XPT file"""
    print(f"📥 Downloading from {url}...")
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        
        save_path.parent.mkdir(parents=True, exist_ok=True)
        with open(save_path, 'wb') as f:
            f.write(response.content)
        
        print(f"✅ Saved to {save_path}")
        return True
    except Exception as e:
        print(f"❌ Download failed: {e}")
        return False

def explore_reproductive_health_module(file_path):
    """Load and summarize RHQ module"""
    print(f"\n📊 Loading {file_path.name}...")
    
    try:
        df = pd.read_sas(file_path, format='xport')
        print(f"✅ Loaded successfully!")
        print(f"   Shape: {df.shape[0]:,} participants × {df.shape[1]} variables")
        
        print("\n" + "="*80)
        print("AVAILABLE REPRODUCTIVE HEALTH VARIABLES")
        print("="*80)
        
        # Show all variable names
        print(f"\nColumn names ({len(df.columns)} total):")
        for i, col in enumerate(df.columns, 1):
            non_null = df[col].notna().sum()
            pct_available = (non_null / len(df)) * 100
            print(f"  {i:2d}. {col:12s} - {non_null:5,} non-null ({pct_available:5.1f}%)")
        
        print("\n" + "="*80)
        print("KEY REPRODUCTIVE VARIABLES - CLINICAL MAPPING")
        print("="*80)
        
        # Key variables we're looking for
        key_vars = {
            'RHQ031': 'Ever been pregnant',
            'RHD042': 'Number of live births',
            'RHD043': 'Age when delivered last baby', 
            'RHQ131': 'Ever been told you had gestational diabetes',
            'RHQ162': 'Ever been told you had preeclampsia',
            'RHD018': 'Age at first menstrual period',
            'RHQ031': 'Had regular periods in past 12 months',
            'RHQ060': 'Age at last menstrual period',
            'RHQ420': 'Ever taken birth control pills',
        }
        
        found_vars = []
        missing_vars = []
        
        for var, description in key_vars.items():
            if var in df.columns:
                found_vars.append((var, description))
                non_null = df[var].notna().sum()
                pct = (non_null / len(df)) * 100
                print(f"✅ {var:10s}: {description:50s} [{non_null:5,} ({pct:5.1f}%)]")
            else:
                missing_vars.append((var, description))
                print(f"❌ {var:10s}: {description:50s} [NOT FOUND]")
        
        print(f"\n📈 Summary: {len(found_vars)}/{len(key_vars)} key variables found")
        
        # Save quick summary
        summary_df = pd.DataFrame({
            'Variable': df.columns,
            'Non_Null_Count': [df[col].notna().sum() for col in df.columns],
            'Percent_Available': [(df[col].notna().sum() / len(df)) * 100 for col in df.columns]
        })
        
        return df, summary_df
        
    except Exception as e:
        print(f"❌ Error loading file: {e}")
        return None, None

def main():
    """Main execution"""
    
    print("="*80)
    print("NHANES REPRODUCTIVE HEALTH DATA ACQUISITION")
    print("="*80)
    
    # NHANES 2017-March 2020 Pre-Pandemic Reproductive Health Questionnaire
    # URL for the RHQ module
    rhq_url = "https://wwwn.cdc.gov/Nchs/Nhanes/2017-2018/P_RHQ.XPT"
    
    # Save location (adjust this to match your project structure)
    data_dir = Path("data/raw")
    rhq_file = data_dir / "P_RHQ.XPT"
    
    # Download
    success = download_nhanes_module(rhq_url, rhq_file)
    
    if success:
        # Explore
        df_rhq, summary = explore_reproductive_health_module(rhq_file)
        
        if df_rhq is not None:
            # Save variable summary
            summary_path = data_dir / "RHQ_variable_summary.csv"
            summary.to_csv(summary_path, index=False)
            print(f"\n💾 Variable summary saved to: {summary_path}")
            
            print("\n" + "="*80)
            print("NEXT STEPS")
            print("="*80)
            print("""
✅ RHQ module downloaded successfully!
            """)
        
    else:
        print("\n⚠️  Download failed. You can manually download from:")
        print(f"   {rhq_url}")
        print(f"\n   Save it to: {rhq_file}")

if __name__ == "__main__":
    main()
