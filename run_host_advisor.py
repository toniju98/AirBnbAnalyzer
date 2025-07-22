#!/usr/bin/env python3
"""
Launcher script for Airbnb Host Advisor - Copenhagen Example
"""

import subprocess
import sys
import os
from pathlib import Path

def main():
    print("🏠 Starting Airbnb Host Advisor - Copenhagen Example...")
    
    # Check if streamlit is installed
    try:
        import streamlit
        print(f"✅ Streamlit version: {streamlit.__version__}")
    except ImportError:
        print("❌ Streamlit not found. Installing...")
        subprocess.run([sys.executable, "-m", "pip", "install", "streamlit"])
    
    # Check if data files exist
    data_files = ['listings.csv', 'listings.csv.gz', 'reviews.csv', 'reviews.csv.gz', 'calendar.csv.gz']
    existing_files = [f for f in data_files if Path(f).exists()]
    
    if existing_files:
        print(f"✅ Found data files: {existing_files}")
    else:
        print("⚠️ No data files found. The app will show sample data.")
    
    # Launch Streamlit app
    print("🚀 Launching Streamlit app...")
    subprocess.run([
        sys.executable, "-m", "streamlit", "run", "airbnb_host_advisor.py",
        "--server.port", "8501",
        "--server.address", "localhost"
    ])

if __name__ == "__main__":
    main() 