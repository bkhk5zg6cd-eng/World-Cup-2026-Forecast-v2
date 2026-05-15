#!/usr/bin/env python3
from pathlib import Path
import json, math, datetime
ROOT=Path(__file__).resolve().parents[1]; LIVE=ROOT/"data"/"live"
def r(n): return json.loads((LIVE/n).read_text(encoding="utf-8"))
def w(n,o): (LIVE/n).write_text(json.dumps(o,indent=2,ensure_ascii=False),encoding="utf-8")
def adj(t,weights,risks):
    total=sum(weights.values()) or 1
    score=weights["fifa"]/total*t["fifaScore"]+weights["elo"]/total*t["eloScore"]+weights["form"]/total*t["recentForm"]+weights["attackDefense"]/total*((t["attack"]+t["defense"])/2)+weights["squad"]/total*((t["squadDepth"]+t["squadValue"])/2)+weights["tournament"]/total*((t["tournamentExperience"]+t["knockoutResilience"])/2)+weights["coach"]/total*t["coachingStability"]
    score+=t.get("marketPrior",0)*(risks["marketInfluence"]/18); score-=t["injuryRisk"]/100*risks["injuryImpact"]; score-=t["pathDifficulty"]/100*risks["pathImpact"]; score-=t["travelBurden"]/100*risks["travelImpact"]; score+=t["climateFit"]/100*risks["climateImpact"]
    if t["region"]=="CONCACAF": score+=1.6
    if t["region"]=="CONMEBOL": score+=.5
    return max(35,min(105,score))
teams=r("teams.json")["teams"]; cfg=r("model-config.json"); scored=[(t,adj(t,cfg["weights"],cfg["riskSettings"])) for t in teams]; den=sum(math.exp((s-58)/13) for t,s in scored); results=[]
for t,s in scored:
    p=math.exp((s-58)/13)/den*100; base=t.get("baselineChampionProbability",0); p=.55*base+.45*p
    results.append({"team":t["name"],"group":t["group"],"region":t["region"],"championProbability":round(p,3),"baselineChampionProbability":round(base,3),"probabilityChange":round(p-base,3),"adjustedStrength":round(s,3)})
results.sort(key=lambda x:x["championProbability"],reverse=True); now=datetime.datetime.utcnow().replace(microsecond=0).isoformat()+"Z"
w("forecast-results.json",{"source":"github-actions-model","lastUpdated":now,"modelVersion":cfg.get("modelVersion","1.0.0"),"latestMatchIncluded":"Latest available public data refresh.","topChampion":results[0]["team"],"topChampionProbability":results[0]["championProbability"],"results":results,"whatChanged":[{"team":results[0]["team"],"change":0,"reason":"Model inputs refreshed from latest available data."}]})
