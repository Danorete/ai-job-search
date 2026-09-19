# MaternalGrid

Georgia labor & delivery access simulation. Models how facility closures and
openings change drive-time access across all 159 counties.

The product specification and technical roadmap is [`../MaternalGrid_DEMO.md`](../MaternalGrid_DEMO.md).

## Contents

| Path | What it is |
|---|---|
| `MaternalGrid_Dashboard.html` | **The demo.** Single self-contained file — open it in a browser, no server |
| `build_dashboard.py` + `dashboard.css` | Source the dashboard is generated from |
| `data/maternalgrid_data.json` | 159 counties + 72 facilities + verified baseline (35 KB) |
| `data/county_cells.json` | Voronoi county polygons derived from the centroids |
| `migration/` | TigerData migration: schema, ETL, load, verification, app queries |
| `migration/server/` | Node/TypeScript API layer against Tiger Cloud |
| `copilot-knowledge/` | Grounding corpus for a Copilot Studio agent |

## Verified baseline

Every surface reproduces these figures from GDPH OASIS 2024 and March of Dimes 2026:

| Metric | Value |
|---|---|
| Counties beyond 30 modeled minutes | **74 / 159 (46.5%)** |
| Annual births beyond 30 minutes | **13,029** |
| Births-weighted average drive time | **11.1 min** |
| March of Dimes maternity care deserts | **70 / 159 (44.0%)** |
| Active delivering facilities | **68** (62 in-state + 6 border) |

The dashboard logs a self-check against these on load; `migration/sql/005_verify.sql`
asserts them as an 18-check gate on every database load.

## Running the demo

Open `MaternalGrid_Dashboard.html`. Present at **1280px wide or more** — below
~1150px the layout stacks to one column. The assistant widget can be hidden
(hover it, click ×) so it never covers the table.

Tour: **1 Current crisis** → **2 Stress test (Lavonia closure)** → **3 Strategic
remedy (Effingham expansion)**.

## Standing up the data layer

See [`migration/README.md`](migration/README.md). Read
[`migration/DATA_PROVENANCE.md`](migration/DATA_PROVENANCE.md) before quoting any
figure — it records which source fields were verified and which were rejected as
synthetic.

## Known limits

- Modeled travel time is Haversine × 1.30 road factor ÷ 45 mph. **Not routed drive
  time** — no traffic, weather, or time of day. Confidence grade B.
- Map cells are **Voronoi catchments around county centroids**, not surveyed county
  boundaries. Census TIGER boundaries drop in without changing the model.
- L&D capacity is a **level-weighted proxy, grade C** — no licensed bed counts exist
  in the dataset.
- `women_15_44` and OB provider counts are deliberately absent; the only available
  source for them was synthetic (see DATA_PROVENANCE.md).
