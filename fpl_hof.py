"""
FPL Hall of Fame generator (v2) — league #37044's original script was lost,
so this rebuilds the same output from clean, versioned data files instead of
one hardcoded script. See ../README.md for how the pieces fit together.

Run:  python fpl_hof.py
Requires: pip install requests
"""
import json
import sys
from datetime import date
from pathlib import Path

import requests

ROOT = Path(__file__).parent
DATA = ROOT / "data"
OUT_HTML = ROOT / "index.html"  # GitHub Pages serves this at the repo root
API = "https://fantasy.premierleague.com/api"

SEASON_ACCENT = {
    "2016/17": "#f59e0b", "2017/18": "#ef4444", "2018/19": "#f59e0b",
    "2019/20": "#8b5cf6", "2020/21": "#06b6d4", "2021/22": "#8b5cf6",
    "2022/23": "#22c55e", "2023/24": "#04f5ff", "2024/25": "#ffd700",
    "2025/26": "#00ff87", "2026/27": "#f97316", "2027/28": "#ec4899",
}
FALLBACK_ACCENTS = ["#f97316", "#ec4899", "#22c55e", "#8b5cf6", "#04f5ff", "#f59e0b"]


def accent_for(season):
    if season in SEASON_ACCENT:
        return SEASON_ACCENT[season]
    year = int(season[:4])
    return FALLBACK_ACCENTS[year % len(FALLBACK_ACCENTS)]


def current_season_label(today=None):
    """PL seasons run Jul-Jun; before July we're still in last year's season."""
    today = today or date.today()
    start_year = today.year if today.month >= 7 else today.year - 1
    return f"{start_year}/{str(start_year + 1)[2:]}"


def load_json(name):
    return json.loads((DATA / name).read_text(encoding="utf-8"))


def fetch_entry_history(entry_id):
    r = requests.get(f"{API}/entry/{entry_id}/history/", timeout=15)
    r.raise_for_status()
    return r.json()


def fetch_entry_picks_gw(entry_id, gw):
    r = requests.get(f"{API}/entry/{entry_id}/event/{gw}/picks/", timeout=15)
    if r.status_code != 200:
        return None
    return r.json()


def fetch_league_standings(league_id):
    r = requests.get(f"{API}/leagues-classic/{league_id}/standings/", timeout=15)
    r.raise_for_status()
    return r.json()


# ── data assembly ──────────────────────────────────────────────────────────

def build_profiles(roster, archive_names, history_seed, current_season):
    """Merge frozen historical data with live data for anyone still tracked."""
    profiles = {}

    # frozen managers: use history_seed verbatim, never touched again
    for name in archive_names:
        if name in history_seed:
            p = history_seed[name]
            if p.get("gw_data") and "gw_season" not in p:
                p["gw_season"] = p["career"][-1]["s"] if p["career"] else None
            profiles[name] = p

    live_season_rows = {}  # season -> list of {name, pts, rank} for winner/runner-up calc

    for name, info in roster.items():
        seed = history_seed.get(name)
        career = list(seed["career"]) if seed else []
        seen_seasons = {c["s"] for c in career}

        hist = fetch_entry_history(info["entry_id"])

        # append any completed season the seed doesn't have yet (e.g. new 2026/27+ results)
        for s in hist.get("past", []):
            sname = s["season_name"]
            if sname < info["join"] or sname in seen_seasons:
                continue
            entry = {
                "s": sname, "rank": s["rank"], "pts": s["total_points"],
                "pos": None, "total": None, "won": False, "runner": False,
            }
            career.append(entry)
            seen_seasons.add(sname)

        career.sort(key=lambda c: c["s"])

        gw_data = seed.get("gw_data", []) if seed else []
        gw_season = seed.get("gw_season", seed.get("career", [{}])[-1].get("s")) if seed and gw_data else None
        cur = hist.get("current", [])
        if cur:
            # live in-progress season overrides the chart with fresh GW data
            gw_data = [
                {
                    "gw": g["event"], "pts": g["points"], "total": g["total_points"],
                    "gw_rank": g.get("rank"), "overall_rank": g.get("overall_rank"),
                    "transfers_cost": g.get("event_transfers_cost", 0),
                    "bench_pts": g.get("points_on_bench", 0),
                }
                for g in cur
            ]
            gw_season = current_season
            live_total = sum(g["points"] for g in cur)
            live_rank = cur[-1].get("overall_rank")
            live_season_rows.setdefault(current_season, []).append(
                {"name": name, "pts": live_total, "rank": live_rank}
            )

        profiles[name] = {
            "join": info["join"],
            "career": career,
            "gw_data": gw_data,
            "gw_season": gw_season,
        }

    for name, p in profiles.items():
        recompute_derived(p)

    return profiles, live_season_rows


