# COGE Testimony Catalog — Handoff

_Last updated: 2026-07-14_

## What this is

An idea-by-idea catalog of public testimony to **COGE** — the NYC **Commission on Government Efficiency**, Mayor Mamdani's 2026 charter revision commission (chair Patrick Gaspard), whose proposals go to voters on the **November 2026 ballot**. Testimony is grouped by **idea** (not by speaker) so proposals raised by many people are visible at a glance. Each backer links to the exact moment in the hearing video, or to a published written submission.

- **Live:** https://vitalcity-nyc.github.io/nyc-coge-testimony/
- **Repo:** github.com/vitalcity-nyc/nyc-coge-testimony (the **vitalcity-nyc** GitHub account)
- **Local:** `/Users/joshgreenman/Experiments/nyc-coge-testimony/`
- **Companion NotebookLM** (public): https://notebooklm.google.com/notebook/265ada6f-453b-4f9e-8b3b-47718a5ff86d — linked from the "Ask the testimony a question" button.

## Current state (2026-07-14)

- **90 ideas / 247 witnesses across 10 hearings.** Both rounds of borough hearings are **complete**: Round 1 (Manhattan, Bronx, Brooklyn, Queens, Staten Island) and Round 2 (same five boroughs).
- Remaining COGE activity: a **written-comment period into mid-July 2026**, then the commission drafts ballot proposals.

## Architecture — the one rule

**`index.html` is GENERATED. Never hand-edit it.** Edit `ideas.json` (data) or `build.py` (template + all CSS/JS), then run `python3 build.py` to regenerate `index.html`. `build.py` inlines `ideas.json` into a `<script id="data">` tag and fills placeholders `__NIDEAS__ __NUNIQ__ __MULTI__ __MAXC__`.

The page is a single static HTML file (Vital City styled: Gascogne serif + Halyard sans, chartreuse/orange). Client-side JS provides: the by-idea/by-person toggle, theme grouping (18 fine categories rolled into ~8 collapsible themes), a role-type filter, search, a ranked "shared threads" chart (top 12 + show-all), shareable deep-links (`#idea-<id>` / `#person-<slug>`), and an AI-caution disclaimer.

### `ideas.json` schema
```
[ { "id": "kebab-case",
    "title": "...", "category": "<one of ~18 fine categories>",
    "summary": "2-4 sentences",
    "proponent_count": <int = distinct names>,
    "hearings": ["Manhattan", "Bronx (Round 2)", ...],
    "proponents": [
      { "name": "...", "name_confidence": "high|medium|low",
        "affiliation": "...", "role_type": "Advocacy org|Labor|Business/industry|Nonprofit|Resident|Government body|Elected official|Academic|Civic-tech",
        "hearing": "Manhattan (Round 2)",
        "url": "https://www.youtube.com/watch?v=<id>&t=<sec>s",   // video deep-link (or a doc URL for Written submission)
        "quote": "...",
        "doc_url": "...", "doc_label": "Full testimony"           // optional: published written testimony
      } ] } ]
```
Themes are derived from `category` at render time via `THEME_MAP` in `build.py` (not stored in the data).

## The ingest pipeline (per new hearing)

Templates: `scripts/transcribe_queens.py`, `scripts/transcribe_statenisland.py`. Worked example commands live in the scheduled task (below).

