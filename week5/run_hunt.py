#!/usr/bin/env python3
"""Local fallback hunt runner: executes the same 4 hunts as the KQL/SPL queries
against the simulated NDJSON log, saves hunt_results.csv and hunt_results.png."""
import json, re, argparse
import pandas as pd
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt

ap = argparse.ArgumentParser()
ap.add_argument("--log", default="logs/sim_sysmon.ndjson")
args = ap.parse_args()

rows = [json.loads(l) for l in open(args.log)]
df = pd.json_normalize(rows)
df.columns = [c.replace(".", "_") for c in df.columns]
for c in ["process_command_line", "process_parent_name", "process_name", "dns_question_name",
          "destination_ip", "file_hash_sha256", "event_code", "host_name", "user_name"]:
    if c not in df: df[c] = ""
df = df.fillna("")

from ioc_loader import load
IOC = load("data/vidar_iocs_normalized.csv")      # our own 170-row dataset
IOC_SHA, IOC_IP, IOC_DOM = IOC["hashes"], IOC["ips"], IOC["domains"]
DEAD_DROP_RE = "|".join(re.escape(h) for h in sorted(IOC["dead_drop"]))
BROWSERS_APPS = {"chrome.exe", "msedge.exe", "firefox.exe", "steam.exe", "telegram.exe"}

# H1 - hypothesis: PowerShell with hidden/encoded/download-cradle args (ClickFix lure)
ps = df[(df.event_code == "1") & df.process_name.str.lower().eq("powershell.exe")]
naive_h1 = ps  # baseline: every PowerShell start (too noisy)
h1_raw = ps[ps.process_command_line.str.contains(r"-enc\b|-encodedcommand|-w(?:indowstyle)? hidden|\biex\b|\birm\b|downloadstring", case=False, regex=True)]
h1 = h1_raw[~h1_raw.process_parent_name.str.lower().isin({"ccmexec.exe"})]  # tuning: exclude SCCM client (known admin tooling)
# H2 - hypothesis: executable launched by PowerShell from user-writable path
h2 = df[(df.event_code == "1") & df.process_parent_name.str.lower().eq("powershell.exe") &
        df.process_command_line.str.contains(r"\\AppData\\|\\Temp\\", case=False, regex=True) &
        df.process_name.str.lower().ne("powershell.exe")]
# H3 - hypothesis: non-browser process resolves dead-drop platforms (Telegram/Steam)
h3 = df[(df.event_code == "22") & df.dns_question_name.str.contains(DEAD_DROP_RE, case=False, regex=True) &
        ~df.process_name.str.lower().isin(BROWSERS_APPS)]
# H4 - intel-driven: match Week 2/3 IOCs
h4 = df[df.file_hash_sha256.str.lower().isin(IOC_SHA) | df.destination_ip.isin(IOC_IP) |
        (df.event_code.eq("22") & df.dns_question_name.str.lower().isin(IOC_DOM))]
h4_cand = df[df.destination_ip.isin(IOC["cand_ips"])]   # low-confidence candidates: triage only, not an alert

hunts = {"H1 PowerShell abuse": h1, "H2 Exec from Temp/AppData via PS": h2,
         "H3 DDR from non-browser": h3, "H4 IOC match (intel-driven)": h4}
out = []
for name, d in hunts.items():
    for _, r in d.iterrows():
        out.append({"hunt": name, "time": r["@timestamp"], "host": r.host_name, "user": r.user_name,
                    "process": r.process_name, "detail": r.process_command_line or r.dns_question_name or r.destination_ip})
res = pd.DataFrame(out)
res.to_csv("hunt_results.csv", index=False)

print(f"Total events: {len(df)} | IOCs loaded: {len(IOC_SHA)} hashes, {len(IOC_IP)} IPs, {len(IOC_DOM)} domains, {len(IOC['dead_drop'])} dead-drop hosts")
print(f"Low-confidence candidate IP contacts (watchlist): {len(h4_cand)}")
print(f"H1 tuning: naive={len(naive_h1)} -> pattern={len(h1_raw)} -> tuned={len(h1)}")
print(res.groupby("hunt").size().to_string())
print("\nHosts hit:\n", res.groupby(["hunt", "host"]).size().to_string())

counts = res.groupby("hunt").size().reindex(hunts.keys(), fill_value=0)
ax = counts.plot(kind="barh", figsize=(8, 3.5), color="#3b6ea5")
ax.set_xlabel("matching events"); ax.set_title("Week 5 hunt hits (simulated telemetry)")
plt.tight_layout(); plt.savefig("hunt_results.png", dpi=150)
print("\n[+] saved hunt_results.csv, hunt_results.png")
