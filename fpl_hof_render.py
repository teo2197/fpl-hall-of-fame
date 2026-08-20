"""HTML rendering for fpl_hof.py — template (CSS/JS) is a verbatim copy of
the last known-good generated site; only the Python building the dynamic
sections and the embedded data blob is new."""
import json

from fpl_hof import accent_for

HEAD = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>FPL Classics — Hall of Fame</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@400;600;700;800;900&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
<style>
:root{
  --bg:#08090f;--bg2:#0d0f1a;--card:#111420;--border:#1e2535;
  --text:#e8ecf5;--dim:#5a6a85;--green:#00ff87;--teal:#04f5ff;
  --gold:#ffd700;--silver:#c0c0c0;--red:#ef4444;
}
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:'Inter',system-ui,sans-serif;background:var(--bg);color:var(--text);min-height:100vh}

/* ── HERO ── */
.hero{position:relative;padding:70px 40px 60px;text-align:center;overflow:hidden;
  background:radial-gradient(ellipse 80% 60% at 50% -10%,rgba(255,215,0,0.12) 0%,transparent 70%),
    radial-gradient(ellipse 60% 40% at 10% 100%,rgba(0,255,135,0.06) 0%,transparent 60%),
    radial-gradient(ellipse 60% 40% at 90% 100%,rgba(4,245,255,0.06) 0%,transparent 60%),#08090f}
.hero::before{content:'';position:absolute;inset:0;
  background-image:radial-gradient(rgba(255,255,255,0.03) 1px,transparent 1px);
  background-size:32px 32px;pointer-events:none}
.hero-eyebrow{font-family:'Barlow Condensed',sans-serif;font-size:.8rem;letter-spacing:4px;text-transform:uppercase;color:var(--dim);margin-bottom:16px}
.hero-title{font-family:'Barlow Condensed',sans-serif;font-size:clamp(3rem,8vw,6.5rem);font-weight:900;line-height:.9;letter-spacing:-2px;text-transform:uppercase;
  background:linear-gradient(135deg,#ffd700 0%,#fffde1 40%,#ffd700 60%,#b8860b 100%);
  -webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;
  filter:drop-shadow(0 0 30px rgba(255,215,0,.3))}
.hero-sub{font-family:'Barlow Condensed',sans-serif;font-size:clamp(1.2rem,3vw,2rem);font-weight:600;letter-spacing:3px;text-transform:uppercase;color:rgba(255,255,255,.5);margin-top:8px}
.hero-badges{display:flex;gap:12px;justify-content:center;margin-top:28px;flex-wrap:wrap}
.hero-badge{background:rgba(255,255,255,.06);border:1px solid rgba(255,255,255,.12);border-radius:20px;padding:6px 16px;font-size:.72rem;letter-spacing:2px;text-transform:uppercase;color:rgba(255,255,255,.5)}
.hero-badge span{color:var(--green)}

/* ── LAYOUT ── */
.section{max-width:1280px;margin:0 auto;padding:60px 32px 0}
.sec-label{font-family:'Barlow Condensed',sans-serif;font-size:.72rem;letter-spacing:4px;text-transform:uppercase;color:var(--dim);margin-bottom:20px;display:flex;align-items:center;gap:12px}
.sec-label::before{content:'';width:40px;height:1px;background:var(--border)}
.sec-label::after{content:'';flex:1;height:1px;background:var(--border)}

/* ── CARDS ── */
.card{background:var(--card);border:1px solid var(--border);border-radius:14px;overflow:hidden}

/* ── CLICKABLE NAMES ── */
.plink{cursor:pointer;transition:color .15s}
.plink:hover{color:var(--green);text-decoration:underline;text-underline-offset:3px}

/* ── SEASON CARDS ── */
.sc-grid{display:grid;grid-template-columns:repeat(5,1fr);gap:16px}
@media(max-width:1100px){.sc-grid{grid-template-columns:repeat(3,1fr)}}
@media(max-width:700px){.sc-grid{grid-template-columns:1fr 1fr}}
@media(max-width:480px){.sc-grid{grid-template-columns:1fr}}
.sc{background:var(--card);border:1px solid var(--border);border-radius:14px;overflow:hidden;transition:transform .2s,box-shadow .2s;display:flex;flex-direction:column}
.sc:hover{transform:translateY(-3px);box-shadow:0 8px 32px rgba(0,0,0,.4)}
.sc-top{display:flex;align-items:center;justify-content:space-between;padding:10px 14px}
.sc-year{font-family:'Barlow Condensed',sans-serif;font-size:1rem;font-weight:800;letter-spacing:1px}
.sc-new{font-size:.6rem;letter-spacing:2px;text-transform:uppercase;background:var(--gold);color:#000;border-radius:4px;padding:2px 7px;font-weight:700}
.sc-body{padding:16px 16px 12px;flex:1;text-align:center}
.sc-trophy{font-size:2rem;margin-bottom:8px}
.sc-wname{font-family:'Barlow Condensed',sans-serif;font-size:1.4rem;font-weight:800;letter-spacing:.5px;line-height:1.1}
.sc-winfo{display:flex;align-items:center;justify-content:center;gap:8px;margin-top:8px;flex-wrap:wrap}
.sc-pts{font-size:.78rem;color:var(--dim)}
.sc-rank-pill{font-size:.72rem;font-weight:600;border-radius:20px;padding:2px 9px;font-family:'Barlow Condensed',sans-serif;letter-spacing:.5px}
.sc-footer{background:rgba(0,0,0,.25);border-top:1px solid var(--border);padding:10px 14px;display:flex;align-items:center;gap:8px;font-size:.82rem}
.sc-rname{flex:1;color:rgba(255,255,255,.7)}
.sc-rrank{color:var(--dim);font-size:.75rem;font-family:monospace}

/* ── AWARD CARDS ── */
.awards-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:16px}
@media(max-width:900px){.awards-grid{grid-template-columns:1fr 1fr}}
@media(max-width:480px){.awards-grid{grid-template-columns:1fr}}
.award-card{background:var(--card);border:1px solid var(--border);border-bottom:3px solid var(--ac);border-radius:14px;padding:28px 20px 24px;text-align:center;position:relative;overflow:hidden;transition:transform .2s}
.award-card::before{content:'';position:absolute;inset:0;background:radial-gradient(ellipse 80% 50% at 50% 100%,color-mix(in srgb,var(--ac) 8%,transparent) 0%,transparent 60%);pointer-events:none}
.award-card:hover{transform:translateY(-3px)}
.award-emoji{font-size:2.4rem;margin-bottom:12px;display:block}
.award-title{font-size:.65rem;letter-spacing:3px;text-transform:uppercase;color:var(--dim);margin-bottom:10px}
.award-name{font-family:'Barlow Condensed',sans-serif;font-size:1.3rem;font-weight:700;letter-spacing:.5px;color:var(--text);margin-bottom:6px;line-height:1.1}
.award-stat{font-family:'Barlow Condensed',sans-serif;font-size:2.8rem;font-weight:900;letter-spacing:-1px;line-height:1;margin-bottom:10px}
.award-detail{font-size:.72rem;color:var(--dim);line-height:1.4}

/* ── TABLES ── */
.big-table{width:100%;border-collapse:collapse;font-size:.88rem}
.big-table th{padding:11px 16px;text-align:left;font-size:.65rem;text-transform:uppercase;letter-spacing:2px;color:var(--dim);border-bottom:1px solid var(--border);background:rgba(255,255,255,.02)}
.big-table td{padding:12px 16px;border-bottom:1px solid rgba(30,37,53,.8)}
.big-table tbody tr:last-child td{border-bottom:none}
.big-table tbody tr:hover td{background:rgba(255,255,255,.02)}
.tnum{text-align:right;font-family:monospace;font-variant-numeric:tabular-nums}
.tname{font-weight:600}.tc{font-size:1.1rem;letter-spacing:2px}
.dim{color:var(--dim)}.green{color:var(--green)}.teal{color:var(--teal)}.red{color:var(--red)}.rank-good{color:var(--green)}.rank-num{color:var(--dim)}
.hof-table-wrap{overflow-x:auto}
.hof-table{width:100%;border-collapse:collapse;font-size:.9rem;min-width:700px}
.hof-table th{padding:12px 18px;text-align:left;font-size:.65rem;text-transform:uppercase;letter-spacing:2px;color:var(--dim);border-bottom:1px solid var(--border);background:rgba(255,255,255,.02)}
.hof-table td{padding:14px 18px;border-bottom:1px solid rgba(30,37,53,.6)}
.hof-table tbody tr:last-child td{border-bottom:none}
.hof-table tbody tr:hover td{background:rgba(255,255,255,.02)}
.season-tag{font-family:'Barlow Condensed',sans-serif;font-size:1rem;font-weight:700;letter-spacing:1px}
.winner-cell{font-family:'Barlow Condensed',sans-serif;font-size:1.05rem;font-weight:700}
.rank-cell{font-family:monospace;text-align:right;color:var(--dim);font-size:.82rem}
.pts-cell{font-family:monospace;text-align:right;font-size:.85rem}
.gold-text{color:var(--gold)}.silver-text{color:var(--silver)}

/* ── HONOUR ROWS ── */
.grid-2{display:grid;grid-template-columns:1fr 1fr;gap:24px}
@media(max-width:700px){.grid-2{grid-template-columns:1fr}}
.honour-row{display:flex;align-items:center;gap:12px;padding:14px 18px;border-bottom:1px solid rgba(30,37,53,.5);flex-wrap:wrap}
.honour-row:last-child{border-bottom:none}
.honour-name{font-weight:600;min-width:160px}
.honour-count{color:var(--green);font-size:.85rem;min-width:90px}
.badges{display:flex;gap:6px;flex-wrap:wrap}
.badge{background:rgba(167,139,250,.15);border:1px solid rgba(167,139,250,.35);color:#a78bfa;border-radius:6px;padding:2px 8px;font-size:.72rem;font-weight:600}
.silver-badge{background:rgba(192,192,192,.12);border-color:rgba(192,192,192,.3);color:var(--silver)}
.left-badge{background:rgba(255,77,77,.15);border:1px solid rgba(255,77,77,.3);color:var(--red);border-radius:4px;padding:1px 6px;font-size:.65rem;font-weight:600}

/* ── CALLOUTS ── */
.callout{background:var(--card);border:1px solid var(--border);border-radius:14px;padding:20px 22px}
.callout-label{font-size:.7rem;text-transform:uppercase;letter-spacing:1.5px;color:var(--dim);margin-bottom:6px}
.callout-value{font-size:1.1rem;font-weight:600;color:var(--green);line-height:1.4}

/* ── STANDINGS ── */
.standings-grid{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:16px}
@media(max-width:1000px){.standings-grid{grid-template-columns:1fr 1fr}}
@media(max-width:500px){.standings-grid{grid-template-columns:1fr}}
.standing-title{font-family:'Barlow Condensed',sans-serif;font-size:1.1rem;font-weight:700;padding:14px 18px;border-bottom:1px solid var(--border);letter-spacing:1px}
.standings-grid .big-table{font-size:.78rem}
.standings-grid .big-table td,.standings-grid .big-table th{padding:8px 10px;white-space:nowrap}
.standings-grid .tname{white-space:nowrap;overflow:hidden;text-overflow:ellipsis;max-width:100px}

/* ════════════════════════════════════════════════════
   PROFILE OVERLAY
════════════════════════════════════════════════════ */
#pov{
  position:fixed;inset:0;
  background:rgba(0,0,0,.8);
  backdrop-filter:blur(8px);
  -webkit-backdrop-filter:blur(8px);
  z-index:1000;
  display:flex;align-items:center;justify-content:center;
  opacity:0;pointer-events:none;transition:opacity .25s;
  padding:16px;
}
#pov.open{opacity:1;pointer-events:all}
#pnl{
  background:#0d1020;
  border:1px solid #1e2535;
  border-radius:20px;
  width:min(860px,100%);
  max-height:88vh;
  overflow-y:auto;
  transform:translateY(20px) scale(.97);
  transition:transform .25s;
  scrollbar-width:thin;
  scrollbar-color:#1e2535 transparent;
}
#pov.open #pnl{transform:translateY(0) scale(1)}
.p-close{
  position:absolute;top:18px;right:18px;
  background:rgba(255,255,255,.08);border:1px solid rgba(255,255,255,.15);
  color:var(--text);border-radius:50%;width:36px;height:36px;
  font-size:1rem;cursor:pointer;transition:background .15s;
  display:flex;align-items:center;justify-content:center;
}
.p-close:hover{background:rgba(255,255,255,.15)}
.p-header{
  position:relative;padding:40px 32px 28px;
  background:linear-gradient(135deg,#0f1a30 0%,#0d1020 100%);
  border-bottom:1px solid #1e2535;
}
.p-label{font-size:.7rem;letter-spacing:3px;text-transform:uppercase;color:var(--dim);margin-bottom:6px}
.p-name{font-family:'Barlow Condensed',sans-serif;font-size:clamp(2.2rem,5vw,3.5rem);font-weight:900;letter-spacing:-1px;line-height:1}
.p-since{font-size:.8rem;color:var(--dim);margin-top:6px}
.p-stats{display:grid;grid-template-columns:repeat(5,1fr);gap:1px;background:#1e2535;border-bottom:1px solid #1e2535}
@media(max-width:600px){.p-stats{grid-template-columns:repeat(3,1fr)}}
.p-stat{background:#0d1020;padding:20px 16px;text-align:center}
.p-stat-val{font-family:'Barlow Condensed',sans-serif;font-size:1.8rem;font-weight:900;line-height:1}
.p-stat-key{font-size:.62rem;letter-spacing:1.5px;text-transform:uppercase;color:var(--dim);margin-top:4px}
.p-badges{display:flex;flex-wrap:wrap;gap:8px;padding:20px 32px;border-bottom:1px solid #1e2535}
.p-badge{
  background:rgba(255,255,255,.05);border:1px solid rgba(255,255,255,.12);
  border-radius:20px;padding:5px 14px;font-size:.75rem;color:rgba(255,255,255,.7);
}
.p-gw-section{padding:0 32px 8px;border-bottom:1px solid #1e2535}
.p-gw-title{font-family:'Barlow Condensed',sans-serif;font-size:.7rem;letter-spacing:3px;text-transform:uppercase;color:var(--dim);padding:20px 0 14px}
.p-gw-stats{display:flex;gap:20px;margin-bottom:14px;flex-wrap:wrap}
.p-gw-stat{font-size:.75rem;color:var(--dim)}
.p-gw-stat strong{color:var(--text);font-size:.88rem}
.p-chart-wrap{position:relative;height:160px;margin-bottom:20px}
.p-seasons-title{font-family:'Barlow Condensed',sans-serif;font-size:.7rem;letter-spacing:3px;text-transform:uppercase;color:var(--dim);padding:20px 32px 10px}
.p-seasons{padding:0 24px 24px}
.season-row{
  display:grid;grid-template-columns:70px 28px 1fr 80px 110px 90px;
  align-items:center;gap:10px;
  padding:11px 8px;border-radius:8px;margin-bottom:4px;
  transition:background .15s;
}
.season-row:hover{background:rgba(255,255,255,.03)}
.sr-won{background:rgba(255,215,0,.05)!important;border:1px solid rgba(255,215,0,.15);border-radius:8px}
.sr-runner{background:rgba(192,192,192,.04)!important;border:1px solid rgba(192,192,192,.12);border-radius:8px}
.sr-season{font-family:'Barlow Condensed',sans-serif;font-size:.9rem;font-weight:700}
.sr-badge{font-size:1rem;text-align:center}
.sr-bar-wrap{height:8px;background:rgba(255,255,255,.05);border-radius:4px;overflow:hidden}
.sr-bar{height:100%;border-radius:4px;transition:width .4s ease}
.sr-pos{font-size:.78rem;color:var(--dim);text-align:right;font-family:monospace}
.sr-rank{font-size:.78rem;font-family:monospace;text-align:right}
.sr-pts{font-size:.78rem;color:var(--teal);text-align:right;font-family:monospace}
@media(max-width:580px){
  .season-row{grid-template-columns:65px 24px 1fr 70px 90px}
  .sr-pts{display:none}
}

.footer{text-align:center;padding:60px 20px 40px;color:var(--dim);font-size:.75rem;line-height:1.8;max-width:600px;margin:0 auto}

/* ── PRIZE POT ── */
.pot-summary{display:grid;grid-template-columns:repeat(3,1fr);gap:16px;margin-bottom:16px}
@media(max-width:700px){.pot-summary{grid-template-columns:1fr}}
.pot-stat{background:var(--card);border:1px solid var(--border);border-radius:14px;padding:20px 22px;text-align:center}
.pot-stat-val{font-family:'Barlow Condensed',sans-serif;font-size:2.2rem;font-weight:900;line-height:1;color:var(--green)}
.pot-stat-key{font-size:.68rem;letter-spacing:1.5px;text-transform:uppercase;color:var(--dim);margin-top:6px}
.pot-bar-wrap{height:10px;background:rgba(255,255,255,.06);border-radius:5px;overflow:hidden;margin:4px 0 24px}
.pot-bar{height:100%;background:linear-gradient(90deg,#00ff87,#04f5ff);border-radius:5px;transition:width .4s ease}
.prize-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:14px;margin-bottom:24px}
@media(max-width:800px){.prize-grid{grid-template-columns:1fr 1fr}}
.prize-card{background:var(--card);border:1px solid var(--border);border-radius:14px;padding:18px;text-align:center}
.prize-card-label{font-size:.65rem;letter-spacing:2px;text-transform:uppercase;color:var(--dim);margin-bottom:8px}
.prize-card-val{font-family:'Barlow Condensed',sans-serif;font-size:1.9rem;font-weight:800}
.paid-columns{display:grid;grid-template-columns:1fr 1fr;gap:24px}
@media(max-width:700px){.paid-columns{grid-template-columns:1fr}}
.paid-item,.unpaid-item{display:flex;align-items:center;gap:10px;padding:10px 18px;border-bottom:1px solid rgba(30,37,53,.5);font-size:.88rem}
.paid-item:last-child,.unpaid-item:last-child{border-bottom:none}
.paid-check{color:var(--green)}
.unpaid-check{color:var(--dim)}

/* ── NAV ── */
.topnav{display:flex;justify-content:center;gap:8px;padding:20px 20px 0}
.topnav a{font-family:'Barlow Condensed',sans-serif;font-size:.85rem;letter-spacing:1.5px;text-transform:uppercase;font-weight:700;
  color:rgba(255,255,255,.55);text-decoration:none;padding:8px 18px;border-radius:20px;border:1px solid transparent;transition:all .15s}
.topnav a:hover{color:var(--text);border-color:var(--border)}
.topnav a.active{color:var(--bg);background:var(--green)}
</style>
</head>
<body>
"""

SCRIPT_TAIL = r"""
function openProfile(name) {
  const p = PR[name];
  if (!p) return;

  const label = getLabel(p);
  const accentColor = p.wins_count > 0 ? '#ffd700' : p.ru_count > 0 ? '#c0c0c0' : '#00ff87';
  const badges = getBadges(p);

  const careerRows = p.career.map(c => {
    const col = SC[c.s] || '#888';
    const pct = c.pos && c.total ? Math.round((c.total - c.pos + 1) / c.total * 100) : 50;
    const badge = c.won ? '🏆' : c.runner ? '🥈' : '';
    const posLabel = c.pos ? c.pos + ord(c.pos) + (c.total ? '/' + c.total : '') : '—';
    const rankStr = c.rank ? '#' + c.rank.toLocaleString() : '—';
    const ptsStr  = c.pts  ? c.pts.toLocaleString() + ' pts' : '—';
    const rowCls  = c.won ? 'sr-won' : c.runner ? 'sr-runner' : '';
    return `<div class="season-row ${rowCls}">
      <span class="sr-season" style="color:${col}">${c.s}</span>
      <span class="sr-badge">${badge}</span>
      <div class="sr-bar-wrap"><div class="sr-bar" style="width:${pct}%;background:${col}50;border-right:3px solid ${col}"></div></div>
      <span class="sr-pos dim">${posLabel}</span>
      <span class="sr-rank" style="color:${c.rank && c.rank < 100000 ? '#00ff87' : c.rank && c.rank > 1000000 ? '#ef4444' : '#7a8fa6'}">${rankStr}</span>
      <span class="sr-pts">${ptsStr}</span>
    </div>`;
  }).join('');

  const badgesHtml = badges.length
    ? '<div class="p-badges">' + badges.map(b => `<span class="p-badge">${b}</span>`).join('') + '</div>'
    : '';

  const gw = p.gw_data || [];
  const gwHtml = gw.length ? (() => {
    const totalPts    = gw.reduce((a,g) => a + g.pts, 0);
    const gwWithRank  = gw.filter(g => g.gw_rank);
    const best        = gwWithRank.length ? gwWithRank.reduce((a,g) => g.gw_rank < a.gw_rank ? g : a, gwWithRank[0]) : gw.reduce((a,g) => g.pts > a.pts ? g : a, gw[0]);
    const worst       = gwWithRank.length ? gwWithRank.reduce((a,g) => g.gw_rank > a.gw_rank ? g : a, gwWithRank[0]) : gw.reduce((a,g) => g.pts < a.pts ? g : a, gw[0]);
    const totalHits   = gw.reduce((a,g) => a + (g.transfers_cost || 0), 0);
    const totalBench  = gw.reduce((a,g) => a + (g.bench_pts || 0), 0);
    const avg         = (totalPts / gw.length).toFixed(1);
    return `
    <div class="p-gw-section">
      <div class="p-gw-title">${p.gw_season || CUR_SEASON} — Points per GW · colour = GW rank (green above avg, red below)</div>
      <div class="p-gw-stats">
        <div class="p-gw-stat"><strong>${gw.length}</strong> GWs played</div>
        <div class="p-gw-stat"><strong>${avg}</strong> avg pts/GW</div>
        <div class="p-gw-stat"><strong>GW${best.gw}</strong> best GW rank (${best.gw_rank ? '#'+best.gw_rank.toLocaleString() : best.pts+'pts'})</div>
        <div class="p-gw-stat"><strong>GW${worst.gw}</strong> worst GW rank (${worst.gw_rank ? '#'+worst.gw_rank.toLocaleString() : worst.pts+'pts'})</div>
        <div class="p-gw-stat"><strong>${totalHits}</strong> pts lost to hits</div>
        <div class="p-gw-stat"><strong>${totalBench}</strong> pts left on bench</div>
      </div>
      <div class="p-chart-wrap"><canvas id="gwChart"></canvas></div>
    </div>`;
  })() : '';

  document.getElementById('pct').innerHTML = `
    <div class="p-header" style="border-top:4px solid ${accentColor}">
      <button class="p-close" onclick="closeProfile()">✕</button>
      <div class="p-label">${label}</div>
      <div class="p-name" style="color:${accentColor}">${name}</div>
      <div class="p-since">League member since ${p.join}</div>
    </div>
    <div class="p-stats">
      <div class="p-stat">
        <div class="p-stat-val" style="color:#ffd700">${p.wins_count || '0'}</div>
        <div class="p-stat-key">Titles</div>
      </div>
      <div class="p-stat">
        <div class="p-stat-val" style="color:#c0c0c0">${p.ru_count || '0'}</div>
        <div class="p-stat-key">Runner-Ups</div>
      </div>
      <div class="p-stat">
        <div class="p-stat-val">${p.career.length}</div>
        <div class="p-stat-key">Seasons</div>
      </div>
      <div class="p-stat">
        <div class="p-stat-val" style="color:#00ff87">${p.best_rank ? '#' + p.best_rank.toLocaleString() : '—'}</div>
        <div class="p-stat-key">Best Rank</div>
      </div>
      <div class="p-stat">
        <div class="p-stat-val" style="color:#04f5ff">${p.best_pts ? p.best_pts.toLocaleString() : '—'}</div>
        <div class="p-stat-key">Most Pts</div>
      </div>
    </div>
    ${badgesHtml}
    ${gwHtml}
    <div class="p-seasons-title">Season by Season</div>
    <div class="p-seasons">${careerRows || '<div style="padding:20px 8px;color:#5a6a85;font-size:.85rem">No season data available.</div>'}</div>
  `;

  if (gw.length) {
    const ctx = document.getElementById('gwChart').getContext('2d');
    if (window._gwChart) window._gwChart.destroy();

    const gwRanks  = gw.map(g => g.gw_rank).filter(r => r != null);
    const avgGwRnk = gwRanks.length ? gwRanks.reduce((a,b)=>a+b,0)/gwRanks.length : null;
    const avgPts   = gw.reduce((a,g)=>a+g.pts,0) / gw.length;

    const colors = gw.map(g => {
      if (g.gw_rank == null) return accentColor + '66';
      return g.gw_rank <= avgGwRnk ? accentColor + 'cc' : '#ef444488';
    });

    window._gwChart = new Chart(ctx, {
      type: 'bar',
      data: {
        labels: gw.map(g => 'GW' + g.gw),
        datasets: [{
          label: 'Points',
          data: gw.map(g => g.pts),
          backgroundColor: colors,
          borderRadius: 4,
          borderSkipped: false,
        }, {
          label: 'Avg',
          data: gw.map(() => avgPts),
          type: 'line',
          borderColor: 'rgba(255,255,255,0.2)',
          borderWidth: 1.5,
          borderDash: [4,4],
          pointRadius: 0,
          fill: false,
          tension: 0,
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        animation: { duration: 400 },
        plugins: {
          legend: { display: false },
          tooltip: {
            backgroundColor: '#0d1020',
            borderColor: '#1e2535',
            borderWidth: 1,
            callbacks: {
              title: items => 'GW' + gw[items[0].dataIndex].gw,
              label: item => {
                const g = gw[item.dataIndex];
                if (!g) return '';
                const lines = [];
                if (g.gw_rank) lines.push(`GW Rank: #${g.gw_rank.toLocaleString()}`);
                lines.push(`Points: ${g.pts}`);
                if (g.transfers_cost) lines.push(`Hit: -${g.transfers_cost} pts`);
                if (g.bench_pts) lines.push(`Bench: ${g.bench_pts} pts`);
                return lines;
              }
            }
          }
        },
        scales: {
          x: { grid: { color: 'rgba(255,255,255,0.04)' }, ticks: { color: '#5a6a85', font: { size: 10 } } },
          y: { grid: { color: 'rgba(255,255,255,0.06)' }, ticks: { color: '#5a6a85', font: { size: 10 } }, beginAtZero: true }
        }
      }
    });
  }

  document.getElementById('pov').classList.add('open');
  document.getElementById('pnl').scrollTop = 0;
}

function closeProfile() {
  document.getElementById('pov').classList.remove('open');
}

document.addEventListener('keydown', e => e.key === 'Escape' && closeProfile());

function ord(n) {
  const s = ['th','st','nd','rd'], v = n % 100;
  return s[(v - 20) % 10] || s[v] || s[0];
}

function getLabel(p) {
  if (p.wins_count >= 3) return 'The Dynasty';
  if (p.wins_count === 2) return 'Double Champion';
  if (p.wins_count === 1 && p.ru_count >= 1) return 'Champion';
  if (p.wins_count === 1) return 'Champion';
  if (p.ru_count >= 3 && p.wins_count === 0) return 'The Eternal Bridesmaid';
  if (p.ru_count >= 2) return 'The Silver Specialist';
  if (p.ru_count === 1) return 'So Close...';
  if (p.best_rank && p.best_rank < 10000) return 'The Elite';
  if (p.best_rank && p.best_rank < 50000) return 'The Dark Horse';
  if (p.join === '2016/17') return 'Founding Member';
  return 'League Member';
}

function getBadges(p) {
  const b = [];
  if (p.join === '2016/17') b.push('🏛️ Founding Member');
  if (p.wins_count >= 3)    b.push('👑 Dynasty (' + p.wins_count + ' titles)');
  else if (p.wins_count > 0) b.push('🏆 ' + (p.wins_count > 1 ? p.wins_count + '× ' : '') + 'Champion');
  if (p.ru_count >= 3)      b.push('🥈 3× Runner-Up');
  else if (p.ru_count > 0)  b.push('🥈 ' + (p.ru_count > 1 ? p.ru_count + '× ' : '') + 'Runner-Up');
  if (p.best_rank && p.best_rank < 10000)  b.push('⚡ Top 10k (' + p.best_rank.toLocaleString() + ')');
  else if (p.best_rank && p.best_rank < 50000) b.push('🎯 Top 50k (' + p.best_rank.toLocaleString() + ')');
  if (p.career.length >= 8) b.push('📅 ' + p.career.length + '-Season Veteran');
  if (p.best_pts && p.best_pts >= 2500) b.push('🔥 ' + p.best_pts.toLocaleString() + ' pts in a season');
  if (p.wins_count === 0 && p.ru_count === 0 && p.career.length >= 4) b.push('💪 Consistent Competitor');
  return b;
}
"""


def esc(s):
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def plink(name):
    return f'<span class="plink" onclick="openProfile(\'{esc(name)}\')">{esc(name)}</span>'


def fmt(n):
    return f"{n:,}" if n is not None else "—"


def nav_html(active):
    def link(href, label, key):
        cls = ' class="active"' if key == active else ""
        return f'<a href="{href}"{cls}>{label}</a>'
    return f"""
<div class="topnav">
  {link("index.html", "Hall of Fame", "home")}
  {link("prize-pot.html", "💰 Prize Pot", "prizes")}
</div>
"""


def build_prize_pot_section(roster, payments):
    fee = payments["fee_per_person"]
    currency = payments.get("currency", "EUR")
    paid_names = set(payments["paid"])
    all_names = sorted(roster.keys())
    unpaid_names = [n for n in all_names if n not in paid_names]

    collected = len(paid_names) * fee
    expected = len(all_names) * fee
    pct_collected = round(100 * len(paid_names) / len(all_names)) if all_names else 0

    prizes = payments["prizes"]
    monthly_pool_pct = prizes["monthly_pool_pct"] * 100
    monthly_each_pct = prizes["monthly_pool_pct"] * 100 / prizes["monthly_count"]
    podium = prizes["podium_pct"]

    prize_cards = f"""
      <div class="prize-card" style="border-bottom:3px solid #ffd700">
        <div class="prize-card-label">🥇 1st Place</div>
        <div class="prize-card-val" style="color:#ffd700">{podium['1st']*100:.0f}%</div>
      </div>
      <div class="prize-card" style="border-bottom:3px solid #c0c0c0">
        <div class="prize-card-label">🥈 2nd Place</div>
        <div class="prize-card-val" style="color:#c0c0c0">{podium['2nd']*100:.0f}%</div>
      </div>
      <div class="prize-card" style="border-bottom:3px solid #cd7f32">
        <div class="prize-card-label">🥉 3rd Place</div>
        <div class="prize-card-val" style="color:#cd7f32">{podium['3rd']*100:.0f}%</div>
      </div>
      <div class="prize-card" style="border-bottom:3px solid #22c55e">
        <div class="prize-card-label">📅 Per Month ({prizes['monthly_count']}×)</div>
        <div class="prize-card-val" style="color:#22c55e">{monthly_each_pct:.1f}%</div>
      </div>"""

    paid_html = "".join(
        f'<div class="paid-item"><span class="paid-check">✓</span>{esc(n)}</div>' for n in sorted(paid_names)
    )
    unpaid_html = "".join(
        f'<div class="unpaid-item"><span class="unpaid-check">○</span>{esc(n)}</div>' for n in unpaid_names
    )

    return f"""
<div class="section">
  <div class="sec-label">Prize Pot — {payments.get('season', '')}</div>
  <div class="pot-summary">
    <div class="pot-stat"><div class="pot-stat-val">{len(paid_names)}/{len(all_names)}</div><div class="pot-stat-key">Managers Paid</div></div>
    <div class="pot-stat"><div class="pot-stat-val">{fee} {currency}</div><div class="pot-stat-key">Entry Fee (p/p)</div></div>
    <div class="pot-stat"><div class="pot-stat-val">{collected:,} / {expected:,} {currency}</div><div class="pot-stat-key">Collected / Full Pot</div></div>
  </div>
  <div class="pot-bar-wrap"><div class="pot-bar" style="width:{pct_collected}%"></div></div>
  <div class="sec-label" style="margin-top:8px">Prize Structure (% of final pot — 1st/2nd/3rd + {prizes['monthly_count']} monthly prizes, {monthly_pool_pct:.0f}% of pot total)</div>
  <div class="prize-grid">{prize_cards}</div>
  <div class="card">
    <div class="paid-columns">
      <div><div style="padding:14px 18px;font-weight:700;border-bottom:1px solid var(--border)">✅ Paid ({len(paid_names)})</div>{paid_html}</div>
      <div><div style="padding:14px 18px;font-weight:700;border-bottom:1px solid var(--border)">⏳ Not Paid Yet ({len(unpaid_names)})</div>{unpaid_html}</div>
    </div>
  </div>
</div>
"""


def render_prizes_page(roster, payments):
    body = build_prize_pot_section(roster, payments)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Prize Pot — FPL Classics</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@400;600;700;800;900&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
<style>
{HEAD.split("<style>")[1].split("</style>")[0]}
</style>
</head>
<body>
{nav_html("prizes")}
<div class="hero" style="padding:50px 40px 30px">
  <div class="hero-eyebrow">FPL Classics · League #37785</div>
  <div class="hero-title" style="font-size:clamp(2.2rem,6vw,4rem)">Prize Pot</div>
</div>
{body}
<div class="footer"><p>FPL Classics · League #37785</p></div>
</body>
</html>"""


def render(profiles, known_seasons, tables, cur_season):
    all_seasons = sorted(known_seasons.keys())
    latest = all_seasons[-1] if all_seasons else None
    distinct_winners = {v["winner"]["name"] for v in known_seasons.values()}
    managers_with_data = sum(1 for p in profiles.values() if p["career"])

    hero = f"""
<div class="hero">
  <div class="hero-eyebrow">FPL Classics · League #37785</div>
  <div class="hero-title">Hall of Fame</div>
  <div class="hero-sub">The Definitive Record · {all_seasons[0][:4] if all_seasons else ''} – {cur_season[:4]}</div>
  <div class="hero-badges">
    <div class="hero-badge"><span>{len(all_seasons)}</span> Seasons</div>
    <div class="hero-badge"><span>{managers_with_data}</span> Managers</div>
    <div class="hero-badge"><span>{len(distinct_winners)}</span> Different Winners</div>
    <div class="hero-badge">Est. <span>{all_seasons[0] if all_seasons else ''}</span></div>
  </div>
</div>
"""

    # ── season cards ──
    cards = []
    for s in all_seasons:
        r = known_seasons[s]
        w, ru = r["winner"], r["runner_up"]
        c = accent_for(s)
        latest_badge = '<span class="sc-new">LATEST</span>' if s == latest else ""
        ru_line = (
            f'<span class="sc-rname">{plink(ru["name"])}</span><span class="sc-rrank">{fmt(ru["rank"])}</span>'
            if not ru.get("left_league")
            else f'<span class="sc-rname">{esc(ru["name"])}</span><span class="sc-rrank">—</span>'
        )
        cards.append(f"""
      <div class="sc" style="--c:{c};{'box-shadow:0 0 30px ' + c + '40,0 0 60px ' + c + '20;' if s == latest else ''}">
        <div class="sc-top" style="background:{c}15;border-top:3px solid {c}">
          <span class="sc-year" style="color:{c}">{s}</span>
          {latest_badge}
        </div>
        <div class="sc-body">
          <div class="sc-trophy">🏆</div>
          <div class="sc-wname">{plink(w["name"])}</div>
          <div class="sc-winfo">
            <span class="sc-pts">{fmt(w["pts"])} pts</span>
            <span class="sc-rank-pill" style="background:{c}22;color:{c};border:1px solid {c}44">#{fmt(w["rank"])}</span>
          </div>
        </div>
        <div class="sc-footer">
          <span class="sc-silver">🥈</span>
          {ru_line}
        </div>
      </div>""")

    season_cards_section = f"""
<div class="section">
  <div class="sec-label">All-Time Winners — click a name to view profile</div>
  <div class="sc-grid">{''.join(cards)}</div>
</div>
"""

    # ── full HOF table ──
    hof_rows = []
    for s in all_seasons:
        r = known_seasons[s]
        w, ru = r["winner"], r["runner_up"]
        c = accent_for(s)
        ru_cell = (
            f'<span class="silver-text">🥈</span> {plink(ru["name"])}</td><td class="pts-cell">{fmt(ru["pts"])}</td><td class="rank-cell">{fmt(ru["rank"])}'
            if not ru.get("left_league")
            else f'<span class="silver-text">🥈</span> {esc(ru["name"])}</td><td class="pts-cell">—</td><td class="rank-cell">—'
        )
        hof_rows.append(f"""
          <tr>
            <td><span class="season-tag" style="color:{c}">{s}</span></td>
            <td><span class="winner-cell">🏆 {plink(w["name"])}</span></td>
            <td class="pts-cell gold-text">{fmt(w["pts"])}</td>
            <td class="rank-cell">{fmt(w["rank"])}</td>
            <td>{ru_cell}</td>
          </tr>""")

    hof_table_section = f"""
<div class="section">
  <div class="sec-label">Full Hall of Fame Record</div>
  <div class="card">
    <div class="hof-table-wrap">
      <table class="hof-table">
        <thead><tr><th>Season</th><th>Winner</th><th style="text-align:right">Pts</th><th style="text-align:right">Overall Rank</th><th>Runner-Up</th><th style="text-align:right">Pts</th><th style="text-align:right">Overall Rank</th></tr></thead>
        <tbody>{''.join(hof_rows)}</tbody>
      </table>
    </div>
  </div>
</div>
"""

    # ── champions board / bridesmaid award ──
    champs = {}
    rus = {}
    for s in all_seasons:
        r = known_seasons[s]
        champs.setdefault(r["winner"]["name"], []).append(s)
        if not r["runner_up"].get("left_league"):
            rus.setdefault(r["runner_up"]["name"], []).append(s)
        else:
            rus.setdefault(r["runner_up"]["name"], []).append((s, True))

    def honour_rows(d, cls=""):
        rows = []
        for name, seasons in sorted(d.items(), key=lambda kv: -len(kv[1])):
            left = any(isinstance(s, tuple) for s in seasons)
            seasons_clean = [s[0] if isinstance(s, tuple) else s for s in seasons]
            n = len(seasons_clean)
            label = f'{n} title{"s" if n != 1 else ""}' if not cls else f'{n}× runner-up'
            name_html = esc(name) + " <span class='left-badge'>left</span>" if left else plink(name)
            badges = "".join(f'<span class="badge {cls}">{s}</span>' for s in seasons_clean)
            rows.append(f"""
        <div class="honour-row">
          <div class="honour-name">{name_html}</div>
          <div class="honour-count">{label}</div>
          <div class="badges">{badges}</div>
        </div>""")
        return "".join(rows)

    champs_section = f"""
<div class="section">
  <div class="grid-2">
    <div><div class="sec-label">Champions Board</div><div class="card">{honour_rows(champs)}</div></div>
    <div><div class="sec-label">The Bridesmaid Award</div><div class="card">{honour_rows(rus, "silver-badge")}</div></div>
  </div>
</div>
"""

    # ── awards ──
    def wins_count_of(name):
        return profiles.get(name, {}).get("wins_count", 0)

    most_titles = max(profiles.items(), key=lambda kv: kv[1]["wins_count"])
    most_ru = max(profiles.items(), key=lambda kv: kv[1]["ru_count"])
    best_rank_ever = min(
        (p for p in profiles.values() if p.get("best_rank")), key=lambda p: p["best_rank"]
    )
    best_rank_name = next(n for n, p in profiles.items() if p is best_rank_ever)
    best_pts_ever = max(
        (p for p in profiles.values() if p.get("best_pts")), key=lambda p: p["best_pts"]
    )
    best_pts_name = next(n for n, p in profiles.items() if p is best_pts_ever)

    consistency = tables["consistency"]
    mr_consistent = consistency[0] if consistency else None

    worst_rank_row = None
    for s in all_seasons:
        for name, p in profiles.items():
            for c in p["career"]:
                if c["s"] == s and c.get("rank"):
                    if worst_rank_row is None or c["rank"] > worst_rank_row[1]:
                        worst_rank_row = (name, c["rank"], s)

    gaps = []
    for s in all_seasons:
        r = known_seasons[s]
        if r["runner_up"].get("left_league") or r["winner"]["pts"] is None or r["runner_up"]["pts"] is None:
            continue
        gaps.append((s, r["winner"], r["runner_up"], r["winner"]["pts"] - r["runner_up"]["pts"]))
    gaps.sort(key=lambda g: -g[3])
    dominant = gaps[0] if gaps else None
    closest = gaps[-1] if gaps else None

    awards_row1 = f"""
<div class="section">
  <div class="sec-label">League Awards</div>
  <div class="awards-grid">
      <div class="award-card" style="--ac:#ffd700">
        <div class="award-emoji">👑</div>
        <div class="award-title">MOST LEAGUE TITLES</div>
        <div class="award-name">{plink(most_titles[0])}</div>
        <div class="award-stat" style="color:#ffd700;text-shadow:0 0 20px #ffd70080">×{most_titles[1]['wins_count']}</div>
        <div class="award-detail">{' · '.join(most_titles[1]['win_seasons'])}</div>
      </div>
      <div class="award-card" style="--ac:#c0c0c0">
        <div class="award-emoji">🥈</div>
        <div class="award-title">THE ETERNAL BRIDESMAID</div>
        <div class="award-name">{plink(most_ru[0])}</div>
        <div class="award-stat" style="color:#c0c0c0;text-shadow:0 0 20px #c0c0c080">×{most_ru[1]['ru_count']} Runner-Up</div>
        <div class="award-detail">{' · '.join(most_ru[1]['ru_seasons'])}</div>
      </div>
      <div class="award-card" style="--ac:#00ff87">
        <div class="award-emoji">⚡</div>
        <div class="award-title">BEST FPL RANK EVER</div>
        <div class="award-name">{plink(best_rank_name)}</div>
        <div class="award-stat" style="color:#00ff87;text-shadow:0 0 20px #00ff8780">#{fmt(best_rank_ever['best_rank'])}</div>
        <div class="award-detail">{best_rank_ever['best_rank_s']}</div>
      </div>
      <div class="award-card" style="--ac:#04f5ff">
        <div class="award-emoji">📈</div>
        <div class="award-title">MOST POINTS EVER</div>
        <div class="award-name">{plink(best_pts_name)}</div>
        <div class="award-stat" style="color:#04f5ff;text-shadow:0 0 20px #04f5ff80">{fmt(best_pts_ever['best_pts'])} pts</div>
        <div class="award-detail">{best_pts_ever['best_pts_s']}</div>
      </div></div>
</div>"""

    awards_row2 = f"""
<div class="section" style="padding-top:16px">
  <div class="awards-grid">
      <div class="award-card" style="--ac:#22c55e">
        <div class="award-emoji">🎯</div>
        <div class="award-title">MR. CONSISTENT</div>
        <div class="award-name">{plink(mr_consistent[0]) if mr_consistent else '—'}</div>
        <div class="award-stat" style="color:#22c55e;text-shadow:0 0 20px #22c55e80">#{fmt(mr_consistent[1]) if mr_consistent else '—'} avg</div>
        <div class="award-detail">Best avg overall rank (founders from 2019/20, others from join season)</div>
      </div>
      <div class="award-card" style="--ac:#ef4444">
        <div class="award-emoji">💀</div>
        <div class="award-title">WOODEN SPOON</div>
        <div class="award-name">{plink(worst_rank_row[0]) if worst_rank_row else '—'}</div>
        <div class="award-stat" style="color:#ef4444;text-shadow:0 0 20px #ef444480">#{fmt(worst_rank_row[1]) if worst_rank_row else '—'}</div>
        <div class="award-detail">{worst_rank_row[2] if worst_rank_row else ''} — worst overall rank in league history</div>
      </div>
      <div class="award-card" style="--ac:#f59e0b">
        <div class="award-emoji">🔥</div>
        <div class="award-title">MOST DOMINANT WIN</div>
        <div class="award-name">{plink(dominant[1]['name']) if dominant else '—'}</div>
        <div class="award-stat" style="color:#f59e0b;text-shadow:0 0 20px #f59e0b80">+{dominant[3] if dominant else '—'} pts</div>
        <div class="award-detail">{dominant[0] if dominant else ''} vs {dominant[2]['name'] if dominant else ''}</div>
      </div>
      <div class="award-card" style="--ac:#a78bfa">
        <div class="award-emoji">😬</div>
        <div class="award-title">PHOTO FINISH</div>
        <div class="award-name">{plink(closest[1]['name']) if closest else '—'}</div>
        <div class="award-stat" style="color:#a78bfa;text-shadow:0 0 20px #a78bfa80">+{closest[3] if closest else '—'} pts</div>
        <div class="award-detail">{closest[0] if closest else ''} — just {closest[3] if closest else ''}pts clear of {closest[2]['name'] if closest else ''}</div>
      </div></div>
</div>"""

    # ── all-time table ──
    at_rows = []
    for i, row in enumerate(tables["all_time"], 1):
        p = profiles[row["name"]]
        honours = "🏆" * row["wins"] + "🥈" * row["ru"]
        bg = "style='background:rgba(255,215,0,0.05)'" if row["wins"] > 0 else ""
        best_rank_str = f"#{fmt(row['best_rank'])} ({row['best_rank_s']})" if row["best_rank"] else "—"
        at_rows.append(
            f"<tr {bg}><td class=\"tnum dim\">{i}</td><td class=\"tname\">{plink(row['name'])}</td>"
            f"<td class=\"tc\">{honours or '—'}</td><td class=\"tnum\">{row['wins']}</td>"
            f"<td class=\"tnum\">{row['ru']}</td><td class=\"tnum dim\">{row['seasons']}</td>"
            f"<td class=\"tnum rank-good\">{best_rank_str}</td></tr>"
        )

    all_time_section = f"""
<div class="section">
  <div class="sec-label">All-Time League Table</div>
  <div class="card">
    <table class="big-table">
      <thead><tr><th style="text-align:right">#</th><th>Manager</th><th>Honours</th><th style="text-align:right">Wins</th><th style="text-align:right">Runner-Ups</th><th style="text-align:right">FPL Seasons</th><th style="text-align:right">Best Rank (league era)</th></tr></thead>
      <tbody>{''.join(at_rows)}</tbody>
    </table>
  </div>
</div>
"""

    # ── consistency leaderboard ──
    con_rows = []
    for i, (name, avg) in enumerate(tables["consistency"], 1):
        marker = " 🎯" if i == 1 else (" 💀" if i == len(tables["consistency"]) else "")
        cls = "green" if i == 1 else ("red" if i == len(tables["consistency"]) else "")
        con_rows.append(
            f'<tr><td class="tnum dim">{i}</td><td class="tname">{plink(name)}{marker}</td>'
            f'<td class="tnum {cls}">{fmt(avg)}</td></tr>'
        )
    consistency_section = f"""
<div class="section">
  <div class="sec-label">Consistency Leaderboard — Avg Overall Rank (founding members from 2019/20 · others from join season)</div>
  <div class="card">
    <table class="big-table">
      <thead><tr><th style="text-align:right">#</th><th>Manager</th><th style="text-align:right">Avg Overall Rank</th></tr></thead>
      <tbody>{''.join(con_rows)}</tbody>
    </table>
  </div>
</div>
"""

    # ── points gap ──
    gap_rows = []
    for s, w, ru, gap in gaps:
        c = accent_for(s)
        cls = "green" if gap >= 20 else ("red" if gap <= 10 else "")
        gap_rows.append(
            f'<tr><td><span class="season-tag" style="color:{c}">{s}</span></td>'
            f'<td class="tname">{plink(w["name"])}</td><td class="pts-cell gold-text">{fmt(w["pts"])}</td>'
            f'<td>{plink(ru["name"])}</td><td class="pts-cell">{fmt(ru["pts"])}</td>'
            f'<td class="tnum {cls}">+{gap}</td></tr>'
        )
    points_gap_section = f"""
<div class="section">
  <div class="sec-label">Points Gap — Winner vs Runner-Up</div>
  <div style="display:grid;grid-template-columns:1fr 1fr;gap:16px;margin-bottom:16px">
    <div class="callout"><div class="callout-label">🔥 Most Dominant Win</div><div class="callout-value">{dominant[0] if dominant else ''} — {plink(dominant[1]['name']) if dominant else ''} won by <strong>{dominant[3] if dominant else ''}pts</strong></div></div>
    <div class="callout"><div class="callout-label">😬 Closest Race</div><div class="callout-value">{closest[0] if closest else ''} — {plink(closest[1]['name']) if closest else ''} beat {plink(closest[2]['name']) if closest else ''} by just <strong>{closest[3] if closest else ''}pts</strong></div></div>
  </div>
  <div class="card">
    <table class="big-table">
      <thead><tr><th>Season</th><th>Winner</th><th style="text-align:right">Pts</th><th>Runner-Up</th><th style="text-align:right">Pts</th><th style="text-align:right">Gap</th></tr></thead>
      <tbody>{''.join(gap_rows)}</tbody>
    </table>
  </div>
</div>
"""

    footer = f"""
<div class="footer">
  <p>FPL Classics · League #37785 · Est. {all_seasons[0] if all_seasons else ''}</p>
  <p>Data from the official FPL API. Early seasons ({all_seasons[0]}–2021/22) winner records verified manually. Individual stats filtered to league-era seasons only.</p>
</div>

<div id="pov" onclick="if(event.target===this)closeProfile()">
  <div id="pnl"><div id="pct"></div></div>
</div>
"""

    pr_json = json.dumps(profiles, ensure_ascii=False, separators=(",", ": "))
    sc_json = json.dumps(SEASON_ACCENT_FOR_JS(all_seasons), ensure_ascii=False)

    script = f"""
<script>
const PR = {pr_json};
const SC = {sc_json};
const CUR_SEASON = {json.dumps(cur_season, ensure_ascii=False)};
{SCRIPT_TAIL}
</script>
</body>
</html>"""

    return (
        HEAD
        + nav_html("home")
        + hero
        + season_cards_section
        + hof_table_section
        + champs_section
        + awards_row1
        + awards_row2
        + all_time_section
        + "".join(build_standings_grid(profiles, all_seasons))
        + consistency_section
        + points_gap_section
        + footer
        + script
    )


def SEASON_ACCENT_FOR_JS(all_seasons):
    return {s: accent_for(s) for s in all_seasons}


def build_standings_grid(profiles, all_seasons):
    """Season-by-season full standings for the last 4 completed seasons,
    matching the original site's window."""
    recent = all_seasons[-4:]
    cards = []
    for s in recent:
        rows = []
        for name, p in profiles.items():
            for c in p["career"]:
                if c["s"] == s and c.get("pts"):
                    rows.append((name, c["pts"], c.get("rank")))
        rows.sort(key=lambda r: (-r[1], r[2] if r[2] is not None else float("inf")))
        trs = []
        medals = ["🥇", "🥈", "🥉"]
        for i, (name, pts, rank) in enumerate(rows, 1):
            pos = medals[i - 1] if i <= 3 else str(i)
            trs.append(
                f'<tr><td class="tnum">{pos}</td><td class="tname">{plink(name)}</td>'
                f'<td class="tnum teal">{fmt(pts)}</td><td class="tnum rank-num">{fmt(rank)}</td></tr>'
            )
        cards.append(
            f'<div class="card"><div class="standing-title" style="color:{accent_for(s)}">{s}</div>'
            f'<table class="big-table"><thead><tr><th>#</th><th>Manager</th>'
            f'<th style="text-align:right">Pts</th><th style="text-align:right">Rank</th></tr></thead>'
            f'<tbody>{"".join(trs)}</tbody></table></div>'
        )
    return [f"""
<div class="section">
  <div class="sec-label">Full Season Standings ({recent[0]} – {recent[-1]})</div>
  <div class="standings-grid">{''.join(cards)}</div>
</div>
"""]
