#!/usr/bin/env python
"""
Script to download required model files for ChatSentimentAnalysis
Uses gdown for Google Drive downloads
"""

import os
import sys

def download_file(url, output_path):
    """Download a file from URL to output path"""
    try:
        import urllib.request
        print(f"Downloading: {output_path}")
        
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # Download the file
        urllib.request.urlretrieve(url, output_path)
        
        # Check if file was downloaded successfully
        if os.path.exists(output_path) and os.path.getsize(output_path) > 0:
            size_mb = os.path.getsize(output_path) / (1024 * 1024)
            print(f"[OK] Downloaded: {output_path} ({size_mb:.2f} MB)")
            return True
        else:
            print(f"[FAILED] File appears to be empty or missing")
            return False
    except Exception as e:
        print(f"[FAILED] Error: {str(e)}")
        return False

def download_google_drive(file_id, output_path):
    """Download from Google Drive using gdown"""
    try:
        import gdown
        print(f"Downloading from Google Drive: {output_path}")
        
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # Google Drive URL format
        url = f"https://drive.google.com/uc?id={file_id}"
        
        # Download using gdown
        gdown.download(url, output_path, quiet=False)
        
        # Check if file was downloaded successfully
        if os.path.exists(output_path) and os.path.getsize(output_path) > 0:
            size_mb = os.path.getsize(output_path) / (1024 * 1024)
            print(f"[OK] Downloaded: {output_path} ({size_mb:.2f} MB)")
            return True
        else:
            print(f"[FAILED] File appears to be empty or missing")
            return False
    except ImportError:
        print("[ERROR] gdown is not installed. Installing...")
        try:
            import subprocess
            subprocess.check_call([sys.executable, "-m", "pip", "install", "gdown"])
            print("gdown installed. Retrying download...")
            return download_google_drive(file_id, output_path)
        except Exception as e:
            print(f"[FAILED] Could not install gdown: {str(e)}")
            print(f"Please install gdown manually: pip install gdown")
            return False
    except Exception as e:
        print(f"[FAILED] Error: {str(e)}")
        return False

def main():
    print("=" * 60)
    print("ChatSentimentAnalysis - Model Files Downloader")
    print("=" * 60)
    print()
    
    # Create directories
    directories = [
        "Text/sentiment/finetuned",
        "Text/model",
        "Image"
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"Created directory: {directory}")
    
    print()
    
    downloads = []
    
    # 1. DeepMoji SS-Twitter Model
    print("[1/4] DeepMoji SS-Twitter Model")
    result = download_google_drive(
        "1ZLD2iSgl4PggYPAG9iG_eoFx2DEegqSL",
        "Text/sentiment/finetuned/twitter_ss.hdf5"
    )
    downloads.append({"name": "Twitter Model", "success": result})
    print()
    
    # 2. DeepMoji SS-YouTube Model
    print("[2/4] DeepMoji SS-YouTube Model")
    result = download_google_drive(
        "1iWc0sUmk7FwXBFPQ8FOIWKhJ8jS2iplh",
        "Text/sentiment/finetuned/youtube_ss.hdf5"
    )
    downloads.append({"name": "YouTube Model", "success": result})
    print()
    
    # 3. DeepMoji Weights (Dropbox)
    print("[3/4] DeepMoji Weights")
    result = download_file(
        "https://www.dropbox.com/s/xqarafsl6a8f9ny/deepmoji_weights.hdf5?dl=1",
        "Text/model/deepmoji_weights.hdf5"
    )
    downloads.append({"name": "DeepMoji Weights", "success": result})
    print()
    
    # 4. C3D Sentiment Model
    print("[4/4] C3D Sentiment Model")
    result = download_google_drive(
        "1UeEsQYrItUF0NOpD1frvS8qxdqGCUTg9",
        "Image/c3d_sentiment.hdf5"
    )
    downloads.append({"name": "C3D Model", "success": result})
    print()
    
    # Summary
    print("=" * 60)
    print("Download Summary:")
    print("=" * 60)
    
    success_count = sum(1 for d in downloads if d["success"])
    
    for download in downloads:
        status = "[OK]" if download["success"] else "[FAILED]"
        color = "\033[92m" if download["success"] else "\033[91m"
        reset = "\033[0m"
        print(f"{color}{status}{reset} {download['name']}")
    
    print()
    print(f"Downloaded {success_count} out of {len(downloads)} files.")
    
    if success_count < len(downloads):
        print()
        print("Some files failed to download automatically.")
        print("Please download them manually:")
        print("1. Twitter Model: https://drive.google.com/open?id=1ZLD2iSgl4PggYPAG9iG_eoFx2DEegqSL")
        print("2. YouTube Model: https://drive.google.com/open?id=1iWc0sUmk7FwXBFPQ8FOIWKhJ8jS2iplh")
        print("3. DeepMoji Weights: https://www.dropbox.com/s/xqarafsl6a8f9ny/deepmoji_weights.hdf5?dl=0")
        print("4. C3D Model: https://drive.google.com/open?id=1UeEsQYrItUF0NOpD1frvS8qxdqGCUTg9")
    else:
        print()
        print("All files downloaded successfully!")

if __name__ == "__main__":
    main()

