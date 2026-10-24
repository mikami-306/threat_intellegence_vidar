# Threat Intelligence & Emulation: Vidar Stealer

## Week 8 — Adversary Emulation Plan

Week 8 extends the single detection rule built in Week 7 (`CAR-2013-07-001`, which catches hidden/encoded PowerShell execution on `WS-04`) into a complete, five-stage emulation plan covering the Vidar infection chain:

| Stage | ATT&CK Technique(s) | Purpose |
|---|---|---|
| Initial Access / Execution | T1566.001, T1204.002, T1059.001 | Simulated phishing-triggered encoded PowerShell execution |
| Defense Evasion | T1027 | Obfuscated/encoded command, caught by the same rule |
| Persistence *(optional, loader-based)* | T1053.005, T1547.001 | Simulated scheduled task / Run key, representing a loader often dropped with Vidar |
| Collection | T1555.003, T1539, T1005 | Canary "browser credential" and "wallet" files, archived |
| C2 / Exfiltration | T1102.001, T1041, T1070.004 | Dead-drop-style C2 lookup, HTTP upload to a local lab server, self-cleanup |

Full details, detection queries (ELK/KQL), and the results table are in [`week8/week8_adversary_emulation_plan.md`](week8/week8_adversary_emulation_plan.md).

### Why "optional" persistence?

Vidar itself is primarily a smash-and-grab stealer and does not typically establish its own persistence. The persistence stage is included because the assignment requires an Initial Access → Persistence → Exfiltration structure, and because loaders frequently delivered alongside Vidar do persist. This is called out explicitly rather than overstated.

### Safety notes

- All scripts are benign: no real malware is downloaded, executed, or stored in this repo.
- `step3_collection.ps1` only creates **canary files** with placeholder content — it never touches a real browser profile or real credentials.
- `step4_exfiltration.ps1` and `server/exfil_server.py` only talk to each other inside an isolated lab network — no real internet C2 is contacted.
- Everything is intended to run only on a disposable lab VM (`WS-04`), ideally from a reverted snapshot.

## How to read this repo

1. Start with `week8/week8_adversary_emulation_plan.md` for the narrative report and the detection logic.
2. Look at `week8/scripts/` to see how each ATT&CK technique is modeled in a safe, reversible way.
3. Look at `week8/detections/sigma_encoded_powershell.yml` for the Sigma-format version of each ELK query, mapped one rule per stage.
4. The results table in the report (filled in after lab runs) shows what telemetry and alerts were actually observed on `WS-04`.

## Next steps

Week 9 will replace the manual PowerShell emulation with equivalent **Atomic Red Team** tests for the same ATT&CK techniques, run against the same `WS-04` host, to compare results against this week's hand-built emulation.

## Group members

_<add names here>_

## References

- MITRE ATT&CK: https://attack.mitre.org
- MITRE CAR: https://car.mitre.org
- MITRE CALDERA documentation
- Atomic Red Team: https://github.com/redcanaryco/atomic-red-team
- Kyle Wilhoit, *Operationalizing Threat Intelligence*, 2022
- Chad Maurice, *The Foundations of Threat Hunting*, 2022
