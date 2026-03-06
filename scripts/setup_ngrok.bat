@echo off
setlocal ENABLEDELAYEDEXPANSION

if "%~1"=="" (
  echo Usage: setup_ngrok.bat ^<AUTHTOKEN^> [PORT]
  echo Example: setup_ngrok.bat 2RrXyourTokenHere 7860
  exit /b 1
)
set AUTHTOKEN=%~1
set PORT=%~2
if "%PORT%"=="" set PORT=7860

if not exist "%~dp0..\ngrok.exe" (
  echo ngrok.exe not found in project root. Please download from https://ngrok.com/download and place it there.
  exit /b 1
)

pushd "%~dp0.."

echo Applying ngrok authtoken...
ngrok.exe config add-authtoken %AUTHTOKEN%
if errorlevel 1 (
  echo Failed to set authtoken.
  popd
  exit /b 1
)

echo Starting tunnel on http://127.0.0.1:%PORT% ...
echo Press Ctrl+C to stop.
ngrok.exe http %PORT%

popd
endlocal
