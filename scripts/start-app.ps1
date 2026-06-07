<#
.SYNOPSIS
    OmniVoice 快速啟動腳本
.DESCRIPTION
    檢查環境 → 啟動應用 → 自動開啟瀏覽器
.PARAMETER NoBrowser
    不自動開啟瀏覽器
.PARAMETER Port
    指定埠號（預設 8080）
#>

param(
    [switch]$NoBrowser,
    [int]$Port = 8080
)

$rootDir = $PSScriptRoot | Split-Path -Parent
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$OutputEncoding = [System.Text.Encoding]::UTF8

Write-Host "╔══════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║      OmniVoice TTS — 快速啟動       ║" -ForegroundColor Cyan
Write-Host "╚══════════════════════════════════════╝" -ForegroundColor Cyan

# ── 1. 確認 uv ──
if (-not (Get-Command "uv" -ErrorAction SilentlyContinue)) {
    Write-Host "❌ uv 未安裝，請先安裝: https://docs.astral.sh/uv/#installation" -ForegroundColor Red
    exit 1
}
Write-Host "   ✅ uv 就緒" -ForegroundColor Green

# ── 2. 確認 .venv ──
$venvDir = Join-Path $rootDir ".venv"
if (-not (Test-Path $venvDir)) {
    Write-Host "   ⏳ 建立虛擬環境..." -ForegroundColor Yellow
    & uv venv --python 3.10 2>&1 | Out-Null
    Write-Host "   ✅ 虛擬環境已建立" -ForegroundColor Green
}

# ── 3. 確認依賴 ──
$needsSync = $false
try {
    & uv run python -c "import nicegui" 2>$null
} catch {
    $needsSync = $true
}
if ($needsSync) {
    Write-Host "   ⏳ 同步依賴中..." -ForegroundColor Yellow
    & uv sync 2>&1 | Out-Null
    Write-Host "   ✅ 依賴已安裝" -ForegroundColor Green
} else {
    Write-Host "   ✅ 依賴就緒" -ForegroundColor Green
}

# ── 4. 啟動 ──
$env:OMNIVOICE_PORT = $Port
Write-Host "`n   🚀 啟動應用中..." -ForegroundColor Green
Write-Host "   🌐 http://localhost:$Port" -ForegroundColor White

$url = "http://localhost:$Port"
if (-not $NoBrowser) {
    Start-Process $url
}

Write-Host "   ⏎ 按 Ctrl+C 停止伺服器`n" -ForegroundColor Gray

# 啟動應用
Push-Location $rootDir
try {
    & uv run python -m app.main 2>&1
} finally {
    Pop-Location
}
