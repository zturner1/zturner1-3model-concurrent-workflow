@echo off
setlocal enabledelayedexpansion
title OpenAI Codex - Terminal AI Workflow

:: Navigate to project root (two levels up from this script)
set "PROJECT_ROOT=%~dp0..\.."
pushd "%PROJECT_ROOT%"

:: Load .env if exists
if exist ".env" (
    for /f "usebackq tokens=1,* delims==" %%a in (".env") do (
        set "%%a=%%b"
    )
)

:: Read the task
set "TASK="
if exist "config\tasks\openai.txt" (
    set /p TASK=<"config\tasks\openai.txt"
)

echo.
echo  ========================================
echo   OpenAI Codex
echo  ========================================
echo.
if defined TASK (
    echo  Task: !TASK!
    echo.
    echo  ----------------------------------------
    echo.
    :: Use 'exec --full-auto' for non-interactive mode with auto-approval
    codex exec --full-auto --skip-git-repo-check "!TASK!"
) else (
    echo  No task assigned. Starting interactive mode...
    echo.
    codex
)

popd
endlocal
