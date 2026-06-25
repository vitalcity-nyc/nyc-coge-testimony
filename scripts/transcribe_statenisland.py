import json, time, whisper
WAV="transcripts/audio/statenisland.wav"
m=whisper.load_model("base.en")
t=time.time()
r=m.transcribe(WAV, language="en", fp16=False, verbose=False)
print(f"transcribed in {(time.time()-t)/60:.1f} min, {len(r['segments'])} segments")
segs=[{"text":s["text"].strip(),"start":s["start"],"duration":s["end"]-s["start"]} for s in r["segments"]]
json.dump(segs, open("transcripts/statenisland.json","w"), ensure_ascii=False, indent=1)
def mmss(t): t=int(t); return f"{t//60:02d}:{t%60:02d}"
blocks=[]; cur=[]; cs=None
for s in segs:
    if cs is None: cs=s["start"]
    cur.append(s["text"])
    if s["start"]-cs>=20: blocks.append((cs," ".join(cur))); cur=[]; cs=None
if cur: blocks.append((cs," ".join(cur)))
with open("transcripts/statenisland.txt","w") as f:
    for st,txt in blocks: f.write(f"[{mmss(st)} | t={int(st)}] {txt}\n")
print(f"wrote statenisland.txt: {len(blocks)} blocks, last t={int(segs[-1]['start'])}s")
