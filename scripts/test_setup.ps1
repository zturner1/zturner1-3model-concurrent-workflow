# test_setup.ps1 - Comprehensive validation of system setup

param(
    [switch]$Verbose,
    [switch]$Fix
)

$ErrorActionPreference = "Continue"
$script:errors = 0
$script:warnings = 0

function Write-Check {
    param($Status, $Message, $Detail = "")
    switch ($Status) {
        "pass" {
            Write-Host "  [+] $Message" -ForegroundColor Green
            if ($Detail -and $Verbose) { Write-Host "      $Detail" -ForegroundColor Gray }
        }
        "fail" {
            Write-Host "  [-] $Message" -ForegroundColor Red
            if ($Detail) { Write-Host "      $Detail" -ForegroundColor Gray }
            $script:errors++
        }
        "warn" {
            Write-Host "  [!] $Message" -ForegroundColor Yellow
            if ($Detail) { Write-Host "      $Detail" -ForegroundColor Gray }
            $script:warnings++
        }
        "info" {
            Write-Host "  [i] $Message" -ForegroundColor Cyan
        }
    }
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host " System Validation" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# ========================================
# 1. Prerequisites
# ========================================
Write-Host "=== Prerequisites ===" -ForegroundColor White

# Node.js
$node = Get-Command node -ErrorAction SilentlyContinue
if ($node) {
    $nodeVersion = (node --version 2>$null)
    Write-Check "pass" "Node.js installed" $nodeVersion
} else {
    Write-Check "fail" "Node.js not found" "Install from https://nodejs.org"
}

# npm
$npm = Get-Command npm -ErrorAction SilentlyContinue
if ($npm) {
    $npmVersion = (npm --version 2>$null)
    Write-Check "pass" "npm installed" "v$npmVersion"
} else {
    Write-Check "fail" "npm not found"
}

# Git
$git = Get-Command git -ErrorAction SilentlyContinue
if ($git) {
    Write-Check "pass" "Git installed"
} else {
    Write-Check "warn" "Git not found" "Recommended for version control"
}

Write-Host ""

# ========================================
# 2. CLI Tools
# ========================================
Write-Host "=== CLI Tools ===" -ForegroundColor White

$tools = @(
    @{ name = "claude"; display = "Claude Code" },
    @{ name = "gemini"; display = "Gemini CLI" },
    @{ name = "codex"; display = "OpenAI Codex" }
)

foreach ($tool in $tools) {
    $cmd = Get-Command $tool.name -ErrorAction SilentlyContinue
    if ($cmd) {
        $version = & $tool.name --version 2>$null
        Write-Check "pass" "$($tool.display) installed" $version
    } else {
        Write-Check "fail" "$($tool.display) not found" "Run install.bat to install"
    }
}

Write-Host ""

# ========================================
# 3. Required Files
# ========================================
Write-Host "=== Required Files ===" -ForegroundColor White

$requiredFiles = @(
    @{ path = "run.bat"; desc = "Main router script" },
    @{ path = "config\role_config.json"; desc = "Routing configuration" },
    @{ path = "scripts\route_tasks.ps1"; desc = "Task routing logic" },
    @{ path = "scripts\run_cli.ps1"; desc = "CLI mode executor" },
    @{ path = "scripts\tools\launch_claude.bat"; desc = "Claude launcher" },
    @{ path = "scripts\tools\launch_gemini.bat"; desc = "Gemini launcher" },
    @{ path = "scripts\tools\launch_openai.bat"; desc = "OpenAI launcher" }
)

foreach ($file in $requiredFiles) {
    if (Test-Path $file.path) {
        Write-Check "pass" $file.path
    } else {
        Write-Check "fail" "$($file.path) missing" $file.desc
    }
}

Write-Host ""

# ========================================
# 4. Context Files
# ========================================
Write-Host "=== Context Files ===" -ForegroundColor White

$contextFiles = @("CLAUDE.md", "GEMINI.md", "OPENAI.md", "shared-context.md")

foreach ($file in $contextFiles) {
    if (Test-Path $file) {
        $size = (Get-Item $file).Length
        Write-Check "pass" $file "$size bytes"
    } else {
        Write-Check "warn" "$file missing" "Optional but recommended"
    }
}

Write-Host ""

# ========================================
# 5. Configuration Validation
# ========================================
Write-Host "=== Configuration ===" -ForegroundColor White

# Check role_config.json
if (Test-Path "config\role_config.json") {
    try {
        $config = Get-Content "config\role_config.json" -Raw | ConvertFrom-Json
        Write-Check "pass" "role_config.json valid JSON"

        # Validate structure
        if ($config.roles) {
            $roleCount = ($config.roles.PSObject.Properties | Measure-Object).Count
            Write-Check "pass" "Roles defined" "$roleCount roles"
        } else {
            Write-Check "fail" "No 'roles' section in config"
        }

        if ($config.auth_status) {
            $authCount = ($config.auth_status.PSObject.Properties | Where-Object { $_.Value -eq $true } | Measure-Object).Count
            Write-Check "pass" "Auth status defined" "$authCount tools authenticated"
        } else {
            Write-Check "warn" "No 'auth_status' section in config"
        }
    } catch {
        Write-Check "fail" "Invalid JSON in role_config.json" $_.Exception.Message
    }
} else {
    Write-Check "fail" "role_config.json not found"
}

# Check .env
if (Test-Path ".env") {
    Write-Check "pass" ".env file exists"

    $envContent = Get-Content ".env" -ErrorAction SilentlyContinue
    $hasOpenAI = $envContent | Where-Object { $_ -match "^OPENAI_API_KEY=" -and $_ -notmatch "your.*key" }
    if ($hasOpenAI) {
        Write-Check "pass" "OPENAI_API_KEY configured in .env"
    } else {
        Write-Check "warn" "OPENAI_API_KEY not set in .env" "Required for OpenAI CLI"
    }
} else {
    if (Test-Path ".env.example") {
        Write-Check "warn" ".env not found" "Copy .env.example to .env and configure"
    } else {
        Write-Check "warn" ".env not found"
    }
}

Write-Host ""

# ========================================
# 6. Directory Structure
# ========================================
Write-Host "=== Directories ===" -ForegroundColor White

$directories = @(
    @{ path = "logs"; required = $true },
    @{ path = "config"; required = $true },
    @{ path = "scripts"; required = $true },
    @{ path = "scripts\tools"; required = $true },
    @{ path = "research"; required = $false },
    @{ path = "drafts"; required = $false },
    @{ path = "output"; required = $false },
    @{ path = "workspace"; required = $false }
)

foreach ($dir in $directories) {
    if (Test-Path $dir.path) {
        Write-Check "pass" $dir.path
    } elseif ($dir.required) {
        Write-Check "fail" "$($dir.path) missing"
        if ($Fix) {
            New-Item -ItemType Directory -Path $dir.path -Force | Out-Null
            Write-Host "      Created $($dir.path)" -ForegroundColor Gray
        }
    } else {
        Write-Check "info" "$($dir.path) not created yet (optional)"
    }
}

Write-Host ""

# ========================================
# 7. Test Routing (if verbose)
# ========================================
if ($Verbose) {
    Write-Host "=== Routing Test ===" -ForegroundColor White

    $testInput = "Research trends. Build summary. Review draft."
    Write-Host "  Test input: $testInput" -ForegroundColor Gray

    if (-not (Test-Path "config\tasks")) {
        New-Item -ItemType Directory -Path "config\tasks" -Force | Out-Null
    }

    $testInput | Set-Content "config\tasks\_input.txt" -Encoding UTF8

    try {
        & .\scripts\route_tasks.ps1 2>$null

        if (Test-Path "config\tasks\_active.txt") {
            $active = Get-Content "config\tasks\_active.txt" -Raw
            Write-Check "pass" "Routing successful" "Active: $active"
        } else {
            Write-Check "fail" "Routing produced no output"
        }
    } catch {
        Write-Check "fail" "Routing error" $_.Exception.Message
    }

    Write-Host ""
}

# ========================================
# Summary
# ========================================
Write-Host "========================================" -ForegroundColor Cyan
if ($script:errors -eq 0 -and $script:warnings -eq 0) {
    Write-Host " All checks passed!" -ForegroundColor Green
} elseif ($script:errors -eq 0) {
    Write-Host " Passed with $($script:warnings) warning(s)" -ForegroundColor Yellow
} else {
    Write-Host " $($script:errors) error(s), $($script:warnings) warning(s)" -ForegroundColor Red
}
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

if ($script:errors -gt 0) {
    Write-Host "Run 'install.bat' to fix missing components." -ForegroundColor Gray
    Write-Host ""
}

exit $script:errors
