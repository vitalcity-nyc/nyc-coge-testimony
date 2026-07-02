#!/usr/bin/env python3
"""Apply transcripts/round2_merge.json to ideas.json deterministically.

- Adds any new_ideas (with empty proponents) preserving category grouping.
- Appends each assignment's proponent to its idea, deduping on (name, hearing)
  per idea so a witness is never double-listed on the same idea for the same hearing.
- Recomputes proponent_count and the hearings list (distinct, insertion order).
"""
import json, sys, collections

ROOT = "/Users/joshgreenman/Experiments/nyc-coge-testimony"
ideas = json.load(open(f"{ROOT}/ideas.json"))
plan  = json.load(open(f"{ROOT}/transcripts/round2_merge.json"))

by_id = {i["id"]: i for i in ideas}

# 1) create new ideas
created = []
for ni in plan.get("new_ideas", []):
    if ni["id"] in by_id:
        print(f"WARN new_idea id already exists, will just append: {ni['id']}")
        continue
    idea = {
        "id": ni["id"],
        "title": ni["title"],
        "category": ni["category"],
        "summary": ni["summary"],
        "proponent_count": 0,
        "hearings": [],
        "proponents": [],
    }
    by_id[ni["id"]] = idea
    ideas.append(idea)
    created.append(ni["id"])

# 2) apply assignments
missing = []
added = 0
dupes = 0
for a in plan.get("assignments", []):
    iid = a["idea_id"]
    idea = by_id.get(iid)
    if idea is None:
        missing.append(iid)
        continue
    p = a["proponent"]
    key = (p["name"].strip().lower(), p["hearing"])
    existing = {(q["name"].strip().lower(), q["hearing"]) for q in idea["proponents"]}
    if key in existing:
        dupes += 1
        continue
    idea["proponents"].append(p)
    added += 1

if missing:
    print("ERROR: assignments reference unknown idea ids:", sorted(set(missing)))
    sys.exit(1)

# 3) recompute counts + hearings (distinct, insertion order)
for idea in ideas:
    idea["proponent_count"] = len(idea["proponents"])
    seen = []
    for p in idea["proponents"]:
        if p["hearing"] not in seen:
            seen.append(p["hearing"])
    idea["hearings"] = seen

# sort ideas by proponent_count desc so the catalog leads with the most-backed
ideas.sort(key=lambda i: (-i["proponent_count"], i["title"].lower()))

json.dump(ideas, open(f"{ROOT}/ideas.json", "w"), ensure_ascii=False, indent=1)

uniq = len({p["name"] for i in ideas for p in i["proponents"]})
links = sum(len(i["proponents"]) for i in ideas)
print(f"applied: +{added} proponent links ({dupes} dupes skipped)")
print(f"new ideas created: {len(created)} -> {created}")
print(f"totals now: {len(ideas)} ideas, {uniq} unique witnesses, {links} links")
