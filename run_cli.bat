@echo off
:: ========================================
:: Terminal AI Workflow - Sequential CLI
:: ========================================
:: Runs tools one at a time in CLI mode
:: For concurrent mode, use run.bat instead

setlocal enabledelayedexpansion
cd /d "%~dp0"

echo.
echo  ========================================
echo   Terminal AI Workflow - CLI Mode
echo  ========================================
echo.

:: Check if input provided as argument
if not "%~1"=="" (
    set "INPUT=%*"
    goto :process
)

:: Prompt for input
echo  Enter your task(s). Use periods to separate multiple tasks.
echo.
set /p INPUT="  > "

if "!INPUT!"=="" (
    echo  No input provided. Exiting.
    exit /b 1
)

:process
:: Write input to temp file
echo !INPUT!> "config\tasks\_input.txt"

:: Route tasks
echo.
echo  Routing tasks...
powershell -ExecutionPolicy Bypass -File "scripts\route_tasks.ps1"
if errorlevel 1 (
    echo  Error routing tasks.
    exit /b 1
)

:: Run sequentially
echo.
powershell -ExecutionPolicy Bypass -File "scripts\run_cli.ps1"

echo.
echo  ========================================
echo   Complete
echo  ========================================
endlocal
