<#
.SYNOPSIS
    OmniVoice 環境檢查腳本
.DESCRIPTION
    檢查 uv、Python、虛擬環境、依賴是否就緒，並可選擇性執行測試。
#>

param(
    [switch]$RunTests
)

$ErrorActionPreference = "Stop"
$rootDir = $PSScriptRoot | Split-Path -Parent  # scripts/ 的上層 = 專案根目錄
$venvDir = Join-Path $rootDir ".venv"

# 設定 UTF-8 輸出
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$OutputEncoding = [System.Text.Encoding]::UTF8

function Write-Step {
    param([string]$Message)
    Write-Host "`n>> $Message" -ForegroundColor Cyan
}

function Write-Pass {
    Write-Host "   ✅ 通過" -ForegroundColor Green
}

function Write-Fail {
    param([string]$Detail)
    Write-Host "   ❌ 失敗" -ForegroundColor Red
    if ($Detail) { Write-Host "      $Detail" -ForegroundColor Red }
}

function Write-Warn {
    param([string]$Detail)
    Write-Host "   ⚠️  警告" -ForegroundColor Yellow
    if ($Detail) { Write-Host "      $Detail" -ForegroundColor Yellow }
}

# ──────────────────────────────────────────────
# 1. uv
# ──────────────────────────────────────────────
Write-Step "1/6  檢查 uv 套件管理器"

$uvPath = Get-Command "uv" -ErrorAction SilentlyContinue
if (-not $uvPath) {
    Write-Fail "uv 未安裝。請參考 https://docs.astral.sh/uv/#installation"
    Write-Host "   建議安裝方式: winget install --id=astral.uv -e" -ForegroundColor Yellow
    exit 1
}
$uvVer = & uv --version 2>&1
Write-Pass
Write-Host "   uv $uvVer" -ForegroundColor Gray

# ──────────────────────────────────────────────
# 2. Python
# ──────────────────────────────────────────────
Write-Step "2/6  檢查 Python 版本"

try {
    $pyVerRaw = & uv run python --version 2>&1
} catch {
    # fallback: 直接用 python
    $pyVerRaw = python --version 2>$null
    if (-not $pyVerRaw) {
        Write-Fail "找不到 Python，請安裝 Python 3.10+"
        exit 1
    }
}

if ($pyVerRaw -match "Python (\d+)\.(\d+)") {
    $major = [int]$Matches[1]
    $minor = [int]$Matches[2]
    if ($major -ge 3 -and $minor -ge 10) {
        Write-Pass
        Write-Host "   $pyVerRaw" -ForegroundColor Gray
    } else {
        Write-Fail "Python 版本不足 ($pyVerRaw)，需要 >= 3.10"
        exit 1
    }
} else {
    Write-Warn "無法解析 Python 版本 ($pyVerRaw)"
}

# ──────────────────────────────────────────────
# 3. .venv
# ──────────────────────────────────────────────
Write-Step "3/6  檢查虛擬環境"

if (Test-Path $venvDir) {
    Write-Pass
    Write-Host "   虛擬環境: $venvDir" -ForegroundColor Gray
} else {
    Write-Host "   建立虛擬環境中..." -ForegroundColor Yellow
    try {
        & uv venv --python 3.10 2>&1 | Out-Null
        Write-Pass
        Write-Host "   已建立: $venvDir" -ForegroundColor Gray
    } catch {
        Write-Fail "建立虛擬環境失敗: $_"
        exit 1
    }
}

# ──────────────────────────────────────────────
# 4. uv sync
# ──────────────────────────────────────────────
Write-Step "4/6  檢查依賴安裝"

$venvMarker = Join-Path $venvDir "pyvenv.cfg"
if (-not (Test-Path $venvMarker)) {
    Write-Warn "虛擬環境不完整，重新建立中..."
    & uv venv 2>&1 | Out-Null
}

# 判斷是否已同步：檢查有無 nicegui 站點套件
try {
    & uv run python -c "import nicegui" 2>$null
    Write-Pass
    Write-Host "   依賴已安裝" -ForegroundColor Gray
} catch {
    Write-Host "   同步依賴中..." -ForegroundColor Yellow
    try {
        & uv sync 2>&1 | Out-Null
        Write-Pass
        Write-Host "   依賴同步完成" -ForegroundColor Gray
    } catch {
        Write-Fail "同步失敗: $_"
        exit 1
    }
}

# ──────────────────────────────────────────────
# 5. 主要套件匯入檢查
# ──────────────────────────────────────────────
Write-Step "5/6  主要套件匯入檢查"

$packages = @{
    nicegui   = "UI 框架"
    edge_tts  = "Edge-TTS 引擎"
    gtts      = "gTTS 引擎"
    pydantic  = "資料模型"
    mutagen   = "音頻元資料"
    aiofiles  = "非同步檔案 IO"
}

$allOk = $true
foreach ($pkg in $packages.Keys) {
    $desc = $packages[$pkg]
    try {
        & uv run python -c "import $pkg" 2>$null
        Write-Host "   $($pkg.PadRight(16)) $desc  ✅" -ForegroundColor Gray
    } catch {
        Write-Host "   $($pkg.PadRight(16)) $desc  ❌ 未安裝" -ForegroundColor Red
        $allOk = $false
    }
}

if (-not $allOk) {
    Write-Host "`n部分套件缺失，執行 uv sync 安裝..." -ForegroundColor Yellow
    & uv sync 2>&1 | Out-Null
    Write-Pass
}

# ──────────────────────────────────────────────
# 6. 測試（選擇性）
# ──────────────────────────────────────────────
if ($RunTests) {
    Write-Step "6/6  執行測試"
    try {
        & uv run pytest -v 2>&1
    } catch {
        Write-Fail "測試執行失敗: $_"
    }
} else {
    Write-Step "6/6  跳過測試（加上 -RunTests 參數以執行測試）"
}

# ──────────────────────────────────────────────
# 完成
# ──────────────────────────────────────────────
Write-Host "`n═══════════════════════════════════════" -ForegroundColor Cyan
Write-Host "  環境檢查完成" -ForegroundColor Cyan
Write-Host "  啟動方式: cd $rootDir && uv run python -m app.main" -ForegroundColor White
Write-Host "═══════════════════════════════════════" -ForegroundColor Cyan
