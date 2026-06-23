#!/usr/bin/env python3
"""Generate index.html (Vital City styled, idea-centric) from ideas.json."""
import json

ideas = json.load(open("ideas.json"))
# safety: total proponents and unique
total_links = sum(len(i["proponents"]) for i in ideas)
uniq = set()
for i in ideas:
    for p in i["proponents"]:
        uniq.add(p["name"])
n_uniq = len(uniq)
n_ideas = len(ideas)
maxc = max(i["proponent_count"] for i in ideas)
multi = sum(1 for i in ideas if len(set(i["hearings"])) >= 2)

data_json = json.dumps(ideas, ensure_ascii=False).replace("<", "\\u003c")

HTML = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>The ideas New Yorkers brought to the efficiency commission</title>
<meta name="description" content="An idea-by-idea catalog of public testimony to New York City's 2026 Commission on Government Efficiency (COGE), drawn from the hearing record. Vital City.">
<link rel="stylesheet" href="https://use.typekit.net/qqk2vto.css">
<style>
@font-face{
  font-family:'GascogneTS';
  src:url('fonts/GascogneTS-Light.ttf') format('truetype');
  font-weight:300; font-style:normal; font-display:swap;
}
:root{
  --vc-black:#050507; --vc-white:#ffffff; --vc-cloud:#dddddd;
  --vc-chartreuse:#dde44c; --vc-orange:#ff7c53; --vc-periwinkle:#9b9fbc;
  --vc-rose:#cea9be; --vc-magenta:#e7466d; --vc-charcoal:#707175;
  --vc-indigo:#394882; --vc-cerulean:#217ebe;
  --vc-chartreuse-20:#f7f8dd; --vc-chartreuse-50:#edefa8;
  --vc-orange-20:#fde5dd;
  --sans:'halyard-text','Inter','Helvetica Neue',Arial,sans-serif;
  --serif:'GascogneTS','Source Serif 4',Georgia,'Times New Roman',serif;
}
*{box-sizing:border-box;}
html{-webkit-text-size-adjust:100%;}
body{margin:0;background:var(--vc-white);color:var(--vc-black);
  font-family:var(--sans);font-weight:300;line-height:1.5;font-size:17px;}
a{color:var(--vc-black);}
.wrap{max-width:1080px;margin:0 auto;padding:0 22px;}

/* top bar */
.topbar{border-bottom:2px solid var(--vc-black);}
.topbar .wrap{display:flex;align-items:center;justify-content:space-between;padding:14px 22px;}
.wordmark{font-family:var(--sans);font-weight:900;letter-spacing:.02em;font-size:19px;text-transform:uppercase;text-decoration:none;color:var(--vc-black);}
.topbar .tag{font-family:var(--sans);font-weight:700;font-size:11px;letter-spacing:.13em;text-transform:uppercase;color:var(--vc-charcoal);}

/* hero */
.hero .wrap{padding:38px 22px 26px;}
.kicker{font-family:var(--sans);font-weight:700;font-size:12px;letter-spacing:.15em;text-transform:uppercase;color:var(--vc-orange);margin-bottom:14px;}
h1{font-family:var(--serif);font-weight:300;font-size:clamp(30px,5.4vw,56px);line-height:1.04;margin:0 0 18px;letter-spacing:-.01em;}
.dek{font-family:var(--sans);font-weight:300;font-size:clamp(17px,2.2vw,21px);color:var(--vc-black);max-width:780px;margin:0 0 14px;line-height:1.45;}
.byline{font-family:var(--sans);font-weight:700;font-size:12px;letter-spacing:.04em;text-transform:uppercase;color:var(--vc-charcoal);}

/* verdict */
.verdict{border:2px solid var(--vc-black);border-radius:4px;padding:22px 24px;margin:8px 0 0;background:var(--vc-chartreuse-20);}
.verdict .lab{font-family:var(--sans);font-weight:700;font-size:11px;letter-spacing:.13em;text-transform:uppercase;color:var(--vc-charcoal);margin-bottom:8px;}
.verdict .head{font-family:var(--serif);font-size:clamp(20px,3vw,28px);line-height:1.18;margin:0 0 10px;}
.verdict p{font-size:15px;margin:0 0 8px;line-height:1.5;}
.verdict p:last-child{margin-bottom:0;}
.verdict .chan{font-size:13.5px;color:var(--vc-charcoal);}
.verdict a{color:var(--vc-black);text-decoration:underline;text-decoration-color:var(--vc-orange);text-decoration-thickness:2px;}

