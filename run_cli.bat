@echo off
:: ========================================
:: Terminal AI Workflow - Python CLI
:: ========================================
:: Interactive REPL with rich output
:: For GUI mode, use run_gui.bat instead

setlocal
cd /d "%~dp0"

set "PYTHON_EXE="
where python >nul 2>nul && set "PYTHON_EXE=python"
if not defined PYTHON_EXE (
    where py >nul 2>nul && set "PYTHON_EXE=py"
)

if not defined PYTHON_EXE (
    echo ERROR: Python not found. Install Python 3 and ensure python or py is in PATH.
    exit /b 1
)

if /i "%PYTHON_EXE%"=="py" (
    py -3 "%~dp0scripts\run_cli.py" %*
) else (
    python "%~dp0scripts\run_cli.py" %*
)

endlocal
