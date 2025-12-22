@echo off
setlocal enabledelayedexpansion
cd /d "%~dp0..\.."

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
echo Task: !TASK!
echo.
echo ----------------------------------------

:: Launch codex with the task as argument
if defined TASK (
    codex "!TASK!"
) else (
    codex
)
