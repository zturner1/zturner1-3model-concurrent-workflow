@echo off
setlocal enabledelayedexpansion
cd /d "%~dp0..\.."

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
