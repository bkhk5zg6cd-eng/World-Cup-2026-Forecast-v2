#!/usr/bin/env python3
from pathlib import Path
import json, sys
LIVE=Path(__file__).resolve().parents[1]/"data"/"live"
errors=[]
for n in ["teams.json","forecast-results.json","data-health.json","model-config.json"]:
    try: json.loads((LIVE/n).read_text(encoding="utf-8"))
    except Exception as e: errors.append(f"{n}: {e}")
if len(json.loads((LIVE/"teams.json").read_text(encoding="utf-8")).get("teams",[]))!=48: errors.append("Expected 48 teams")
if errors: print("\n".join(errors)); sys.exit(1)
print("Data validation passed.")
