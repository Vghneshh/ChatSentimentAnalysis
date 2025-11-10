# Script to download required model files for ChatSentimentAnalysis

Write-Host "Starting download of model files..." -ForegroundColor Green
Write-Host ""

# Create directories if they don't exist
$finetunedDir = "Text\sentiment\finetuned"
$modelDir = "Text\model"
$imageDir = "Image"

if (-not (Test-Path $finetunedDir)) {
    New-Item -ItemType Directory -Path $finetunedDir -Force | Out-Null
}
if (-not (Test-Path $modelDir)) {
    New-Item -ItemType Directory -Path $modelDir -Force | Out-Null
}
if (-not (Test-Path $imageDir)) {
    New-Item -ItemType Directory -Path $imageDir -Force | Out-Null
}

# Function to download from Google Drive
function Download-GoogleDrive {
    param(
        [string]$FileId,
        [string]$OutputPath
    )
    
    $url = "https://drive.google.com/uc?export=download&id=$FileId"
    Write-Host "Downloading: $OutputPath" -ForegroundColor Yellow
    
    try {
        # Try direct download with confirm parameter
        $downloadUrl = "https://drive.google.com/uc?export=download&confirm=t&id=$FileId"
        Invoke-WebRequest -Uri $downloadUrl -OutFile $OutputPath -UseBasicParsing -ErrorAction Stop
        Write-Host "[OK] Downloaded: $OutputPath" -ForegroundColor Green
        return $true
    } catch {
        Write-Host "[FAILED] Could not download: $OutputPath" -ForegroundColor Red
        Write-Host "  Error: $($_.Exception.Message)" -ForegroundColor Red
        Write-Host "  Please download manually from:" -ForegroundColor Yellow
        Write-Host "  https://drive.google.com/open?id=$FileId" -ForegroundColor Cyan
        return $false
    }
}

# Function to download from Dropbox
function Download-Dropbox {
    param(
        [string]$Url,
        [string]$OutputPath
    )
    
    Write-Host "Downloading: $OutputPath" -ForegroundColor Yellow
    
    try {
        # Convert dl=0 to dl=1 for direct download
        $downloadUrl = $Url -replace '\?dl=0', '?dl=1'
        Invoke-WebRequest -Uri $downloadUrl -OutFile $OutputPath -UseBasicParsing -ErrorAction Stop
        Write-Host "[OK] Downloaded: $OutputPath" -ForegroundColor Green
        return $true
    } catch {
        Write-Host "[FAILED] Could not download: $OutputPath" -ForegroundColor Red
        Write-Host "  Error: $($_.Exception.Message)" -ForegroundColor Red
        Write-Host "  Please download manually from: $Url" -ForegroundColor Cyan
        return $false
    }
}

# Download files
$downloads = @()

# 1. DeepMoji SS-Twitter Model
Write-Host "[1/4] DeepMoji SS-Twitter Model" -ForegroundColor Cyan
$result = Download-GoogleDrive -FileId "1ZLD2iSgl4PggYPAG9iG_eoFx2DEegqSL" -OutputPath "$finetunedDir\twitter_ss.hdf5"
$downloads += @{Name="Twitter Model"; Success=$result}

Write-Host ""

# 2. DeepMoji SS-YouTube Model
Write-Host "[2/4] DeepMoji SS-YouTube Model" -ForegroundColor Cyan
$result = Download-GoogleDrive -FileId "1iWc0sUmk7FwXBFPQ8FOIWKhJ8jS2iplh" -OutputPath "$finetunedDir\youtube_ss.hdf5"
$downloads += @{Name="YouTube Model"; Success=$result}

Write-Host ""

# 3. DeepMoji Weights
Write-Host "[3/4] DeepMoji Weights" -ForegroundColor Cyan
$result = Download-Dropbox -Url "https://www.dropbox.com/s/xqarafsl6a8f9ny/deepmoji_weights.hdf5?dl=0" -OutputPath "$modelDir\deepmoji_weights.hdf5"
$downloads += @{Name="DeepMoji Weights"; Success=$result}

Write-Host ""

# 4. C3D Sentiment Model
Write-Host "[4/4] C3D Sentiment Model" -ForegroundColor Cyan
$result = Download-GoogleDrive -FileId "1UeEsQYrItUF0NOpD1frvS8qxdqGCUTg9" -OutputPath "$imageDir\c3d_sentiment.hdf5"
$downloads += @{Name="C3D Model"; Success=$result}

Write-Host ""
Write-Host "Download Summary:" -ForegroundColor Green
Write-Host "=================" -ForegroundColor Green

foreach ($download in $downloads) {
    if ($download.Success) {
        Write-Host "[OK] $($download.Name)" -ForegroundColor Green
    } else {
        Write-Host "[FAILED] $($download.Name) - Please download manually" -ForegroundColor Red
    }
}

$successCount = ($downloads | Where-Object { $_.Success }).Count
Write-Host ""
Write-Host "Downloaded $successCount out of $($downloads.Count) files." -ForegroundColor $(if ($successCount -eq $downloads.Count) { "Green" } else { "Yellow" })

if ($successCount -lt $downloads.Count) {
    Write-Host ""
    Write-Host "Some files failed to download automatically." -ForegroundColor Yellow
    Write-Host "Please download them manually:" -ForegroundColor Yellow
    Write-Host "1. Twitter Model: https://drive.google.com/open?id=1ZLD2iSgl4PggYPAG9iG_eoFx2DEegqSL" -ForegroundColor Cyan
    Write-Host "2. YouTube Model: https://drive.google.com/open?id=1iWc0sUmk7FwXBFPQ8FOIWKhJ8jS2iplh" -ForegroundColor Cyan
    Write-Host "3. DeepMoji Weights: https://www.dropbox.com/s/xqarafsl6a8f9ny/deepmoji_weights.hdf5?dl=0" -ForegroundColor Cyan
    Write-Host "4. C3D Model: https://drive.google.com/open?id=1UeEsQYrItUF0NOpD1frvS8qxdqGCUTg9" -ForegroundColor Cyan
}
