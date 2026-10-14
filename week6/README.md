# Week 6: ATT&CK Framework Mapping & TTP Analysis

## Overview
This week focuses on mapping the simulated Vidar Stealer infection chain (executed on host `WS-04`) to the **MITRE ATT&CK Framework**, defining Tactics, Techniques, and Procedures (TTPs).

## Attack Chain & ATT&CK Mapping Table

| Phase / Step | Host | Description of Activity | MITRE Tactic | Technique ID & Name |
| :--- | :--- | :--- | :--- | :--- |
| **1. Initial Access** | WS-04 | User navigates to a malicious campaign site (`win11install.com`) via browser. | Initial Access | **T1189** - Drive-by Compromise |
| **2. Execution** | WS-04 | Hidden PowerShell execution (`-w hidden -enc ...`) triggered by the user/campaign. | Execution | **T1059.001** - Command and Scripting Interpreter: PowerShell |
| **3. Defense Evasion** | WS-04 | Execution parameters obscure command-line arguments to bypass security controls. | Defense Evasion | **T1027** - Obfuscated Files or Information |
| **4. Discovery / Action** | WS-04 | Payload dropped and executed from user temporary directory (`AppData\Local\Temp`). | Execution / Persistence | **T1204.002** - User Execution: Malicious File |
| **5. Command & Control** | WS-04 | Queries public platforms (Telegram/Steam) for C2 infrastructure via Dead Drop Resolvers (DDR). | Command and Control | **T1102** - Web Service (Alternative Protocol) |
| **6. Exfiltration** | WS-04 | Successful outbound connection to the C2 server (`195.201.250.209`) for data theft. | Exfiltration | **T1041** - Exfiltration Over C2 Channel |

## Methodology Focus: Technique T1059.001 (PowerShell)
As highlighted in the syllabus, we deep-dived into **T1059 (Command-Line Interface / Scripting)**[cite: 1]. Specifically, PowerShell abuse represents one of the most versatile attack vectors, allowing adversaries to execute memory-resident payloads without touching the disk initially.

## MITRE ATT&CK Navigator Export / Layer Details
The associated custom enterprise layer JSON can be used in the [ATT&CK Navigator](https://mitre-attack.github.io/attack-navigator/) to visually highlight the exact path taken by the Vidar Stealer simulation.