@echo off
:: ========================================
:: Terminal AI Workflow - Main Entry Point
:: ========================================
:: Routes tasks to Claude, Gemini, and OpenAI
:: Launches tools concurrently in separate windows

setlocal enabledelayedexpansion
cd /d "%~dp0"

:: Initialize logging
set "LOGFILE=logs\run.log"
if not exist "logs" mkdir logs
for /f "tokens=*" %%I in ('powershell -Command "Get-Date -Format 'yyyy-MM-dd HH:mm:ss'"') do set "TIMESTAMP=%%I"

echo.
echo  ========================================
echo   Terminal AI Workflow
echo  ========================================
echo.

:: Check if input provided as argument
if not "%~1"=="" (
    set "INPUT=%*"
    goto :process
)

:: Prompt for input
echo  Enter your task(s) or use a /command:
echo.
echo  Commands:
echo    /help     - Show this help message
echo    /status   - Check tool availability
echo    /config   - Show current configuration
echo    /history  - List recent sessions
echo    /summary  - View outputs from last session
echo    /log      - View recent log entries
echo    /clear    - Clear task files
echo    /cleanup  - Remove old workspaces
echo    /test     - Run system validation
echo.
echo  Examples:
echo    - Research Python web frameworks
echo    - Build a REST API. Research best practices. Analyze for security.
echo.
set /p INPUT="  > "

if "!INPUT!"=="" (
    echo.
    echo  No input provided. Exiting.
    exit /b 1
)

:: Validate input - check for obviously invalid characters
echo !INPUT! | findstr /r "[\<\>\|\&]" >nul
if not errorlevel 1 (
    echo.
    echo  Invalid characters in input. Please avoid ^< ^> ^| ^&
    exit /b 1
)

:: Handle slash commands
if /i "!INPUT!"=="/help" goto :cmd_help
if /i "!INPUT!"=="/status" goto :cmd_status
if /i "!INPUT!"=="/config" goto :cmd_config
if /i "!INPUT!"=="/history" goto :cmd_history
if /i "!INPUT!"=="/summary" goto :cmd_summary
if /i "!INPUT!"=="/clear" goto :cmd_clear
if /i "!INPUT!"=="/cleanup" goto :cmd_cleanup
if /i "!INPUT!"=="/log" goto :cmd_log
if /i "!INPUT!"=="/test" goto :cmd_test

:process
:: Log the task submission
echo [%TIMESTAMP%] TASK: !INPUT! >> "%LOGFILE%"
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

:: Check for active tools
if not exist "config\tasks\_active.txt" (
    echo  No tasks to execute.
    exit /b 0
)

:: Read active tools
set /p ACTIVE=<"config\tasks\_active.txt"
echo.
echo  Active tools: %ACTIVE%
echo.

:: Ask for execution mode
echo  How would you like to run?
echo    [1] Concurrent - Launch all tools in separate windows
echo    [2] Sequential - Run tools one at a time (CLI mode)
echo    [3] Exit
echo.
set /p MODE="  Choice (1/2/3): "

if "%MODE%"=="1" goto :concurrent
if "%MODE%"=="2" goto :sequential
if "%MODE%"=="3" goto :end
goto :end

:concurrent
echo.
echo  Launching tools concurrently...

:: Launch each active tool in a new window
echo %ACTIVE% | findstr /i "claude" >nul
if not errorlevel 1 (
    start "Claude Code" cmd /k "scripts\tools\launch_claude.bat"
)

echo %ACTIVE% | findstr /i "gemini" >nul
if not errorlevel 1 (
    start "Gemini CLI" cmd /k "scripts\tools\launch_gemini.bat"
)

echo %ACTIVE% | findstr /i "openai" >nul
if not errorlevel 1 (
    start "OpenAI Codex" cmd /k "scripts\tools\launch_openai.bat"
)

:: Arrange windows
timeout /t 2 /nobreak >nul
powershell -ExecutionPolicy Bypass -File "scripts\tools\arrange_windows.ps1"

echo.
echo  Tools launched. Check the opened windows.
goto :end

:sequential
echo.
powershell -ExecutionPolicy Bypass -File "scripts\run_cli.ps1"
goto :end

:: ========================================
:: Slash Commands
:: ========================================

