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

# Write task files and show routing
$activeTools = @()

foreach ($tool in $tasks.Keys) {
    if ($tasks[$tool].Count -gt 0) {
        $taskFile = "config\tasks\$tool.txt"
        $tasks[$tool] -join "`n" | Set-Content $taskFile -Encoding UTF8
        Write-Host "    $tool -> $($tasks[$tool] -join '; ')"
        $activeTools += $tool
    }
}

# Write active tools list
if ($activeTools.Count -gt 0) {
    $activeTools -join ',' | Set-Content 'config\tasks\_active.txt' -Encoding UTF8
} else {
    Write-Host "    No tasks to route"
}

exit 0
