# Week 7: Implementing MITRE CAR (Cyber Analytics Repository) Analytics

## Overview
This week focuses on utilizing the **MITRE Cyber Analytics Repository (CAR)** to bridge the gap between abstract threat models (ATT&CK) and practical SIEM detections. We selected a behavioral analytic model and mapped it to our ELK/Sysmon simulation environment on host `WS-04`.

## Selected CAR Analytic
* **Analytic ID:** `CAR-2013-07-001` (Suspicious Command-Line Arguments / Hidden Execution)
* **Associated ATT&CK Technique:** **T1059.001** (Command and Scripting Interpreter: PowerShell) & **T1027** (Obfuscated Files or Information)
* **Data Source:** Sysmon Event ID 1 (Process Creation)

## Analytic Description & Logic
The selected CAR analytic looks for command-line executions containing anomalous flags, window styles (such as `-w hidden`), or encoded command parameters (`-enc`) typically utilized by malicious scripts (like Vidar Stealer) to evade analyst visibility.

### Implementation Logic (Pseudocode / KQL representation)
```kql
// ELK KQL Query implementing CAR-2013-07-001 logic for Sysmon
event.code: "1" 
  and process.name: "powershell.exe" 
  and (process.command_line: "*windowstyle hidden*" 
       or process.command_line: "*-w hidden*" 
       or process.command_line: "*-enc*")
  and host.name: "WS-04"