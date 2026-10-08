"""Load hunt IOCs from our own dataset (data/vidar_iocs_normalized.csv, 170 rows)."""
import re, pandas as pd

SHARED_PLATFORMS = {"github.com", "t.me", "telegram.me", "steamcommunity.com", "ieji.de", "koyu.space"}  # legit hosts: not usable as domain IOC (FP source)

def load(path="data/vidar_iocs_normalized.csv"):
    df = pd.read_csv(path)
    act = df[df.to_ids == True]                      # actionable only (159); low-confidence candidates handled separately
    hashes = set(act[act.ioc_type.isin(["sha256", "md5", "imphash"])].value.str.lower())
    ips = set(act[act.ioc_type == "ip"].value)
    cand_ips = set(df[(df.ioc_type == "ip") & (df.to_ids == False)].value)   # e.g. 31.59.44.104 (c2_candidate, low)
    dist_domains = set(act[act.ioc_type == "domain"].value.str.lower())
    for u in act[(act.ioc_type == "url")].value:      # host part of distribution URLs
        host = re.sub(r"^https?://", "", u).split("/")[0].lower()
        (ips if re.fullmatch(r"\d+\.\d+\.\d+\.\d+", host) else dist_domains).add(host)
    # dead drops: hostnames of role == dead_drop (t.me, telegram.me, steamcommunity.com, mastodon instances...)
    dd = df[df.role == "dead_drop"].value
    dist_domains -= SHARED_PLATFORMS
    dead_drop_hosts = {re.sub(r"^https?://", "", u).split("/")[0].lower() for u in dd}
    return dict(hashes=hashes, ips=ips, cand_ips=cand_ips, domains=dist_domains, dead_drop=dead_drop_hosts, df=df)

if __name__ == "__main__":
    d = load()
    for k, v in d.items():
        if k != "df": print(k, len(v), sorted(v)[:5])
