@echo off
setlocal enabledelayedexpansion

echo ========================================
echo  Terminal AI Workflow - 3 Model System
echo ========================================
echo.
echo  Type your task and press Enter.
echo  Commands: /help, /status, /exit
echo ========================================
echo.

:prompt
set "INPUT="
set /p INPUT="> "

if "!INPUT!"=="" goto prompt
if /i "!INPUT!"=="/exit" goto end
if /i "!INPUT!"=="/quit" goto end

if /i "!INPUT!"=="/help" (
    echo.
    echo  First word determines routing:
    echo    research, search, find    -^> Gemini
    echo    review, analyze, evaluate -^> OpenAI
    echo    build, create, fix        -^> Claude
    echo.
    echo  Commands:
    echo    /help   - Show this help
    echo    /status - Check tool availability
    echo    /exit   - Exit the CLI
    echo.
    goto prompt
)

if /i "!INPUT!"=="/status" (
    echo.
    echo  Checking tool availability...
    where claude >nul 2>nul && echo    [+] Claude available || echo    [-] Claude not found
    where gemini >nul 2>nul && echo    [+] Gemini available || echo    [-] Gemini not found
    where codex >nul 2>nul && echo    [+] OpenAI available || echo    [-] OpenAI not found
    echo.
    goto prompt
)

:: Extract first word
for /f "tokens=1" %%w in ("!INPUT!") do set "KEYWORD=%%w"

:: Route based on keyword
set "TARGET=claude"

:: Research keywords
for %%k in (research search find explore lookup investigate discover learn) do (
    if /i "!KEYWORD!"=="%%k" set "TARGET=gemini"
)

:: Analysis keywords
for %%k in (review analyze evaluate compare assess critique audit examine) do (
    if /i "!KEYWORD!"=="%%k" set "TARGET=openai"
)

echo.
echo  Routing: !KEYWORD! -^> !TARGET!
echo  ----------------------------------------

if "!TARGET!"=="claude" call claude
if "!TARGET!"=="gemini" call gemini
if "!TARGET!"=="openai" call codex

echo  ----------------------------------------
echo  Session ended.
echo.
goto prompt

:end
echo Goodbye!
endlocal
