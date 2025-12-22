# arrange_windows.ps1 - Arrange tool windows side by side

Add-Type @"
using System;
using System.Runtime.InteropServices;

public class WindowHelper {
    [DllImport("user32.dll")]
    public static extern bool MoveWindow(IntPtr hWnd, int X, int Y, int nWidth, int nHeight, bool bRepaint);

    [DllImport("user32.dll")]
    public static extern bool SetForegroundWindow(IntPtr hWnd);

    [DllImport("user32.dll")]
    public static extern bool ShowWindow(IntPtr hWnd, int nCmdShow);
}
"@

# Get screen dimensions
Add-Type -AssemblyName System.Windows.Forms
$screen = [System.Windows.Forms.Screen]::PrimaryScreen.WorkingArea
$screenWidth = $screen.Width
$screenHeight = $screen.Height

# Wait a moment for windows to open
Start-Sleep -Milliseconds 1500

# Find windows by title
$processes = Get-Process | Where-Object { $_.MainWindowTitle -ne "" }

$claudeProc = $processes | Where-Object { $_.MainWindowTitle -like "*Claude*" } | Select-Object -First 1
$geminiProc = $processes | Where-Object { $_.MainWindowTitle -like "*Gemini*" } | Select-Object -First 1
$openaiProc = $processes | Where-Object { $_.MainWindowTitle -like "*OpenAI*" -or $_.MainWindowTitle -like "*Codex*" } | Select-Object -First 1

# Count active windows
$windows = @($claudeProc, $geminiProc, $openaiProc) | Where-Object { $_ -ne $null }
$count = $windows.Count

if ($count -eq 0) {
    Write-Host "No tool windows found to arrange."
    exit 0
}

# Calculate positions based on number of windows
if ($count -eq 1) {
    # Single window - center and make large
    $width = [int]($screenWidth * 0.8)
    $height = [int]($screenHeight * 0.8)
    $x = [int](($screenWidth - $width) / 2)
    $y = [int](($screenHeight - $height) / 2)

    $hwnd = $windows[0].MainWindowHandle
    [WindowHelper]::ShowWindow($hwnd, 9) | Out-Null  # SW_RESTORE
    [WindowHelper]::MoveWindow($hwnd, $x, $y, $width, $height, $true) | Out-Null
}
elseif ($count -eq 2) {
    # Two windows - side by side
    $width = [int]($screenWidth / 2)
    $height = $screenHeight

    $i = 0
    foreach ($proc in $windows) {
        $hwnd = $proc.MainWindowHandle
        $x = $i * $width
        [WindowHelper]::ShowWindow($hwnd, 9) | Out-Null
        [WindowHelper]::MoveWindow($hwnd, $x, 0, $width, $height, $true) | Out-Null
        $i++
    }
}
else {
    # Three windows - side by side
    $width = [int]($screenWidth / 3)
    $height = $screenHeight

    # Order: Claude (left), Gemini (center), OpenAI (right)
    $ordered = @()
    if ($claudeProc) { $ordered += $claudeProc }
    if ($geminiProc) { $ordered += $geminiProc }
    if ($openaiProc) { $ordered += $openaiProc }

    $i = 0
    foreach ($proc in $ordered) {
        $hwnd = $proc.MainWindowHandle
        $x = $i * $width
        [WindowHelper]::ShowWindow($hwnd, 9) | Out-Null
        [WindowHelper]::MoveWindow($hwnd, $x, 0, $width, $height, $true) | Out-Null
        [WindowHelper]::SetForegroundWindow($hwnd) | Out-Null
        $i++
    }
}

Write-Host "    Windows arranged: $count tool(s)"
