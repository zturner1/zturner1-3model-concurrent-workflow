@echo off
setlocal

echo ========================================
echo  Terminal AI Workflow - 3 Model System
echo ========================================
echo.
echo  Project: %cd%
echo.
echo  [1] Claude Code  - Deep work, agents, complex tasks
echo  [2] Gemini CLI   - Research, exploration, web search
echo  [3] OpenAI CLI   - High-level analysis, code review
echo  [4] All Three    - Open in separate terminals
echo  [5] Exit
echo.
set /p choice="Select tool (1-5): "

if "%choice%"=="1" goto claude
if "%choice%"=="2" goto gemini
if "%choice%"=="3" goto openai
if "%choice%"=="4" goto all
if "%choice%"=="5" goto end

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

:openai
echo.
echo Starting OpenAI CLI (Codex)...
echo Context will load from OPENAI.md
echo.
call codex
goto end

:all
echo.
echo Launching all three AI tools...
echo.
echo [1/3] Opening Claude Code...
start cmd /k "cd /d %cd% && title Claude Code && claude"
timeout /t 1 >nul

echo [2/3] Opening Gemini CLI...
start cmd /k "cd /d %cd% && title Gemini CLI && gemini"
timeout /t 1 >nul

echo [3/3] Opening OpenAI CLI...
start cmd /k "cd /d %cd% && title OpenAI Codex && codex"

echo.
echo All three tools launched in separate windows.
echo.
echo Workflow tips:
echo   - Use Claude for complex tasks and agents
echo   - Use Gemini for research and web search
echo   - Use OpenAI for analysis and code review
echo   - Update shared-context.md when switching focus
echo.
pause
goto end

:end
endlocal
