<#
.SYNOPSIS
    Week 8 - Vidar emulation - Step 2: Persistence (OPTIONAL / loader-based)
    ATT&CK: T1053.005 (Scheduled Task), T1547.001 (Registry Run Key)

.DESCRIPTION
    Vidar itself is mostly a "smash and grab" stealer that does not usually
    persist. This step is included because loaders/droppers delivered
    alongside Vidar often DO persist, and because the assignment requires a
    full emulation chain. Clearly label this as optional in your report/demo.

    THIS SCRIPT IS BENIGN. The "payload" the scheduled task / run key points
    to is notepad.exe (or a harmless script), never anything malicious.

    Run on an ISOLATED LAB VM ONLY. Use step2_cleanup below (or cleanup.ps1)
    to remove artifacts afterward.
#>

param(
    [string]$TaskName = "EmuVidarPersistTask",
    [string]$RunKeyName = "EmuVidarPersistRun"
)

Write-Host "[*] Week 8 Emulation - Step 2: Persistence (optional, loader-based)" -ForegroundColor Cyan

# --- T1053.005: Scheduled Task persistence ---
Write-Host "[*] Creating benign scheduled task: $TaskName" -ForegroundColor Yellow
schtasks /create /tn $TaskName /tr "notepad.exe" /sc onlogon /f | Out-Null

# --- T1547.001: Registry Run Key persistence ---
$runKeyPath = "HKCU:\Software\Microsoft\Windows\CurrentVersion\Run"
Write-Host "[*] Creating benign Run key: $RunKeyName" -ForegroundColor Yellow
New-ItemProperty -Path $runKeyPath -Name $RunKeyName -Value "notepad.exe" -PropertyType String -Force | Out-Null

Write-Host "[+] Step 2 complete." -ForegroundColor Green
Write-Host "[i] Expected telemetry: Sysmon EID 1 (schtasks.exe), Security 4698 (task created)," -ForegroundColor DarkGray
Write-Host "    Sysmon EID 13 (registry value set) on $runKeyPath\$RunKeyName" -ForegroundColor DarkGray
Write-Host "[!] Remember to clean up: run scripts\cleanup.ps1 after the exercise." -ForegroundColor Red