:cmd_help
echo.
echo  ========================================
echo   Available Commands
echo  ========================================
echo.
echo   /help     - Show this help message
echo   /status   - Check tool availability (claude, gemini, codex)
echo   /config   - Show current role configuration
echo   /history  - List recent sessions
echo   /summary  - View outputs from last session
echo   /log      - View recent log entries
echo   /clear    - Clear all task files
echo   /cleanup  - Remove workspaces older than 7 days
echo   /test     - Run full system validation
echo.
echo   Task Examples:
echo     Research machine learning trends
echo     Build a REST API. Analyze for security. Review code quality.
echo.
goto :end

:cmd_status
echo.
echo  Checking tool availability...
echo.
where claude >nul 2>nul && (echo   [+] Claude Code: installed) || (echo   [-] Claude Code: not found)
where gemini >nul 2>nul && (echo   [+] Gemini CLI: installed) || (echo   [-] Gemini CLI: not found)
where codex >nul 2>nul && (echo   [+] OpenAI Codex: installed) || (echo   [-] OpenAI Codex: not found)
echo.
goto :end

:cmd_config
echo.
echo  Current Configuration:
echo.
powershell -ExecutionPolicy Bypass -Command "Get-Content 'config\role_config.json' | ConvertFrom-Json | ForEach-Object { $_.roles.PSObject.Properties | ForEach-Object { Write-Host ('  ' + $_.Name + ': primary=' + $_.Value.primary + ', keywords=[' + ($_.Value.keywords -join ',') + ']') } }"
echo.
goto :end

:cmd_history
echo.
echo  Recent Sessions:
echo.
powershell -ExecutionPolicy Bypass -Command "Get-ChildItem 'workspace' -Directory -ErrorAction SilentlyContinue | Sort-Object Name -Descending | Select-Object -First 10 | ForEach-Object { $session = Get-Content (Join-Path $_.FullName '_session.json') -ErrorAction SilentlyContinue | ConvertFrom-Json; if ($session) { Write-Host ('  ' + $_.Name + ' - ' + ($session.tasks.PSObject.Properties.Name -join ', ')) } else { Write-Host ('  ' + $_.Name) } }"
echo.
goto :end

:cmd_clear
echo.
echo  Clearing task files...
del /q "config\tasks\*.txt" 2>nul
echo   [+] Task files cleared
echo.
goto :end

:cmd_log
echo.
echo  ========================================
echo   Recent Log Entries
echo  ========================================
echo.
if exist "%LOGFILE%" (
    powershell -ExecutionPolicy Bypass -Command "Get-Content '%LOGFILE%' -Tail 20"
) else (
    echo   No log file found yet. Run some tasks first.
)
echo.
goto :end

:cmd_summary
echo.
echo  ========================================
echo   Last Session Summary
echo  ========================================
echo.
powershell -ExecutionPolicy Bypass -Command "$latest = Get-ChildItem 'workspace' -Directory -ErrorAction SilentlyContinue | Sort-Object Name -Descending | Select-Object -First 1; if ($latest) { Write-Host '  Session: ' $latest.Name -ForegroundColor Cyan; $session = Get-Content (Join-Path $latest.FullName '_session.json') -ErrorAction SilentlyContinue | ConvertFrom-Json; if ($session) { Write-Host '  Tasks:' -ForegroundColor Yellow; $session.tasks.PSObject.Properties | ForEach-Object { Write-Host ('    ' + $_.Name + ': ' + $_.Value) } }; Write-Host ''; Write-Host '  Outputs:' -ForegroundColor Yellow; Get-ChildItem $latest.FullName -Filter '*_output.txt' | ForEach-Object { Write-Host ('    ' + $_.Name + ':') -ForegroundColor Green; Get-Content $_.FullName -TotalCount 10 | ForEach-Object { Write-Host ('      ' + $_) }; Write-Host '      ...' } } else { Write-Host '  No sessions found.' }"
echo.
goto :end

:cmd_cleanup
echo.
echo  ========================================
echo   Cleanup Old Workspaces
echo  ========================================
echo.
powershell -ExecutionPolicy Bypass -Command "$cutoff = (Get-Date).AddDays(-7); $old = Get-ChildItem 'workspace' -Directory -ErrorAction SilentlyContinue | Where-Object { $_.CreationTime -lt $cutoff }; if ($old) { $count = $old.Count; $old | Remove-Item -Recurse -Force; Write-Host ('  Removed ' + $count + ' workspace(s) older than 7 days.') -ForegroundColor Green } else { Write-Host '  No old workspaces to clean up.' -ForegroundColor Yellow }"
echo.
goto :end

:cmd_test
echo.
powershell -ExecutionPolicy Bypass -File "scripts\test_setup.ps1"
goto :end

:end
echo.
echo  ========================================
echo   Done
echo  ========================================
endlocal
