# Week 1 Report: Glossary, Threat Classification & CTI Fundamentals

**Project Title:** Detection Engineering and Threat Intelligence Analysis of Vidar Stealer Distributed via Cracked Software, SEO Poisoning, and Fake YouTube Downloads

---

## 1. Malware Profile and Why Vidar

Vidar Stealer is an information-stealing virus based on the older Arkei stealer. Cybercriminals buy it on darknet forums under the Malware as a Service model for around \$130 to \$750 per month.  
Its main goal is financial profit. Vidar steals browser passwords, session cookies, saved forms, cryptocurrency wallets, and login tokens.

### Distribution Channels:
* **Fake software cracks** and pirated games
* **Links under fake YouTube tutorials**
* **SEO poisoning** (fake sites ranking high on Google)
* **Malvertising** (dangerous online ads)

### Why We Chose Vidar Instead of RedLine:
RedLine was very famous, but international police disabled its infrastructure at the end of 2024 (Operation Magnus). Because of this, RedLine is not very active today and fresh data is hard to find. Vidar is extremely active right now. Unit 42 reported a major Vidar campaign in April 2026, and Vidar 2.0 was released around late 2025. Choosing Vidar gives us fresh, real-world data to analyze.

---

## 2. Threat Intelligence Levels

* **Strategic Level:**  
  High-level trends. Cybercriminals prefer buying MaaS subscriptions like Vidar because it is cheap, updated regularly, and makes data theft easy.

* **Tactical Level:**  
  How the attack works step by step (TTPs):  
  `SEO Poisoning` ➔ `Fake ZIP Archive Download` ➔ `Malicious DLL Side-Loading` ➔ `Telegram/Steam C2 Discovery` ➔ `Password and Cookie Extraction`.

* **Technical Level:**  
  The actual indicators (IoCs) we use for blocking: SHA256 hashes (`e93511363f7781c4c7ff3ed0698db6c4634092fe7e93ca96d666509a9412e73e`), C2 IP addresses (`31.59.44.104`), fake domains, and registry keys.

---

## 3. Simple Glossary

* **Infostealer:** A type of virus created to steal logins, cookies, crypto wallets, and browser data from a computer.
* **Malware as a Service (MaaS):** A model where virus developers rent out their malware and control panels to other hackers for a monthly fee.
* **SEO Poisoning:** A trick where attackers optimize dangerous websites so they appear at the top of search engine results for keywords like *"free software download"*.
* **DLL Side Loading:** A trick where a legitimate program is tricked into loading a dangerous DLL file placed in the same folder.
* **Dead Drop Resolver:** Using safe public sites like Telegram channels or Steam profiles to hide the real server IP address.
* **Stealer Log:** A zip file created by the virus that holds all stolen passwords and system info before sending it to the hacker.