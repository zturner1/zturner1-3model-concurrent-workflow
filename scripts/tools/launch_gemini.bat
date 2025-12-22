@echo off
setlocal enabledelayedexpansion
cd /d "%~dp0..\.."

:: Read the task
set "TASK="
if exist "config\tasks\gemini.txt" (
    set /p TASK=<"config\tasks\gemini.txt"
)

echo.
echo Task: !TASK!
echo.
echo ----------------------------------------

:: Launch gemini with the task as argument
if defined TASK (
    gemini "!TASK!"
) else (
    gemini
)
