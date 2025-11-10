#!/usr/bin/env python
"""
Setup script for ChatSentimentAnalysis project.
Installs dependencies and sets up the project.
"""

import os
import sys
import subprocess

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"\n{description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, 
                               capture_output=True, text=True)
        print(f"✓ {description} completed successfully")
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Error: {e}")
        if e.stdout:
            print(f"Output: {e.stdout}")
        if e.stderr:
            print(f"Error: {e.stderr}")
        return False

def check_python_version():
    """Check if Python 3.6 is installed"""
    print("Checking Python version...")
    version = sys.version_info
    if version.major == 3 and version.minor == 6:
        print(f"✓ Python {version.major}.{version.minor}.{version.micro} detected")
        return True
    else:
        print(f"⚠ Warning: Python {version.major}.{version.minor}.{version.micro} detected")
        print("This project is designed for Python 3.6")
        print("You may encounter compatibility issues with newer versions")
        response = input("Continue anyway? (y/n): ")
        return response.lower() in ['y', 'yes']

def main():
    print("=" * 60)
    print("ChatSentimentAnalysis - Project Setup")
    print("=" * 60)
    
    # Check Python version
    if not check_python_version():
        print("\nPlease install Python 3.6 and try again.")
        print("See INSTALL_PYTHON.md for instructions.")
        sys.exit(1)
    
    # Check if requirements.txt exists
    if not os.path.exists('requirements.txt'):
        print("\n✗ requirements.txt not found!")
        print("Please run this script from the project root directory.")
        sys.exit(1)
    
    # Install dependencies
    print("\n" + "=" * 60)
    print("Installing Dependencies")
    print("=" * 60)
    
    if not run_command("pip install -r requirements.txt", 
                      "Installing requirements"):
        print("\n⚠ Some dependencies may have failed to install.")
        print("This is common with older packages.")
        print("You may need to install some packages manually.")
    
    # Install deepmoji package
    print("\n" + "=" * 60)
    print("Setting up DeepMoji")
    print("=" * 60)
    
    if os.path.exists('Text/setup.py'):
        os.chdir('Text')
        if not run_command("pip install -e .", 
                          "Installing deepmoji package"):
            print("\n⚠ DeepMoji package installation failed.")
            print("You may need to install it manually:")
            print("  cd Text")
            print("  pip install -e .")
        os.chdir('..')
    
    # Check for model files
    print("\n" + "=" * 60)
    print("Checking Model Files")
    print("=" * 60)
    
    model_files = {
        'Text/model/deepmoji_weights.hdf5': 'DeepMoji Base Weights',
        'Text/sentiment/finetuned/twitter_ss.hdf5': 'Twitter Model',
        'Text/sentiment/finetuned/youtube_ss.hdf5': 'YouTube Model',
        'Image/c3d_sentiment.hdf5': 'C3D Image Model'
    }
    
    missing = []
    for file_path, name in model_files.items():
        if os.path.exists(file_path):
            size_mb = os.path.getsize(file_path) / (1024 * 1024)
            print(f"✓ {name}: {file_path} ({size_mb:.2f} MB)")
        else:
            print(f"✗ {name}: {file_path} - MISSING")
            missing.append(name)
    
    if missing:
        print("\n⚠ Missing model files:")
        for name in missing:
            print(f"  - {name}")
        print("\nYou can:")
        print("1. Train the models using train_twitter_model.py and train_youtube_model.py")
        print("2. Download from original sources (if available)")
        print("3. Use the base model (lower accuracy)")
    
    # Summary
    print("\n" + "=" * 60)
    print("Setup Complete!")
    print("=" * 60)
    
    print("\nNext steps:")
    print("1. Test emoji sentiment: python testEmojiSentiment.py")
    
    if 'Twitter Model' in missing or 'YouTube Model' in missing:
        print("2. Train missing models: python train_twitter_model.py")
        print("   (This will take several hours)")
    else:
        print("2. Test full sentiment: python testSentimentAnalysis.py")
    
    print("\nFor more information, see:")
    print("  - INSTALL_PYTHON.md - Python installation guide")
    print("  - SOLUTION_404.md - Solutions for missing models")
    print("  - TRAIN_MODELS.md - Guide for training models")

if __name__ == "__main__":
    main()

