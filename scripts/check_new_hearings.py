#!/usr/bin/env python3
"""Watch the COGE YouTube channel for new hearing videos.
If new videos appear vs. scripts/known_videos.json, send an iMessage to Josh
and record them in scripts/new_hearings_pending.json so the catalog can be refreshed.
Runs daily via launchd. Detection-only: it does not rebuild the site (clustering
needs the Claude pipeline), it just flags that there is new testimony to ingest.
"""
import json, os, subprocess, sys, datetime

HERE = os.path.dirname(os.path.abspath(__file__))
CHANNEL = "https://www.youtube.com/@NYCCOGE2026/videos"
KNOWN = os.path.join(HERE, "known_videos.json")
PENDING = os.path.join(HERE, "new_hearings_pending.json")
LOG = os.path.join(HERE, "watcher.log")
PHONE = "9175823254"


def log(msg):
    ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG, "a") as f:
        f.write(f"[{ts}] {msg}\n")


def list_channel():
    """Return list of {id,title} for the channel, via yt-dlp."""
    out = subprocess.run(
        [sys.executable, "-m", "yt_dlp", "--flat-playlist",
         "--print", "%(id)s\t%(title)s", CHANNEL],
        capture_output=True, text=True, timeout=180)
    if out.returncode != 0:
        log(f"yt-dlp error: {out.stderr.strip()[:300]}")
        return None
    vids = []
    for line in out.stdout.strip().splitlines():
        if "\t" in line:
            vid, title = line.split("\t", 1)
            vids.append({"id": vid.strip(), "title": title.strip()})
    return vids


def send_imessage(text):
    """Best-effort iMessage to Josh. Logs failure rather than raising."""
    script = (
        'tell application "Messages"\n'
        '  set svc to 1st service whose service type = iMessage\n'
        f'  send "{text}" to participant "{PHONE}" of svc\n'
        'end tell'
    )
    try:
        r = subprocess.run(["osascript", "-e", script],
                           capture_output=True, text=True, timeout=30)
        if r.returncode != 0:
            log(f"iMessage send failed: {r.stderr.strip()[:200]}")
            return False
        return True
    except Exception as e:
        log(f"iMessage exception: {e}")
        return False


def main():
    known = json.load(open(KNOWN)) if os.path.exists(KNOWN) else []
    known_ids = {v["id"] for v in known}
    current = list_channel()
    if current is None:
        log("Could not list channel; skipping this run.")
        return
    new = [v for v in current if v["id"] not in known_ids]
    if not new:
        log(f"No new videos ({len(current)} total).")
        return

    titles = "; ".join(v["title"] for v in new)
    log(f"NEW: {titles}")
    msg = (f"COGE watcher: {len(new)} new hearing video(s) posted - {titles}. "
           f"Ask Claude to refresh the COGE testimony tool.")
    send_imessage(msg)

    # record pending so a refresh run can pick them up, and update known list
    pending = json.load(open(PENDING)) if os.path.exists(PENDING) else []
    pending.extend(new)
    json.dump(pending, open(PENDING, "w"), indent=1)
    json.dump(current, open(KNOWN, "w"), indent=1)


if __name__ == "__main__":
    main()
