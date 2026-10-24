<#
.SYNOPSIS
    Week 8 - Vidar emulation - Step 1: Initial Access / Execution
    ATT&CK: T1566.001 (Phishing Attachment - simulated), T1204.002 (User Execution),
            T1059.001 (PowerShell)

.DESCRIPTION
    THIS SCRIPT IS 100% BENIGN. It does not download, execute, or contain any
    real malware. It only simulates the *behavioral pattern* a Vidar-style
    loader shows at initial access, so our SIEM/Sysmon detections can be
    tested and validated.

    What it actually does:
      1. Simulates an Office document launching PowerShell (we just call
         powershell.exe directly from this script with an -EncodedCommand,
         which is what Sysmon/EDR actually sees and alerts on).
      2. The encoded command only runs 'whoami' and writes a timestamped
         marker file to C:\Temp\emu_marker.txt.

    Run this on an ISOLATED LAB VM ONLY. Never on a production machine.

.NOTES
    Author: <group name>
    Course: Introduction to Threat Hunting - Assignment 5 (Week 8)
#>

param(
    [string]$MarkerPath = "C:\Temp\emu_marker.txt"
)

Write-Host "[*] Week 8 Emulation - Step 1: Initial Access / Execution" -ForegroundColor Cyan

# Ensure the working folder exists
$workDir = Split-Path $MarkerPath
if (-not (Test-Path $workDir)) {
    New-Item -ItemType Directory -Path $workDir -Force | Out-Null
}

# This is the "payload" the fake encoded command will run.
# It is intentionally harmless: only 'whoami' + writing a marker file.
$innerCommand = "whoami | Out-File -FilePath '$MarkerPath' -Append; " +
                "Get-Date | Out-File -FilePath '$MarkerPath' -Append"

$bytes = [System.Text.Encoding]::Unicode.GetBytes($innerCommand)
$encodedCommand = [Convert]::ToBase64String($bytes)

Write-Host "[*] Simulating: Office/Explorer -> powershell.exe -EncodedCommand ..." -ForegroundColor Yellow

# This is the line Sysmon Event ID 1 / PowerShell 4104 should catch.
Start-Process -FilePath "powershell.exe" `
    -ArgumentList "-NoProfile -EncodedCommand $encodedCommand" `
    -WindowStyle Hidden -Wait

Write-Host "[+] Step 1 complete. Marker file written to: $MarkerPath" -ForegroundColor Green
Write-Host "[i] Expected telemetry: Sysmon EID 1 (process create), EID 11 (file create)," -ForegroundColor DarkGray
Write-Host "    PowerShell Script Block Log EID 4104, parent-child Office/Explorer->powershell.exe" -ForegroundColor DarkGray