def recompute_derived(p):
    career = p["career"]
    wins = [c for c in career if c.get("won")]
    rus = [c for c in career if c.get("runner")]
    p["wins_count"] = len(wins)
    p["win_seasons"] = [c["s"] for c in wins]
    p["ru_count"] = len(rus)
    p["ru_seasons"] = [c["s"] for c in rus]

    ranked = [c for c in career if c.get("rank")]
    if ranked:
        best = min(ranked, key=lambda c: c["rank"])
        worst = max(ranked, key=lambda c: c["rank"])
        p["best_rank"], p["best_rank_s"] = best["rank"], best["s"]
        p["worst_rank"], p["worst_rank_s"] = worst["rank"], worst["s"]
    else:
        p["best_rank"] = p["worst_rank"] = None

    pointed = [c for c in career if c.get("pts")]
    if pointed:
        best_pts = max(pointed, key=lambda c: c["pts"])
        p["best_pts"], p["best_pts_s"] = best_pts["pts"], best_pts["s"]
    else:
        p["best_pts"] = None


def apply_known_seasons(profiles, known_seasons):
    """Stamp won/runner flags + fill missing pos/total onto career rows using
    the curated historical record, so the frozen per-manager data and the
    hardcoded season table can never disagree (this is what caused the
    original 2018/19 bug — two sources of truth that drifted apart)."""
    for season, result in known_seasons.items():
        for role, flag in (("winner", "won"), ("runner_up", "runner")):
            who = result[role]["name"]
            if who not in profiles:
                continue
            for c in profiles[who]["career"]:
                if c["s"] == season:
                    c[flag] = True
    for p in profiles.values():
        recompute_derived(p)


def consistency_scope(name, join_season, founding_cutoff="2019/20"):
    founding = join_season == "2016/17"
    return founding_cutoff if founding else join_season


def build_awards_and_tables(profiles, known_seasons):
    names = sorted(profiles.keys())

    consistency = []
    for name in names:
        p = profiles[name]
        scope = consistency_scope(name, p["join"])
        ranks = [c["rank"] for c in p["career"] if c["s"] >= scope and c.get("rank")]
        if len(ranks) >= 3:
            # round-half-up, matching the original JS Math.round semantics
            import math
            consistency.append((name, math.floor(sum(ranks) / len(ranks) + 0.5)))
    consistency.sort(key=lambda x: x[1])

    all_time = []
    for name in names:
        p = profiles[name]
        if not p["career"]:
            continue  # no recorded seasons yet (e.g. just joined, hasn't played a GW)
        all_time.append({
            "name": name, "wins": p["wins_count"], "ru": p["ru_count"],
            "seasons": len(p["career"]), "best_rank": p["best_rank"],
            "best_rank_s": p.get("best_rank_s"),
        })
    all_time.sort(key=lambda r: (-r["wins"], -r["ru"], r["best_rank"] or float("inf")))

    return {"consistency": consistency, "all_time": all_time}


# ── entry point ─────────────────────────────────────────────────────────────

def main():
    roster_doc = load_json("roster.json")
    roster = roster_doc["managers"]
    league_id = roster_doc["league_id"]
    archive_names = load_json("archive.json")["frozen_managers"]
    history_seed = load_json("history_seed.json")
    known_seasons = load_json("known_seasons.json")["seasons"]
    payments = load_json("payments.json")
    cur_season = current_season_label()

    print(f"Current season: {cur_season}")
    print(f"Fetching live data for {len(roster)} active managers...")

    profiles, live_rows = build_profiles(roster, archive_names, history_seed, cur_season)
    apply_known_seasons(profiles, known_seasons)
    tables = build_awards_and_tables(profiles, known_seasons)

    if live_rows.get(cur_season):
        standing = sorted(live_rows[cur_season], key=lambda r: r["rank"] or float("inf"))
        print(f"\n{cur_season} is live/in progress ({len(standing)} managers with data).")
        print("Not added to the Hall of Fame table yet -- once the season finishes,")
        print("add its winner/runner-up to data/known_seasons.json to freeze it:")
        for row in standing[:3]:
            print(f"  {row['name']}: {row['pts']} pts, rank #{row['rank']}")
    else:
        print(f"\n{cur_season} has no live data yet (season likely hasn't started).")

    print(f"\nManagers tracked: {len(profiles)} ({len(roster)} live + {len(archive_names)} frozen)")
    print("Rendering HTML...")

    from fpl_hof_render import render
    html = render(profiles, known_seasons, tables, cur_season, roster, payments)
    OUT_HTML.write_text(html, encoding="utf-8")
    print(f"Wrote {OUT_HTML} ({len(html):,} bytes)")


if __name__ == "__main__":
    main()
