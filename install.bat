@echo off
setlocal enabledelayedexpansion

echo ========================================
echo  Terminal AI Workflow - Installation
echo ========================================
echo.

:: Check for Node.js
echo [1/4] Checking Node.js...
where node >nul 2>nul
if %errorlevel% neq 0 (
    echo ERROR: Node.js not found!
    echo Please install from: https://nodejs.org
    echo.
    pause
    exit /b 1
)
for /f "tokens=*" %%i in ('node --version') do set NODE_VER=%%i
echo Found Node.js %NODE_VER%

:: Check for npm
echo.
echo [2/4] Checking npm...
where npm >nul 2>nul
if %errorlevel% neq 0 (
    echo ERROR: npm not found!
    pause
    exit /b 1
)
for /f "tokens=*" %%i in ('npm --version') do set NPM_VER=%%i
echo Found npm v%NPM_VER%

:: Install Claude Code
echo.
echo [3/4] Installing Claude Code...
call npm install -g @anthropic-ai/claude-code
if %errorlevel% neq 0 (
    echo WARNING: Claude Code installation may have failed.
) else (
    echo Claude Code installed successfully.
)

:: Install Gemini CLI
echo.
echo [4/4] Installing Gemini CLI...
call npm install -g @google/gemini-cli
if %errorlevel% neq 0 (
    echo WARNING: Gemini CLI installation may have failed.
) else (
    echo Gemini CLI installed successfully.
)

echo.
echo ========================================
echo  Installation Complete!
echo ========================================
echo.
echo Next steps:
echo   1. Run 'claude' to authenticate with Anthropic
echo   2. Run 'gemini' to authenticate with Google
echo   3. Run 'run.bat' to start working
echo.
pause
