param(
    [Parameter(Mandatory=$true)][string]$AuthToken,
    [int]$Port = 7860
)

$ErrorActionPreference = 'Stop'

# Resolve ngrok path
$ngrokPath = Join-Path -Path (Get-Location) -ChildPath 'ngrok.exe'
if (-not (Test-Path $ngrokPath)) {
    Write-Error "ngrok.exe not found at $ngrokPath. Download from https://ngrok.com/download and place it in the project root."    
}

Write-Host "Applying ngrok authtoken..." -ForegroundColor Cyan
& $ngrokPath config add-authtoken $AuthToken
if ($LASTEXITCODE -ne 0) { Write-Error "Failed to set authtoken (exit $LASTEXITCODE)." }

Write-Host "Starting tunnel on http://127.0.0.1:$Port ..." -ForegroundColor Cyan
Write-Host "Press Ctrl+C to stop." -ForegroundColor Yellow

# Start tunnel (foreground)
& $ngrokPath http $Port
