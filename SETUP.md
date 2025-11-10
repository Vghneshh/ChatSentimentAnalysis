# Setup Guide for ChatSentimentAnalysis

This guide will help you set up and run the ChatSentimentAnalysis project.

## Prerequisites

- Python 3.6 (required as per project specifications)
- pip (Python package installer)

## Step 1: Install Python Dependencies

Install all required Python packages using pip:

```bash
pip install -r requirements.txt
```

**Note:** This project uses older versions of TensorFlow (1.8.0) and Keras (2.0.9). If you encounter compatibility issues with newer Python versions, you may need to:
- Use Python 3.6 specifically
- Or consider updating the dependencies (though this may require code modifications)

## Step 2: Download Required Model Files

The project requires several pre-trained model files that need to be downloaded manually:

### 2.1 DeepMoji Models

1. **DeepMoji SS-Twitter Model:**
   - Download from: https://drive.google.com/open?id=1ZLD2iSgl4PggYPAG9iG_eoFx2DEegqSL
   - Place as: `Text/sentiment/finetuned/twitter_ss.hdf5`

2. **DeepMoji SS-YouTube Model:**
   - Download from: https://drive.google.com/open?id=1iWc0sUmk7FwXBFPQ8FOIWKhJ8jS2iplh
   - Place as: `Text/sentiment/finetuned/youtube_ss.hdf5`

3. **DeepMoji Weights:**
   - Download from: https://www.dropbox.com/s/xqarafsl6a8f9ny/deepmoji_weights.hdf5?dl=0
   - Place as: `Text/model/deepmoji_weights.hdf5`

### 2.2 C3D Image Model

1. **C3D Sentiment Model:**
   - Download from: https://drive.google.com/open?id=1UeEsQYrItUF0NOpD1frvS8qxdqGCUTg9
   - Place as: `Image/c3d_sentiment.hdf5`

## Step 3: Verify Directory Structure

Ensure your project has the following structure:

```
ChatSentimentAnalysis-master/
├── Text/
│   ├── sentiment/
│   │   └── finetuned/
│   │       ├── twitter_ss.hdf5
│   │       └── youtube_ss.hdf5
│   └── model/
│       ├── vocabulary.json (already included)
│       └── deepmoji_weights.hdf5
├── Image/
│   └── c3d_sentiment.hdf5
├── Emoji/
├── requirements.txt
└── ... (other project files)
```

## Step 4: Run the Project

### Test Individual Components

1. **Test Emoji Sentiment:**
   ```bash
   python testEmojiSentiment.py
   ```

2. **Test Text Sentiment:**
   ```bash
   python testTextSentiment.py
   ```

3. **Test Image Sentiment:**
   ```bash
   python testImageSentiment.py
   ```

### Test Full Sentiment Analysis

Run the main test:
```bash
python testSentimentAnalysis.py
```

This will:
- Load all models (this may take a few minutes)
- Test sentiment analysis on sample sentences containing text, emojis, and images
- Display sentiment scores for each sentence

## Troubleshooting

### Common Issues

1. **Import Errors:**
   - Make sure you've installed all dependencies: `pip install -r requirements.txt`
   - Ensure you're running from the project root directory

2. **Model File Not Found:**
   - Verify all model files are downloaded and placed in the correct directories
   - Check file names match exactly (case-sensitive)

3. **TensorFlow/Keras Compatibility:**
   - This project uses TensorFlow 1.8.0 and Keras 2.0.9
   - If you have issues, try using Python 3.6 with a virtual environment

4. **Memory Issues:**
   - Loading models requires significant RAM
   - Close other applications if you encounter memory errors

### Creating a Virtual Environment (Recommended)

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## Usage Example

```python
from SentimentAnalysis import load_models, get_sentiments

# Load models (do this once)
image_model, text_model_ensemble = load_models()

# Analyze sentiment
sentences = [
    'we lost 😒 😅 😛 <img>https://media.giphy.com/media/2rtQMJvhzOnRe/giphy.gif</img>',
    'wow you are so funny 👮',
    'you suck 😂'
]

sentiments = get_sentiments(sentences, image_model, text_model_ensemble)

for sentence, sentiment in zip(sentences, sentiments):
    print(f"{sentence} | {sentiment}")
```

## Notes

- The first time you run the project, model loading may take several minutes
- Image sentiment analysis requires downloading GIFs from URLs, which may take time
- Sentiment scores range from -1 (negative) to +1 (positive)

