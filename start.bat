@echo off
REM OmniVoice quick start — double-click to launch

set "SCRIPT=%~dp0scripts\start-app.ps1"

where pwsh >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    pwsh -ExecutionPolicy Bypass -File "%SCRIPT%" %*
) else (
    powershell -ExecutionPolicy Bypass -File "%SCRIPT%" %*
)

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo Launch failed. Check messages above.
    pause
)