/* stats */
.stats{display:grid;grid-template-columns:repeat(4,1fr);gap:0;margin:34px 0 6px;border-top:2px solid var(--vc-black);border-bottom:2px solid var(--vc-black);}
.stat{padding:18px 16px;border-right:1px solid var(--vc-cloud);}
.stat:last-child{border-right:none;}
.stat .n{font-family:var(--serif);font-size:46px;line-height:.95;color:var(--vc-black);}
.stat .l{font-family:var(--sans);font-weight:300;font-size:13px;color:var(--vc-charcoal);margin-top:8px;line-height:1.3;}

/* section heads */
.sec-head{display:flex;align-items:baseline;justify-content:space-between;border-bottom:2px solid var(--vc-black);padding-bottom:7px;margin:46px 0 6px;}
.sec-head h2{font-family:var(--sans);font-weight:900;font-size:23px;margin:0;letter-spacing:-.01em;}
.sec-head .note{font-family:var(--sans);font-weight:700;font-size:11px;letter-spacing:.1em;text-transform:uppercase;color:var(--vc-charcoal);}
.sec-sub{font-size:14px;color:var(--vc-charcoal);margin:10px 0 18px;max-width:760px;}

/* ranked chart */
.chart{margin:6px 0 10px;}
.crow{display:grid;grid-template-columns:1fr 240px;gap:14px;align-items:center;padding:5px 0;cursor:pointer;border-radius:3px;}
.crow:hover{background:var(--vc-chartreuse-20);}
.crow .clabel{font-size:13.5px;text-align:right;line-height:1.25;}
.crow .clabel .cat{display:block;font-family:var(--sans);font-weight:700;font-size:10px;letter-spacing:.08em;text-transform:uppercase;color:var(--vc-charcoal);}
.crow .cbarwrap{display:flex;align-items:center;gap:9px;}
.crow .cbar{height:17px;background:var(--vc-chartreuse);min-width:2px;}
.crow .cval{font-family:var(--sans);font-weight:700;font-size:13px;color:var(--vc-black);}
.crow.dim{opacity:.32;}

/* controls */
.controls{margin:8px 0 6px;}
.search{width:100%;padding:13px 15px;font-size:16px;font-family:var(--sans);font-weight:300;border:2px solid var(--vc-black);border-radius:3px;background:var(--vc-white);color:var(--vc-black);}
.search:focus{outline:none;border-color:var(--vc-orange);}
.chips{display:flex;flex-wrap:wrap;gap:7px;margin-top:13px;}
.chip{font-family:var(--sans);font-weight:700;font-size:11.5px;letter-spacing:.04em;text-transform:uppercase;border:1.5px solid var(--vc-cloud);background:var(--vc-white);color:var(--vc-charcoal);padding:6px 11px;border-radius:999px;cursor:pointer;transition:all .12s;}
.chip:hover{border-color:var(--vc-black);color:var(--vc-black);}
.chip.active{background:var(--vc-black);border-color:var(--vc-black);color:var(--vc-white);}
.toolbar{display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:10px;margin:18px 0 8px;}
.count{font-family:var(--sans);font-weight:700;font-size:12px;letter-spacing:.06em;text-transform:uppercase;color:var(--vc-charcoal);}
.count b{color:var(--vc-black);}
.tools-right{display:flex;gap:14px;align-items:center;}
.sortsel{font-family:var(--sans);font-size:13px;border:1.5px solid var(--vc-cloud);border-radius:3px;padding:6px 9px;background:var(--vc-white);color:var(--vc-black);}
.reset{background:none;border:none;color:var(--vc-black);font-family:var(--sans);font-weight:700;font-size:12px;text-transform:uppercase;letter-spacing:.06em;cursor:pointer;text-decoration:underline;text-decoration-color:var(--vc-orange);text-decoration-thickness:2px;padding:0;}

