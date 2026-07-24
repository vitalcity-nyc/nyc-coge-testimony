#!/usr/bin/env python3
"""Reconcile Queens (Round 2) against the official COGE meeting minutes.

Source: https://www.nyc.gov/assets/charter/downloads/pdf/meetings-hearings/
        7132026-COGE-Queens-2-Meeting-Minutes-pages-deleted-pages.pdf
(July 13, 2026, Queens Borough Hall. Pages 1-2 are text; page 3 is a scanned
image read visually.)

Every rename below is the official-minutes spelling confirmed against an
independent public record (see NOTES). Names the minutes spell differently but
public records do not support are left alone.
"""
import json
import shutil

HEARING = "Queens (Round 2)"

# old name -> (new name, new confidence, note)
RENAMES = {
    "Alex Kamarda": ("Alex Camarda", "high", "Reinvent Albany staff page"),
    "Alex Moreno": ("Alex Morano", "high", "Streetsblog author page + prior Council testimony"),
    "Edgar Alfonso": ("Edgar Alfonseca", "high", "Streetsblog hearing coverage + QCB6 appointee list"),
    "Judy": ("Judy Wessler", "high", "minutes; longtime CPHS co-founder/director"),
    "Kevin Lera": ("Kevin LaCherra", "high", "prior Council testimony; his own press contact line"),
    "May Frank": ("Mae Francke", "high", "Transportation Alternatives staff page"),
    "Merrill Labour": ("Meryl LaBorde", "high", "Streetsblog coverage of this hearing"),
    "Michelle Yanchi": ("Michelle Yanche", "high", "Good Shepherd Services site"),
    "Misha Nonnen": ("Misha Nonen", "high", "NYC Criminal Justice Agency staff page"),
    "Namaka Gibbi": ("Nwamaka Ejebe", "high", "NYC Council press release naming its general counsel"),
    "Nyla Rosario": ("Naila Caicedo-Rosario", "high", "her own One Fair Wage bio page"),
    "Sarah Catalinato": ("Sara Catalinotto", "high", "NY1 profile of the PIST NYC founder (Sara, no h)"),
    "Xavier Puok": ("Xavier Pu-Folkes", "low", "minutes spelling; no public record either way"),
    "Gail Brewer": ("Gale Brewer", "high", "official Council page: Gale A. Brewer"),
}

# names the minutes confirm outright, so provisional confidence can be raised
CONFIRMED = {
    "Eric Huntley": "high",
    "Karen Wharton": "high",
    "Lourdes Blanco": "high",
    "Rex Tai": "high",
    "Geoff Brown": "high",  # minutes say "Geoffrey"; he uses Geoff publicly
}

shutil.copy("ideas.json", "ideas.backup-pre-qr2-minutes.json")
ideas = json.load(open("ideas.json"))

renamed = {}
raised = {}
for idea in ideas:
    for p in idea["proponents"]:
        if p["hearing"] != HEARING:
            continue
        if p["name"] in RENAMES:
            new, conf, _ = RENAMES[p["name"]]
            renamed.setdefault((p["name"], new), 0)
            renamed[(p["name"], new)] += 1
            p["name"] = new
            p["name_confidence"] = conf
        elif p["name"] in CONFIRMED:
            if p["name_confidence"] != CONFIRMED[p["name"]]:
                raised.setdefault(p["name"], 0)
                raised[p["name"]] += 1
            p["name_confidence"] = CONFIRMED[p["name"]]

# A rename can collide with an existing proponent on the same idea. Only dedupe
# names this script actually touched -- pre-existing multi-hearing rows for the
# same person (e.g. Michael Piccirillo at Manhattan R1 and R2) are left alone;
# they do not inflate proponent_count, which counts distinct names.
touched = {new for new, _, _ in RENAMES.values()}
dropped = []
for idea in ideas:
    seen = set()
    keep = []
    for p in idea["proponents"]:
        if p["name"] in touched and p["name"] in seen:
            dropped.append((idea["id"], p["name"], p["hearing"]))
            continue
        seen.add(p["name"])
        keep.append(p)
    idea["proponents"] = keep
    idea["proponent_count"] = len({p["name"] for p in idea["proponents"]})

ideas.sort(key=lambda i: -i["proponent_count"])
json.dump(ideas, open("ideas.json", "w"), indent=1, ensure_ascii=False)

names = {p["name"] for i in ideas for p in i["proponents"]}
print("renames applied:")
for (old, new), n in sorted(renamed.items()):
    print(f"  {old} -> {new}  ({n} rows)")
print("confidence raised:", dict(raised))
print("duplicate rows dropped:", dropped)
print(f"totals: {len(ideas)} ideas / {len(names)} distinct witnesses")
