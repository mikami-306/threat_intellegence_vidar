<#
.SYNOPSIS
    Week 8 - Vidar emulation - Cleanup
    Removes all artifacts created by step1-step4 scripts so the lab VM
    is restored to a clean state. Run this after you've captured your
    telemetry/screenshots, or just revert the VM snapshot instead.
#>

param(
    [string]$TaskName    = "EmuVidarPersistTask",
    [string]$RunKeyName  = "EmuVidarPersistRun",
    [string]$EmuRoot     = "C:\Temp\EmuVidarProfile",
    [string]$LootZip     = "C:\Temp\emu_loot.zip",
    [string]$MarkerPath  = "C:\Temp\emu_marker.txt"
)

Write-Host "[*] Cleaning up Week 8 emulation artifacts..." -ForegroundColor Cyan

# Remove scheduled task
schtasks /delete /tn $TaskName /f 2>$null | Out-Null

# Remove Run key
$runKeyPath = "HKCU:\Software\Microsoft\Windows\CurrentVersion\Run"
Remove-ItemProperty -Path $runKeyPath -Name $RunKeyName -ErrorAction SilentlyContinue

# Remove files/folders
foreach ($path in @($EmuRoot, $LootZip, $MarkerPath)) {
    if (Test-Path $path) {
        Remove-Item -Path $path -Recurse -Force -ErrorAction SilentlyContinue
    }
}

Write-Host "[+] Cleanup complete. VM restored to pre-emulation state (best effort)." -ForegroundColor Green
Write-Host "[i] For a guaranteed clean state, revert to your VM snapshot." -ForegroundColor DarkGray
