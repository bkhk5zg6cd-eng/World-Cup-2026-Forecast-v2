#!/usr/bin/env python3
from pathlib import Path
import json, re
ROOT=Path(__file__).resolve().parents[1]; LIVE=ROOT/"data"/"live"; HISTORY=ROOT/"data"/"history"; SNAP=HISTORY/"snapshots"; SNAP.mkdir(parents=True,exist_ok=True)
f=json.loads((LIVE/"forecast-results.json").read_text(encoding="utf-8")); h=json.loads((LIVE/"data-health.json").read_text(encoding="utf-8")); ts=f["lastUpdated"]; snap={"timestamp":ts,"modelVersion":f.get("modelVersion"),"latestMatchIncluded":f.get("latestMatchIncluded"),"topChampion":f.get("topChampion"),"topChampionProbability":f.get("topChampionProbability"),"top10":f.get("results",[])[:10],"dataHealth":h.get("sources",[])}
(SNAP/(re.sub(r"[^0-9A-Za-z]+","-",ts).strip("-")+".json")).write_text(json.dumps(snap,indent=2,ensure_ascii=False),encoding="utf-8")
p=HISTORY/"forecast-history.json"; hist=json.loads(p.read_text(encoding="utf-8")) if p.exists() else {"snapshots":[]}
hist["snapshots"]=[s for s in hist.get("snapshots",[]) if s.get("timestamp")!=ts]+[snap]; hist["snapshots"]=hist["snapshots"][-300:]; hist["generatedAt"]=ts; p.write_text(json.dumps(hist,indent=2,ensure_ascii=False),encoding="utf-8")
