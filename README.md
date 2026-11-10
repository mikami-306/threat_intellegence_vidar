# Vidar Stealer: End-to-End Threat Intelligence & Detection Engineering

## Project & Authors Information
- **Authors:** Amangeldina Milana, Imatayeva Aisha
- **Academic Status:** 3rd-year Undergraduate Students in Cybersecurity
- **Course:** Introduction to Threat Hunting
- **Course Instructor:** Tendikov Noyan

---

## Overview
A hands-on threat intelligence and detection engineering project tracking Vidar Stealer, an active Malware-as-the-Service (MaaS) infostealer. While legacy stealers like RedLine took a major hit during Operation Magnus, Vidar continues to evolve, heavily relying on SEO poisoning, malvertising networks, fake software cracks, and FDC-ClickFix social engineering scripts.

This repository documents an end-to-end intelligence workflow: harvesting and cleaning raw IoCs, structuring data for MISP ingestion, mapping behavior to the Lockheed Martin Cyber Kill Chain and MITRE ATT&CK, writing production-grade Sigma detection rules, implementing behavioral analytics via MITRE CAR, planning adversary emulation, and validating telemetry with Atomic Red Team.

---

## Project Phases

### Phase 1: Threat Intelligence & Foundations (Week 1)
- Defined CTI taxonomy across strategic, tactical, and technical levels.
- Developed a glossary covering core concepts: MaaS, SEO Poisoning, Dead Drop Resolvers, and In-Memory Injection.
- Analyzed initial vector trends (cracked installers, rogue YouTube tutorials).

### Phase 2: Infrastructure & Collection (Week 2)
- Gathered raw indicators from MalwareBazaar and VirusTotal.
- Investigated C2 infrastructure using Shodan and mapped Dead Drop Resolvers (Telegram bios, Steam community profiles) used to mask active C2 IPs.

### Phase 3: Data Normalization & MISP Export (Week 3)
- Wrote a custom Python cleaning script (`process_data.py`) to parse, deduplicate, and validate raw indicators.
- Built the clean master dataset (`vidar_iocs_normalized.csv`) featuring 170 unique IoCs.
- Generated EDA visualization charts (`ioc_distribution.png` for type breakdown and `confidence_distribution.png` for source confidence levels).
- Added MISP taxonomy flags (`misp_type`, `misp_category`, `to_ids`).

### Phase 4: Cyber Kill Chain & MITRE TTP Mapping (Week 4)
- Performed a 7-stage Lockheed Martin Cyber Kill Chain analysis tailored to Vidar's execution flow.
- Mapped phases to exact MITRE ATT&CK Enterprise TTPs (`T1555.003`, `T1059.001`, `T1102.001`, `T1082`, `T1189`).
- Compared linear Kill Chain defense models against matrix-based MITRE telemetry tracking.
- Compiled machine-readable mappings (`week4/kill_chain_mapping.json`).

### Phase 5: Threat Hunting & Detection Engineering (Week 5)
- Deployed a local Docker-based ELK Stack (Elasticsearch and Kibana) for simulated telemetry analysis.
- Automated data ingestion and IoC parsing using repository pipelines (`load_to_elk.py`, `ioc_loader.py`, `generate_logs.py`).
- Formulated and tested hunting hypotheses (H1–H4) leveraging Windows Sysmon Event ID 1 (Process Creation) and network telemetry on simulated host `WS-04`.
- Tuned queries to eliminate noise from legitimate background utilities (such as SCCM `ccmexec.exe`) and shared platforms (GitHub, Telegram).

### Phase 6: MITRE ATT&CK Framework Mapping & TTP Deep-Dive (Week 6)
- Structured the complete Vidar infection chain into standardized Tactics, Techniques, and Procedures (TTPs).
- Conducted a deep-dive analysis into technique `T1059.001` (Command and Scripting Interpreter: PowerShell) and obfuscation flag abuse (`T1027`).
- Mapped Dead Drop Resolvers (DDR) and C2 traffic to `T1102` and `T1041`.
- Formatted attack path parameters for interactive rendering in the MITRE ATT&CK Navigator.

