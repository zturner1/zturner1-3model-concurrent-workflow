@echo off
setlocal enabledelayedexpansion

:: ========================================
:: Terminal AI Workflow - Task Router
:: ========================================
:: Routes tasks to appropriate AI tools based on first word of each sentence

if "%~1"=="" (
    echo Usage: router.bat "Your task description here"
    echo.
    echo Example: router.bat "Research AI trends. Build a summary. Review the code."
    echo.
    pause
    exit /b 1
)

set "INPUT=%~1"

echo ========================================
echo  Task Router - Analyzing Input
echo ========================================
echo.
echo Input: %INPUT%
echo.

:: Use PowerShell to parse sentences and route to tools
powershell -ExecutionPolicy Bypass -Command ^
"$input = '%INPUT%'; ^
$config = Get-Content 'config\role_config.json' | ConvertFrom-Json; ^
$sentences = $input -split '[.!?]' | Where-Object { $_.Trim() -ne '' } | ForEach-Object { $_.Trim() }; ^
$tasks = @{}; ^
$tasks['claude'] = @(); ^
$tasks['gemini'] = @(); ^
$tasks['openai'] = @(); ^
foreach ($sentence in $sentences) { ^
    $firstWord = ($sentence -split '\s+')[0].ToLower(); ^
    $matchedRole = $null; ^
    $matchedTool = $null; ^
    foreach ($roleName in $config.roles.PSObject.Properties.Name) { ^
        $role = $config.roles.$roleName; ^
        if ($role.keywords -contains $firstWord) { ^
            $matchedRole = $roleName; ^
            $primary = $role.primary; ^
            if ($config.auth_status.$primary) { ^
                $matchedTool = $primary; ^
            } else { ^
                foreach ($fb in $role.fallback) { ^
                    if ($config.auth_status.$fb) { ^
                        $matchedTool = $fb; ^
                        break; ^
                    } ^
                } ^
            } ^
            break; ^
        } ^
    } ^
    if (-not $matchedTool) { ^
        if ($config.auth_status.claude) { $matchedTool = 'claude' } ^
        elseif ($config.auth_status.openai) { $matchedTool = 'openai' } ^
        elseif ($config.auth_status.gemini) { $matchedTool = 'gemini' } ^
    } ^
    if ($matchedTool) { ^
        $tasks[$matchedTool] += $sentence; ^
    } ^
} ^
foreach ($tool in $tasks.Keys) { ^
    if ($tasks[$tool].Count -gt 0) { ^
        $taskFile = \"config\tasks\$tool.txt\"; ^
        $tasks[$tool] -join \"`n\" | Set-Content $taskFile -Encoding UTF8; ^
        Write-Host \"  $tool -> $($tasks[$tool] -join '; ')\"; ^
    } ^
} ^
$tools = $tasks.Keys | Where-Object { $tasks[$_].Count -gt 0 }; ^
$tools -join ',' | Set-Content 'config\tasks\_active.txt' -Encoding UTF8"

echo.
echo ----------------------------------------
echo  Launching Tools
echo ----------------------------------------

:: Read active tools and launch them
if exist "config\tasks\_active.txt" (
    for /f "tokens=*" %%t in (config\tasks\_active.txt) do set "ACTIVE_TOOLS=%%t"
)

:: Parse and launch each tool
for %%t in (!ACTIVE_TOOLS!) do (
    if "%%t"=="claude" (
        echo   Starting Claude Code...
        start cmd /k "title Claude Code - Deep Work && cd /d %cd% && echo Task: && type config\tasks\claude.txt && echo. && echo ---------------------------------------- && claude"
    )
    if "%%t"=="gemini" (
        echo   Starting Gemini CLI...
        start cmd /k "title Gemini CLI - Research && cd /d %cd% && echo Task: && type config\tasks\gemini.txt && echo. && echo ---------------------------------------- && gemini"
    )
    if "%%t"=="openai" (
        echo   Starting OpenAI Codex...
        start cmd /k "title OpenAI Codex - Analysis && cd /d %cd% && echo Task: && type config\tasks\openai.txt && echo. && echo ---------------------------------------- && codex"
    )
)

:: Update shared-context.md with task distribution
echo.
echo ----------------------------------------
echo  Updating shared-context.md
echo ----------------------------------------

powershell -ExecutionPolicy Bypass -Command ^
"$date = Get-Date -Format 'yyyy-MM-dd HH:mm'; ^
$tasks = @{}; ^
if (Test-Path 'config\tasks\claude.txt') { $tasks['claude'] = Get-Content 'config\tasks\claude.txt' -Raw } ^
if (Test-Path 'config\tasks\gemini.txt') { $tasks['gemini'] = Get-Content 'config\tasks\gemini.txt' -Raw } ^
if (Test-Path 'config\tasks\openai.txt') { $tasks['openai'] = Get-Content 'config\tasks\openai.txt' -Raw } ^
$entry = \"`n## Active Tasks (routed $date)`n\"; ^
foreach ($tool in $tasks.Keys) { ^
    if ($tasks[$tool].Trim()) { ^
        $entry += \"- $tool`: $($tasks[$tool].Trim())`n\"; ^
    } ^
} ^
Add-Content 'shared-context.md' $entry; ^
Write-Host '  Updated shared-context.md'"

echo.
echo ========================================
echo  Routing Complete
echo ========================================
echo.
pause
