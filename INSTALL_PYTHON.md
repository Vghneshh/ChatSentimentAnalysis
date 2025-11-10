# Install Python 3.6 - Step by Step Guide

## Why Python 3.6?

This project requires Python 3.6 specifically because it uses older versions of TensorFlow (1.8.0) and Keras (2.0.9) that are compatible with Python 3.6.

## Installation Options

### Option 1: Download from Python.org (Recommended)

1. **Download Python 3.6:**
   - Go to: https://www.python.org/downloads/release/python-360/
   - Download: **Windows x86-64 executable installer** (or x86 if you have 32-bit Windows)
   - File will be named something like: `python-3.6.0-amd64.exe`

2. **Install Python:**
   - Run the installer
   - **IMPORTANT:** Check "Add Python 3.6 to PATH" at the bottom
   - Click "Install Now"
   - Wait for installation to complete

3. **Verify Installation:**
   - Open a new PowerShell/Command Prompt
   - Run: `python --version`
   - You should see: `Python 3.6.x`

### Option 2: Microsoft Store

1. Open Microsoft Store
2. Search for "Python 3.6"
3. Install Python 3.6
4. Note: May need to use `python3` or `py -3.6` instead of `python`

### Option 3: Anaconda (For Data Science)

1. Download Anaconda: https://www.anaconda.com/products/individual
2. Install Anaconda
3. Create Python 3.6 environment:
   ```bash
   conda create -n sentiment python=3.6
   conda activate sentiment
   ```

## After Installation

1. **Close and reopen your terminal** (important for PATH to update)

2. **Verify Python:**
   ```bash
   python --version
   ```

3. **Install dependencies:**
   ```bash
   cd C:\Users\ADMIN\Documents\ChatSentimentAnalysis-master
   pip install -r requirements.txt
   ```

4. **Install the deepmoji package:**
   ```bash
   cd Text
   pip install -e .
   cd ..
   ```

## Troubleshooting

### Python not found after installation
- Close and reopen your terminal
- Check if Python is in PATH: `where python`
- If not, add Python to PATH manually:
  1. Search "Environment Variables" in Windows
  2. Edit "Path" variable
  3. Add: `C:\Python36` and `C:\Python36\Scripts`

### Wrong Python version
- Make sure you installed Python 3.6, not 3.7+
- Check version: `python --version`
- Should show: `Python 3.6.x`

### pip not found
- Python 3.6 should include pip
- Try: `python -m pip --version`
- If not found, install pip manually

## Next Steps After Python Installation

Once Python 3.6 is installed, you can:

1. **Test the project:**
   ```bash
   python testEmojiSentiment.py
   ```

2. **Train the missing models:**
   ```bash
   python train_twitter_model.py
   python train_youtube_model.py
   ```

3. **Run full sentiment analysis:**
   ```bash
   python testSentimentAnalysis.py
   ```

## Quick Setup Script

After installing Python, run:
```bash
python setup_project.py
```

This will install all dependencies and set up the project.