### Phase 7: MITRE CAR Analytics & SIEM Detection Logic (Week 7)
- Evaluated behavioral analytics from the MITRE Cyber Analytics Repository (CAR).
- Selected CAR-2013-07-001 (Suspicious Command-Line Arguments) to target obfuscated PowerShell execution patterns.
- Implemented production KQL detection logic targeting Sysmon Event ID 1 telemetry.
- Differentiated abstract analytic models from operational SIEM detections tuned for noise reduction.

### Phase 8: Adversary Emulation Plan & Kill Chain Orchestration (Week 8)
- Designed a multi-stage adversary emulation plan mirroring the realistic Vidar infection chain on host `WS-04`.
- Developed benign testing scripts under `week8/scripts/` covering Initial Access, Defense Evasion, Persistence, Collection, and Exfiltration.
- Formulated complementary ELK KQL detection queries for persistence (scheduled tasks, Run keys via Sysmon EID 1/13), collection (canary file access, `Compress-Archive`), and exfiltration (network POST requests, file deletion tracking via EID 23/26).
- Validated correlated multi-stage alert correlation over time windows rather than isolated rules.

### Phase 9: Atomic Red Team Testing & SIEM Telemetry Validation (Week 9)
- Installed and executed `Invoke-AtomicRedTeam` framework tests on target host `WS-04`.
- Simulated adversary behavior for techniques **T1059.001** (PowerShell Execution) and **T1003** (OS Credential Dumping).
- Verified telemetry ingestion in Kibana (`sysmon-sim` index), validating Sysmon Event ID 1 (Process Creation) and Event ID 10 (Process Access) logging.
- Executed automated cleanup procedures (`-Cleanup`) to maintain endpoint hygiene post-testing.

### Phase 10: APT29 (Cozy Bear) CTI Analysis & Advanced TTP Mapping (Week 10)
- Analyzed CTI vendor reports (Mandiant, CrowdStrike) covering state-sponsored APT29 operations.
- Mapped APT29 attack vectors to MITRE ATT&CK, including Supply Chain Compromise (`T1195.002`), OAuth Credential Modification (`T1098.005`), and Cloud Exfiltration (`T1567.002`).
- Formulated identity-centric (Entra ID) and endpoint-centric (Sysmon/EDR) telemetry collection strategies.
- Defined Enterprise defense recommendations focused on Zero Trust Architecture and Credential Guard deployment.

---

## Data Normalization Pipeline
To handle messy open-source intelligence feeds, a custom python parser (`week3/process_data.py`) standardizes the dataset:
- **Regex Validation:** Validates SHA256/MD5 hashes and IPv4 structures.
- **Sanitization:** Converts domains to lowercase, strips whitespaces, and removes defanged strings (`hxxp`, `[.]`).
- **MISP Taxonomies:** Assigns operational categories (Payload delivery, Network activity) with `to_ids=True`.

---

## AI Usage & Declaration
Artificial Intelligence tools like Gemini adn Claude were utilized as technical accelerators and analytical collaborators throughout this project:
- **Detection Engineering & Logic Tuning:** AI was leveraged to assist in structuring Sigma rule definitions, refining Kibana Query Language (KQL) expressions, and normalizing Sysmon telemetry mappings.
- **Code Optimization & Data Pipelines:** Assisted in drafting regex parameters for the Python data normalization parser (`process_data.py`) and debugging automated ingestion scripts.
- **Documentation & Formatting:** Used for formatting Markdown reports, aligning ATT&CK matrices, and refining English technical documentation across all project phases.
- **Threat Research Partnering:** Employed as a reasoning aid to synthesize vendor CTI reports (Mandiant, CrowdStrike) and map adversary tactics to MITRE ATT&CK standards.