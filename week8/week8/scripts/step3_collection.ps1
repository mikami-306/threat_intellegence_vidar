<#
.SYNOPSIS
    Week 8 - Vidar emulation - Step 3: Collection
    ATT&CK: T1555.003 (Credentials from Web Browsers), T1539 (Steal Web Session Cookie),
            T1005 (Data from Local System), T1560.001 (Archive via Utility)

.DESCRIPTION
    THIS SCRIPT NEVER TOUCHES A REAL BROWSER PROFILE OR REAL CREDENTIALS.
    It builds a FAKE "browser profile" folder with canary files that only
    contain placeholder text, then a FAKE "wallet" folder the same way, and
    finally zips them up the way a stealer would package loot before
    exfiltration.

    Run on an ISOLATED LAB VM ONLY, using a dedicated emulation folder.
#>

param(
    [string]$EmuRoot    = "C:\Temp\EmuVidarProfile",
    [string]$LootZip    = "C:\Temp\emu_loot.zip"
)

Write-Host "[*] Week 8 Emulation - Step 3: Collection" -ForegroundColor Cyan

# Build fake browser-profile-like paths (canary data only)
$browserPath = Join-Path $EmuRoot "AppData\Local\FakeBrowser\User Data\Default"
$walletPath  = Join-Path $EmuRoot "Documents\FakeWallet"

New-Item -ItemType Directory -Path $browserPath -Force | Out-Null
New-Item -ItemType Directory -Path $walletPath -Force | Out-Null

# Canary "Login Data" / "Cookies" style files - clearly fake content
"CANARY-LOGIN-DATA :: user=test@example.com pass=NOT_A_REAL_PASSWORD" |
    Out-File -FilePath (Join-Path $browserPath "Login Data") -Encoding ascii
"CANARY-COOKIES :: session=NOT_A_REAL_COOKIE_VALUE" |
    Out-File -FilePath (Join-Path $browserPath "Cookies") -Encoding ascii
"CANARY-WALLET :: seed=NOT_A_REAL_SEED_PHRASE" |
    Out-File -FilePath (Join-Path $walletPath "wallet.dat") -Encoding ascii

Write-Host "[*] Canary browser/wallet files created under $EmuRoot" -ForegroundColor Yellow

# --- T1005: collect, T1560.001: archive via utility ---
if (Test-Path $LootZip) { Remove-Item $LootZip -Force }
Compress-Archive -Path $EmuRoot\* -DestinationPath $LootZip -Force

Write-Host "[+] Step 3 complete. Loot archive created at: $LootZip" -ForegroundColor Green
Write-Host "[i] Expected telemetry: Sysmon EID 11 (file create) under browser-profile-like paths," -ForegroundColor DarkGray
Write-Host "    PowerShell 4104 for Compress-Archive, EID 11 for the .zip file creation" -ForegroundColor DarkGray
