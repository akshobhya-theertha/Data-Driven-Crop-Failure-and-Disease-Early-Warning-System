param(
  [int]$Port = 5000
)

$ErrorActionPreference = "Stop"

Set-Location $PSScriptRoot

Write-Host "Project dir: $PWD"

# Ensure venv exists
if (-not (Test-Path ".\.venv\Scripts\python.exe")) {
  Write-Host "Creating virtual environment..."
  py -3 -m venv .venv
}

Write-Host "Installing/updating requirements..."
.\.venv\Scripts\python.exe -m pip install --upgrade pip | Out-Host
.\.venv\Scripts\python.exe -m pip install -r requirements.txt | Out-Host

# Ensure a model exists so the UI can start
if (-not (Test-Path ".\model\crop_disease_model.h5")) {
  Write-Host "No model found. Creating demo model..."
  .\.venv\Scripts\python.exe create_demo_model.py | Out-Host
}

# Free the port if something is stuck
$pids = @()
try {
  $pids = Get-NetTCPConnection -LocalPort $Port -State Listen -ErrorAction SilentlyContinue |
    Select-Object -ExpandProperty OwningProcess -Unique
} catch { }

foreach ($procId in $pids) {
  if ($procId) {
    Write-Host "Stopping process on port $Port (PID $procId)..."
    try { Stop-Process -Id $procId -Force -ErrorAction SilentlyContinue } catch { }
  }
}

Write-Host "Starting web app on port $Port..."
$env:FLASK_PORT = "$Port"
$env:FLASK_HOST = "0.0.0.0"
$env:USE_WAITRESS = "1"

Start-Process -FilePath ".\.venv\Scripts\python.exe" -ArgumentList "run_webapp.py" -WindowStyle Normal | Out-Null

# Wait until server responds, then open browser
$url = "http://127.0.0.1:$Port/"
Write-Host "Waiting for server: $url"
for ($i = 0; $i -lt 90; $i++) {
  try {
    $r = Invoke-WebRequest -UseBasicParsing $url -TimeoutSec 2
    if ($r.StatusCode -eq 200) { break }
  } catch { Start-Sleep -Seconds 1 }
}

Start-Process $url | Out-Null
Write-Host "Opened: $url"
