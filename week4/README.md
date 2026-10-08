# Week 4 Report: Cyber Kill Chain Analysis & MITRE ATT&CK Mapping
 
---

## 1. Objective & Scope

In accordance with Week 4 syllabus requirements (*The Cyber Kill Chain & MITRE ATT&CK Comparison*), this phase focuses on:
* Analyzing the end-to-end attack lifecycle of **Vidar Stealer** using the 7-stage **Lockheed Martin Cyber Kill Chain** framework.
* Mapping each stage of the attack directly to corresponding **MITRE ATT&CK Enterprise TTPs** (Tactics, Techniques, and Procedures).
* Comparing the structural and operational methodologies of the Lockheed Martin Kill Chain versus the MITRE ATT&CK framework for modern detection engineering.

---

## 2. Lockheed Martin Cyber Kill Chain vs. MITRE ATT&CK Mapping

The table below illustrates how Vidar Stealer operates across all 7 stages of the Cyber Kill Chain and maps them directly to MITRE ATT&CK TTPs based on our dataset (`vidar_iocs_normalized.csv`).

| Kill Chain Stage | Attack Vector / Vidar Behavior | MITRE ATT&CK Tactic | MITRE ATT&CK TTP (ID & Name) |
| :--- | :--- | :--- | :--- |
| **1. Reconnaissance** | Malware authors profile high-value targets via search traffic, SEO poisoning keywords, and cracking forums. | Reconnaissance | `T1595` - Active Scanning<br>`T1593` - Search Open Technical Databases |
| **2. Weaponization** | Compiling the Vidar C++ executable payload, packing/cryptex obfuscation (WinGo wrappers), binding inside pirated software / ISO images / FDC-ClickFix PowerShell lures. | Resource Development / Execution | `T1587.001` - Develop Capabilities: Malware<br>`T1027` - Obfuscated Files or Information |
| **3. Delivery** | Distribution via **Malvertising Factory** campaigns (Unit42), fake software cracks (Win11 Photoshop), and social engineering prompts (ClickFix copy-paste PS scripts). | Initial Access | `T1566.002` - Phishing: Spearphishing Link<br>`T1189` - Drive-by Compromise |
| **4. Exploitation** | User executes the malicious installer or powershell payload, bypassing basic SmartScreen prompts or downloading secondary payloads from malicious landing URLs. | Execution | `T1059.001` - PowerShell<br>`T1204.002` - User Execution: Malicious File |
| **5. Installation** | Vidar drops temporary `.exe` binaries into `%TEMP%` or `%APPDATA%` folders and loads required DLL dependencies (`freebl3.dll`, `mozglue.dll`, `sqlite3.dll`) to interface with local databases. | Persistence / Defense Evasion | `T1547.001` - Registry Run Keys / Startup Folder<br>`T1036` - Masquerading |
| **6. Command & Control (C2)** | Resolves active C2 IP addresses dynamically via **Dead Drop Resolvers** (Telegram channel bios, Steam profiles) to bypass static IP blacklisting, then initiates HTTP POST communication. | Command and Control | `T1102.001` - Web Service: Dead Drop Resolver<br>`T1071.001` - Application Layer Protocol: Web Protocols |
| **7. Actions on Objectives** | Steals stored browser credentials, SQLite database cookies, crypto wallet keys, auto-fill forms, system information (`T1082`), archives into a `.zip` file, and exfiltrates to C2. | Credential Access / Discovery / Exfiltration | `T1555.003` - Credentials from Password Stores: Credentials from Web Browsers<br>`T1041` - Exfiltration Over C2 Channel |

---

## 3. Structural Comparison: Kill Chain vs. MITRE ATT&CK

To meet the syllabus requirements comparing **Lockheed Martin Intelligence-Driven Defense** and **MITRE ATT&CK**, we evaluate their application to modern infostealers:

| Feature / Aspect | Lockheed Martin Cyber Kill Chain | MITRE ATT&CK Framework |
| :--- | :--- | :--- |
| **Model Structure** | Linear, sequential 7-stage pipeline. Assumes the attacker must complete each step in order. | Non-linear, matrix-based framework (14 Tactics, 190+ Techniques). |
| **Primary Focus** | High-level perimeter defense and preventing initial breach completion. | Deep post-compromise behavior analysis, telemetry, and detection engineering. |
| **Grain & Detail** | High-level conceptual stages (e.g., "Exploitation"). | Highly granular sub-techniques with procedural examples, IOCs, and mitigation strategies. |
| **Infostealer Context** | Effective for tracking delivery channels (ClickFix/Malvertising), but lacks depth for internal credential theft. | Ideal for mapping exact host-based telemetry (e.g., querying Chrome's `Login Data` SQLite DB). |

---

## 4. Key Takeaways for Detection Engineering

1. **Breaking the Chain Early:** Stopping Vidar during **Delivery** (`T1189` - Drive-by Compromise) or **Exploitation** (`T1059.001` - PowerShell execution) prevents credential exfiltration entirely.
2. **C2 Resilience:** Vidar uses **Dead Drop Resolvers** (`T1102.001` - Telegram/Steam profiles) during Stage 6. Blocking C2 IPs alone is insufficient; SOC teams must monitor unauthorized outbound network access to public platforms used as resolvers.
3. **Data Access Monitoring:** Detecting unauthorized access to `%LOCALAPPDATA%\Google\Chrome\User Data\Default\Login Data` (`T1555.003`) serves as the final host-based defense layer before exfiltration.

---

## 5. Repository Artifacts

* **`week4/README.md`**: Complete Cyber Kill Chain & MITRE ATT&CK analysis report.
* **`week4/kill_chain_mapping.json`**: Machine-readable JSON mapping of all 7 Kill Chain stages to MITRE ATT&CK TTPs.