"""Work out the monthly prize winner (highest points across that month's gameweeks).

A gameweek belongs to the month its deadline falls in (same rule used for
August = GW1-2 and September = GW3-5). Points are the FPL API's per-gameweek
figures, which are net of transfer hits.

Usage:
  python monthly_winner.py                  # dry run for last calendar month
  python monthly_winner.py --month 2026-10  # dry run for a specific month
  python monthly_winner.py --apply          # also record the winner in data/monthly_winners.json

--apply refuses to write if the month isn't finished, is already recorded, or
the top spot is tied (ties need a human decision). It never commits or pushes.
Exit codes: 0 = winner found, 2 = not ready / already recorded, 3 = tie.
"""
import argparse
import json
import sys
import time
from datetime import date
from pathlib import Path

import requests

ROOT = Path(__file__).parent
DATA = ROOT / "data"
API = "https://fantasy.premierleague.com/api"
MONTHS = ["January", "February", "March", "April", "May", "June", "July",
          "August", "September", "October", "November", "December"]


def get_json(url, tries=3):
    for i in range(tries):
        try:
            r = requests.get(url, timeout=20)
            r.raise_for_status()
            return r.json()
        except requests.RequestException:
            if i == tries - 1:
                raise
            time.sleep(2)


def previous_month(today):
    y, m = (today.year, today.month - 1) if today.month > 1 else (today.year - 1, 12)
    return f"{y}-{m:02d}"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--month", help="YYYY-MM (default: last calendar month)")
    ap.add_argument("--apply", action="store_true", help="record the winner in monthly_winners.json")
    args = ap.parse_args()

    month = args.month or previous_month(date.today())
    y, m = int(month[:4]), int(month[5:7])
    label = f"{MONTHS[m - 1]} {y}"

    events = get_json(f"{API}/bootstrap-static/")["events"]
    gws = [e for e in events if e["deadline_time"].startswith(month)]
    if not gws:
        print(f"{label}: no gameweeks have a deadline in this month.")
        return 2
    unfinished = [e["id"] for e in gws if not e["finished"]]
    gw_ids = [e["id"] for e in gws]
    print(f"{label}: GW{gw_ids[0]}-GW{gw_ids[-1]} ({len(gw_ids)} gameweeks)")
    if unfinished:
        print(f"NOT READY: GW{unfinished} not finished yet.")
        return 2

    winners_path = DATA / "monthly_winners.json"
    winners = json.loads(winners_path.read_text(encoding="utf-8"))
    if any(x["label"] == label for x in winners["months"]):
        print(f"ALREADY RECORDED: {label} is in monthly_winners.json.")
        return 2

    roster = json.loads((DATA / "roster.json").read_text(encoding="utf-8"))["managers"]
    totals = []
    for name, info in roster.items():
        cur = get_json(f"{API}/entry/{info['entry_id']}/history/").get("current", [])
        by_gw = {g["event"]: g["points"] for g in cur}
        pts = [by_gw.get(g, 0) for g in gw_ids]
        totals.append((sum(pts), name, pts))
    totals.sort(key=lambda t: (-t[0], t[1]))

    print("\nTop 5:")
    for total, name, pts in totals[:5]:
        print(f"  {total:4d}  {name}  {pts}")

    top = totals[0][0]
    tied = [t[1] for t in totals if t[0] == top]
    if len(tied) > 1:
        print(f"\nTIE for first on {top} pts: {', '.join(tied)}. Needs a human decision.")
        return 3

    total, winner, _ = totals[0]
    margin = total - totals[1][0]
    print(f"\nWINNER: {winner} with {total} pts (+{margin} on {totals[1][1]})")

    if args.apply:
        prize = winners["months"][-1]["prize_eur"] if winners["months"] else 40
        winners["months"].append({
            "label": label, "gameweeks": gw_ids, "winner": winner,
            "points": total, "prize_eur": prize,
        })
        winners_path.write_text(json.dumps(winners, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"Recorded in {winners_path.name} (prize {prize} EUR). Not committed or pushed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
