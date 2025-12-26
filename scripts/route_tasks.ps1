# route_tasks.ps1 - Parse input and route to appropriate tools

$ErrorActionPreference = "Stop"

# Logging function
$logFile = "logs\run.log"
function Write-Log {
    param([string]$Message)
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    "[$timestamp] $Message" | Add-Content -Path $logFile -ErrorAction SilentlyContinue
}

try {
    # Read input from temp file
    $inputFile = "config\tasks\_input.txt"
    if (-not (Test-Path $inputFile)) {
        Write-Host "    Error: No input file found" -ForegroundColor Red
        Write-Log "ERROR: Input file not found"
        exit 1
    }

    $input = Get-Content $inputFile -Raw
    if (-not $input -or $input.Trim() -eq '') {
        Write-Host "    Error: Empty input" -ForegroundColor Red
        Write-Log "ERROR: Empty input provided"
        exit 1
    }
    $input = $input.Trim()

    # Load config
    $configFile = "config\role_config.json"
    if (-not (Test-Path $configFile)) {
        Write-Host "    Error: Config file not found" -ForegroundColor Red
        Write-Log "ERROR: Config file not found"
        exit 1
    }

    try {
        $config = Get-Content $configFile -Raw | ConvertFrom-Json
    } catch {
        Write-Host "    Error: Invalid config JSON - $_" -ForegroundColor Red
        Write-Log "ERROR: Invalid config JSON - $_"
        exit 1
    }

    # Split into sentences
    $sentences = $input -split '[.!?]' | Where-Object { $_.Trim() -ne '' } | ForEach-Object { $_.Trim() }

    if ($sentences.Count -eq 0) {
        Write-Host "    Error: No valid sentences found" -ForegroundColor Red
        Write-Log "ERROR: No valid sentences found in input"
        exit 1
    }

    # Initialize task buckets
    $tasks = @{
        'claude' = @()
        'gemini' = @()
        'openai' = @()
    }

    # Route each sentence
    foreach ($sentence in $sentences) {
        $words = $sentence -split '\s+'
        if ($words.Count -eq 0) { continue }

        $firstWord = $words[0].ToLower()
        $matchedTool = $null

        # Check each role for keyword match
    foreach ($roleName in $config.roles.PSObject.Properties.Name) {
        $role = $config.roles.$roleName
        if ($role.keywords -contains $firstWord) {
            $primary = $role.primary
            if ($config.auth_status.$primary) {
                $matchedTool = $primary
            } else {
                foreach ($fb in $role.fallback) {
                    if ($config.auth_status.$fb) {
                        $matchedTool = $fb
                        break
                    }
                }
            }
            break
        }
    }

    # Default to claude if no match
    if (-not $matchedTool) {
        if ($config.auth_status.claude) { $matchedTool = 'claude' }
        elseif ($config.auth_status.openai) { $matchedTool = 'openai' }
        elseif ($config.auth_status.gemini) { $matchedTool = 'gemini' }
    }

    if ($matchedTool) {
        $tasks[$matchedTool] += $sentence
    }
}

# Create session workspace
$sessionId = Get-Date -Format "yyyy-MM-dd_HH-mm-ss"
$workspaceDir = "workspace\$sessionId"
if (-not (Test-Path $workspaceDir)) {
    New-Item -ItemType Directory -Path $workspaceDir -Force | Out-Null
}

# Write session info
$sessionInfo = @{
    id = $sessionId
    started = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    original_input = $input
    tasks = @{}
}

# Use UTF8 without BOM
$utf8NoBom = New-Object System.Text.UTF8Encoding $false

    # Write task files with collaboration context
    $activeTools = @()

    foreach ($tool in $tasks.Keys) {
        if ($tasks[$tool].Count -gt 0) {
            $taskContent = $tasks[$tool] -join "`n"
            $sessionInfo.tasks[$tool] = $taskContent

            # Build collaboration prompt
            $otherTools = @()
            foreach ($otherTool in $tasks.Keys) {
                if ($otherTool -ne $tool -and $tasks[$otherTool].Count -gt 0) {
                    $otherTools += "$otherTool is working on: $($tasks[$otherTool] -join '; ')"
                }
            }

            $collabContext = ""
            if ($otherTools.Count -gt 0) {
                $collabContext = @"

---
COLLABORATION CONTEXT:
You are part of a 3-agent team working simultaneously.
$($otherTools -join "`n")

SHARED WORKSPACE: $workspaceDir
- Write your outputs to this folder
- Check this folder for outputs from other agents
- Coordinate by reading/writing to shared files
---

"@
            }

            $fullTask = $taskContent + $collabContext

            try {
                $taskFile = "config\tasks\$tool.txt"
                [System.IO.File]::WriteAllText($taskFile, $fullTask, $utf8NoBom)
            } catch {
                Write-Host "    Error: Failed to write task file for $tool - $_" -ForegroundColor Red
                Write-Log "ERROR: Failed to write task file for $tool - $_"
            }

            Write-Host "    $tool -> $($tasks[$tool] -join '; ')"
            Write-Log "ROUTE: $tool <- $($tasks[$tool] -join '; ')"
            $activeTools += $tool
        }
    }

    # Write session manifest
    try {
        $manifestPath = "$workspaceDir\_session.json"
        $sessionInfo | ConvertTo-Json -Depth 3 | Set-Content $manifestPath -Encoding UTF8
        Write-Log "SESSION: Created $workspaceDir"
    } catch {
        Write-Host "    Warning: Failed to write session manifest - $_" -ForegroundColor Yellow
        Write-Log "WARN: Failed to write session manifest - $_"
    }

    # Write active tools list
    if ($activeTools.Count -gt 0) {
        try {
            $content = $activeTools -join ','
            [System.IO.File]::WriteAllText('config\tasks\_active.txt', $content, $utf8NoBom)

            # Also save workspace path for run.bat
            [System.IO.File]::WriteAllText('config\tasks\_workspace.txt', $workspaceDir, $utf8NoBom)
            Write-Log "ACTIVE: $content"
        } catch {
            Write-Host "    Error: Failed to write active tools file - $_" -ForegroundColor Red
            Write-Log "ERROR: Failed to write active tools file - $_"
            exit 1
        }
    } else {
        Write-Host "    No tasks to route"
        Write-Log "WARN: No tasks to route"
    }

    exit 0

} catch {
    Write-Host "    Fatal error: $_" -ForegroundColor Red
    Write-Log "ERROR: Fatal - $_"
    exit 1
}
