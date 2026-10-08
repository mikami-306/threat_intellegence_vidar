# Week 1 Report: Glossary, Classification, OSINT Reconnaissance & Project Scope

**Project Title:** Detection Engineering and Threat Intelligence Analysis of Vidar Stealer Distributed via Cracked Software, SEO Poisoning, and Fake YouTube Downloads

---

## 1. Malware Profile and Why Vidar

**Vidar Stealer** is an information-stealing virus based on the older Arkei stealer. Cybercriminals buy it on darknet forums under the **Malware-as-a-Service (MaaS)** model for around \$130 to \$750 per month. 

Its main goal is financial profit. Vidar steals browser passwords, session cookies, saved forms, cryptocurrency wallets, and login tokens.

### Distribution Channels:
* Fake software cracks and pirated games.
* Links under fake YouTube tutorials and videos.
* **SEO poisoning** (fake sites ranking high on Google).
* **Malvertising** (dangerous online ads).

### Why Vidar Instead of RedLine?
RedLine was very famous, but international police disabled its infrastructure at the end of 2024 (**Operation Magnus**). Because of this, RedLine is not very active today, and fresh data is hard to find. Vidar is extremely active right now. Unit 42 reported a major Vidar campaign in April 2026, and Vidar 2.0 was released around late 2025. Choosing Vidar gives us fresh, real-world data to analyze.

---

## 2. Threat Intelligence Levels

* **Strategic Level:** High-level trends. Cybercriminals prefer buying MaaS subscriptions like Vidar because it is cheap, updated regularly, and makes data theft easy.
* **Tactical Level:** How the attack works step-by-step (TTPs): SEO poisoning -> Fake ZIP archive download -> Malicious DLL side-loading -> Telegram/Steam C2 discovery -> Password and cookie extraction.
* **Technical Level:** The actual indicators of compromise (IoCs) we use for blocking: SHA256 hashes, C2 IP addresses, fake domains, and registry keys.

---

## 3. Simple Glossary

* **Infostealer:** A type of virus created to steal logins, cookies, crypto wallets, and browser data from a computer.
* **Malware as a Service (MaaS):** A business model where virus developers rent out their malware and control panels to other hackers for a monthly fee.
* **SEO Poisoning:** A trick where attackers optimize dangerous websites so they appear at the top of search engine results for keywords like *"free software download"*.
* **DLL Side Loading:** A technique where a legitimate program is tricked into loading a dangerous DLL file placed in the same folder.
* **Dead Drop Resolver (DDR):** Using safe public sites like Telegram channels or Steam profiles to dynamically resolve and hide the real C2 server IP address.
* **Stealer Log:** A compressed ZIP file created by the virus that holds all stolen passwords and system info before sending it to the hacker.

---

## 4. OSINT Data Source Mapping

| Source | Type | Data Collected | Reliability | Usage in Project |
| :--- | :--- | :--- | :--- | :--- |
| **ThreatFox** | Free / Open | C2 IPs and domain URLs | High | Gathering active Vidar server addresses |
| **MalwareBazaar** | Free / Open | SHA256 / MD5 Hashes | High | Getting file hashes of Vidar samples |
| **VirusTotal** | Free / Open | Antivirus scan results & graphs | Very High | Validating collected hashes & IPs |
| **Shodan** | Free / Open | Open ports & C2 server info | High | Checking C2 panel hosting details |

---

## 5. Investigation Results & Project Dataset

### A. Case Study: VirusTotal & Shodan OSINT Analysis
We selected a fresh Vidar Stealer sample SHA256 (`e93511363f7781c4c7ff3ed0698db6c4634092fe7e93ca96d666509a9412e73e`) from MalwareBazaar and analyzed it on VirusTotal:

* **File Name:** `lf3t32pa.exe`
* **File Size:** 97.06 MB
* **Detection Rate:** 7 out of 68 security vendors flagged this file as malicious.
* **Threat Classification:** `trojan.wingo/krypt` (identified as a Trojan/WinGo Packer by vendors like ESET, Sophos, and Google).

### B. Aggregated Master Dataset Scope
In addition to individual sample research, during this initial phase, we aggregated and normalized a dataset of **170 unique Indicators of Compromise (IoCs)** stored in the project root (`data.csv`). This dataset includes:
* **File Hashes:** SHA256 samples across recent campaigns.
* **Network Indicators:** C2 IP endpoints and domain URLs associated with active Vidar infrastructure.
* **Metadata:** Source provenance, threat tags, and confidence scoring for subsequent SIEM/Sigma integration.