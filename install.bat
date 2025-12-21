@echo off
setlocal enabledelayedexpansion

echo ========================================
echo  Terminal AI Workflow - Installation
echo ========================================
echo.

:: Track installation status
set CLAUDE_OK=0
set GEMINI_OK=0
set CODEX_OK=0
set PATH_WARNING=0

:: Check for Node.js
echo [1/6] Checking Node.js...
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
echo [2/6] Checking npm...
where npm >nul 2>nul
if %errorlevel% neq 0 (
    echo ERROR: npm not found!
    pause
    exit /b 1
)
for /f "tokens=*" %%i in ('npm --version') do set NPM_VER=%%i
echo Found npm v%NPM_VER%

:: Get npm global bin path (standard Windows location)
set "NPM_GLOBAL=%APPDATA%\npm"

:: Install Claude Code
echo.
echo [3/6] Installing Claude Code...
call npm install -g @anthropic-ai/claude-code >nul 2>&1
if %errorlevel% neq 0 (
    echo FAILED: Claude Code installation failed.
) else (
    echo Installed Claude Code.
    set CLAUDE_OK=1
)

:: Install Gemini CLI
echo.
echo [4/6] Installing Gemini CLI...
call npm install -g @google/gemini-cli >nul 2>&1
if %errorlevel% neq 0 (
    echo FAILED: Gemini CLI installation failed.
) else (
    echo Installed Gemini CLI.
    set GEMINI_OK=1
)

:: Install OpenAI CLI
echo.
echo [5/6] Installing OpenAI CLI (Codex)...
call npm install -g @openai/codex >nul 2>&1
if %errorlevel% neq 0 (
    echo FAILED: OpenAI CLI installation failed.
) else (
    echo Installed OpenAI Codex.
    set CODEX_OK=1
)

:: Verify installations and PATH
echo.
echo [6/6] Verifying installations...
echo.

:: Check Claude
where claude >nul 2>nul
if %errorlevel% neq 0 (
    if %CLAUDE_OK%==1 (
        echo   claude  : Installed but NOT IN PATH
        set PATH_WARNING=1
    ) else (
        echo   claude  : Not installed
    )
) else (
    for /f "tokens=*" %%i in ('claude --version 2^>nul') do echo   claude  : %%i
)

:: Check Gemini
where gemini >nul 2>nul
if %errorlevel% neq 0 (
    if %GEMINI_OK%==1 (
        echo   gemini  : Installed but NOT IN PATH
        set PATH_WARNING=1
    ) else (
        echo   gemini  : Not installed
    )
) else (
    for /f "tokens=*" %%i in ('gemini --version 2^>nul') do echo   gemini  : v%%i
)

:: Check Codex
where codex >nul 2>nul
if %errorlevel% neq 0 (
    if %CODEX_OK%==1 (
        echo   codex   : Installed but NOT IN PATH
        set PATH_WARNING=1
    ) else (
        echo   codex   : Not installed
    )
) else (
    for /f "tokens=1,2" %%i in ('codex --version 2^>nul') do echo   codex   : %%i %%j
)

:: Fix PATH if needed
if %PATH_WARNING%==1 (
    echo.
    echo ----------------------------------------
    echo  Fixing PATH...
    echo ----------------------------------------
    echo   Adding: !NPM_GLOBAL!

    :: Get current user PATH from registry
    for /f "tokens=2*" %%a in ('reg query "HKCU\Environment" /v Path 2^>nul') do set "USER_PATH=%%b"

    :: Check if already present
    echo "!USER_PATH!" | findstr /i /c:"!NPM_GLOBAL!" >nul 2>&1
    if !errorlevel!==0 (
        echo   Already in PATH, but terminal needs restart.
    ) else (
        :: Add to user PATH
        if defined USER_PATH (
            setx PATH "!USER_PATH!;!NPM_GLOBAL!" >nul 2>&1
        ) else (
            setx PATH "!NPM_GLOBAL!" >nul 2>&1
        )
        if !errorlevel!==0 (
            echo   PATH updated successfully.
        ) else (
            echo   ERROR: Could not update PATH automatically.
            echo   Manually add: !NPM_GLOBAL!
        )
    )

    :: Update current session PATH too
    set "PATH=!PATH!;!NPM_GLOBAL!"

    echo.
    echo ========================================
    echo  Installation Complete!
    echo ========================================
    echo.
    echo  NOTE: Restart your terminal for PATH
    echo        changes to take full effect.
) else (
    echo.
    echo ========================================
    echo  Installation Complete!
    echo ========================================
)

echo.
echo ========================================
echo  Authentication Setup
echo ========================================
echo.

:: Check for existing OpenAI API key
set "HAS_OPENAI_KEY=0"
if defined OPENAI_API_KEY set "HAS_OPENAI_KEY=1"

:: Show current auth status
echo Current status:
if !HAS_OPENAI_KEY!==1 (
    echo   OpenAI API Key: Set
) else (
    echo   OpenAI API Key: Not set
)
echo   Claude/Gemini: Require browser login
echo.

:: Ask about authentication
set /p DO_AUTH="Set up authentication now? (Y/N): "
if /i "!DO_AUTH!" neq "Y" goto :skip_auth

:: OpenAI API Key
echo.
echo ----------------------------------------
echo  OpenAI API Key
echo ----------------------------------------
if !HAS_OPENAI_KEY!==1 (
    echo   Already set. Skipping.
) else (
    echo   Get your key at: https://platform.openai.com/api-keys
    echo.
    set /p OPENAI_KEY="  Enter API key (or press Enter to skip): "
    if defined OPENAI_KEY (
        setx OPENAI_API_KEY "!OPENAI_KEY!" >nul 2>&1
        if !errorlevel!==0 (
            set "OPENAI_API_KEY=!OPENAI_KEY!"
            echo   API key saved successfully.
            :: Update auth_status in config
            powershell -Command "(Get-Content 'config\role_config.json') -replace '\"openai\": false', '\"openai\": true' | Set-Content 'config\role_config.json'" >nul 2>&1
        ) else (
            echo   ERROR: Could not save API key.
        )
    ) else (
        echo   Skipped.
    )
)

:: Claude Code
echo.
echo ----------------------------------------
echo  Claude Code Authentication
echo ----------------------------------------
echo   This will open a browser for login.
set /p DO_CLAUDE="  Authenticate Claude now? (Y/N): "
if /i "!DO_CLAUDE!"=="Y" (
    echo   Launching Claude Code...
    echo   Complete the browser login, then type 'exit' to continue.
    echo.
    call claude
    echo   Claude authentication complete.
    :: Update auth_status in config
    powershell -Command "(Get-Content 'config\role_config.json') -replace '\"claude\": false', '\"claude\": true' | Set-Content 'config\role_config.json'" >nul 2>&1
)

:: Gemini CLI
echo.
echo ----------------------------------------
echo  Gemini CLI Authentication
echo ----------------------------------------
echo   This will open a browser for Google login.
set /p DO_GEMINI="  Authenticate Gemini now? (Y/N): "
if /i "!DO_GEMINI!"=="Y" (
    echo   Launching Gemini CLI...
    echo   Complete the browser login, then type 'exit' to continue.
    echo.
    call gemini
    echo   Gemini authentication complete.
    :: Update auth_status in config
    powershell -Command "(Get-Content 'config\role_config.json') -replace '\"gemini\": false', '\"gemini\": true' | Set-Content 'config\role_config.json'" >nul 2>&1
)

:skip_auth
echo.
echo ========================================
echo  Setup Complete!
echo ========================================
echo.
echo   Run 'run.bat' to start working.
echo.
pause
