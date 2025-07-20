#!/usr/bin/env python3
"""
Setup script for Airbnb Data Analysis Project
"""

import subprocess
import sys
import os
from pathlib import Path

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error during {description}: {e}")
        print(f"Error output: {e.stderr}")
        return False

def main():
    print("🚀 Setting up Airbnb Data Analysis Environment\n")
    
    # Check if Python is available
    print("📋 Checking Python version...")
    python_version = sys.version_info
    print(f"   Python {python_version.major}.{python_version.minor}.{python_version.micro}")
    
    if python_version < (3, 8):
        print("❌ Python 3.8 or higher is required!")
        return False
    
    # Check if pip is available
    print("\n📦 Checking pip...")
    if not run_command("pip --version", "Checking pip"):
        print("❌ pip is not available. Please install pip first.")
        return False
    
    # Upgrade pip
    print("\n⬆️ Upgrading pip...")
    run_command("python -m pip install --upgrade pip", "Upgrading pip")
    
    # Install core requirements
    print("\n📚 Installing core packages...")
    if not run_command("pip install -r requirements.txt", "Installing requirements"):
        print("❌ Failed to install requirements!")
        return False
    
    # Install Jupyter kernel
    print("\n📓 Setting up Jupyter...")
    run_command("python -m ipykernel install --user --name=airbnb_analysis", "Installing Jupyter kernel")
    
    # Create data directory if it doesn't exist
    data_dir = Path("data")
    data_dir.mkdir(exist_ok=True)
    print(f"📁 Created data directory: {data_dir}")
    
    print("\n✅ Setup completed successfully!")
    print("\n🎯 Next steps:")
    print("1. Activate your virtual environment (if using one)")
    print("2. Start Jupyter: jupyter notebook")
    print("3. Open airbnb_analysis.ipynb")
    print("4. Run the analysis cells")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 