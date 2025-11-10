# Quick Start Guide

## Step 1: Install Python 3.6

This project requires **Python 3.6**. You can download it from:
- https://www.python.org/downloads/release/python-360/
- Or use the Microsoft Store (search for "Python 3.6")

**Important:** Make sure to check "Add Python to PATH" during installation.

## Step 2: Verify Python Installation

Open PowerShell or Command Prompt and run:
```bash
python --version
```

You should see: `Python 3.6.x`

## Step 3: Install Dependencies

Navigate to the project directory and install dependencies:
```bash
cd C:\Users\ADMIN\Documents\ChatSentimentAnalysis-master
pip install -r requirements.txt
```

**Note:** If you encounter issues with TensorFlow 1.8.0 on newer systems, you may need to:
- Use a virtual environment
- Or upgrade dependencies (may require code changes)

## Step 4: Download Model Files

Before running the project, you need to download these model files:

1. **DeepMoji SS-Twitter Model** → `Text/sentiment/finetuned/twitter_ss.hdf5`
   - https://drive.google.com/open?id=1ZLD2iSgl4PggYPAG9iG_eoFx2DEegqSL

2. **DeepMoji SS-YouTube Model** → `Text/sentiment/finetuned/youtube_ss.hdf5`
   - https://drive.google.com/open?id=1iWc0sUmk7FwXBFPQ8FOIWKhJ8jS2iplh

3. **DeepMoji Weights** → `Text/model/deepmoji_weights.hdf5`
   - https://www.dropbox.com/s/xqarafsl6a8f9ny/deepmoji_weights.hdf5?dl=0

4. **C3D Sentiment Model** → `Image/c3d_sentiment.hdf5`
   - https://drive.google.com/open?id=1UeEsQYrItUF0NOpD1frvS8qxdqGCUTg9

**Important:** Create the `Text/sentiment/finetuned/` directory if it doesn't exist (already created).

## Step 5: Run the Project

### Test Individual Components:

```bash
# Test emoji sentiment
python testEmojiSentiment.py

# Test text sentiment
python testTextSentiment.py

# Test image sentiment
python testImageSentiment.py
```

### Test Full Sentiment Analysis:

```bash
python testSentimentAnalysis.py
```

## Troubleshooting

### Python Not Found
- Make sure Python is installed and added to PATH
- Try restarting your terminal after installation

### Module Not Found Errors
- Run: `pip install -r requirements.txt`
- Make sure you're in the project root directory

### Model File Errors
- Verify all model files are downloaded and in correct locations
- Check file names match exactly (case-sensitive)

### TensorFlow/Keras Issues
- This project uses old versions (TensorFlow 1.8.0, Keras 2.0.9)
- Consider using a virtual environment with Python 3.6

## Using Virtual Environment (Recommended)

```bash
# Create virtual environment
python -m venv venv

# Activate (Windows PowerShell)
.\venv\Scripts\Activate.ps1

# Activate (Windows CMD)
venv\Scripts\activate.bat

# Install dependencies
pip install -r requirements.txt
```

For more detailed information, see `SETUP.md`.

