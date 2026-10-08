#!/usr/bin/env python3
"""Bulk-load simulated logs into local Elasticsearch (index sysmon-sim). Needs: pip install requests"""
import json, requests
URL = "http://localhost:9200"
lines = [json.loads(l) for l in open("logs/sim_sysmon.ndjson")]
body = "".join(json.dumps({"index": {"_index": "sysmon-sim"}}) + "\n" + json.dumps(d) + "\n" for d in lines)
r = requests.post(f"{URL}/_bulk", data=body, headers={"Content-Type": "application/x-ndjson"})
print(r.status_code, "errors:", r.json().get("errors"), "indexed:", len(lines))
