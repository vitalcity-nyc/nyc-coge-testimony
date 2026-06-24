import json
from youtube_transcript_api import YouTubeTranscriptApi

VID = "m_5OyXGAhIQ"
OUT_JSON = "transcripts/queens.json"
OUT_TXT  = "transcripts/queens.txt"

# Pull transcript (try new API shape, fall back to old)
try:
    api = YouTubeTranscriptApi()
    fetched = api.fetch(VID)
    segs = [{"text": s.text, "start": s.start, "duration": s.duration} for s in fetched]
except Exception:
    raw = YouTubeTranscriptApi.get_transcript(VID)
    segs = [{"text": s["text"], "start": s["start"], "duration": s.get("duration",0)} for s in raw]

json.dump(segs, open(OUT_JSON, "w"), ensure_ascii=False, indent=1)

# Aggregate into ~20s blocks, matching existing format
def mmss(t):
    t=int(t); return f"{t//60:02d}:{t%60:02d}"

blocks=[]; cur=[]; cur_start=None
for s in segs:
    if cur_start is None: cur_start=s["start"]
    cur.append(s["text"].replace("\n"," ").strip())
    if s["start"]-cur_start >= 20:
        blocks.append((cur_start, " ".join(cur)))
        cur=[]; cur_start=None
if cur:
    blocks.append((cur_start, " ".join(cur)))

with open(OUT_TXT,"w") as f:
    for st,txt in blocks:
        f.write(f"[{mmss(st)} | t={int(st)}] {txt}\n")

print(f"segments: {len(segs)}  blocks: {len(blocks)}  last t={int(segs[-1]['start'])}s ({mmss(segs[-1]['start'])})")
