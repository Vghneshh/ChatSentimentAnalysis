# Release & Model Download Instructions

This document explains options for distributing the large model files used by this project and how to download them if you did not fetch them via Git LFS.

## Recommended (Git LFS)
- The repository tracks `.hdf5` files via Git LFS. If you cloned the repo normally, run:

```powershell
git lfs install
git lfs pull
```

This will download the large model files tracked by LFS.

## Manual download (alternative)
If you prefer to fetch model files manually (or if LFS is not used), download the files listed below and place them in the exact paths.

Files to download and where to save them:

1. DeepMoji base weights
   - URL: (Dropbox link included in project docs)
   - Save to: `Text/model/deepmoji_weights.hdf5`

2. SS-Twitter finetuned model
   - Save to: `Text/sentiment/finetuned/twitter_ss.hdf5`

3. SS-YouTube finetuned model
   - Save to: `Text/sentiment/finetuned/youtube_ss.hdf5`

4. C3D image sentiment model (optional)
   - Save to: `Image/c3d_sentiment.hdf5`

> See `DOWNLOAD_INSTRUCTIONS.md` and `DOWNLOAD_STATUS.txt` in the repo for the original links and troubleshooting steps.

## Release assets on GitHub (recommended for sharing)
- If you want stable direct downloads without LFS, create a GitHub Release and attach the model files as release assets. Then include direct links in this file.

## Verifying model files
After downloading, verify file size (quick check):

```powershell
Get-Item Text\sentiment\finetuned\twitter_ss.hdf5 | Select-Object Name,@{n='SizeMB';e={[math]::Round($_.Length/1MB,2)}}
```

You can also check integrity with `Get-FileHash` (SHA256):

```powershell
Get-FileHash Text\sentiment\finetuned\twitter_ss.hdf5 -Algorithm SHA256
```

## Notes
- Model files are large (~150–200 MB each). Use a reliable internet connection.
- If you plan to distribute models with the repo, Git LFS is the most convenient method. If you expect many collaborators, consider hosting models on GitHub Releases, S3, or another CDN.
