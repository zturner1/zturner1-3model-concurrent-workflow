@echo off
setlocal enabledelayedexpansion

echo ========================================
echo  Terminal AI Workflow - Installation
echo ========================================
echo.

:: Check for Node.js
echo [1/5] Checking Node.js...
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
echo [2/5] Checking npm...
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
echo [3/5] Installing Claude Code...
call npm install -g @anthropic-ai/claude-code
if %errorlevel% neq 0 (
    echo WARNING: Claude Code installation may have failed.
) else (
    echo Claude Code installed successfully.
)

:: Install Gemini CLI
echo.
echo [4/5] Installing Gemini CLI...
call npm install -g @google/gemini-cli
if %errorlevel% neq 0 (
    echo WARNING: Gemini CLI installation may have failed.
) else (
    echo Gemini CLI installed successfully.
)

:: Install OpenAI CLI
echo.
echo [5/5] Installing OpenAI CLI (Codex)...
call npm install -g @openai/codex
if %errorlevel% neq 0 (
    echo WARNING: OpenAI CLI installation may have failed.
    echo You may need to install manually or use: pip install openai
) else (
    echo OpenAI CLI installed successfully.
)

echo.
echo ========================================
echo  Installation Complete!
echo ========================================
echo.
echo Next steps - Authenticate each tool:
echo.
echo   1. Claude Code:
echo      Run 'claude' and follow browser login
echo.
echo   2. Gemini CLI:
echo      Run 'gemini' and authenticate with Google
echo.
echo   3. OpenAI CLI:
echo      Set your API key:
echo      set OPENAI_API_KEY=your-key-here
echo      Or add to environment variables permanently
echo.
echo   4. Run 'run.bat' to start working
echo.
pause
