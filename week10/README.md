# Week 10: Cyber Threat Intelligence & APT29 TTP Analysis

## 1. Executive Summary
This week focuses on analyzing the Tactics, Techniques, and Procedures (TTPs) of Advanced Persistent Threat (APT) groups using Cyber Threat Intelligence (CTI) vendor reports (Mandiant, CrowdStrike). For this analysis, **APT29** (also known as Cozy Bear, Nobelium, or Midnight Blizzard) was selected. The observed attack vectors were mapped to the **MITRE ATT&CK** framework to establish defensive metrics and detection strategies.

---

## 2. APT Group Overview: APT29 (Cozy Bear)
- **Origin / Attribution:** Russia (SVR / Foreign Intelligence Service)
- **Target Sectors:** Government agencies, diplomatic missions, think tanks, cloud service providers, and technology vendors worldwide.
- **Key Characteristics:** Advanced operational security (OpSec), heavy reliance on legitimate administrative tools (Living off the Land), supply chain compromise, and cloud infrastructure targeting (Microsoft 365 / Azure AD).

---

## 3. Threat Intelligence Case Study & MITRE ATT&CK Mapping

Based on intelligence reports from Mandiant and CrowdStrike, APT29 operations demonstrate systematic progression across the Cyber Kill Chain:

| Attack Phase | MITRE ATT&CK ID | Technique Name | Operational Details & Artifacts |
| :--- | :--- | :--- | :--- |
| **Initial Access** | `T1195.002` | Supply Chain Compromise | Compromising third-party software updates (e.g., SolarWinds Orion platform breach) to distribute trojanized binaries. |
| **Initial Access** | `T1566.002` | Spearphishing Link / Attachment | Targeted phishing campaigns deploying malicious ISO/ZIP archives containing hidden LNK files or DLL side-loading payloads. |
| **Execution** | `T1059.001` | PowerShell Execution | Utilizing obfuscated PowerShell scripts and custom cradles to load payloads directly into memory. |
| **Persistence** | `T1098.005` | Key Credential Modification | Registering malicious OAuth applications and adding secondary credentials/certificates to Azure AD applications. |
| **Privilege Escalation**| `T1548.002` | Bypass User Account Control | Utilizing UAC bypass techniques via registry manipulation (e.g., `eventvwr.exe` or `fodhelper.exe`) to elevate privileges. |
| **Credential Access** | `T1003.001` | LSASS Memory Dumping | Extracting plaintext credentials or NTLM hashes from LSASS memory using custom Mimikatz variants or OS dump utilities. |
| **Lateral Movement** | `T1021.002` | SMB / Windows Admin Shares | Moving laterally across domain hosts using compromised domain credentials via `PsExec` or WMI. |
| **Defense Evasion** | `T1027` | Obfuscated Files / Information | Encoders and steganography to conceal C2 communications, coupled with timestomping and clearing Windows event logs. |
| **Exfiltration** | `T1567.002` | Exfiltration to Cloud Storage | Exfiltrating sensitive emails and documents via legitimate cloud storage APIs (e.g., Dropbox, OneDrive, Mega). |

---

## 4. Detection & Telemetry Strategy

To counter APT29's TTPs, enterprise monitoring must focus on specific high-fidelity log sources and telemetry:

1. **Identity & Access Management (M365 / Entra ID):**
   - Monitor audit logs for newly added Service Principal credentials (`Update application - Certificates and secrets management`).
   - Enable Conditional Access Policies and mandatory Multi-Factor Authentication (MFA).

2. **Endpoint Telemetry (Sysmon / EDR):**
   - **Event ID 1 (Process Create):** Flag PowerShell sessions executing with `-EncodedCommand`, `-NoProfile`, or downloading remote content.
   - **Event ID 10 (Process Access):** Detect non-system processes requesting `PROCESS_VM_READ` or `PROCESS_VM_WRITE` access to `lsass.exe`.
   - **Event ID 11 (File Create):** Monitor creation of `.lnk` or `.iso` files in user `Downloads` and `Temp` directories.

---

## 5. Defense & Mitigation Recommendations

- **Zero Trust Architecture:** Implement strict conditional access policies and restrict OAuth app consent to administrators only.
- **Credential Protection:** Deploy Windows Defender Credential Guard to isolate LSASS memory from unauthorized process access.
- **Software Supply Chain Hygiene:** Enforce binary code signing policies (AppLocker / WDAC) and verify hash integrity for third-party software updates.