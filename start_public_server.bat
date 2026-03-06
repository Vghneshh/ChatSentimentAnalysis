@echo off
setlocal ENABLEDELAYEDEXPANSION

echo ==================================================
echo Starting Chat Sentiment Analysis Public Server
echo ==================================================
echo.

REM Check if ngrok.exe exists
if not exist "%~dp0ngrok.exe" (
    echo ERROR: ngrok.exe not found
    echo Please download from https://ngrok.com/download
    pause
    exit /b 1
)

REM Check if virtual environment exists
if not exist "%~dp0.venv\Scripts\Activate.ps1" (
    echo ERROR: Virtual environment not found
    echo Please run setup first
    pause
    exit /b 1
)

REM Kill existing instances
echo Cleaning up any existing instances...
taskkill /F /IM python.exe /FI "WINDOWTITLE eq *ChatSentimentAnalysis*" >nul 2>&1
taskkill /F /IM ngrok.exe >nul 2>&1
timeout /t 2 /nobreak >nul

REM Start server in new window
echo Starting local server on port 7860...
start "Sentiment Server" cmd /k "cd /d "%~dp0" && .venv\Scripts\activate.bat && python server.py"

REM Wait for server to start
echo Waiting for server to initialize...
timeout /t 8 /nobreak >nul

REM Start ngrok in new window
echo Starting ngrok tunnel...
start "ngrok Tunnel" cmd /k "cd /d "%~dp0" && ngrok.exe http 7860"

REM Wait for ngrok
echo Waiting for ngrok to establish tunnel...
timeout /t 5 /nobreak >nul

echo.
echo ==================================================
echo SETUP COMPLETE
echo ==================================================
echo.
echo Local URL:  http://127.0.0.1:7860
echo Public URL: Check the ngrok window for the HTTPS URL
echo.
echo Both services are running in separate windows
echo Close those windows to stop the services
echo.
echo ==================================================
pause
