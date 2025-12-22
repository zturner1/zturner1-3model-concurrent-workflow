@echo off
setlocal enabledelayedexpansion

:: Navigate to project root (two levels up from this script)
set "PROJECT_ROOT=%~dp0..\.."
pushd "%PROJECT_ROOT%"

:: Read the task
set "TASK="
if exist "config\tasks\claude.txt" (
    set /p TASK=<"config\tasks\claude.txt"
)

echo.
echo Task: !TASK!
echo.
echo ----------------------------------------

:: Launch claude with the task as argument
if defined TASK (
    claude "!TASK!"
) else (
    claude
)
