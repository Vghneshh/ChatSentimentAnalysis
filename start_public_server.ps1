# Start Public Sentiment Server with ngrok
# This script starts both the local server and ngrok tunnel together

$ErrorActionPreference = 'Stop'

Write-Host "==================================================" -ForegroundColor Cyan
Write-Host "Starting Chat Sentiment Analysis Public Server" -ForegroundColor Cyan
Write-Host "==================================================" -ForegroundColor Cyan
Write-Host ""

# Check if ngrok.exe exists
if (-not (Test-Path ".\ngrok.exe")) {
    Write-Error "ngrok.exe not found. Please download from https://ngrok.com/download"
    exit 1
}

# Check if virtual environment exists
if (-not (Test-Path ".\.venv\Scripts\Activate.ps1")) {
    Write-Error "Virtual environment not found. Please run setup first."
    exit 1
}

# Kill any existing instances
Write-Host "Cleaning up any existing instances..." -ForegroundColor Yellow
Get-Process python -ErrorAction SilentlyContinue | Where-Object {$_.Path -like '*ChatSentimentAnalysis*'} | Stop-Process -Force -ErrorAction SilentlyContinue
Get-Process ngrok -ErrorAction SilentlyContinue | Stop-Process -Force -ErrorAction SilentlyContinue
Start-Sleep -Seconds 2

# Activate virtual environment and start server in background
Write-Host "Starting local server on port 7860..." -ForegroundColor Green
$serverJob = Start-Job -ScriptBlock {
    param($projectPath)
    Set-Location $projectPath
    & "$projectPath\.venv\Scripts\Activate.ps1"
    & python "$projectPath\server.py"
} -ArgumentList $PWD

# Wait for server to start
Write-Host "Waiting for server to initialize..." -ForegroundColor Yellow
Start-Sleep -Seconds 8

# Check if server started successfully
$serverRunning = $false
for ($i = 0; $i -lt 10; $i++) {
    try {
        $response = Invoke-WebRequest -Uri "http://127.0.0.1:7860" -UseBasicParsing -TimeoutSec 2 -ErrorAction SilentlyContinue
        if ($response.StatusCode -eq 200) {
            $serverRunning = $true
            break
        }
    } catch {
        Start-Sleep -Seconds 1
    }
}

if (-not $serverRunning) {
    Write-Error "Server failed to start on port 7860"
    Stop-Job $serverJob -ErrorAction SilentlyContinue
    Remove-Job $serverJob -ErrorAction SilentlyContinue
    exit 1
}

Write-Host "Server is running on http://127.0.0.1:7860" -ForegroundColor Green
Write-Host ""

# Start ngrok
Write-Host "Starting ngrok tunnel..." -ForegroundColor Green
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PWD'; Write-Host 'ngrok Tunnel Active' -ForegroundColor Cyan; .\ngrok.exe http 7860"

# Wait for ngrok to initialize
Write-Host "Waiting for ngrok to establish tunnel..." -ForegroundColor Yellow
Start-Sleep -Seconds 5

# Get public URL
$publicUrl = $null
for ($i = 0; $i -lt 10; $i++) {
    try {
        $tunnelInfo = Invoke-RestMethod -Uri "http://127.0.0.1:4040/api/tunnels" -ErrorAction SilentlyContinue
        if ($tunnelInfo.tunnels -and $tunnelInfo.tunnels.Count -gt 0) {
            $publicUrl = $tunnelInfo.tunnels[0].public_url
            break
        }
    } catch {
        Start-Sleep -Seconds 1
    }
}

Write-Host ""
Write-Host "==================================================" -ForegroundColor Cyan
Write-Host "SETUP COMPLETE" -ForegroundColor Green
Write-Host "==================================================" -ForegroundColor Cyan
Write-Host ""

if ($publicUrl) {
    Write-Host "Local URL:  http://127.0.0.1:7860" -ForegroundColor White
    Write-Host "Public URL: $publicUrl" -ForegroundColor Green
    Write-Host ""
    Write-Host "Share the public URL with anyone!" -ForegroundColor Yellow
    Write-Host "(First-time visitors will see an ngrok interstitial - click 'Visit Site')" -ForegroundColor Gray
} else {
    Write-Host "Local URL:  http://127.0.0.1:7860" -ForegroundColor White
    Write-Host "Public URL: Check the ngrok window for the URL" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "==================================================" -ForegroundColor Cyan
Write-Host "To stop:" -ForegroundColor White
Write-Host "  1. Close the ngrok window" -ForegroundColor Gray
Write-Host "  2. Press Ctrl+C in this window" -ForegroundColor Gray
Write-Host "==================================================" -ForegroundColor Cyan
Write-Host ""

# Monitor server job
Write-Host "Press Ctrl+C to stop the server..." -ForegroundColor Yellow
try {
    while ($true) {
        Start-Sleep -Seconds 5
        
        # Check if server job is still running
        if ($serverJob.State -ne 'Running') {
            Write-Host "Server stopped unexpectedly!" -ForegroundColor Red
            break
        }
        
        # Check if server is responding
        try {
            $null = Invoke-WebRequest -Uri "http://127.0.0.1:7860" -UseBasicParsing -TimeoutSec 2 -ErrorAction Stop
        } catch {
            Write-Host "Server not responding, restarting..." -ForegroundColor Yellow
            Stop-Job $serverJob -ErrorAction SilentlyContinue
            Remove-Job $serverJob -ErrorAction SilentlyContinue
            
            $serverJob = Start-Job -ScriptBlock {
                param($projectPath)
                Set-Location $projectPath
                & "$projectPath\.venv\Scripts\Activate.ps1"
                & python "$projectPath\server.py"
            } -ArgumentList $PWD
            
            Start-Sleep -Seconds 8
        }
    }
} finally {
    Write-Host "Cleaning up..." -ForegroundColor Yellow
    Stop-Job $serverJob -ErrorAction SilentlyContinue
    Remove-Job $serverJob -ErrorAction SilentlyContinue
    Get-Process ngrok -ErrorAction SilentlyContinue | Stop-Process -Force -ErrorAction SilentlyContinue
    Write-Host "Stopped successfully" -ForegroundColor Green
}
