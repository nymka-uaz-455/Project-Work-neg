# Functional Specification

Project: Player Feedback Data Warehouse (2026-LA-03)
Author: Nyamryenchin Tuvshin (A0PYWU)

Status legend: **Done** = working and verified | **Written** = code exists, not yet verified on real data | **Planned** = not started

## 1. Purpose

The system collects player feedback about three games from two public sources, stores it unchanged in a staging layer, cleans and integrates it, and loads it into a dimensional data warehouse. Analysts can then compare feedback across games, platforms, time periods and languages with SQL.

## 2. Users

| User | What they do with the system |
|---|---|
| Data engineer (project owner) | Runs the extraction and ETL, monitors loads, fixes data-quality problems |
| Database analyst / researcher | Runs the analytical SQL queries and reads the results |

There is no graphical interface. The system is used through scripts and SQL (web UI and BI dashboard are out of scope).

## 3. Scope

- **Sources:** Steam reviews, YouTube comments
- **Games:** Counter-Strike 2 (Steam app 730), Cyberpunk 2077 (1091500), Grand Theft Auto V (271590)
- **Database:** Microsoft SQL Server (to be confirmed by supervisor)
- **Out of scope:** web application, extra games or platforms, mandatory sentiment analysis, mandatory dashboard

## 4. System overview

```
Steam reviews API ──┐                                      ┌─ dim_game
                    ├─> Extraction ─> Staging ─> ETL ─>    ├─ dim_source
YouTube comments API┘   (Python)      (stg.*)    (SQL+Py)  ├─ dim_date
                                                           ├─ dim_language
                                                           └─ fact_feedback
                                                                   │
                                                          Analytical queries
```

## 5. Functional requirements

### 5.1 Data collection
| ID | Requirement | Status |
|---|---|---|
| FR-01 | Collect Steam reviews for a given game through the public Steam review endpoint, using cursor pagination | Written |
| FR-02 | Collect YouTube comments for chosen videos of each game through the YouTube Data API (commentThreads) | Planned |
| FR-03 | Support all three games for both sources | Planned |
| FR-04 | Keep API keys outside the repository (`.env`, git-ignored) | Done |
| FR-05 | Respect API limits (pause between requests, YouTube daily quota) | Written (Steam), Planned (YouTube) |

### 5.2 Staging layer
| ID | Requirement | Status |
|---|---|---|
| FR-06 | Store raw records per source in `stg` tables without cleaning | Written |
| FR-07 | Record every load in `stg.load_log` (source, game, start/end time, row count, status) | Written |
| FR-08 | Stamp every staged row with `load_id` and `loaded_at` for traceability | Written |
| FR-09 | Do not store personal identifiers that the analysis does not need (player name, profile link, avatar) | Done (by design) |

### 5.3 Transformation and loading (ETL)
| ID | Requirement | Status |
|---|---|---|
| FR-10 | Convert data types (Unix timestamps to dates, flags to bits) | Planned |
| FR-11 | Standardize language names across sources | Planned |
| FR-12 | Handle missing values (empty text, null counts) with documented rules | Planned |
| FR-13 | Remove duplicates using the key (source, source record id) | Planned |
| FR-14 | Load dimensions first, then the fact table, using surrogate keys | Planned |
| FR-15 | Incremental loading: each run loads only records newer than the last successful load | Planned |
| FR-16 | A failed load must not leave partial data in the warehouse | Planned |

### 5.4 Warehouse
| ID | Requirement | Status |
|---|---|---|
| FR-17 | Dimensions: game, source, date, language | Planned |
| FR-18 | Fact table with feedback characteristics (see section 6) | Planned |
| FR-19 | Compare a shared fact table with separate fact tables per source, and justify the choice with measurements | Planned |

### 5.5 Analysis
| ID | Requirement | Status |
|---|---|---|
| FR-20 | At least 10 analytical queries (section 7) | Planned |
| FR-21 | Measure and optimize at least 5 queries (execution plan, time, reads before and after) | Planned |

### 5.6 Quality and documentation
| ID | Requirement | Status |
|---|---|---|
| FR-22 | Automated data-quality tests (row counts, duplicates, nulls, referential integrity) | Planned |
| FR-23 | Git repository with regular commits | Done |
| FR-24 | Documentation: setup, design decisions, results, limitations | In progress |

## 6. Data model (draft)

**Fact table `fact_feedback`:** one row per review or comment.

| Column | Meaning | Steam | YouTube |
|---|---|---|---|
| game_key, source_key, date_key, language_key | links to dimensions | yes | yes |
| source_record_id | original id (traceability, dedup) | recommendationid | comment id |
| text_length | length of the text | yes | yes |
| like_count | helpful votes / likes | votes_up | likeCount |
| reply_count | replies / comments | comment_count | totalReplyCount |
| is_positive | recommended or not | voted_up | not available |
| playtime_hours | author playtime at review | yes | not available |
| load_id | which load brought it in | yes | yes |

**Design question to decide (FR-19):** a shared fact table is simple for cross-source comparison but has columns that are empty for one source. Separate fact tables fit each source better but need a UNION for comparison. The decision will be based on query simplicity and measured performance.

## 7. Planned analytical queries

1. Reviews and comments per game per month (temporal trend)
2. Share of positive Steam reviews per game per month
3. Game comparison: volume, average text length, average likes
4. Source comparison: Steam vs YouTube volume per game
5. Language distribution per game (top 10 languages)
6. Languages whose positive share differs most from the average
7. Peak activity days (spikes around updates or events)
8. Relationship between playtime and positive/negative reviews
9. Most-liked feedback per game per source
10. Month-over-month growth with a window function

Queries 1, 3, 5, 7 and 10 are the first candidates for performance optimization (indexes, columnstore, partitioning, statistics).

## 8. Non-functional requirements

- **Reproducible:** a new user can rebuild everything from the repository and the README
- **Traceable:** every warehouse row can be linked to its source and load
- **Scalable:** works with several hundred thousand records, tested with increasing volumes
- **Secure:** no credentials in the repository

## 9. Testing approach

- Row-count reconciliation between staging and warehouse
- Duplicate check on (source, source record id)
- Null and range checks on key columns
- Referential integrity between fact and dimensions
- Re-running a load must not create duplicates (idempotence)
- Query results checked against a small hand-calculated sample

## 10. Risks and limitations

| Risk / limitation | Plan |
|---|---|
| YouTube comments have no positive/negative label, so positive-share queries only apply to Steam | State this clearly; sentiment analysis is out of scope. Discuss with supervisor whether a simple approach is wanted |
| YouTube API daily quota | Collect over several days, store progress in `load_log` |
| Some videos have comments disabled | Skip and log them |
| Steam returns reviews in many languages, with inconsistent names | Standardize in a language dimension |
| Steam's review endpoint is public but undocumented-limit; heavy use may be rate limited | Pause between requests, resume from the cursor |
| Data volume target not yet reached | Monitor row counts per game; add more videos if needed |

## 11. Milestones

| # | Milestone | Status |
|---|---|---|
| M1 | Repository, structure, requirements | Done |
| M2 | Staging schema + Steam prototype (one game) | Written, to be verified |
| M3 | Dimensional model decision + warehouse tables | Planned |
| M4 | ETL for Steam | Planned |
| M5 | YouTube extraction + all three games | Planned |
| M6 | Cleaning, deduplication, incremental loading | Planned |
| M7 | 10 analytical queries | Planned |
| M8 | Performance measurement and optimization | Planned |
| M9 | Final documentation and presentation | Planned |
