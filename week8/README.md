# Week 8 – Creating a Plan to Emulate an Attacker's Action

---

## 1. Overview

Week 7 implemented a single MITRE CAR analytic (`CAR-2013-07-001`) that detects hidden/encoded PowerShell execution on `WS-04`, mapped to T1059.001 and T1027 and tied to Vidar Stealer's command-line evasion behavior.

Week 8 extends that single detection into a **full adversary emulation plan**: a chain of four stages — Initial Access → Execution → Persistence (optional) → Collection → Exfiltration — built around the actual Vidar infection chain, so the Week 7 analytic can be tested as part of a realistic attack path instead of in isolation. All stages are emulated on `WS-04` with benign scripts (no live Vidar sample), and each stage is mapped to an ATT&CK technique and a detection query in the same ELK/Sysmon format used last week.

## 2. Emulation plan: stage → technique → detection

| # | Stage | ATT&CK Technique | What is emulated on WS-04 | Detection query (ELK/Sysmon) |
|---|---|---|---|---|
| 1 | Initial Access / Execution | T1566.001 Phishing Attachment, T1204.002 User Execution, **T1059.001** PowerShell | A test file launches `powershell.exe` with `-enc`, exactly the pattern Week 7's CAR analytic was built to catch | Re-use `CAR-2013-07-001` query from Week 7 |
| 2 | Defense Evasion | **T1027** Obfuscated Files or Information | The encoded command from Stage 1 decodes to a benign payload (writes a marker file) | Same `CAR-2013-07-001` query (`-enc` clause) + decode check in Sysmon EID 1 |
| 3 | Persistence (optional, loader-based) | T1053.005 Scheduled Task, T1547.001 Run Key | Benign scheduled task / Run key pointing to `notepad.exe`, representing a loader dropped alongside Vidar | New query below (3a) |
| 4 | Collection | T1555.003 Credentials from Web Browsers, T1539 Steal Web Session Cookie, T1005 Data from Local System | Canary "Login Data" / "Cookies" / "wallet.dat" files created and zipped on WS-04 (no real browser data touched) | New query below (3b) |
| 5 | C2 / Exfiltration | T1102.001 Dead Drop Resolver, T1041 Exfiltration Over C2 Channel, T1070.004 File Deletion | `powershell.exe` fetches a C2 address from a lab-only "dead drop" text file, POSTs the zip to a local test server, then deletes local artifacts | New query below (3c) |

## 3. New detection logic for Week 8 (ELK/Sysmon, same format as Week 7)

### 3a. Persistence — scheduled task / Run key on WS-04

```
// ELK KQL - persistence stage, loader-based, mapped to T1053.005 / T1547.001
event.code: "1"
  and (process.name: "schtasks.exe" and process.command_line: "*/create*")
  and host.name: "WS-04"

// Run key variant (Sysmon EID 13 - registry value set)
event.code: "13"
  and registry.path: "*CurrentVersion\\Run*"
  and host.name: "WS-04"
```

### 3b. Collection — non-browser process touching credential-store-style paths

```
// ELK KQL - collection stage, mapped to T1555.003 / T1539 / T1005
event.code: "11"
  and file.path: ("*\\User Data\\Default\\Login Data*" or "*\\User Data\\Default\\Cookies*")
  and not process.name: ("chrome.exe" or "msedge.exe" or "firefox.exe")
  and host.name: "WS-04"

// Archive step (Sysmon EID 1) - packaging loot before exfil
event.code: "1"
  and process.name: "powershell.exe"
  and process.command_line: "*Compress-Archive*"
  and host.name: "WS-04"
```

### 3c. Exfiltration — dead-drop lookup and outbound POST

```
// ELK KQL - exfiltration stage, mapped to T1102.001 / T1041
event.code: "3"
  and process.name: "powershell.exe"
  and destination.port: 80
  and host.name: "WS-04"

// Companion check - file deletion right after the network event (T1070.004)
event.code: "23" or event.code: "26"
  and host.name: "WS-04"
```

This gives WS-04 a single correlated kill chain instead of one isolated rule: Stage-1/2 fire first (`CAR-2013-07-001`), optionally Stage-3, then Stage-4, then Stage-5 within a short time window. Correlating all four alerts on the same host/process lineage is a much stronger signal than any one rule alone — this is the main takeaway for the defense.

## 4. Emulation scripts (committed under `week8/scripts/`)

All stages above are implemented as benign PowerShell scripts, run only on the isolated `WS-04` VM:

- `scripts/step1_initial_access.ps1` – encoded PowerShell execution (feeds CAR-2013-07-001)
- `scripts/step2_persistence.ps1` – scheduled task + Run key (optional/loader-based)
- `scripts/step3_collection.ps1` – canary browser/wallet files + zip
- `scripts/step4_exfiltration.ps1` – dead-drop lookup + POST to lab server + cleanup
- `scripts/cleanup.ps1` – reverts all artifacts
- `server/exfil_server.py` – local Python server simulating the dead drop + upload endpoint
- `detections/sigma_encoded_powershell.yml` – Sigma versions of the Week 7 + Week 8 queries above

None of these scripts contact the real internet or touch real credentials; `server/exfil_server.py` only listens on the isolated lab network.

## 5. Results table (fill in after running on WS-04)

| Stage | Technique | Executed on WS-04? | Sysmon event seen? | ELK query fired? | Notes / gaps |
|---|---|---|---|---|---|
| 1–2 | T1059.001 / T1027 | | | (CAR-2013-07-001) | |
| 3 | T1053.005 / T1547.001 | | | | |
| 4 | T1555.003 / T1005 | | | | |
| 5 | T1102.001 / T1041 / T1070.004 | | | | |

## 6. Honest scoping note

Vidar itself is primarily a smash-and-grab stealer; it does not typically establish its own persistence. Stage 3 is kept in the plan because the assignment requires Initial Access → Persistence → Exfiltration, and because loaders delivered alongside Vidar frequently do persist — we label it "optional/loader-based" in the Navigator layer and in the defense.

