# run_cli.ps1 - Run tools sequentially in CLI mode

param(
    [switch]$Quiet
)

$ErrorActionPreference = "Stop"

# Load .env if exists
if (Test-Path ".env") {
    Get-Content ".env" | ForEach-Object {
        if ($_ -and -not $_.StartsWith("#")) {
            $parts = $_ -split "=", 2
            if ($parts.Count -eq 2) {
                [Environment]::SetEnvironmentVariable($parts[0], $parts[1], "Process")
            }
        }
    }
}

# Get workspace path
$workspacePath = ""
if (Test-Path "config\tasks\_workspace.txt") {
    $workspacePath = (Get-Content "config\tasks\_workspace.txt" -Raw).Trim()
}

if (-not $workspacePath -or -not (Test-Path $workspacePath)) {
    if (-not $Quiet) {
        Write-Host "    Error: No workspace found" -ForegroundColor Red
    }
    exit 1
}

# Get active tools
if (-not (Test-Path "config\tasks\_active.txt")) {
    if (-not $Quiet) {
        Write-Host "    Error: No active tools found" -ForegroundColor Red
    }
    exit 1
}

$activeTools = (Get-Content "config\tasks\_active.txt" -Raw).Trim() -split ","

# Tool configuration
$toolConfig = @{
    "claude" = @{
        "name" = "Claude Code"
        "command" = "claude"
        "taskFile" = "config\tasks\claude.txt"
    }
    "gemini" = @{
        "name" = "Gemini CLI"
        "command" = "gemini"
        "taskFile" = "config\tasks\gemini.txt"
    }
    "openai" = @{
        "name" = "OpenAI Codex"
        "command" = "codex"
        "taskFile" = "config\tasks\openai.txt"
    }
}

if (-not $Quiet) {
    Write-Host ""
    Write-Host "  ========================================" -ForegroundColor Cyan
    Write-Host "  CLI Mode - Sequential Execution" -ForegroundColor Cyan
    Write-Host "  ========================================" -ForegroundColor Cyan
    Write-Host "  Workspace: $workspacePath"
    Write-Host ""
}

$totalTools = $activeTools.Count
$currentTool = 0

foreach ($tool in $activeTools) {
    $currentTool++
    $config = $toolConfig[$tool]

    if (-not $config) {
        if (-not $Quiet) {
            Write-Host "  [$currentTool/$totalTools] Unknown tool: $tool" -ForegroundColor Yellow
        }
        continue
    }

    $taskFile = $config.taskFile
    $outputFile = "$workspacePath\$($tool)_output.txt"

    if (-not (Test-Path $taskFile)) {
        if (-not $Quiet) {
            Write-Host "  [$currentTool/$totalTools] No task file for $($config.name)" -ForegroundColor Yellow
        }
        continue
    }

    $task = Get-Content $taskFile -Raw
    $taskFirstLine = $task.Split("`n")[0].Trim()

    if (-not $Quiet) {
        Write-Host "  [$currentTool/$totalTools] Running $($config.name)..." -ForegroundColor White
        Write-Host "      Task: $taskFirstLine" -ForegroundColor Gray
    }

    $startTime = Get-Date

    try {
        $command = $config.command

        if ($Quiet) {
            # Quiet mode: run directly, show only output
            & $command $taskFirstLine 2>&1 | Tee-Object -FilePath $outputFile
        } else {
            # Verbose mode: run in subprocess with full output
            $tempScript = "$workspacePath\_run_$tool.ps1"
            @"
`$task = @'
$taskFirstLine
'@
& $command `$task 2>&1 | Tee-Object -FilePath '$outputFile'
"@ | Set-Content $tempScript -Encoding UTF8

            $process = Start-Process powershell -ArgumentList "-ExecutionPolicy Bypass -File `"$tempScript`"" -PassThru -NoNewWindow -Wait

            $duration = ((Get-Date) - $startTime).TotalSeconds

            if ($process.ExitCode -eq 0) {
                Write-Host "      Done ($([math]::Round($duration, 1))s)" -ForegroundColor Green
            } else {
                Write-Host "      Completed with warnings ($([math]::Round($duration, 1))s)" -ForegroundColor Yellow
            }
            Write-Host "      Output: $outputFile" -ForegroundColor Gray

            Remove-Item $tempScript -ErrorAction SilentlyContinue
        }
    }
    catch {
        Write-Host "      Error: $_" -ForegroundColor Red
        "Error: $_" | Set-Content $outputFile
    }

    if (-not $Quiet) {
        Write-Host ""
    }
}

if (-not $Quiet) {
    Write-Host "  ========================================" -ForegroundColor Cyan
    Write-Host "  Complete - Results in $workspacePath" -ForegroundColor Green
    Write-Host "  ========================================" -ForegroundColor Cyan
    Write-Host ""
}
