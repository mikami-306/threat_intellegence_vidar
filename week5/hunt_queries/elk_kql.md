# ELK / Kibana hunt queries (Discover -> KQL), data view: `sysmon-sim*`

## H1 - Suspicious PowerShell (hypothesis-driven)
```
event.code : "1" and process.name : "powershell.exe" and
process.command_line : (*-enc* or *-encodedcommand* or *hidden* or *iex* or *irm* or *downloadstring*) and
not process.parent.name : "ccmexec.exe"
```

## H2 - Executable from Temp/AppData started by PowerShell
```
event.code : "1" and process.parent.name : "powershell.exe" and
process.command_line : (*\\AppData\\* or *\\Temp\\*) and not process.name : "powershell.exe"
```

## H3 - Dead Drop Resolver lookups by non-browser process
```
event.code : "22" and dns.question.name : (*t.me or *telegram.me or *steamcommunity.com) and
not process.name : ("chrome.exe" or "msedge.exe" or "firefox.exe" or "Steam.exe" or "Telegram.exe")
```

## H4 - Intel-driven: IOCs from Week 2/3
```
file.hash.sha256 : "e93511363f7781c4c7ff3ed0698db6c4634092fe7e93ca96d666509a9412e73e" or destination.ip : "31.59.44.104"
```

## Pivot (after a hit): everything on the suspicious host, +/- 10 minutes
```
host.name : "WS-04"
```
Sort by @timestamp ascending; add columns: process.name, process.parent.name, process.command_line, dns.question.name, destination.ip.
