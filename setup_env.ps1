# =============================================================================
#  LLM-Guard Playground  —  Environment Setup
#  Run this ONCE to create the virtual environment and install dependencies.
# =============================================================================

$ErrorActionPreference = "Stop"

Write-Host ""
Write-Host "========================================================" -ForegroundColor Cyan
Write-Host "   LLM-Guard Playground  —  Environment Setup" -ForegroundColor Cyan
Write-Host "========================================================" -ForegroundColor Cyan
Write-Host ""

# ── 1. Locate Python 3.11 ─────────────────────────────────────────────────
Write-Host "[1/5] Locating Python 3.11..." -ForegroundColor Yellow

$python = $null

# Try py launcher first (most reliable on Windows with multiple versions)
try {
    $ver = & py -3.11 --version 2>&1
    if ($ver -match "Python 3\.11") {
        $python = "py -3.11"
        Write-Host "      Found via py launcher: $ver" -ForegroundColor Green
    }
} catch {}

# Try common install paths
if (-not $python) {
    $candidates = @(
        "C:\Python311\python.exe",
        "C:\Python311\python3.exe",
        "$env:LOCALAPPDATA\Programs\Python\Python311\python.exe",
        "$env:LOCALAPPDATA\Programs\Python\Python311-32\python.exe"
    )
    foreach ($c in $candidates) {
        if (Test-Path $c) {
            $ver = & $c --version 2>&1
            if ($ver -match "Python 3\.11") {
                $python = $c
                Write-Host "      Found at: $c  ($ver)" -ForegroundColor Green
                break
            }
        }
    }
}

# Try plain 'python' / 'python3' — only if version is 3.11
if (-not $python) {
    foreach ($cmd in @("python", "python3")) {
        try {
            $ver = & $cmd --version 2>&1
            if ($ver -match "Python 3\.11") {
                $python = $cmd
                Write-Host "      Found on PATH: $cmd  ($ver)" -ForegroundColor Green
                break
            }
        } catch {}
    }
}

if (-not $python) {
    Write-Host ""
    Write-Host "  ERROR: Python 3.11 not found." -ForegroundColor Red
    Write-Host ""
    Write-Host "  LLM-Guard requires Python 3.11.x (tested on 3.11.9)." -ForegroundColor Red
    Write-Host "  Python 3.12+ has known compatibility issues with LLM-Guard dependencies." -ForegroundColor Red
    Write-Host ""
    Write-Host "  Download Python 3.11.9 from:" -ForegroundColor White
    Write-Host "  https://www.python.org/downloads/release/python-3119/" -ForegroundColor Cyan
    Write-Host ""
    Read-Host "Press Enter to exit"
    exit 1
}

# ── 2. Create virtual environment ─────────────────────────────────────────
Write-Host ""
Write-Host "[2/5] Creating virtual environment (.venv)..." -ForegroundColor Yellow

$venvPath = Join-Path $PSScriptRoot ".venv"

if (Test-Path $venvPath) {
    Write-Host "      .venv already exists — skipping creation." -ForegroundColor DarkYellow
    Write-Host "      (Delete .venv and re-run this script to rebuild from scratch)" -ForegroundColor DarkGray
} else {
    if ($python -eq "py -3.11") {
        & py -3.11 -m venv .venv
    } else {
        & $python -m venv .venv
    }
    Write-Host "      Virtual environment created at .venv\" -ForegroundColor Green
}

# ── 3. Activate + upgrade pip ─────────────────────────────────────────────
Write-Host ""
Write-Host "[3/5] Activating environment and upgrading pip..." -ForegroundColor Yellow

$activateScript = Join-Path $PSScriptRoot ".venv\Scripts\Activate.ps1"
if (-not (Test-Path $activateScript)) {
    Write-Host "  ERROR: Could not find .venv\Scripts\Activate.ps1" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

& $activateScript

python -m pip install --upgrade pip --quiet
Write-Host "      pip upgraded." -ForegroundColor Green

# ── 4. Install dependencies ────────────────────────────────────────────────
Write-Host ""
Write-Host "[4/5] Installing dependencies (this may take a few minutes)..." -ForegroundColor Yellow
Write-Host "      fastapi, uvicorn, llm-guard..." -ForegroundColor DarkGray
Write-Host ""

pip install `
    "fastapi>=0.110.0" `
    "uvicorn[standard]>=0.29.0" `
    "llm-guard>=0.3.14" `
    "python-multipart>=0.0.9" `
    "psutil>=5.9.0" `
    "httpx>=0.27.0"

Write-Host ""
Write-Host "      Dependencies installed." -ForegroundColor Green

# ── 5. Verify ─────────────────────────────────────────────────────────────
Write-Host ""
Write-Host "[5/5] Verifying installation..." -ForegroundColor Yellow

$pyVer    = python --version 2>&1
$guardVer = python -c "import llm_guard; print(llm_guard.__version__)" 2>&1
$fastapiV = python -c "import fastapi; print(fastapi.__version__)" 2>&1

Write-Host "      Python  : $pyVer" -ForegroundColor Green
Write-Host "      llm-guard: $guardVer" -ForegroundColor Green
Write-Host "      FastAPI  : $fastapiV" -ForegroundColor Green

# ── Done ──────────────────────────────────────────────────────────────────
Write-Host ""
Write-Host "========================================================" -ForegroundColor Cyan
Write-Host "   Setup complete!" -ForegroundColor Green
Write-Host ""
Write-Host "   Run the project daily with:" -ForegroundColor White
Write-Host "   .\run.ps1" -ForegroundColor Cyan
Write-Host "========================================================" -ForegroundColor Cyan
Write-Host ""

Read-Host "Press Enter to exit"