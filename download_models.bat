@echo off
echo ============================================================
echo ChatSentimentAnalysis - Model Files Downloader
echo ============================================================
echo.
echo This will open download links in your browser.
echo Please save each file to the correct location:
echo.
echo 1. Twitter Model - Save to: Text\sentiment\finetuned\twitter_ss.hdf5
echo 2. YouTube Model - Save to: Text\sentiment\finetuned\youtube_ss.hdf5
echo 3. DeepMoji Weights - Save to: Text\model\deepmoji_weights.hdf5
echo 4. C3D Model - Save to: Image\c3d_sentiment.hdf5
echo.
pause

echo.
echo Opening download links...
echo.

start https://drive.google.com/open?id=1ZLD2iSgl4PggYPAG9iG_eoFx2DEegqSL
timeout /t 3 /nobreak >nul

start https://drive.google.com/open?id=1iWc0sUmk7FwXBFPQ8FOIWKhJ8jS2iplh
timeout /t 3 /nobreak >nul

start https://www.dropbox.com/s/xqarafsl6a8f9ny/deepmoji_weights.hdf5?dl=0
timeout /t 3 /nobreak >nul

start https://drive.google.com/open?id=1UeEsQYrItUF0NOpD1frvS8qxdqGCUTg9
timeout /t 3 /nobreak >nul

echo.
echo All download links have been opened in your browser.
echo.
echo IMPORTANT: For Google Drive files:
echo   1. Click the download button or use the download icon
echo   2. If you see a virus scan warning, click "Download anyway"
echo   3. Save the file to the correct location shown above
echo.
echo For Dropbox file:
echo   1. Click the download button
echo   2. Save the file to the correct location shown above
echo.
pause

