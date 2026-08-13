# =============================================================================
#  LLM-Guard Playground  —  Start Server
#  Run this daily to launch the playground.
# =============================================================================

$ErrorActionPreference = "Stop"

Write-Host ""
Write-Host "========================================================" -ForegroundColor Cyan
Write-Host "   LLM-Guard Playground  —  Starting..." -ForegroundColor Cyan
Write-Host "========================================================" -ForegroundColor Cyan
Write-Host ""

# ── Check venv exists ─────────────────────────────────────────────────────
$venvActivate = Join-Path $PSScriptRoot ".venv\Scripts\Activate.ps1"
if (-not (Test-Path $venvActivate)) {
    Write-Host "  ERROR: Virtual environment not found." -ForegroundColor Red
    Write-Host "  Please run setup_env.ps1 first." -ForegroundColor Yellow
    Write-Host ""
    Read-Host "Press Enter to exit"
    exit 1
}

# ── Activate venv ─────────────────────────────────────────────────────────
Write-Host "  Activating virtual environment..." -ForegroundColor Yellow
& $venvActivate
Write-Host "  OK" -ForegroundColor Green

# ── Move to project root ───────────────────────────────────────────────────
Set-Location $PSScriptRoot

# ── Launch ────────────────────────────────────────────────────────────────
Write-Host ""
Write-Host "  Server URL  : http://localhost:8000" -ForegroundColor Cyan
Write-Host "  Auto-reload : enabled (edit & save to hot-reload)" -ForegroundColor DarkGray
Write-Host "  Stop server : Ctrl+C" -ForegroundColor DarkGray
Write-Host ""

# Open browser after a short delay (gives uvicorn time to bind)
Start-Job -ScriptBlock {
    Start-Sleep -Seconds 2
    Start-Process "http://localhost:8000"
} | Out-Null

# Start uvicorn — run from project root so 'backend.*' imports resolve correctly
python -m uvicorn backend.main:app --reload --host 127.0.0.1 --port 8000

Write-Host ""
Write-Host "  Server stopped." -ForegroundColor Yellow
Read-Host "Press Enter to exit"