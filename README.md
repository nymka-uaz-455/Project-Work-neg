# Player Feedback Data Warehouse

Data warehouse for collecting, integrating and analyzing player feedback from **Steam reviews** and **YouTube comments** for **Counter-Strike 2**, **Cyberpunk 2077** and **Grand Theft Auto V**.

Project ID: 2026-LA-03 | Author: Nyamryenchin Tuvshin (A0PYWU)

## Architecture (planned)

```
Steam API ─┐                                   ┌─ dim_game
           ├─> extraction ─> staging ─> ETL ─> ├─ dim_source
YouTube API┘   (src/extraction)  (database/staging)  (src/etl)  ├─ dim_date
                                               ├─ dim_language
                                               └─ fact_feedback
```

## Repository layout

| Path | Purpose |
|---|---|
| `docs/` | Introduction, requirements, architecture, design decisions |
| `database/staging/` | Staging-layer DDL |
| `database/warehouse/` | Dimensional model DDL (dims, facts, indexes) |
| `database/queries/` | The 10+ analytical queries |
| `src/extraction/` | Steam / YouTube collectors |
| `src/etl/` | Cleaning, deduplication, incremental loading |
| `tests/` | Data-quality and pipeline tests |
| `results/` | Query timings, execution plans, before/after optimization |

## Setup

github.com/nymka-uaz-455/Project-work-neg/: database installation, Python environment, API keys (via `.env`, never committed), how to run the pipeline.

## Status

See `docs/requirements.md` for the checklist.
