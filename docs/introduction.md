# Introduction

This project builds a data warehouse that integrates player feedback from Steam reviews and YouTube comments about Counter-Strike 2, Cyberpunk 2077 and Grand Theft Auto V.

Raw data is first stored in a staging layer, then cleaned, standardized and loaded into a dimensional model that supports analysis by game, source, time, language and feedback characteristics.

## Goals
- A documented, reproducible warehouse
- Incremental loading and data-quality handling
- At least 10 analytical queries
- Measured optimization of at least 5 queries

## Out of scope
Web interface, additional games/platforms, mandatory sentiment analysis, mandatory BI dashboard.

## Approach
1. Prototype with one game and one source
2. Extend to both sources and all three games
3. Add incremental loading and data quality rules
4. Write analytical queries
5. Measure and optimize performance
6. Document and present
