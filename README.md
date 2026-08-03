# Fantasy Football League Median Standings

_Created by Noah Ford_

Live site: [nhford.github.io/median-standings](https://nhford.github.io/median-standings)

My fantasy football league's platform, ESPN, includes "Bonus Wins": each week you can earn a win for beating your opponent, plus a bonus win for scoring in the top half of the league (a win against the median on other platforms).

ESPN only shows your chance to beat your current opponent, not your chance to finish in the top 50%. The same percentile math also estimates your chance of finishing as the top-scoring team, which matters in our league because that team earns part of the buy-in pool.

## How it works

`backend/median-np.py` runs Monte Carlo simulations with a gamma distribution around each player's ESPN projected points, sums team totals, and ranks teams to estimate median and payout probabilities.

This methodology is imperfect: gamma is a rough fit for player scoring, and ESPN projections aren't always true means. Individual team totals are more variable than real results; a large simulation count dampens that noise in the aggregate percentages.

## Stack

- Next.js (static export) + React + Tailwind, deployed to GitHub Pages
- Python scraper/simulator using `espn-api`, NumPy, SciPy, and pandas

## Local setup

### Frontend

```bash
npm install
npm run dev
```

### Backend (refresh standings)

1. Copy `.env.example` to `.env` and fill in ESPN cookies from your browser session on espn.com (`espn_s2`, `SWID`).
2. Install Python deps and run the script from the repo root:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r backend/requirements.txt
python backend/median-np.py
```

That writes `app/standings.json`, `app/metadata.json`, and an archive snapshot under `backend/archive/`.

## GitHub Actions

Scheduled and manual runs need repository secrets:

- `ESPN_S2`
- `ESPN_SWID`

Optional repository variables: `ESPN_LEAGUE_ID`, `ESPN_SEASON_ID`.

If those cookies were ever committed in plaintext, rotate them in ESPN/your browser session and update the secrets.
