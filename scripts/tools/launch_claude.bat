@echo off
setlocal enabledelayedexpansion
title Claude Code - Terminal AI Workflow

:: Navigate to project root (two levels up from this script)
set "PROJECT_ROOT=%~dp0..\.."
pushd "%PROJECT_ROOT%"

:: Read the task
set "TASK="
if exist "config\tasks\claude.txt" (
    set /p TASK=<"config\tasks\claude.txt"
)

echo.
echo  ========================================
echo   Claude Code
echo  ========================================
echo.
if defined TASK (
    echo  Task: !TASK!
    echo.
    echo  ----------------------------------------
    echo.
    :: Use --print mode for non-interactive output with auto-approval
    claude --print --dangerously-skip-permissions "!TASK!"
) else (
    echo  No task assigned. Starting interactive mode...
    echo.
    claude
)

popd
endlocal
