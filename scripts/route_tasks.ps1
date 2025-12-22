# route_tasks.ps1 - Parse input and route to appropriate tools

$ErrorActionPreference = "Stop"

# Read input from temp file
$inputFile = "config\tasks\_input.txt"
if (-not (Test-Path $inputFile)) {
    Write-Host "    Error: No input file found"
    exit 1
}

$input = Get-Content $inputFile -Raw
$input = $input.Trim()

# Load config
$configFile = "config\role_config.json"
if (-not (Test-Path $configFile)) {
    Write-Host "    Error: Config file not found"
    exit 1
}

$config = Get-Content $configFile | ConvertFrom-Json

# Split into sentences
$sentences = $input -split '[.!?]' | Where-Object { $_.Trim() -ne '' } | ForEach-Object { $_.Trim() }

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

        $taskFile = "config\tasks\$tool.txt"
        [System.IO.File]::WriteAllText($taskFile, $fullTask, $utf8NoBom)

        Write-Host "    $tool -> $($tasks[$tool] -join '; ')"
        $activeTools += $tool
    }
}

# Write session manifest
$manifestPath = "$workspaceDir\_session.json"
$sessionInfo | ConvertTo-Json -Depth 3 | Set-Content $manifestPath -Encoding UTF8

# Write active tools list
if ($activeTools.Count -gt 0) {
    $content = $activeTools -join ','
    [System.IO.File]::WriteAllText('config\tasks\_active.txt', $content, $utf8NoBom)

    # Also save workspace path for run.bat
    [System.IO.File]::WriteAllText('config\tasks\_workspace.txt', $workspaceDir, $utf8NoBom)
} else {
    Write-Host "    No tasks to route"
}

exit 0
