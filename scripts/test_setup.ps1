# test_setup.ps1 - Test all components

Write-Host "=== Testing .env loading ===" -ForegroundColor Cyan
if (Test-Path '.env') {
    $envContent = Get-Content '.env'
    foreach ($line in $envContent) {
        if ($line -and -not $line.StartsWith('#')) {
            Write-Host "  Found: $line"
        }
    }
} else {
    Write-Host "  [-] .env file not found" -ForegroundColor Red
}

Write-Host ""
Write-Host "=== Testing tool availability ===" -ForegroundColor Cyan
$tools = @('claude', 'gemini', 'codex')
foreach ($tool in $tools) {
    $cmd = Get-Command $tool -ErrorAction SilentlyContinue
    if ($cmd) {
        Write-Host "  [+] $tool found" -ForegroundColor Green
    } else {
        Write-Host "  [-] $tool not found" -ForegroundColor Red
    }
}

Write-Host ""
Write-Host "=== Testing config loading ===" -ForegroundColor Cyan
try {
    $config = Get-Content 'config/role_config.json' | ConvertFrom-Json
    Write-Host "  [+] Config loaded successfully" -ForegroundColor Green
    Write-Host "  Roles: $($config.roles.PSObject.Properties.Name -join ', ')"

    foreach ($roleName in $config.roles.PSObject.Properties.Name) {
        $role = $config.roles.$roleName
        Write-Host "    - $roleName : keywords=[$($role.keywords -join ', ')] primary=$($role.primary)"
    }
} catch {
    Write-Host "  [-] Error: $_" -ForegroundColor Red
}

Write-Host ""
Write-Host "=== Testing routing ===" -ForegroundColor Cyan
$testInput = "Research dog types. Build a database. Analyze for accuracy."
Write-Host "  Input: $testInput"
$testInput | Set-Content 'config/tasks/_input.txt'

& .\scripts\route_tasks.ps1

Write-Host ""
Write-Host "=== Checking output files ===" -ForegroundColor Cyan
if (Test-Path 'config/tasks/_active.txt') {
    Write-Host "  Active tools: $(Get-Content 'config/tasks/_active.txt')"
}
foreach ($tool in @('claude', 'gemini', 'openai')) {
    $file = "config/tasks/$tool.txt"
    if (Test-Path $file) {
        Write-Host "  $tool.txt: $(Get-Content $file)"
    }
}

Write-Host ""
Write-Host "=== All tests complete ===" -ForegroundColor Green
