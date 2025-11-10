@echo off
echo Opening download links in your browser...
echo.
echo Please download and save files to:
echo   Text\sentiment\finetuned\twitter_ss.hdf5
echo   Text\sentiment\finetuned\youtube_ss.hdf5
echo   Text\model\deepmoji_weights.hdf5
echo   Image\c3d_sentiment.hdf5
echo.

start "" "https://drive.google.com/open?id=1ZLD2iSgl4PggYPAG9iG_eoFx2DEegqSL"
ping 127.0.0.1 -n 2 >nul

start "" "https://drive.google.com/open?id=1iWc0sUmk7FwXBFPQ8FOIWKhJ8jS2iplh"
ping 127.0.0.1 -n 2 >nul

start "" "https://www.dropbox.com/s/xqarafsl6a8f9ny/deepmoji_weights.hdf5?dl=0"
ping 127.0.0.1 -n 2 >nul

start "" "https://drive.google.com/open?id=1UeEsQYrItUF0NOpD1frvS8qxdqGCUTg9"

echo.
echo All links opened! Check your browser.
echo See DOWNLOAD_INSTRUCTIONS.md for detailed steps.
pause

