@echo off
setlocal enabledelayedexpansion

:: Read auth status from config
set "CLAUDE_AUTH=0"
set "GEMINI_AUTH=0"
set "OPENAI_AUTH=0"

if exist "config\role_config.json" (
    powershell -ExecutionPolicy Bypass -Command ^
        "$config = Get-Content 'config\role_config.json' | ConvertFrom-Json; ^
        if ($config.auth_status.claude) { exit 1 } else { exit 0 }"
    if !errorlevel!==1 set "CLAUDE_AUTH=1"

    powershell -ExecutionPolicy Bypass -Command ^
        "$config = Get-Content 'config\role_config.json' | ConvertFrom-Json; ^
        if ($config.auth_status.gemini) { exit 1 } else { exit 0 }"
    if !errorlevel!==1 set "GEMINI_AUTH=1"

    powershell -ExecutionPolicy Bypass -Command ^
        "$config = Get-Content 'config\role_config.json' | ConvertFrom-Json; ^
        if ($config.auth_status.openai) { exit 1 } else { exit 0 }"
    if !errorlevel!==1 set "OPENAI_AUTH=1"
)

:: Set status indicators
if !CLAUDE_AUTH!==1 (set "CLAUDE_STATUS=[+]") else (set "CLAUDE_STATUS=[-]")
if !GEMINI_AUTH!==1 (set "GEMINI_STATUS=[+]") else (set "GEMINI_STATUS=[-]")
if !OPENAI_AUTH!==1 (set "OPENAI_STATUS=[+]") else (set "OPENAI_STATUS=[-]")

echo ========================================
echo  Terminal AI Workflow - 3 Model System
echo ========================================
echo.
echo  Project: %cd%
echo.
echo  Tool Status:
echo    !CLAUDE_STATUS! Claude  - Deep work, agents, complex tasks
echo    !GEMINI_STATUS! Gemini  - Research, exploration
echo    !OPENAI_STATUS! OpenAI  - High-level analysis, code review
echo.
echo  ----------------------------------------
echo.
echo  [1] Describe task (auto-route)
echo  [2] Claude Code
if !CLAUDE_AUTH!==0 echo      ^(not authenticated^)
echo  [3] Gemini CLI
if !GEMINI_AUTH!==0 echo      ^(not authenticated^)
echo  [4] OpenAI CLI
if !OPENAI_AUTH!==0 echo      ^(not authenticated^)
echo  [5] All authenticated tools
echo  [6] Exit
echo.
set /p choice="Select option (1-6): "

if "!choice!"=="1" goto autoroute
if "!choice!"=="2" goto claude
if "!choice!"=="3" goto gemini
if "!choice!"=="4" goto openai
if "!choice!"=="5" goto all
if "!choice!"=="6" goto end

echo Invalid choice.
pause
goto end

:autoroute
echo.
set /p TASK="Describe your task: "
if "!TASK!"=="" (
    echo No task entered.
    pause
    goto end
)
call router.bat "!TASK!"
goto end

:claude
if !CLAUDE_AUTH!==0 (
    echo.
    echo WARNING: Claude is not authenticated.
    echo Run install.bat to authenticate first.
    pause
    goto end
)
echo.
echo Starting Claude Code...
echo Context will load from CLAUDE.md
echo.
call claude
goto end

:gemini
if !GEMINI_AUTH!==0 (
    echo.
    echo WARNING: Gemini is not authenticated.
    echo Run install.bat to authenticate first.
    pause
    goto end
)
echo.
echo Starting Gemini CLI...
echo Context will load from GEMINI.md
echo.
call gemini
goto end

:openai
if !OPENAI_AUTH!==0 (
    echo.
    echo WARNING: OpenAI is not authenticated.
    echo Run install.bat to authenticate first.
    pause
    goto end
)
echo.
echo Starting OpenAI CLI (Codex)...
echo Context will load from OPENAI.md
echo.
call codex
goto end

:all
echo.
echo Launching all authenticated tools...
echo.

set "LAUNCHED=0"

if !CLAUDE_AUTH!==1 (
    echo   Starting Claude Code...
    start cmd /k "cd /d %cd% && title Claude Code - Deep Work && claude"
    timeout /t 1 >nul
    set /a LAUNCHED+=1
)

if !GEMINI_AUTH!==1 (
    echo   Starting Gemini CLI...
    start cmd /k "cd /d %cd% && title Gemini CLI - Research && gemini"
    timeout /t 1 >nul
    set /a LAUNCHED+=1
)

if !OPENAI_AUTH!==1 (
    echo   Starting OpenAI Codex...
    start cmd /k "cd /d %cd% && title OpenAI Codex - Analysis && codex"
    set /a LAUNCHED+=1
)

if !LAUNCHED!==0 (
    echo.
    echo No tools are authenticated!
    echo Run install.bat first to set up authentication.
) else (
    echo.
    echo !LAUNCHED! tool(s) launched in separate windows.
    echo.
    echo Workflow tips:
    echo   - Use Claude for complex tasks and agents
    echo   - Use Gemini for research and web search
    echo   - Use OpenAI for analysis and code review
    echo   - Update shared-context.md when switching focus
)
echo.
pause
goto end

:end
endlocal