/* idea cards */
.ideas{margin:14px 0 10px;}
.idea{border-bottom:1px solid var(--vc-cloud);padding:24px 0;}
.idea:first-child{border-top:2px solid var(--vc-black);}
.idea .ihead{display:grid;grid-template-columns:auto 1fr;gap:18px;align-items:start;}
.rank{font-family:var(--serif);font-size:42px;line-height:.85;color:var(--vc-cloud);min-width:54px;}
.idea h3{font-family:var(--sans);font-weight:900;font-size:21px;line-height:1.18;margin:0 0 8px;letter-spacing:-.01em;}
.idea .imeta{display:flex;flex-wrap:wrap;gap:8px 14px;align-items:center;margin-bottom:11px;}
.cat-tag{font-family:var(--sans);font-weight:700;font-size:10.5px;letter-spacing:.08em;text-transform:uppercase;color:var(--vc-orange);}
.pcount{font-family:var(--sans);font-weight:700;font-size:11px;letter-spacing:.04em;text-transform:uppercase;color:var(--vc-black);background:var(--vc-chartreuse);padding:3px 9px;border-radius:999px;}
.hreach{font-family:var(--sans);font-weight:300;font-size:12px;color:var(--vc-charcoal);}
.idea .summary{font-size:15.5px;line-height:1.5;margin:0 0 14px;}
.propbtn{font-family:var(--sans);font-weight:700;font-size:12px;letter-spacing:.05em;text-transform:uppercase;background:none;border:none;color:var(--vc-black);cursor:pointer;padding:0;display:inline-flex;align-items:center;gap:6px;}
.propbtn .arr{color:var(--vc-orange);transition:transform .15s;}
.propbtn.open .arr{transform:rotate(90deg);}
.props{margin:14px 0 0;display:none;}
.props.open{display:block;}
.prop{display:grid;grid-template-columns:1fr auto;gap:12px;padding:11px 0;border-top:1px dotted var(--vc-cloud);align-items:start;}
.prop .who{font-size:14.5px;}
.prop .who .nm{font-family:var(--sans);font-weight:700;}
.prop .who .uncertain{color:var(--vc-charcoal);font-weight:300;cursor:help;border-bottom:1px dotted var(--vc-charcoal);}
.prop .who .aff{color:var(--vc-charcoal);font-size:13px;}
.prop .who .qt{font-family:var(--serif);font-size:14.5px;color:var(--vc-black);margin-top:5px;line-height:1.4;}
.prop .watch{font-family:var(--sans);font-weight:700;font-size:11.5px;letter-spacing:.04em;text-transform:uppercase;white-space:nowrap;text-decoration:none;color:var(--vc-black);border:1.5px solid var(--vc-black);padding:5px 10px;border-radius:3px;}
.prop .watch:hover{background:var(--vc-black);color:var(--vc-white);}
.prop .watch.doc{border-color:var(--vc-cerulean);color:var(--vc-cerulean);}
.prop .watch.doc:hover{background:var(--vc-cerulean);color:var(--vc-white);}
.prop .plinks{display:flex;flex-direction:column;gap:6px;align-items:flex-end;}
.prop .watch.doc2{border-color:var(--vc-black);background:var(--vc-chartreuse);color:var(--vc-black);}
.prop .watch.doc2:hover{background:var(--vc-black);color:var(--vc-chartreuse);}
.prop .hearing-tag{font-family:var(--sans);font-weight:700;font-size:10px;letter-spacing:.06em;text-transform:uppercase;color:var(--vc-charcoal);margin-top:4px;}
.empty{text-align:center;color:var(--vc-charcoal);padding:50px 0;}

/* methodology */
.method{background:var(--vc-cloud);margin-top:42px;}
.method .wrap{padding:34px 22px 46px;}
.method h2{font-family:var(--sans);font-weight:900;font-size:22px;margin:0 0 8px;}
.method h3{font-family:var(--sans);font-weight:700;font-size:14px;letter-spacing:.04em;text-transform:uppercase;margin:22px 0 6px;}
.method p,.method li{font-size:14.5px;color:var(--vc-black);line-height:1.55;}
.method a{color:var(--vc-black);text-decoration:underline;text-decoration-color:var(--vc-orange);text-decoration-thickness:2px;}
.method ul{padding-left:20px;}

/* footer */
footer{background:var(--vc-orange);color:var(--vc-white);}
footer .wrap{padding:30px 22px;display:flex;flex-wrap:wrap;justify-content:space-between;gap:18px;align-items:center;}
footer .fm{font-family:var(--sans);font-weight:900;font-size:22px;text-transform:uppercase;letter-spacing:.02em;}
footer .fl{font-family:var(--sans);font-weight:300;font-size:13px;max-width:560px;}

