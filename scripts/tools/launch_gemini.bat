@echo off
setlocal enabledelayedexpansion
title Gemini CLI - Terminal AI Workflow

:: Navigate to project root (two levels up from this script)
set "PROJECT_ROOT=%~dp0..\.."
pushd "%PROJECT_ROOT%"

:: Read the task
set "TASK="
if exist "config\tasks\gemini.txt" (
    set /p TASK=<"config\tasks\gemini.txt"
)

echo.
echo  ========================================
echo   Gemini CLI
echo  ========================================
echo.
if defined TASK (
    echo  Task: !TASK!
    echo.
    echo  ----------------------------------------
    echo.
    :: Run gemini via PowerShell Start-Job to isolate stdin and prevent abort
    powershell -NoProfile -Command "$job = Start-Job -ScriptBlock { param($t) gemini -y $t } -ArgumentList '%TASK%'; $job | Wait-Job | Receive-Job; $job | Remove-Job -Force"
) else (
    echo  No task assigned. Starting interactive mode...
    echo.
    gemini
)

popd
endlocal
