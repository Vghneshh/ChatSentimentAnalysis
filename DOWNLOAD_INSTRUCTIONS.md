# Download Instructions for Model Files

## Quick Download (Windows)

Double-click `download_models.bat` to open all download links in your browser.

## Manual Download Steps

### 1. DeepMoji SS-Twitter Model
- **Link:** https://drive.google.com/open?id=1ZLD2iSgl4PggYPAG9iG_eoFx2DEegqSL
- **Save to:** `Text/sentiment/finetuned/twitter_ss.hdf5`
- **Instructions:**
  1. Click the link above
  2. Click the download button (or right-click → Download)
  3. If you see a virus scan warning, click "Download anyway"
  4. Move the downloaded file to `Text/sentiment/finetuned/twitter_ss.hdf5`

### 2. DeepMoji SS-YouTube Model
- **Link:** https://drive.google.com/open?id=1iWc0sUmk7FwXBFPQ8FOIWKhJ8jS2iplh
- **Save to:** `Text/sentiment/finetuned/youtube_ss.hdf5`
- **Instructions:**
  1. Click the link above
  2. Click the download button (or right-click → Download)
  3. If you see a virus scan warning, click "Download anyway"
  4. Move the downloaded file to `Text/sentiment/finetuned/youtube_ss.hdf5`

### 3. DeepMoji Weights
- **Link:** https://www.dropbox.com/s/xqarafsl6a8f9ny/deepmoji_weights.hdf5?dl=0
- **Save to:** `Text/model/deepmoji_weights.hdf5`
- **Instructions:**
  1. Click the link above
  2. Click the "Download" button
  3. Move the downloaded file to `Text/model/deepmoji_weights.hdf5`

### 4. C3D Sentiment Model
- **Link:** https://drive.google.com/open?id=1UeEsQYrItUF0NOpD1frvS8qxdqGCUTg9
- **Save to:** `Image/c3d_sentiment.hdf5`
- **Instructions:**
  1. Click the link above
  2. Click the download button (or right-click → Download)
  3. If you see a virus scan warning, click "Download anyway"
  4. Move the downloaded file to `Image/c3d_sentiment.hdf5`

## Using Python Script (If Python is installed)

If you have Python installed, you can use the automated download script:

```bash
# Install gdown for Google Drive downloads
pip install gdown

# Run the download script
python download_models.py
```

## Verify Downloads

After downloading, verify that all files exist:

```
Text/sentiment/finetuned/twitter_ss.hdf5
Text/sentiment/finetuned/youtube_ss.hdf5
Text/model/deepmoji_weights.hdf5
Image/c3d_sentiment.hdf5
```

All files should be several MB in size (model files are typically 50-500 MB each).

## Troubleshooting

### Google Drive Downloads
- If download doesn't start automatically, right-click the file and select "Download"
- Large files may show a virus scan warning - click "Download anyway"
- If you get "Download quota exceeded", wait a few hours and try again

### File Size Issues
- Model files are large (50-500 MB each)
- If a file is very small (< 1 MB), the download likely failed
- Re-download the file if it seems corrupted

### File Location
- Make sure files are saved with the exact names shown above
- File names are case-sensitive: `twitter_ss.hdf5` not `Twitter_SS.hdf5`