/* AI caution */
.ai-btn{position:fixed;right:16px;bottom:16px;z-index:40;background:var(--vc-black);color:var(--vc-white);border:none;border-radius:999px;padding:10px 16px;font-family:var(--sans);font-weight:700;font-size:12px;letter-spacing:.05em;text-transform:uppercase;cursor:pointer;box-shadow:0 4px 14px rgba(0,0,0,.3);}
.ai-pop{position:fixed;right:16px;bottom:62px;z-index:41;width:min(390px,calc(100vw - 32px));background:var(--vc-black);color:var(--vc-white);border-radius:6px;padding:18px;box-shadow:0 10px 40px rgba(0,0,0,.4);display:none;}
.ai-pop.open{display:block;}
.ai-pop h4{font-family:var(--sans);font-weight:900;margin:0 0 8px;font-size:14px;}
.ai-pop ul{margin:0;padding-left:18px;}
.ai-pop li{font-size:12.8px;margin-bottom:7px;color:#e4e4e7;line-height:1.45;}
.ai-pop .x{position:absolute;top:8px;right:11px;background:none;border:none;color:#aaa;font-size:19px;cursor:pointer;}
.ai-pop a{color:var(--vc-chartreuse);}

@media(max-width:740px){
  .stats{grid-template-columns:repeat(2,1fr);}
  .stat:nth-child(2){border-right:none;}
  .crow{grid-template-columns:1fr 150px;}
  .idea .ihead{grid-template-columns:1fr;gap:6px;}
  .rank{font-size:30px;min-width:0;}
  .prop{grid-template-columns:1fr;}
}
</style>
</head>
<body>

<div class="topbar"><div class="wrap">
  <span class="tag">Internal working tool &middot; not for publication</span>
  <span class="tag">NYC charter revision 2026</span>
</div></div>

<header class="hero"><div class="wrap">
  <div class="kicker">Commission on Government Efficiency &middot; testimony by idea</div>
  <h1>Testimony to the Commission on Government Efficiency, by idea</h1>
  <p class="dek">A catalog of public testimony to the Commission on Government Efficiency (COGE), New York City's 2026 charter revision commission, chaired by Patrick Gaspard. Testimony is grouped by idea rather than by speaker, so proposals raised by more than one person are visible at a glance. Each backer links to their testimony &mdash; the moment in the hearing video, or a written submission where one exists.</p>
  <p class="dek" style="font-size:16px;color:var(--vc-charcoal);">Coverage so far is limited to the three first-round hearings (Manhattan, the Bronx and Brooklyn). More hearings and a written-comment period run through mid-July 2026, and this tool will be updated as that testimony comes in. COGE's proposals are due to reach voters on the November 2026 ballot.</p>
  <p class="byline">__NIDEAS__ ideas &middot; __NUNIQ__ witnesses &middot; 3 hearings so far &middot; ~9 hours reviewed</p>

  <div class="verdict">
    <div class="lab">Scope and sources</div>
    <p>COGE does not publish a consolidated record of who testified or what they asked for, and citymeetings.nyc has not transcribed the 2026 hearings. This catalog is compiled from the commission's own hearing videos plus written submissions that testifiers or their organizations have published. Names and quotes are drawn from auto-generated captions and checked against public records where possible; treat them as provisional.</p>
    <p class="chan">Official channels: schedule and livestreams at <a href="https://www.nyc.gov/site/charter/meetings/public-meetings-hearings.page" target="_blank" rel="noopener">nyc.gov/site/charter</a> &middot; submit testimony via the <a href="https://tinyurl.com/COGE2026comments" target="_blank" rel="noopener">comment form</a> or <a href="mailto:CharterTestimony@citycharter.nyc.gov">CharterTestimony@citycharter.nyc.gov</a></p>
  </div>

  <div class="stats">
    <div class="stat"><div class="n">__NIDEAS__</div><div class="l">distinct ideas proposed</div></div>
    <div class="stat"><div class="n">__NUNIQ__</div><div class="l">witnesses across three hearings so far</div></div>
    <div class="stat"><div class="n">__MULTI__</div><div class="l">ideas raised at more than one borough hearing</div></div>
    <div class="stat"><div class="n">12</div><div class="l">backers for the most popular idea, open primaries</div></div>
  </div>
</div></header>

<main class="wrap">

  <div class="sec-head"><h2>The shared threads</h2><span class="note">Ideas ranked by how many people backed them</span></div>
  <p class="sec-sub">Every idea raised at the hearings, ordered by the number of distinct people who argued for it. Click any bar to jump to the detail.</p>
  <div class="chart" id="chart"></div>

  <div class="sec-head"><h2>Every idea, with who backed it</h2><span class="note" id="topcount"></span></div>
  <div class="controls">
    <input type="text" class="search" id="search" placeholder="Search ideas, people or organizations...">
    <div class="chips" id="catChips"></div>
    <div class="toolbar">
      <div class="count" id="count"></div>
      <div class="tools-right">
        <select class="sortsel" id="sort">
          <option value="count">Sort: most backers first</option>
          <option value="title">Sort: A&ndash;Z</option>
          <option value="category">Sort: by category</option>
        </select>
        <button class="reset" id="reset">Clear</button>
      </div>
    </div>
  </div>

  <div class="ideas" id="ideas"></div>
  <div class="empty" id="empty" style="display:none;">No ideas match these filters.</div>
</main>

<section class="method"><div class="wrap">
  <h2>How this was built</h2>
  <p>This is an idea-centric reading of the public record so far, not an official transcript. The auto-generated captions from COGE's first-round hearing videos (Manhattan, June 9; Bronx, June 10; Brooklyn, June 11) were used to identify each public witness and the concrete proposals they made, then those proposals were clustered into shared ideas. Where a witness or their organization has published their full written testimony or a closely related position, the entry links to it. Two documented written submissions &mdash; from Comptroller Mark Levine and Council Member Phil Wong &mdash; are folded in and labeled. Commissioners, staff and procedural talk are excluded. Further hearings and a written-comment period run through mid-July 2026, and this tool is intended to be updated as that testimony comes in.</p>

  <h3>Why some names look approximate</h3>
  <p>The hearings have no published speaker list, so names came from the auto-captions, which routinely garble them &mdash; especially for the many immigrant and community witnesses in the Bronx. Each name was checked against public records (organization staff pages, news coverage, official rosters) and many were corrected. Names that could not be confirmed are marked with a dotted underline; hover for a note. Treat any flagged spelling as provisional and confirm against the video before quoting by name.</p>

  <h3>COGE only</h3>
  <p>This covers the 2026 Commission on Government Efficiency only. New York City has had four charter commissions in roughly two years, and a lot of widely cited "charter testimony" actually belongs to the 2024 and 2025 commissions. Those were deliberately left out.</p>

  <h3>Who isn't here</h3>
  <p>Some major interests are shaping COGE from inside rather than through testimony: DC 37's Henry Garrido and the Partnership for New York City's Kathryn Wylde sit on the commission itself. A fourth and fifth round of hearings and written comments run into mid-July 2026, so this is a snapshot, not the final word.</p>

  <h3>Sources</h3>
  <ul>
    <li><a href="https://www.youtube.com/watch?v=n6F-Of84tR4" target="_blank" rel="noopener">COGE Round 1 &mdash; Manhattan hearing (full video)</a></li>
    <li><a href="https://www.youtube.com/watch?v=BT7z3EaKSUM" target="_blank" rel="noopener">COGE Round 1 &mdash; Bronx hearing (full video)</a></li>
    <li><a href="https://www.youtube.com/watch?v=lzsMs6xsxY4" target="_blank" rel="noopener">COGE Round 1 &mdash; Brooklyn hearing (full video)</a></li>
    <li><a href="https://comptroller.nyc.gov/newsroom/testimonies/testimony-of-new-york-city-comptroller-mark-levine-before-the-charter-revision-commission-on-government-efficiency-coge/" target="_blank" rel="noopener">Comptroller Mark Levine &mdash; written testimony</a></li>
    <li><a href="https://qns.com/2026/06/cm-wong-nyc-commission-district-30/" target="_blank" rel="noopener">Council Member Phil Wong &mdash; written testimony (QNS)</a></li>
  </ul>
</div></section>

<footer><div class="wrap">
  <span class="fl">Internal working tool. An idea-by-idea catalog of public testimony to New York City's 2026 Commission on Government Efficiency (COGE). Covers the first-round hearings through June 23, 2026; updated as further hearings and written comments come in through mid-July.</span>
</div></footer>

<button class="ai-btn" id="aiBtn">AI caution</button>
<div class="ai-pop" id="aiPop" role="dialog" aria-label="AI caution">
  <button class="x" id="aiX" aria-label="Close">&times;</button>
  <h4>About this catalog &mdash; read before relying on it</h4>
  <ul>
    <li>Built with AI-assisted transcription and clustering of COGE's hearing videos on June 23, 2026. It is a research tool, not the official record.</li>
    <li>Speaker names come from auto-captions and are often misspelled; they were checked against public records and many corrected, but ones still unconfirmed are flagged with a dotted underline. Confirm names and quotes against the linked video before publishing.</li>
    <li>Coverage is the three first-round hearings only; more hearings and written comments run through mid-July 2026 and are not yet included.</li>
    <li>Grouping testimony into "ideas" involves judgment; a backer placed under an idea may have framed it differently. Watch the clip for full context.</li>
    <li>Quotes are transcribed from auto-captions and lightly cleaned; they may not be word-perfect.</li>
    <li>COGE (2026) was separated from the 2024 and 2025 charter commissions; their testimony was excluded.</li>
    <li>A snapshot: later hearings and written comments into mid-July 2026 are not yet captured.</li>
  </ul>
</div>

<script id="data" type="application/json">__DATA__</script>
<script>
const IDEAS = JSON.parse(document.getElementById('data').textContent);
const MAXC = Math.max.apply(null, IDEAS.map(i=>i.proponent_count));
const cats = [...new Set(IDEAS.map(i=>i.category))].sort();
const state = {q:"", cat:new Set(), sort:"count"};

const hearingColor = {Manhattan:"var(--vc-cerulean)",Bronx:"var(--vc-magenta)",Brooklyn:"var(--vc-indigo)","Written submission":"var(--vc-charcoal)"};

function esc(s){return (s||"").replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;");}

// ranked chart (always full set, ordered by count)
function renderChart(){
  const rows = IDEAS.slice().sort((a,b)=>b.proponent_count-a.proponent_count);
  document.getElementById('chart').innerHTML = rows.map(i=>{
    const w = Math.max(2, i.proponent_count/MAXC*100);
    return `<div class="crow" data-id="${i.id}">
      <div class="clabel"><span class="cat">${esc(i.category)}</span>${esc(i.title)}</div>
      <div class="cbarwrap"><div class="cbar" style="width:${w}%"></div><span class="cval">${i.proponent_count}</span></div>
    </div>`;
  }).join("");
  document.querySelectorAll('.crow').forEach(r=>{
    r.addEventListener('click',()=>{
      const el=document.querySelector(`.idea[data-id="${r.dataset.id}"]`);
      if(el){
        // ensure visible: clear filters if hidden
        if(el.style.display==='none'){document.getElementById('reset').click();}
        el.scrollIntoView({behavior:'smooth',block:'center'});
        el.querySelector('.props').classList.add('open');
        el.querySelector('.propbtn').classList.add('open');
        el.style.transition='background .2s';el.style.background='var(--vc-chartreuse-20)';
        setTimeout(()=>el.style.background='',1200);
      }
    });
  });
}

function buildChips(){
  document.getElementById('catChips').innerHTML = cats.map(c=>
    `<span class="chip" data-val="${esc(c)}">${esc(c)}</span>`).join("");
  document.querySelectorAll('#catChips .chip').forEach(ch=>{
    ch.addEventListener('click',()=>{
      const v=ch.dataset.val;
      if(state.cat.has(v)){state.cat.delete(v);ch.classList.remove('active');}
      else{state.cat.add(v);ch.classList.add('active');}
      render();
    });
  });
}

function matches(i){
  if(state.cat.size && !state.cat.has(i.category)) return false;
  if(state.q){
    const hay=(i.title+" "+i.summary+" "+i.category+" "+i.proponents.map(p=>p.name+" "+p.affiliation).join(" ")).toLowerCase();
    if(!hay.includes(state.q.toLowerCase())) return false;
  }
  return true;
}
function sortRows(rows){
  const r=rows.slice();
  if(state.sort==="title") r.sort((a,b)=>a.title.localeCompare(b.title));
  else if(state.sort==="category") r.sort((a,b)=>a.category.localeCompare(b.category)||b.proponent_count-a.proponent_count);
  else r.sort((a,b)=>b.proponent_count-a.proponent_count);
  return r;
}

function propRow(p){
  const isDoc = p.hearing==="Written submission";
  const watchLabel = isDoc ? "Read &rarr;" : "Watch &#9654;";
  const nm = p.name_confidence==="low" || p.name_confidence==="medium"
    ? `<span class="uncertain" title="Name transcribed from auto-captions &mdash; may be misspelled. Confirm against the video.">${esc(p.name)}</span>`
    : esc(p.name);
  const aff = p.affiliation && p.affiliation!=="Unknown" ? ` &middot; <span class="aff">${esc(p.affiliation)}</span>` : "";
  const qt = p.quote ? `<div class="qt">&ldquo;${esc(p.quote)}&rdquo;</div>` : "";
  const primary = `<a class="watch ${isDoc?'doc':''}" href="${esc(p.url)}" target="_blank" rel="noopener">${watchLabel}</a>`;
  const doclink = p.doc_url ? `<a class="watch doc2" href="${esc(p.doc_url)}" target="_blank" rel="noopener">${esc(p.doc_label||'Testimony')} &#8599;</a>` : "";
  return `<div class="prop">
    <div class="who"><span class="nm">${nm}</span>${aff}
      <div class="hearing-tag" style="color:${hearingColor[p.hearing]||'var(--vc-charcoal)'}">${esc(p.hearing)}</div>
      ${qt}
    </div>
    <div class="plinks">${primary}${doclink}</div>
  </div>`;
}

function card(i, idx){
  const reach = i.hearings.join(" &middot; ");
  const plabel = i.proponent_count===1 ? "1 backer" : i.proponent_count+" backers";
  return `<article class="idea" data-id="${i.id}">
    <div class="ihead">
      <div class="rank">${String(idx+1).padStart(2,'0')}</div>
      <div>
        <h3>${esc(i.title)}</h3>
        <div class="imeta">
          <span class="cat-tag">${esc(i.category)}</span>
          <span class="pcount">${plabel}</span>
          <span class="hreach">${reach}</span>
        </div>
        <p class="summary">${esc(i.summary)}</p>
        <button class="propbtn"><span class="arr">&#9654;</span> Who backed it (${i.proponent_count})</button>
        <div class="props">${i.proponents.map(propRow).join("")}</div>
      </div>
    </div>
  </article>`;
}

function render(){
  const rows=sortRows(IDEAS.filter(matches));
  const c=document.getElementById('ideas');
  c.innerHTML=rows.map(card).join("");
  document.getElementById('empty').style.display=rows.length?'none':'block';
  document.getElementById('count').innerHTML=`Showing <b>${rows.length}</b> of ${IDEAS.length} ideas`;
  c.querySelectorAll('.propbtn').forEach(b=>{
    b.addEventListener('click',()=>{
      b.classList.toggle('open');
      b.nextElementSibling.classList.toggle('open');
    });
  });
}

document.getElementById('search').addEventListener('input',e=>{state.q=e.target.value;render();});
document.getElementById('sort').addEventListener('change',e=>{state.sort=e.target.value;render();});
document.getElementById('reset').addEventListener('click',()=>{
  state.q="";state.cat.clear();state.sort="count";
  document.getElementById('search').value="";
  document.getElementById('sort').value="count";
  document.querySelectorAll('#catChips .chip.active').forEach(c=>c.classList.remove('active'));
  render();
});
document.getElementById('topcount').textContent = cats.length+" categories";

const aiBtn=document.getElementById('aiBtn'),aiPop=document.getElementById('aiPop');
aiBtn.addEventListener('click',()=>aiPop.classList.toggle('open'));
document.getElementById('aiX').addEventListener('click',()=>aiPop.classList.remove('open'));

renderChart();
buildChips();
render();
</script>
</body>
</html>
"""

HTML = (HTML
        .replace("__DATA__", data_json)
        .replace("__NIDEAS__", str(n_ideas))
        .replace("__NUNIQ__", str(n_uniq))
        .replace("__MULTI__", str(multi)))

open("index.html", "w").write(HTML)
print(f"Built index.html  ideas={n_ideas} unique_proponents={n_uniq} multi={multi} links={total_links} maxc={maxc}")
