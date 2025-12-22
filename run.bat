@echo off
setlocal enabledelayedexpansion

:: ========================================
:: Terminal AI Workflow - Interactive Router
:: ========================================

:: Load .env file if it exists
if exist ".env" (
    for /f "usebackq tokens=1,* delims==" %%a in (".env") do (
        set "varname=%%a"
        set "varvalue=%%b"
        if not "!varname:~0,1!"=="#" (
            if not "!varname!"=="" (
                set "!varname!=!varvalue!"
            )
        )
    )
)

echo ========================================
echo  Terminal AI Workflow - 3 Model System
echo ========================================
echo.
echo  Type your task(s) and press Enter.
echo  Multiple sentences are split and routed to appropriate tools.
echo.
echo  Commands: /help, /status, /tasks, /exit
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
    echo  Routing is based on first word of each sentence:
    echo.
    echo    deep_work keywords  -^> Claude (default)
    echo      build, create, fix, implement, write, develop,
    echo      refactor, agent, complex, multi-step
    echo.
    echo    research keywords   -^> Gemini
    echo      research
    echo.
    echo    analysis keywords   -^> OpenAI
    echo      analyze, review
    echo.
    echo  Example: "Research AI trends. Build a summary. Review the draft."
    echo           This launches all 3 tools concurrently.
    echo.
    echo  Commands:
    echo    /help   - Show this help
    echo    /status - Check tool availability
    echo    /tasks  - Show current active tasks
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
    echo  Environment:
    if exist ".env" (echo    [+] .env file found) else (echo    [-] .env file not found)
    if defined OPENAI_API_KEY (echo    [+] OPENAI_API_KEY set) else (echo    [-] OPENAI_API_KEY not set)
    echo.
    goto prompt
)

if /i "!INPUT!"=="/tasks" (
    echo.
    echo  Current Active Tasks:
    echo  ----------------------------------------
    if exist "config\tasks\claude.txt" (
        echo  [Claude]
        type "config\tasks\claude.txt"
        echo.
    )
    if exist "config\tasks\gemini.txt" (
        echo  [Gemini]
        type "config\tasks\gemini.txt"
        echo.
    )
    if exist "config\tasks\openai.txt" (
        echo  [OpenAI]
        type "config\tasks\openai.txt"
        echo.
    )
    if not exist "config\tasks\claude.txt" if not exist "config\tasks\gemini.txt" if not exist "config\tasks\openai.txt" (
        echo  No active tasks.
    )
    echo  ----------------------------------------
    echo.
    goto prompt
)

:: Ensure tasks directory exists
if not exist "config\tasks" mkdir "config\tasks"

:: Clear previous task files
if exist "config\tasks\claude.txt" del "config\tasks\claude.txt" >nul 2>nul
if exist "config\tasks\gemini.txt" del "config\tasks\gemini.txt" >nul 2>nul
if exist "config\tasks\openai.txt" del "config\tasks\openai.txt" >nul 2>nul
if exist "config\tasks\_active.txt" del "config\tasks\_active.txt" >nul 2>nul

echo.
echo  ----------------------------------------
echo  Analyzing and Routing Tasks
echo  ----------------------------------------

:: Save input to temp file to avoid quoting issues
echo !INPUT!> "config\tasks\_input.txt"

:: Use PowerShell to parse sentences and route to tools
powershell -ExecutionPolicy Bypass -File "scripts\route_tasks.ps1"

if %errorlevel% neq 0 (
    echo    Error: PowerShell routing failed.
    echo.
    goto prompt
)

echo.
echo  ----------------------------------------
echo  Launching Tools
echo  ----------------------------------------

:: Read active tools and launch them
set "ACTIVE_TOOLS="
if exist "config\tasks\_active.txt" (
    for /f "usebackq tokens=*" %%t in ("config\tasks\_active.txt") do set "ACTIVE_TOOLS=%%t"
)

if "!ACTIVE_TOOLS!"=="" (
    echo    No tools to launch.
    echo.
    goto prompt
)

:: Parse and launch each tool using launcher scripts
for %%t in (!ACTIVE_TOOLS!) do (
    if "%%t"=="claude" (
        echo    Starting Claude Code...
        start "Claude Code - Deep Work" cmd /k "%cd%\scripts\tools\launch_claude.bat"
    )
    if "%%t"=="gemini" (
        echo    Starting Gemini CLI...
        start "Gemini CLI - Research" cmd /k "%cd%\scripts\tools\launch_gemini.bat"
    )
    if "%%t"=="openai" (
        echo    Starting OpenAI Codex...
        start "OpenAI Codex - Analysis" cmd /k "%cd%\scripts\tools\launch_openai.bat"
    )
)

:: Update shared-context.md with task distribution
echo.
echo  ----------------------------------------
echo  Updating shared-context.md
echo  ----------------------------------------

powershell -ExecutionPolicy Bypass -Command ^
"$date = Get-Date -Format 'yyyy-MM-dd HH:mm'; ^
$entry = \"`n## Active Tasks (routed $date)`n\"; ^
if (Test-Path 'config\tasks\claude.txt') { $entry += \"- claude: $(Get-Content 'config\tasks\claude.txt' -Raw)`n\" }; ^
if (Test-Path 'config\tasks\gemini.txt') { $entry += \"- gemini: $(Get-Content 'config\tasks\gemini.txt' -Raw)`n\" }; ^
if (Test-Path 'config\tasks\openai.txt') { $entry += \"- openai: $(Get-Content 'config\tasks\openai.txt' -Raw)`n\" }; ^
Add-Content 'shared-context.md' $entry; ^
Write-Host '    Updated shared-context.md'"

echo.
echo  ========================================
echo  Routing Complete - Tools Running
echo  ========================================
echo.

goto prompt

:end
echo.
echo Goodbye!
endlocal
