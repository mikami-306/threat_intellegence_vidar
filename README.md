# Detection Engineering and Threat Intelligence Analysis of Vidar Stealer

**Authors:** Amangeldina Milana , Imatayeva Aisha 
**Context:** 3rd Year Cyber Security Students (Astana, Kazakhstan)  
**Instructor:** Tendikov Noyan

---

## Overview

A hands-on threat intelligence and detection engineering project tracking **Vidar Stealer**, an active Malware-as-the-Service (MaaS) infostealer. While legacy stealers like RedLine took a major hit during *Operation Magnus*, Vidar continues to evolve, heavily relying on SEO poisoning, malvertising networks, fake software cracks, and FDC-ClickFix social engineering scripts.

This repository documents an end-to-end intelligence workflow: harvesting and cleaning raw IoCs, structuring data for MISP ingestion, mapping behavior to the **Lockheed Martin Cyber Kill Chain** and **MITRE ATT&CK**, and writing production-grade **Sigma detection rules**.

---

## Project Phases

### Phase 1: Threat Intelligence & Foundations (Week 1)
* Defined CTI taxonomy across strategic, tactical, and technical levels.
* Developed a glossary covering core concepts: *MaaS*, *SEO Poisoning*, *Dead Drop Resolvers*, and *In-Memory Injection*.
* Analyzed initial vector trends (cracked installers, rogue YouTube tutorials).

### Phase 2: Infrastructure & Collection (Week 2)
* Gathered raw indicators from **MalwareBazaar** and **VirusTotal**.
* Investigated C2 infrastructure using **Shodan** and mapped **Dead Drop Resolvers** (Telegram bios, Steam community profiles) used to mask active C2 IPs.

* ### Phase 3: Data Normalization & MISP Export (Week 3)
* Wrote a custom Python cleaning script (`process_data.py`) to parse, deduplicate, and validate raw indicators.
* Built the clean master dataset (`vidar_iocs_normalized.csv`) featuring **170 unique IoCs**.
* Generated EDA visualization charts (`ioc_distribution.png` for type breakdown and `confidence_distribution.png` for source confidence levels).
* Added MISP taxonomy flags (`misp_type`, `misp_category`, `to_ids`).

### Phase 4: Cyber Kill Chain & MITRE TTP Mapping (Week 4)
* Performed a 7-stage **Lockheed Martin Cyber Kill Chain** analysis tailored to Vidar's execution flow.
* Mapped phases to exact **MITRE ATT&CK Enterprise TTPs** (`T1555.003`, `T1059.001`, `T1102.001`, `T1082`, `T1189`).
* Compared linear Kill Chain defense models against matrix-based MITRE telemetry tracking.
* Compiled machine-readable mappings (`week4/kill_chain_mapping.json`).

---

## Data Normalization Pipeline

To handle messy open-source intelligence feeds, a custom python parser (`week3/process_data.py`) standardizes the dataset:
1. **Regex Validation:** Validates SHA256/MD5 hashes and IPv4 structures.
2. **Sanitization:** Converts domains to lowercase, strips whitespaces, and removes defanged strings (`hxxp`, `[.]`).
3. **MISP Taxonomies:** Assigns operational categories (`Payload delivery`, `Network activity`) with `to_ids=True`.

### Dataset Breakdown (`vidar_iocs_normalized.csv`)
* **Total Records:** 170 validated IoCs
* **Hashes:** 120 (SHA256, MD5, IMPHASH)
* **Network Indicators:** 49 (URLs, IPs, Domains)
* **Attribution:** Unit42 Malvertising Factory, ClickFix campaigns, Polymorphic C2 infrastructure.

---

## AI Assistant Disclosure

AI tools were used strictly as a development assistant during this project:
* **Python & Regex:** Assisting with Pandas dataframe transformations and regular expression syntax for hash validation.
* **Sigma Validation:** Checking YAML schema compliance and tuning selection filters for `%TEMP%` execution and registry persistence.
* **Framework Cross-Checking:** Reviewing alignment between Kill Chain phases and MITRE sub-techniques.

---
