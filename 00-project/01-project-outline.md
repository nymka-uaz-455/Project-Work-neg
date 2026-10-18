---
name: Nyamryenchin Tuvshin
neptun: A0PYWU
id: 2026-LA-03
github: https://github.com/nymka-uaz-455/Project-Work-neg
github_project: 
---

# Player Feedback Data Warehouse

This project develops a data warehouse for collecting, integrating, and analyzing player feedback from Steam reviews and YouTube comments. The system focuses on Counter-Strike 2, Cyberpunk 2077, and Grand Theft Auto V. It uses a staging layer to preserve source data and an ETL/ELT process to clean, standardize, and load feedback into a dimensional data warehouse. The resulting system supports comparisons across games, data sources, time periods, languages, and feedback characteristics. The implementation will focus on reliable data integration, analytical SQL queries, incremental loading, and query performance optimization.

## Objectives
- **Primary objective:** Design and implement a documented, reproducible data warehouse for analyzing player feedback from multiple online sources.
- **Target users / stakeholders:** Database analysts, data engineers, researchers, and people interested in understanding player feedback about video games.
- **Measurable success criteria:** Collect and integrate data from Steam and YouTube for all three selected games; process several hundred thousand records; implement incremental loading; develop at least ten complex analytical SQL queries; and measure and optimize the performance of at least five queries.
- **Constraints:** Use Microsoft SQL Server or Oracle Database, subject to the final technology decision; use official APIs or documented access methods; preserve source traceability and loading timestamps; handle missing values, duplicate records, and inconsistent data formats; maintain version control; and do not store credentials in the repository.

## Scope

### In scope
- Collecting Steam reviews and YouTube comments for the three selected games.
- Implementing a staging layer to store source data and track loading information.
- Comparing dimensional modeling approaches and justifying the selected design.
- Designing fact and dimension tables for game, source, time, language, and feedback characteristics.
- Developing an ETL/ELT process for data cleaning, standardization, integration, and loading.
- Supporting incremental data loading and handling duplicate records.
- Creating at least ten complex analytical SQL queries for temporal trends, game comparisons, source analysis, language distribution, and positive/negative feedback proportions.
- Measuring and optimizing the performance of at least five analytical queries.
- Testing, documenting, and maintaining the system in a Git repository.

### Out of scope
- Developing a complete social-media analytics application or complex web interface.
- Integrating additional games or online platforms beyond the three selected games and the required data sources in the initial version.
- Implementing AI-based sentiment analysis or automatic topic categorization as mandatory features.
- Developing an interactive business intelligence dashboard as a mandatory component.

## Notes

The first prototype will use a small dataset from one selected game and one available data source to validate the extraction, staging, transformation, and loading process. After the basic pipeline works reliably, the implementation will be extended to the second source and all three games. The dimensional model, incremental loading strategy, and query performance will be evaluated throughout development. Additional features may be considered only after the required data warehouse functionality is complete.