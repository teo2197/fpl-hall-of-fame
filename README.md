# FPL Hall of Fame — v2

The original `fpl_hof_visual.py` (documented in the old `CLAUDE.md`) was lost, and its
source league (#37044) was recreated under a new ID at some point, breaking live
tracking. This rebuilds the same site from clean, versioned data files instead of one
hardcoded script, and fixes a data bug found in the old output along the way (see
"Known fixes" below).

## Files

- `data/roster.json` — active managers tracked live: name → FPL entry_id + join season.
  League #37785 ("Classics League"), admin = Matteo Ebejer.
- `data/archive.json` — names of managers who are **not** in the current league
  (haven't rejoined as of 2026-08-20) and whose data is permanently frozen.
- `data/history_seed.json` — the full verified per-manager historical record through
  2025/26, extracted from the last known-good generated site. This is the source of
  truth for every season up to and including 2025/26 for ALL 26 original managers
  (both the 22 who are still active and the 4 in `archive.json`).
- `data/known_seasons.json` — the curated winner/runner-up record per season
  (2016/17–2025/26). This is what actually drives the season cards and the Hall of
  Fame table — deliberately kept separate from `history_seed.json` so the two can be
  cross-checked against each other (this separation is what caught the 2018/19 bug).
- `fpl_hof.py` — fetches live data, merges it with the frozen files above, computes
  every derived stat (wins, consistency, best/worst rank, etc).
- `fpl_hof_render.py` — turns that data into `fpl_hall_of_fame_visual.html`.

## Running it

```
python fpl_hof.py
```

Requires `pip install requests` (Python 3.12+ confirmed working). Output is written
to `fpl_hall_of_fame_visual.html` in this folder — open it directly or upload it to
Netlify same as before.

## How the season lifecycle works

- **Past seasons (2016/17–2025/26)**: frozen in `known_seasons.json` /
  `history_seed.json`. The script never rewrites these on its own.
- **Current season** (auto-computed from today's date, e.g. `2026/27`): fetched live
  from each roster member's FPL entry history. Shown in the console output when you
  run the script, but *not* added to the Hall of Fame table/season cards yet — it's
  provisional until the season ends.
- **When a season finishes**: run the script, note the winner/runner-up it prints,
  and manually add that season as a new entry in `data/known_seasons.json` (same
  shape as the existing entries) to freeze it permanently. This mirrors how the
  original script's `KNOWN` dict was manually curated — deliberately, so a single
  automated pass can never silently corrupt a past season's record.

## Roster changes

- **Someone leaves the league / doesn't rejoin**: move their name from
  `roster.json` into `archive.json`'s `frozen_managers` list. Their existing data in
  `history_seed.json` stays as the permanent record; the script stops trying to
  fetch new data for them.
- **Someone new joins**: add them to `roster.json` with their `entry_id` (from
  `https://fantasy.premierleague.com/api/leagues-classic/37785/standings/`) and
  `join` set to the season they joined.

## Known fixes vs. the original site

- **2018/19 rank for Matteo Ebejer** was hardcoded as `46,860` (his actual *2019/20*
  rank — the two seasons had identical points, 2,302, which is almost certainly what
  caused the mix-up). Corrected to the true value, `56,628`, verified directly
  against `https://fantasy.premierleague.com/api/entry/184140/history/` on
  2026-08-20. This also means the "Mr. Consistent" average is now computed from
  correct inputs (previously it happened to use the right numbers by coincidence,
  since it read from per-manager data rather than the buggy hardcoded table).
- Rounding for the consistency leaderboard now matches JS `Math.round`'s
  round-half-up behaviour exactly, rather than Python's default round-half-to-even.
- Standings ties are now broken by rank (ascending), matching the original's
  ordering when two managers have identical points in the same season.

## Not carried over from the old league

Four managers from the original 26 haven't (yet) rejoined league #37785 as of
2026-08-20 and have no known `entry_id`: **Andrew Borg, Fran Demicoli, Chrisi H.,
and the original "Adam A"** (a different person named "Adam Ryan" joined the new
league — confirmed via FPL history mismatch, not the same account). Their historical
stats are preserved via `archive.json`. If any of them rejoin, move them back into
`roster.json` with their entry_id once you have it.

Six new people joined the recreated league who weren't in the original Hall of Fame:
Adam Ryan, Erik Gollcher, Luca Brincat, Eamonn Mifsud, Sean Abela, Ben Caruana — all
added to `roster.json` with `join: "2026/27"`. They won't appear in any table until
they've actually played a gameweek (profiles with zero recorded seasons are filtered
out of the All-Time table and the hero manager count).
