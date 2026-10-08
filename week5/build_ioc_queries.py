#!/usr/bin/env python3
"""Generate H4 (intel-driven) KQL and SPL queries from data/vidar_iocs_normalized.csv."""
from ioc_loader import load
d = load()
q = lambda items: " or ".join(f'"{x}"' for x in sorted(items))
kql = f'''# H4 - Intel-driven hunt generated from our dataset (to_ids = True only)

## H4a - file hashes (sha256/md5/imphash: {len(d["hashes"])})
```
file.hash.sha256 : ({q(d["hashes"])})
```

## H4b - C2 / distribution IPs ({len(d["ips"])})
```
destination.ip : ({q(d["ips"])})
```

## H4c - distribution / C2 domains ({len(d["domains"])})
```
dns.question.name : ({q(d["domains"])})
```

## Watchlist (low confidence, to_ids = False -> triage only, do not alert)
```
destination.ip : ({q(d["cand_ips"])})
```
Note: 104.21.x / 172.67.x are Cloudflare ranges, expect many benign hits.
'''
open("hunt_queries/h4_ioc_kql.md", "w").write(kql)
spl = f'''# H4 SPL generated from dataset
index=sysmon (SHA256 IN ({", ".join(f'"{x}"' for x in sorted(d["hashes"]))}) OR DestinationIp IN ({", ".join(f'"{x}"' for x in sorted(d["ips"]))}) OR QueryName IN ({", ".join(f'"{x}"' for x in sorted(d["domains"]))}))
| table _time host Image DestinationIp QueryName SHA256
'''
open("hunt_queries/h4_ioc_spl.txt", "w").write(spl)
print("written h4 queries")
