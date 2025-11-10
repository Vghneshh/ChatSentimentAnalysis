# Troubleshooting 404 Errors - Model Files Not Found

## Problem
The Google Drive links for the model files are returning 404 errors. This means the files have been:
- Deleted
- Moved to a different location
- Had their sharing permissions changed
- The links have expired

## Current Status

✅ **Available:**
- `Text/model/deepmoji_weights.hdf5` - Already downloaded

❌ **Missing (404 errors):**
- `Text/sentiment/finetuned/twitter_ss.hdf5`
- `Text/sentiment/finetuned/youtube_ss.hdf5`
- `Image/c3d_sentiment.hdf5`

## Solutions

### Option 1: Contact Repository Owner
The original repository owner may have updated links or can provide access:
- Repository: ChatSentimentAnalysis (GitHub)
- Email: oisin097@hotmail.com (from README)

### Option 2: Train Models from Scratch

#### For Text Models (Twitter/YouTube):
You can finetune the models yourself using the existing DeepMoji weights:

1. **You need:**
   - `Text/model/deepmoji_weights.hdf5` ✅ (already have)
   - Training data (SS-Twitter and SS-YouTube datasets)
   - Python environment with dependencies

2. **Training scripts exist:**
   - `Text/examples/finetune_youtube_last.py` - Example for YouTube
   - `Text/scripts/finetune_dataset.py` - General finetuning script

3. **Steps:**
   ```bash
   # Install dependencies
   pip install -r requirements.txt
   
   # The training data should be in Text/data/SS-Twitter/ and Text/data/SS-Youtube/
   # Check if raw.pickle files exist there
   
   # Run finetuning (example)
   cd Text
   python examples/finetune_youtube_last.py
   ```

#### For C3D Image Model:
You can train the C3D model if you have training data:

1. **You need:**
   - Training images (GIFs) labeled as positive/negative
   - C3D base weights (C3D_Sport1M_weights.h5)

2. **Training script:**
   - `Image/training/train_C3D.py`

3. **Steps:**
   ```bash
   # Place training data in Image/training/data/train/pos and Image/training/data/train/neg
   # Place validation data in Image/training/data/validation/pos and Image/training/data/validation/neg
   
   cd Image/training
   python train_C3D.py
   ```

### Option 3: Use Partial Functionality

You can still use parts of the project that don't require the missing models:

1. **Emoji Sentiment** - Works without models:
   ```bash
   python testEmojiSentiment.py
   ```

2. **Text Sentiment** - Requires only DeepMoji weights (which you have):
   - You may need to finetune on your own data
   - Or use the base DeepMoji model directly

### Option 4: Search for Alternative Sources

Try searching for:
- "DeepMoji SS-Twitter finetuned model"
- "DeepMoji SS-YouTube finetuned model"
- "C3D sentiment model hdf5"
- Check if the models are available on:
  - Hugging Face
  - Model Zoo repositories
  - Academic paper supplementary materials

### Option 5: Check Repository Issues/Forks

1. Check the original GitHub repository for:
   - Updated links in issues
   - Alternative download methods
   - Community-provided mirrors

2. Check forks of the repository - someone may have:
   - Re-uploaded the models
   - Provided alternative links
   - Created updated versions

## What You Can Do Right Now

### Test What Works:
```bash
# Test emoji sentiment (should work)
python testEmojiSentiment.py

# Test text sentiment (may work with base model)
python testTextSentiment.py
```

### Check Available Data:
```bash
# Check if training data exists
dir Text\data\SS-Twitter
dir Text\data\SS-Youtube
```

If training data exists, you can train the models yourself!

## Next Steps

1. **Try Option 1 first** - Contact the repository owner
2. **Check if training data exists** - If yes, train models (Option 2)
3. **Search for alternatives** - Look for re-uploaded models (Option 4)
4. **Use partial functionality** - Test what works without missing models (Option 3)

## Need Help?

If you have the training data and want to train the models, I can help you:
- Set up the training environment
- Configure the training scripts
- Debug any training issues

Let me know which option you'd like to pursue!

