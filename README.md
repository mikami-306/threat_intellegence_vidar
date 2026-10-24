# Detection Engineering and Threat Intelligence Analysis of Vidar Stealer
### Course: Introduction to Threat Hunting
### Instructor: Tendikov Noyan
### Students: Imatayeva Aisha, Amangeldina Milana— 3rd year, Cyber Security
Lab host: WS-04 | Stack: ELK (Elasticsearch/Kibana) + Sysmon
### About the project
This repo covers our group's work tracking Vidar Stealer, a Malware-as-a-Service infostealer that's been active since 2018. While older stealers like RedLine lost most of their infrastructure after Operation Magnus, Vidar is still very much active, relying on SEO poisoning, malvertising, fake cracked-software installers, and fake "ClickFix" CAPTCHA pages to get onto machines. That made it a reasonable target to track for the semester since there's a steady stream of current indicators and reporting on it.
The project goes from raw threat intel collection, through data cleaning and MISP-style formatting, mapping Vidar's behavior to the Kill Chain and MITRE ATT&CK, building actual Sigma/KQL detections, and finishing with an adversary emulation plan that ties the detections together into a realistic attack chain.
Workflow, roughly in order
We started by building a profile of Vidar and a glossary of the key terms we kept running into (MaaS, SEO poisoning, dead drop resolvers, in-memory injection). From there we pulled raw IoCs from MalwareBazaar and VirusTotal, looked at C2 infrastructure with Shodan, and started noticing the dead-drop pattern - Vidar often pulls its real C2 address from a Telegram bio or Steam profile instead of hardcoding it, which makes blocklisting by IP alone pretty useless.
After that we cleaned the data into a usable dataset, mapped the infection chain to both the Kill Chain and ATT&CK, built and tuned detections on WS-04, and in Week 8 put together a full emulation plan.
### Week by week
### Week 1 — CTI Fundamentals
Built a glossary of core CTI terms and classified Vidar-related threats by type/source. Looked at strategic vs tactical vs technical intel levels and where Vidar fits.
### Week 2 — Data Collection
Pulled indicators from MalwareBazaar and VirusTotal, checked infrastructure with Shodan, mapped out dead drop resolver behavior (Telegram/Steam profiles used to hide live C2 IPs).
### Week 3 — Data Processing
Wrote a cleaning script to normalize the raw IoCs - validating hashes and IPs with regex, lowercasing domains, stripping defanged strings (`hxxp`, [.]`), and tagging everything with MISP-style fields (`misp_type, misp_category, `to_ids`). Output is a normalized CSV we use for the rest of the project.
### Week 4 — Cyber Kill Chain
Walked Vidar's infection flow through the 7 Lockheed Martin Kill Chain stages and mapped each stage to specific ATT&CK techniques (T1555.003, T1059.001, T1102.001, T1082, T1189). Compared the linear Kill Chain view against the matrix-style ATT&CK view for actually tracking telemetry.
### Week 5 — Threat Hunting
Set up a local ELK stack and started hunting on WS-04. Wrote a few hypotheses around suspicious PowerShell activity and tested them against simulated logs, then tuned the queries to cut out noise from normal background processes (things like SCCM's ccmexec.exe kept showing up as false positives early on).
### Week 6 — ATT&CK Framework
Went deeper into T1059.001 (PowerShell) and T1027 (obfuscation flags), and mapped the dead-drop/C2 traffic to T1102 and T1041. Laid out the full attack path so it could be viewed in ATT&CK Navigator.
### Week 7 — MITRE CAR
Picked CAR-2013-07-001 (suspicious command-line arguments) since it fit what we'd already been looking at in Week 6 - hidden window styles and encoded commands in PowerShell. Implemented it as a working KQL query against Sysmon Event ID 1 on WS-04, and talked through the difference between the abstract CAR analytic and the tuned, noise-reduced version we actually run.
### Week 8 — Adversary Emulation Plan
Took the Week 7 detection and built it into a full emulation plan covering the realistic Vidar chain: initial access (encoded PowerShell), persistence (optional - more representative of a loader than Vidar itself), collection (fake browser/wallet data), and exfiltration (dead-drop C2 lookup + upload). Each stage has a matching ATT&CK technique and detection query. Full writeup, scripts, and Sigma rules are in week8.
Data pipeline
The normalization script (`process_data.py`) handles the messy parts of raw OSINT feeds:
- validates SHA256/MD5 hashes and IPv4 addresses with regex
- lowercases domains, strips whitespace, removes defanged markers like hxxp and [.]
- tags each record with MISP category fields and to_ids
Output is vidar_iocs_normalized.csv - <fill in actual record count> validated indicators, split between hashes and network indicators (URLs/IPs/domains).
AI assistance disclosure
### We used AI (Claude) at a few points during this project, mainly as a coding and review assistant:
- helping write/debug the Python cleaning scripts (regex for hash/IP validation, pandas transformations)
- checking Sigma rule YAML syntax and tuning selection filters
