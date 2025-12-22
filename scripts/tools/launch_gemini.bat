@echo off
setlocal enabledelayedexpansion

:: Navigate to project root (two levels up from this script)
set "PROJECT_ROOT=%~dp0..\.."
pushd "%PROJECT_ROOT%"

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
