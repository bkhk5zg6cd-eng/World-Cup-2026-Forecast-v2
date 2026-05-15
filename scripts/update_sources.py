#!/usr/bin/env python3
from pathlib import Path
import json, datetime, urllib.request
ROOT=Path(__file__).resolve().parents[1]; LIVE=ROOT/"data"/"live"
def now(): return datetime.datetime.utcnow().replace(microsecond=0).isoformat()+"Z"
def read(p): return json.loads(p.read_text(encoding="utf-8"))
def write(p,o): p.write_text(json.dumps(o,indent=2,ensure_ascii=False),encoding="utf-8")
def update_health(name,status,freshness,message):
    p=LIVE/"data-health.json"; data=read(p); data["lastUpdated"]=now(); found=False
    for s in data.get("sources",[]):
        if s["name"]==name: s.update({"status":status,"freshness":freshness,"message":message}); found=True
    if not found: data.setdefault("sources",[]).append({"name":name,"status":status,"freshness":freshness,"message":message})
    write(p,data)
try:
    url="https://raw.githubusercontent.com/openfootball/worldcup.json/master/2026/worldcup.json"
    req=urllib.request.Request(url,headers={"User-Agent":"world-cup-forecast-dashboard/1.0"})
    payload=json.loads(urllib.request.urlopen(req,timeout=25).read().decode("utf-8"))
    f=read(LIVE/"fixtures.json"); f["source"]="openfootball-worldcup-json"; f["lastUpdated"]=now(); f["rawOpenFootball"]=payload; write(LIVE/"fixtures.json",f); update_health("fixtures","current","refreshed","OpenFootball JSON fetched successfully.")
except Exception as e:
    update_health("fixtures","warning","last-valid-data",f"OpenFootball fetch failed; preserved local fixtures. Error: {e}")
update_health("injuries","warning","best-effort","No reliable free injury API configured. Existing injury assumptions preserved with confidence flags.")
update_health("results","pending","not-started","No official match results ingested yet. Workflow is ready for tournament results.")
