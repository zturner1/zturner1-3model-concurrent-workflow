@echo off
cd /d "%~dp0..\.."
echo.
echo Task:
type config\tasks\gemini.txt
echo.
echo ----------------------------------------
gemini
