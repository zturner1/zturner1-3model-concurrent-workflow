@echo off
cd /d "%~dp0..\.."

:: Load .env if exists
if exist ".env" (
    for /f "usebackq tokens=1,* delims==" %%a in (".env") do (
        set "%%a=%%b"
    )
)

echo.
echo Task:
type config\tasks\openai.txt
echo.
echo ----------------------------------------
codex
