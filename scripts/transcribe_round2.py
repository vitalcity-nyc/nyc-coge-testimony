import json, time, sys, whisper

# Transcribe both Round 2 hearings with Whisper base.en, matching the
# Queens/Staten Island pipeline (16k mono wav -> segments -> ~20s blocks).
JOBS = [
    ("transcripts/audio/bronx_r2.wav",    "transcripts/bronx_r2"),
    ("transcripts/audio/brooklyn_r2.wav", "transcripts/brooklyn_r2"),
]

def mmss(t): t=int(t); return f"{t//60:02d}:{t%60:02d}"

m = whisper.load_model("base.en")
for wav, stem in JOBS:
    t=time.time()
    r=m.transcribe(wav, language="en", fp16=False, verbose=False)
    print(f"{stem}: transcribed in {(time.time()-t)/60:.1f} min, {len(r['segments'])} segments", flush=True)
    segs=[{"text":s["text"].strip(),"start":s["start"],"duration":s["end"]-s["start"]} for s in r["segments"]]
    json.dump(segs, open(stem+".json","w"), ensure_ascii=False, indent=1)
    blocks=[]; cur=[]; cs=None
    for s in segs:
        if cs is None: cs=s["start"]
        cur.append(s["text"])
        if s["start"]-cs>=20: blocks.append((cs," ".join(cur))); cur=[]; cs=None
    if cur: blocks.append((cs," ".join(cur)))
    with open(stem+".txt","w") as f:
        for st,txt in blocks: f.write(f"[{mmss(st)} | t={int(st)}] {txt}\n")
    print(f"{stem}: wrote .txt {len(blocks)} blocks, last t={int(segs[-1]['start'])}s ({mmss(segs[-1]['start'])})", flush=True)