1. **Detect** new hearing videos: `python3 -m yt_dlp --flat-playlist --no-warnings --print "%(id)s | %(title)s" https://www.youtube.com/@NYCCOGE2026/videos`. Decide what's new by comparing against the **hearing labels already in ideas.json** (NOT just `scripts/known_videos.json` — see gotchas). The "Initial Meeting" video `L-ZQiG9jCtk` is procedural — never ingest it.
2. **Transcript.** Try YouTube auto-captions first: `youtube_transcript_api` (fast, no download). They usually appear a day or two after upload. If absent, download audio (`yt-dlp -f 18 --extractor-args "youtube:player_client=android"`), extract 16k mono wav with `ffmpeg` (`~/.local/bin/ffmpeg`), transcribe with **OpenAI Whisper `base.en`** (`import whisper`; ~28x realtime locally). Write `transcripts/<slug>.txt` in `[MM:SS | t=SECONDS]` ~20-second blocks.
3. **Extract speakers** (subagent) → `transcripts/<slug>_speakers.json`. **Exclude** commissioners/staff AND city agency officials giving invited "expert testimony" (e.g. a DOT/DCAS/FDNY deputy commissioner) — the catalog is public/stakeholder testimony only.
4. **Cluster** each proposal into the existing taxonomy (subagent reads `ideas.json`). Prefer existing ideas; create new only for genuinely new themes, reusing an existing `category`.
5. **Merge** deterministically with a small Python script: back up `ideas.json` first (`ideas.backup-<slug>.json`); append each proponent with `hearing=<label>` and `url=watch?v=<id>&t=<t>s`; **dedup by name-per-idea** (a person already on an idea is skipped — this correctly handles repeat testifiers like Frank Morano and written-then-in-person like Comptroller Levine); append new ideas; recompute `proponent_count` = distinct names; re-sort by count desc. Guard: an assignment may reference an idea both as `new` (with a def) and `existing` (by id) across witnesses — resolve against `existing ∪ created`.
6. **Colors & copy** in `build.py`: add the new label to the `hearingColor` JS map (reuse the borough's color); bump the hardcoded hearing count / "~N hours" / round language. Idea/witness counts are dynamic.
7. **Build + deploy:** `python3 build.py`, commit, `git push`, then **verify the deploy actually went live** (see Pages gotchas).

## Name verification / cleanup

Whisper and YouTube captions garble names. Two sources fix them:
- **Official minutes** (authoritative rosters). COGE posts them per hearing, days-to-weeks later, under `nyc.gov/assets/charter/downloads/pdf/2026/` or `/meetings-hearings/`. Round 1 minutes are **scanned images** (read with the Read tool, which renders PDFs visually); Round 2 minutes have been **text-based** (extract with `pypdf`). Correct only low/medium names; **never overwrite an independently-verified name**, and the minutes outrank a web guess.
- **Public-records web search** (subagent per name) for hearings whose minutes aren't posted yet. See `scripts/name_cleanup_workflow.js` / `si_verify_workflow.js` / `queens_verify_workflow.js` for the pattern. Results saved to `transcripts/*_name_corrections.json`.

Unconfirmed names keep `name_confidence` low/medium and render with a **dotted underline** in the UI. Genuine residents with no public footprint stay flagged — never invent an identity.

## Deployment gotchas (important)

- **GitHub Pages needs `.nojekyll`** in the repo root, or the build fails silently ("Page build failed") and the live site freezes while the repo has new content. It's committed; keep it.
- **Pages builds stall.** After pushing, check `gh api repos/vitalcity-nyc/nyc-coge-testimony/pages/builds/latest`. If `status` is `errored`, or `building` with a frozen `updated_at`, force a fresh build: `gh api -X POST repos/vitalcity-nyc/nyc-coge-testimony/pages/builds`. **Do not trust a push — always poll the live URL until it shows the new content.**
- **GitHub account flips.** The active `gh` account can silently switch to `joshgreenman1973`, causing a **403** to this repo. Always run `gh auth switch --user vitalcity-nyc && gh auth setup-git` before pushing.

## Automation

- **Scheduled task `coge-testimony-watch`** (`~/.claude/scheduled-tasks/coge-testimony-watch/SKILL.md`) runs daily ~10am **while the Claude app is open** (else on next launch). It does the whole loop: detect new videos, ingest, reconcile minutes, verify the deploy, and iMessage Josh (**9175823254**) only when something changed. To edit it, edit that SKILL.md or use the scheduled-tasks tools.
- **The old launchd watcher (`com.josh.coge-watcher`) is DISABLED** and must stay disabled. It wrote new video IDs into `known_videos.json` before the ingest task ran, so the task saw them as "known" and skipped them (this is why SI R2 + Manhattan R2 were silently missed once). If it ever reappears: `launchctl bootout gui/$(id -u)/com.josh.coge-watcher`.
- **NotebookLM sync is manual.** Google gives no API to add sources, so Josh adds each hearing to the notebook **as a YouTube link** by hand. On every ingest, the task's iMessage includes an explicit "Add to NotebookLM: https://www.youtube.com/watch?v=<id>" line. (You can read the notebook's current sources via the claude-in-chrome browser MCP if you need to check what's in it — Josh is logged in.)

## Editorial rules (from Josh)

- **COGE 2026 only.** Exclude the 2024 and 2025 charter revision commissions — the official `nyc.gov/site/charter` URL is reused across commissions, and `citymeetings.nyc` 2025 transcripts are a common trap.
- **Witnesses = members of the public.** Exclude commissioners, staff, and agency officials giving expert testimony.
- **Never fabricate** a name, timestamp, quote, or source.
- **De-branded, matter-of-fact.** No "Vital City" wordmark (this project is an exception to the usual VC branding). AP style, sentence case, no serial comma. Every project gets the AI-caution disclaimer (present).

## Other gotchas

- **Borough↔date on the official hearing pages is cross-wired** for some Round 2 dates (page `06302026` shows the Brooklyn video/minutes; `07012026` shows the Bronx). Trust the **YouTube video title + the minutes header** for the borough, not the page date.
- **YouTube caches the channel** server-side. A fresh `yt-dlp`/curl can lag behind what a logged-in browser shows — if a video "should" be there, verify via the claude-in-chrome browser MCP.
- **Workflow `args` arrive stringified**, so verify/ingest workflows embed their worklist as a `const` in the script rather than relying on `args` (see the `scripts/*_workflow.js` files).

## Key files

| Path | What |
|---|---|
| `build.py` | Generator: template + all CSS/JS. Edit this, then run it. |
| `ideas.json` | The data. |
| `index.html` | Generated output — do not hand-edit. |
| `.nojekyll` | Required for Pages. |
| `transcripts/<slug>.txt` / `.json` | Per-hearing block transcripts + raw segments. |
| `transcripts/<slug>_speakers.json` | Extracted witnesses. |
| `transcripts/minutes_reconciled.json` | Which hearings have been reconciled against official minutes. |
| `scripts/transcribe_*.py` | Whisper transcription templates. |
| `scripts/*_workflow.js` | Name-verification / ingest workflow scripts. |
| `scripts/known_videos.json` | Video list (do not treat as the source of truth for "ingested"). |
| `ideas.backup-*.json` | Pre-merge backups (untracked). |
| `HANDOFF.md` | This file. |

Full running context is also in the memory note `project_coge_testimony_tracker.md`.

## What's outstanding

- **Written-comment period** (into mid-July): COGE takes written submissions via a form / `CharterTestimony@citycharter.nyc.gov`. It publishes no archive of them, so these surface only if a witness/org posts their submission — the periodic written-testimony search sweep (see `scripts/doc_search3_workflow.js`) is how those get found and linked.
- **Minutes still to reconcile:** Staten Island R2 and Manhattan R2 minutes weren't posted as of 2026-07-14; when they appear, reconcile those two hearings' names (many are still provisional). Same for Queens R2 minutes.
- Otherwise the catalog is current with every hearing COGE has posted.
