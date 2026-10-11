# Requirements checklist

Derived from the project brief (2026-LA-03). Tick items off as they are completed.

## Data
- [ ] Source 1: Steam reviews
- [ ] Source 2: YouTube comments
- [ ] Game 1: Counter-Strike 2
- [ ] Game 2: Cyberpunk 2077
- [ ] Game 3: Grand Theft Auto V
- [ ] Several hundred thousand records in total
- [ ] Official APIs / documented access methods only

## Architecture
- [ ] Staging layer (raw source data + load metadata)
- [ ] Dimensional data warehouse (game, source, time, language, feedback characteristics)
- [ ] Comparison of modeling approaches (shared fact table vs separate fact tables) with justification
- [ ] ETL/ELT pipeline

## Data management
- [ ] Data cleaning and standardization
- [ ] Handling of missing values, duplicates, inconsistent formats
- [ ] Incremental loading
- [ ] Source traceability and load timestamps

## Analysis
- [ ] At least 10 complex analytical SQL queries
  - [ ] temporal trends
  - [ ] game comparison
  - [ ] source comparison
  - [ ] language distribution
  - [ ] positive/negative proportions
- [ ] Performance measurement and optimization of at least 5 queries (before/after)

## Engineering
- [ ] Git repository with regular commits
- [ ] No credentials in the repository
- [ ] Documentation (setup, design, results, limitations)
- [ ] Tests
- [ ] Final presentation

## Out of scope (initial version)
Web UI, extra games/platforms, mandatory sentiment analysis, mandatory BI dashboard.

## Open decisions
- [ ] Database: SQL Server vs Oracle (confirm with supervisor)
- [ ] Shared fact table vs separate fact tables
