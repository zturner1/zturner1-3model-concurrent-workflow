@echo off
setlocal enabledelayedexpansion

:menu
cls
echo ========================================
echo  🤖 Terminal AI Workflow - 3 Model System
echo ========================================
echo.
echo  [1] 🟣 Claude Code  - Deep work, agents
echo  [2] 🔵 Gemini CLI   - Research, web search
echo  [3] 🟢 OpenAI CLI   - Analysis, code review
echo  [4] 🚀 All Three    - Launch all concurrently
echo  [5] Exit
echo.
set /p CHOICE="Select option (1-5): "

if "!CHOICE!"=="1" goto claude
if "!CHOICE!"=="2" goto gemini
if "!CHOICE!"=="3" goto openai
if "!CHOICE!"=="4" goto all_three
if "!CHOICE!"=="5" goto end
echo Invalid choice. Please select 1-5.
timeout /t 2 >nul
goto menu

:claude
echo.
echo ========================================
echo  Launching Claude Code
echo ========================================
echo.
where claude >nul 2>nul
if %errorlevel% neq 0 (
    echo ERROR: Claude not found. Run install.bat first.
    pause
    goto menu
)
call claude
echo.
echo Claude session ended.
pause
goto menu

:gemini
echo.
echo ========================================
echo  Launching Gemini CLI
echo ========================================
echo.
where gemini >nul 2>nul
if %errorlevel% neq 0 (
    echo ERROR: Gemini not found. Run install.bat first.
    pause
    goto menu
)
call gemini
echo.
echo Gemini session ended.
pause
goto menu

:openai
echo.
echo ========================================
echo  Launching OpenAI CLI
echo ========================================
echo.
where codex >nul 2>nul
if %errorlevel% neq 0 (
    echo ERROR: OpenAI CLI not found. Run install.bat first.
    pause
    goto menu
)
call codex
echo.
echo OpenAI session ended.
pause
goto menu

:all_three
echo.
echo ========================================
echo  Launching All Three AI Tools
echo ========================================
echo.

:: Check all tools are available
set ALL_OK=1
where claude >nul 2>nul || (
    echo ERROR: Claude not found
    set ALL_OK=0
)
where gemini >nul 2>nul || (
    echo ERROR: Gemini not found
    set ALL_OK=0
)
where codex >nul 2>nul || (
    echo ERROR: OpenAI CLI not found
    set ALL_OK=0
)

if !ALL_OK!==0 (
    echo.
    echo One or more tools not installed. Run install.bat first.
    pause
    goto menu
)

echo Starting Claude Code...
start cmd /k "title Claude Code - Deep Work ^& Agents && cd /d %cd% && echo ======================================== && echo  Claude Code - Deep Work ^& Agents && echo ======================================== && echo. && echo Context: CLAUDE.md && echo. && claude"

echo Starting Gemini CLI...
start cmd /k "title Gemini CLI - Research ^& Web Search && cd /d %cd% && echo ======================================== && echo  Gemini CLI - Research ^& Web Search && echo ======================================== && echo. && echo Context: GEMINI.md && echo. && gemini"

echo Starting OpenAI CLI...
start cmd /k "title OpenAI CLI - Analysis ^& Code Review && cd /d %cd% && echo ======================================== && echo  OpenAI CLI - Analysis ^& Code Review && echo ======================================== && echo. && echo Context: OPENAI.md && echo. && codex"

echo.
echo ========================================
echo  All three tools launched!
echo ========================================
echo.
echo  Check the new windows for each tool.
echo  All tools share the same project folder.
echo  Update shared-context.md when switching focus.
echo.
pause
goto menu

:end
echo.
echo Goodbye!
endlocal
