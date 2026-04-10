#!/usr/bin/env python3
"""
NHANES Data Acquisition Script
Downloads all required modules for Women's CKM Phenotyping Project

Author: Alexandra Velez
Date: February 2026

Data Source: NHANES 2017-March 2020 Pre-Pandemic Cycle
CDC Public Data Files
"""

import requests
from pathlib import Path
import sys

# All NHANES modules needed for the project
# Updated URLs - correct as of February 2026
NHANES_MODULES = {
    'P_DEMO.XPT': {
        'url': 'https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/2017/DataFiles/P_DEMO.xpt',
        'description': 'Demographics'
    },
    'P_BMX.XPT': {
        'url': 'https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/2017/DataFiles/P_BMX.xpt',
        'description': 'Body Measures'
    },
    'P_BPXO.XPT': {
        'url': 'https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/2017/DataFiles/P_BPXO.xpt',
        'description': 'Blood Pressure (Oscillometric)'
    },
    'P_GHB.XPT': {
        'url': 'https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/2017/DataFiles/P_GHB.xpt',
        'description': 'Glycohemoglobin'
    },
    'P_BIOPRO.XPT': {
        'url': 'https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/2017/DataFiles/P_BIOPRO.xpt',
        'description': 'Biochemistry Profile'
    },
    'P_RHQ.XPT': {
        'url': 'https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/2017/DataFiles/P_RHQ.xpt',
        'description': 'Reproductive Health Questionnaire'
    },
}

def download_file(url, filepath, description):
    """
    Download a single file from NHANES
    
    Parameters:
    -----------
    url : str
        Direct download URL
    filepath : Path
        Where to save the file
    description : str
        Human-readable description for logging
    
    Returns:
    --------
    bool : True if successful, False otherwise
    """
    try:
        print(f"📥 Downloading {description} ({filepath.name})...")
        
        # Make the request with a timeout
        response = requests.get(url, timeout=60)
        response.raise_for_status()  # Raises exception for 4XX/5XX errors
        
        # Save the file
        with open(filepath, 'wb') as f:
            f.write(response.content)
        
        # Get file size for verification
        file_size_mb = filepath.stat().st_size / (1024 * 1024)
        print(f"   ✅ Downloaded successfully ({file_size_mb:.2f} MB)")
        return True
        
    except requests.exceptions.Timeout:
        print(f"   ❌ Download timeout - server took too long to respond")
        return False
    except requests.exceptions.RequestException as e:
        print(f"   ❌ Download failed: {e}")
        return False
    except Exception as e:
        print(f"   ❌ Unexpected error: {e}")
        return False

def download_all_modules():
    """
    Download all NHANES modules needed for the project
    """
    print("="*80)
    print("NHANES DATA ACQUISITION")
    print("Women's CKM Phenotyping Project")
    print("="*80)
    print()
    
    # Create data directory if it doesn't exist
    data_dir = Path("data/raw")
    data_dir.mkdir(parents=True, exist_ok=True)
    print(f"📁 Data directory: {data_dir.absolute()}")
    print()
    
    # Track statistics
    total_files = len(NHANES_MODULES)
    downloaded = 0
    skipped = 0
    failed = 0
    
    # Download each module
    for filename, info in NHANES_MODULES.items():
        filepath = data_dir / filename
        
        # Check if file already exists
        if filepath.exists():
            file_size_mb = filepath.stat().st_size / (1024 * 1024)
            print(f"⏭️  {info['description']} ({filename})")
            print(f"   Already exists ({file_size_mb:.2f} MB) - skipping")
            skipped += 1
            print()
            continue
        
        # Download the file
        success = download_file(info['url'], filepath, info['description'])
        
        if success:
            downloaded += 1
        else:
            failed += 1
        
        print()
    
    # Summary
    print("="*80)
    print("DOWNLOAD SUMMARY")
    print("="*80)
    print(f"✅ Successfully downloaded: {downloaded}/{total_files}")
    print(f"⏭️  Already existed:        {skipped}/{total_files}")
    print(f"❌ Failed:                 {failed}/{total_files}")
    print()
    
    if failed > 0:
        print("⚠️  Some downloads failed. You can:")
        print("   1. Run this script again (it will retry failed files)")
        print("   2. Manually download from: https://wwwn.cdc.gov/nchs/nhanes/")
        print()
        return False
    
    if downloaded > 0 or skipped == total_files:
        print("🎉 Data acquisition complete!")
        print()
        print("📊 Total data size:", end=" ")
        total_size = sum((data_dir / f).stat().st_size for f in NHANES_MODULES.keys() 
                         if (data_dir / f).exists())
        print(f"{total_size / (1024 * 1024):.2f} MB")
        print()
        print("🚀 Next steps:")
        print("   1. Run notebooks/00_EXPLORATION.ipynb to explore the data")
        print("   2. See README.md for analysis workflow")
        print()
        return True

def verify_downloads():
    """
    Verify all required files exist
    """
    data_dir = Path("data/raw")
    missing = []
    
    print("="*80)
    print("VERIFYING NHANES DATA FILES")
    print("="*80)
    print()
    
    for filename in NHANES_MODULES.keys():
        filepath = data_dir / filename
        if filepath.exists():
            file_size_mb = filepath.stat().st_size / (1024 * 1024)
            print(f"✅ {filename:15s} - {file_size_mb:6.2f} MB")
        else:
            print(f"❌ {filename:15s} - MISSING")
            missing.append(filename)
    
    print()
    
    if missing:
        print(f"❌ {len(missing)} file(s) missing. Run without --verify to download.")
        return False
    else:
        print("✅ All required files present!")
        return True

if __name__ == "__main__":
    # Check if user wants to verify instead of download
    if len(sys.argv) > 1 and sys.argv[1] == "--verify":
        verify_downloads()
    else:
        download_all_modules()