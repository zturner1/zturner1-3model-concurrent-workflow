@echo off
setlocal

echo ========================================
echo  Terminal AI Workflow
echo ========================================
echo.
echo  Project: %cd%
echo.
echo  [1] Claude Code  - Deep work, agents, code
echo  [2] Gemini CLI   - Research, exploration
echo  [3] Both         - Open in split terminals
echo  [4] Exit
echo.
set /p choice="Select tool (1-4): "

if "%choice%"=="1" goto claude
if "%choice%"=="2" goto gemini
if "%choice%"=="3" goto both
if "%choice%"=="4" goto end

echo Invalid choice.
pause
goto end

:claude
echo.
echo Starting Claude Code...
echo Context will load from CLAUDE.md
echo.
call claude
goto end

:gemini
echo.
echo Starting Gemini CLI...
echo Context will load from GEMINI.md
echo.
call gemini
goto end

:both
echo.
echo Opening Claude in new window...
start cmd /k "cd /d %cd% && claude"
echo.
echo Opening Gemini in new window...
start cmd /k "cd /d %cd% && gemini"
echo.
echo Both tools launched in separate windows.
goto end

:end
endlocal
