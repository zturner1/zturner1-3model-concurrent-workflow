@echo off
setlocal enabledelayedexpansion

:: ========================================
:: Terminal AI Workflow - Interactive Router
:: ========================================

:: Check for CLI mode argument
set "CLI_MODE=0"
set "QUIET_MODE=0"
for %%a in (%*) do (
    if /i "%%a"=="/cli" set "CLI_MODE=1"
    if /i "%%a"=="--cli" set "CLI_MODE=1"
    if /i "%%a"=="/quiet" set "QUIET_MODE=1"
    if /i "%%a"=="--quiet" set "QUIET_MODE=1"
)

:: Setup logging
set "LOGFILE=logs\run.log"
set "MAX_LOG_SIZE=104857600"
if not exist "logs" mkdir "logs"

:: Check log size and rotate if over 100MB
if exist "%LOGFILE%" (
    for %%A in ("%LOGFILE%") do set "LOGSIZE=%%~zA"
    if !LOGSIZE! GEQ %MAX_LOG_SIZE% (
        if exist "logs\run.log.5" del "logs\run.log.5"
        if exist "logs\run.log.4" ren "logs\run.log.4" "run.log.5"
        if exist "logs\run.log.3" ren "logs\run.log.3" "run.log.4"
        if exist "logs\run.log.2" ren "logs\run.log.2" "run.log.3"
        if exist "logs\run.log.1" ren "logs\run.log.1" "run.log.2"
        ren "%LOGFILE%" "run.log.1"
        echo Log rotated: %date% %time% > "%LOGFILE%"
    )
)

:: Append session header
echo. >> "%LOGFILE%"
echo ======================================== >> "%LOGFILE%"
if !CLI_MODE!==1 (
    echo Session started [CLI MODE]: %date% %time% >> "%LOGFILE%"
) else (
    echo Session started: %date% %time% >> "%LOGFILE%"
)
echo ======================================== >> "%LOGFILE%"

:: Load .env file if it exists
if exist ".env" (
    for /f "usebackq tokens=1,* delims==" %%a in (".env") do (
        set "varname=%%a"
        set "varvalue=%%b"
        if not "!varname:~0,1!"=="#" if not "!varname!"=="" set "!varname!=!varvalue!"
    )
)

:: Display header
echo ========================================
if !CLI_MODE!==1 (
    echo  Terminal AI Workflow - CLI Mode
) else (
    echo  Terminal AI Workflow - 3 Model System
)
echo ========================================
echo.
echo  Type your task(s) and press Enter.
echo  Multiple sentences are split and routed to appropriate tools.
echo.
if !CLI_MODE!==1 (
    echo  Mode: CLI (sequential execution, single terminal)
) else (
    echo  Mode: GUI (concurrent execution, separate windows)
)
echo  Commands: /help, /status, /tasks, /log, /exit
echo ========================================
echo.

:prompt
set "INPUT="
set /p INPUT="> "

if "!INPUT!"=="" goto prompt
echo [%time%] Input: !INPUT! >> "%LOGFILE%"

:: Check for commands
if /i "!INPUT!"=="/exit" goto end
if /i "!INPUT!"=="/quit" goto end
if /i "!INPUT!"=="/help" goto cmd_help
if /i "!INPUT!"=="/status" goto cmd_status
if /i "!INPUT!"=="/log" goto cmd_log
if /i "!INPUT!"=="/tasks" goto cmd_tasks

:: Not a command, process as task
goto process_task

:cmd_help
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
echo    /log    - Show recent log entries
echo    /exit   - Exit the CLI
echo.
echo  Launch options:
echo    run.bat          - GUI mode (separate windows)
echo    run.bat /cli     - CLI mode (sequential, single terminal)
echo.
goto prompt

:cmd_status
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
echo  Mode:
if !CLI_MODE!==1 (echo    CLI mode (sequential^)) else (echo    GUI mode (concurrent^))
echo.
goto prompt

:cmd_log
echo.
echo  Recent log entries:
echo  ----------------------------------------
powershell -Command "Get-Content '%LOGFILE%' -Tail 20"
echo  ----------------------------------------
echo.
goto prompt

:cmd_tasks
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
if not exist "config\tasks\claude.txt" if not exist "config\tasks\gemini.txt" if not exist "config\tasks\openai.txt" echo  No active tasks.
echo  ----------------------------------------
echo.
goto prompt

:process_task
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
powershell -ExecutionPolicy Bypass -File "scripts\route_tasks.ps1" >> "%LOGFILE%" 2>&1
if %errorlevel% neq 0 (
    echo    Error: PowerShell routing failed.
    echo [%time%] ERROR: PowerShell routing failed >> "%LOGFILE%"
    echo.
    goto prompt
)

:: Show routing in console
powershell -ExecutionPolicy Bypass -File "scripts\route_tasks.ps1"

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

:: Branch based on mode
if !CLI_MODE!==1 goto launch_cli
goto launch_gui

:launch_cli
:: CLI Mode - Sequential execution in same terminal
echo    Mode: CLI (sequential)
echo [%time%] Launching in CLI mode >> "%LOGFILE%"

if !QUIET_MODE!==1 (
    powershell -ExecutionPolicy Bypass -File "%cd%\scripts\run_cli.ps1" -Quiet
) else (
    powershell -ExecutionPolicy Bypass -File "%cd%\scripts\run_cli.ps1"
)

goto post_launch

:launch_gui
:: GUI Mode - Concurrent execution in separate windows
echo    Mode: GUI (concurrent)

:: Parse and launch each tool using launcher scripts
for %%t in (!ACTIVE_TOOLS!) do (
    if "%%t"=="claude" (
        echo    Starting Claude Code...
        echo [%time%] Launching Claude Code >> "%LOGFILE%"
        start "Claude Code - Deep Work" cmd /k "%cd%\scripts\tools\launch_claude.bat"
    )
    if "%%t"=="gemini" (
        echo    Starting Gemini CLI...
        echo [%time%] Launching Gemini CLI >> "%LOGFILE%"
        start "Gemini CLI - Research" cmd /k "%cd%\scripts\tools\launch_gemini.bat"
    )
    if "%%t"=="openai" (
        echo    Starting OpenAI Codex...
        echo [%time%] Launching OpenAI Codex >> "%LOGFILE%"
        start "OpenAI Codex - Analysis" cmd /k "%cd%\scripts\tools\launch_openai.bat"
    )
)

:: Arrange windows side by side (GUI mode only)
echo.
echo  ----------------------------------------
echo  Arranging Windows
echo  ----------------------------------------
powershell -ExecutionPolicy Bypass -File "%cd%\scripts\tools\arrange_windows.ps1"

:post_launch
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

:: Show workspace location
set "WORKSPACE="
if exist "config\tasks\_workspace.txt" (
    for /f "usebackq tokens=*" %%w in ("config\tasks\_workspace.txt") do set "WORKSPACE=%%w"
)

echo.
echo  ========================================
echo  Routing Complete - Tools Running
echo  ========================================
if defined WORKSPACE (
    echo  Shared Workspace: !WORKSPACE!
    if !CLI_MODE!==1 (
        echo  Output files saved to workspace folder.
    ) else (
        echo  Agents will coordinate via this folder.
    )
)
echo.

goto prompt

:end
echo.
echo Goodbye!
echo [%time%] Session ended >> "%LOGFILE%"
endlocal
