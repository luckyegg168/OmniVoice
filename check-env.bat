@echo off
REM OmniVoice env check — double-click to run
REM Requires PowerShell 7+ (pwsh)

set "SCRIPT=%~dp0scripts\check-env.ps1"

where pwsh >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    pwsh -ExecutionPolicy Bypass -File "%SCRIPT%" %*
) else (
    powershell -ExecutionPolicy Bypass -File "%SCRIPT%" %*
)

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo Environment check failed. See messages above.
    pause
) else (
    echo.
    echo Environment is ready!
    pause
)
