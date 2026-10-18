---
name: Nyamryenchin Tuvshin
neptun: A0PYWU
id: 2026-LA-03
---
# Player Feedback Data Warehouse

## My interpretation of the brief
The goal of this project is to design and implement a data warehouse that collects and analyzes player feedback from multiple online sources. The project focuses on three video games: Counter-Strike 2, Cyberpunk 2077, and Grand Theft Auto V. The main data sources will be Steam reviews and YouTube comments.

The collected data will first be stored in a staging layer and then processed using an ETL or ELT pipeline to clean, standardize, and integrate information from different sources. The processed data will be organized into a dimensional data warehouse that supports analysis by game, source, time, language, and feedback characteristics.

The system should also support incremental data loading, data quality management, and efficient analytical SQL queries. An important part of the project will be comparing different dimensional modeling approaches and evaluating query performance through measurements and optimization.

The final result should be a working, documented, and reproducible data warehouse that enables meaningful comparisons of player feedback across games and platforms.
## Why I am a good fit for this project
As a third-year Computer Science Engineering student, I want to strengthen my practical knowledge of database management, data processing, and software engineering. This project is a good opportunity to apply my existing programming knowledge to a realistic data engineering problem.

I am particularly interested in learning how data from different sources can be integrated into a consistent structure and used to answer analytical questions. I am also motivated to improve my SQL skills, understand dimensional data modeling, and gain experience with ETL/ELT pipelines and query performance optimization.

I believe this project will help me develop both my technical problem-solving skills and my ability to design, implement, test, and document a complete software system.
## Relevant experience and background
As a Computer Science student, I have built a solid understanding of fundamental software engineering principles, algorithm complexity, data structures, and object-oriented programming.

## Proposed approach
I plan to approach the project in several stages.

First, I will investigate the available data sources and identify the relevant fields, access methods, and limitations of collecting Steam reviews and YouTube comments. I will then compare possible dimensional data warehouse designs, including a shared fact table and separate fact tables, and justify the selected approach.

Next, I will design the staging layer and the warehouse schema, including the necessary fact and dimension tables. I will develop an ETL or ELT process to clean, standardize, deduplicate, and load data from the different sources while preserving source information and loading timestamps.

After implementing the basic pipeline, I will add incremental data loading and test the system with increasing data volumes. I will create analytical SQL queries to compare feedback across games, platforms, time periods, and languages. Finally, I will measure query performance, investigate suitable optimization techniques, and document the implementation, testing, results, and limitations.

I plan to use Git for version control throughout development so that changes, improvements, and the progress of the project remain traceable.
## Initial plan
My initial plan is to:

Analyze the project requirements and investigate the available data sources.

Select the database technology and data collection methods.

Create a Git repository and establish the project structure.

Compare dimensional modeling alternatives and design the database schema.

Implement the staging layer and create a small working prototype using a limited dataset.

Develop the ETL/ELT pipeline and implement the dimensional data warehouse.

Add data cleaning, duplicate handling, and incremental loading.

Develop at least ten analytical SQL queries covering the required comparisons and trends.

Measure and optimize the performance of at least five queries.

Test the system, document the results, and prepare the final presentation.

My priority will be to build a correct and reproducible data pipeline first, then improve its scalability, analytical capabilities, and performance.