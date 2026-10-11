# Architecture

Draft. Fill in as decisions are made.

## Layers
1. **Extraction** (`src/extraction/`): pulls raw data from the Steam and YouTube APIs.
2. **Staging** (`database/staging/`): raw records plus `source_name`, `load_id`, `loaded_at`.
3. **ETL** (`src/etl/`): clean, deduplicate, standardize, load.
4. **Warehouse** (`database/warehouse/`): dimensional model.

## Candidate dimensional designs
| | A: One shared fact table | B: Separate fact tables per source |
|---|---|---|
| Cross-source queries | Simple | Need UNION / conformed dims |
| Source-specific attributes | Nullable columns or side table | Natural fit |
| Query speed | Single large table | Smaller tables |

Decision: TBD (justify with measurements later).

## Dimensions (draft)
- `dim_game`, `dim_source`, `dim_date`, `dim_language`
- Feedback characteristics: recommended flag (Steam), likes / helpful votes, text length

## Incremental loading (draft)
- Steam: cursor-based pagination, keep last loaded review timestamp/ID per game
- YouTube: track last published time per video
- Deduplicate on (source, source_record_id)

## Technology
Database: TBD (SQL Server or Oracle). Language for extraction/ETL: TBD (Python suggested).
