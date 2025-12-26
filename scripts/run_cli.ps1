# run_cli.ps1 - Run tools sequentially in CLI mode

param(
    [switch]$Quiet,
    [int]$TimeoutMinutes = 10
)

$ErrorActionPreference = "Stop"

# Logging function
$logFile = "logs\run.log"
function Write-Log {
    param([string]$Message)
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    "[$timestamp] $Message" | Add-Content -Path $logFile -ErrorAction SilentlyContinue
}

# Progress indicator
function Show-Progress {
    param([string]$Activity, [int]$PercentComplete)
    if (-not $Quiet) {
        Write-Progress -Activity $Activity -PercentComplete $PercentComplete
    }
}

# Load .env if exists
try {
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
} catch {
    Write-Log "WARN: Failed to load .env file: $_"
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
$results = @()

foreach ($tool in $activeTools) {
    $currentTool++
    $config = $toolConfig[$tool]
    $percentComplete = [int](($currentTool - 1) / $totalTools * 100)
    Show-Progress -Activity "Running AI tools" -PercentComplete $percentComplete

    if (-not $config) {
        if (-not $Quiet) {
            Write-Host "  [$currentTool/$totalTools] Unknown tool: $tool" -ForegroundColor Yellow
        }
        $results += @{ tool = $tool; status = "skipped"; reason = "unknown" }
        continue
    }

    $taskFile = $config.taskFile
    $outputFile = "$workspacePath\$($tool)_output.txt"

    if (-not (Test-Path $taskFile)) {
        if (-not $Quiet) {
            Write-Host "  [$currentTool/$totalTools] No task file for $($config.name)" -ForegroundColor Yellow
        }
        $results += @{ tool = $tool; status = "skipped"; reason = "no task file" }
        continue
    }

    $task = Get-Content $taskFile -Raw
    $taskFirstLine = $task.Split("`n")[0].Trim()

    if (-not $Quiet) {
        Write-Host "  [$currentTool/$totalTools] Running $($config.name)..." -ForegroundColor White
        Write-Host "      Task: $taskFirstLine" -ForegroundColor Gray
        Write-Host "      Timeout: $TimeoutMinutes minutes" -ForegroundColor DarkGray
    }

    $startTime = Get-Date

    try {
        $command = $config.command

        if ($Quiet) {
            # Quiet mode: run directly, show only output
            if ($tool -eq "gemini") {
                # Gemini needs to run in background job to fully isolate stdin
                $job = Start-Job -ScriptBlock { 
                    param($t) 
                    gemini -y $t 2>&1 
                } -ArgumentList $taskFirstLine
                $output = $job | Wait-Job -Timeout ($TimeoutMinutes * 60) | Receive-Job 2>&1
                $job | Remove-Job -Force -ErrorAction SilentlyContinue
                $output | Tee-Object -FilePath $outputFile
            } elseif ($tool -eq "openai") {
                # Codex needs 'exec' subcommand for non-interactive mode
                # Use workspace path so created files go to session folder
                $job = Start-Job -ScriptBlock { 
                    param($t, $ws) 
                    Set-Location $ws
                    codex exec --full-auto --skip-git-repo-check $t 2>&1 
                } -ArgumentList $taskFirstLine, (Resolve-Path $workspacePath).Path
                $output = $job | Wait-Job -Timeout ($TimeoutMinutes * 60) | Receive-Job 2>&1
                $job | Remove-Job -Force -ErrorAction SilentlyContinue
                $output | Tee-Object -FilePath $outputFile
            } elseif ($tool -eq "claude") {
                # Claude needs --print mode for non-interactive output with --dangerously-skip-permissions
                # Use workspace path so created files go to session folder
                $job = Start-Job -ScriptBlock { 
                    param($t, $ws) 
                    Set-Location $ws
                    claude --print --dangerously-skip-permissions $t 2>&1 
                } -ArgumentList $taskFirstLine, (Resolve-Path $workspacePath).Path
                $output = $job | Wait-Job -Timeout ($TimeoutMinutes * 60) | Receive-Job 2>&1
                $job | Remove-Job -Force -ErrorAction SilentlyContinue
                $output | Tee-Object -FilePath $outputFile
            } else {
                & $command $taskFirstLine 2>&1 | Tee-Object -FilePath $outputFile
            }
            $results += @{ tool = $tool; status = "completed" }
        } else {
            # Verbose mode: run in subprocess with timeout
            $tempScript = "$workspacePath\_run_$tool.ps1"
            
            if ($tool -eq "gemini") {
                # Gemini needs Start-Job to fully isolate stdin and prevent keypress abort
                @"
`$job = Start-Job -ScriptBlock { 
    param(`$t) 
    gemini -y `$t 2>&1 
} -ArgumentList '$taskFirstLine'
`$output = `$job | Wait-Job -Timeout (10 * 60) | Receive-Job 2>&1
`$job | Remove-Job -Force -ErrorAction SilentlyContinue
`$output | Tee-Object -FilePath '$outputFile'
"@ | Set-Content $tempScript -Encoding UTF8
            } elseif ($tool -eq "openai") {
                # Codex needs 'exec' subcommand for non-interactive mode with --full-auto
                # Use workspace path so created files go to session folder
                $wsFullPath = (Resolve-Path $workspacePath).Path
                @"
`$job = Start-Job -ScriptBlock { 
    param(`$t, `$ws) 
    Set-Location `$ws
    codex exec --full-auto --skip-git-repo-check `$t 2>&1 
} -ArgumentList '$taskFirstLine', '$wsFullPath'
`$output = `$job | Wait-Job -Timeout (10 * 60) | Receive-Job 2>&1
`$job | Remove-Job -Force -ErrorAction SilentlyContinue
`$output | Tee-Object -FilePath '$outputFile'
"@ | Set-Content $tempScript -Encoding UTF8
            } elseif ($tool -eq "claude") {
                # Claude needs --print mode for non-interactive output
                # Use workspace path so created files go to session folder
                $wsFullPath = (Resolve-Path $workspacePath).Path
                @"
`$job = Start-Job -ScriptBlock { 
    param(`$t, `$ws) 
    Set-Location `$ws
    claude --print --dangerously-skip-permissions `$t 2>&1 
} -ArgumentList '$taskFirstLine', '$wsFullPath'
`$output = `$job | Wait-Job -Timeout (10 * 60) | Receive-Job 2>&1
`$job | Remove-Job -Force -ErrorAction SilentlyContinue
`$output | Tee-Object -FilePath '$outputFile'
"@ | Set-Content $tempScript -Encoding UTF8
            } else {
                @"
`$task = @'
$taskFirstLine
'@
& $command `$task 2>&1 | Tee-Object -FilePath '$outputFile'
"@ | Set-Content $tempScript -Encoding UTF8
            }

            $process = Start-Process powershell -ArgumentList "-ExecutionPolicy Bypass -File `"$tempScript`"" -PassThru -NoNewWindow
            
            # Wait with timeout
            $timeoutSeconds = $TimeoutMinutes * 60
            $process | Wait-Process -Timeout $timeoutSeconds -ErrorAction SilentlyContinue
            
            $duration = ((Get-Date) - $startTime).TotalSeconds

            if (-not $process.HasExited) {
                # Process timed out
                $process | Stop-Process -Force -ErrorAction SilentlyContinue
                Write-Host "      TIMEOUT after $TimeoutMinutes minutes" -ForegroundColor Red
                Write-Log "TIMEOUT: $tool exceeded $TimeoutMinutes minutes"
                "TIMEOUT: Process exceeded $TimeoutMinutes minutes" | Add-Content $outputFile
                $results += @{ tool = $tool; status = "timeout"; duration = $duration }
            } elseif ($process.ExitCode -eq 0) {
                Write-Host "      Done ($([math]::Round($duration, 1))s)" -ForegroundColor Green
                Write-Log "EXEC: $tool completed in $([math]::Round($duration, 1))s"
                $results += @{ tool = $tool; status = "completed"; duration = $duration }
            } else {
                Write-Host "      Completed with warnings ($([math]::Round($duration, 1))s)" -ForegroundColor Yellow
                Write-Log "WARN: $tool completed with warnings in $([math]::Round($duration, 1))s"
                $results += @{ tool = $tool; status = "warning"; duration = $duration }
            }
            Write-Host "      Output: $outputFile" -ForegroundColor Gray

            Remove-Item $tempScript -ErrorAction SilentlyContinue
        }
    }
    catch {
        Write-Host "      Error: $_" -ForegroundColor Red
        Write-Log "ERROR: $tool failed - $_"
        "Error: $_" | Set-Content $outputFile
        $results += @{ tool = $tool; status = "error"; error = $_.ToString() }
    }

    if (-not $Quiet) {
        Write-Host ""
    }
}

Show-Progress -Activity "Running AI tools" -PercentComplete 100
Write-Progress -Activity "Running AI tools" -Completed

Write-Log "COMPLETE: Sequential execution finished"

# Show summary
if (-not $Quiet) {
    Write-Host "  ========================================" -ForegroundColor Cyan
    Write-Host "  Execution Summary" -ForegroundColor Cyan
    Write-Host "  ========================================" -ForegroundColor Cyan
    foreach ($r in $results) {
        $statusColor = switch ($r.status) {
            "completed" { "Green" }
            "warning" { "Yellow" }
            "timeout" { "Red" }
            "error" { "Red" }
            default { "Gray" }
        }
        $durationStr = if ($r.duration) { " ($([math]::Round($r.duration, 1))s)" } else { "" }
        Write-Host "    $($r.tool): $($r.status)$durationStr" -ForegroundColor $statusColor
    }
    Write-Host ""
    Write-Host "  Results in: $workspacePath" -ForegroundColor Green
    Write-Host "  ========================================" -ForegroundColor Cyan
    Write-Host ""
}
