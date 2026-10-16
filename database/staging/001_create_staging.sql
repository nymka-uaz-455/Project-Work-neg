-- Staging layer: raw source data + load metadata.
-- Run after 000_create_database.sql.
USE PlayerFeedbackDW;
GO

IF SCHEMA_ID(N'stg') IS NULL EXEC(N'CREATE SCHEMA stg');
GO

-- One row per extraction run (traceability + incremental loading support)
IF OBJECT_ID(N'stg.load_log') IS NULL
CREATE TABLE stg.load_log (
    load_id        INT IDENTITY(1,1) PRIMARY KEY,
    source_name    NVARCHAR(30)  NOT NULL,          -- 'steam' | 'youtube'
    game_name      NVARCHAR(100) NOT NULL,
    source_game_id NVARCHAR(50)  NOT NULL,          -- Steam app id / YouTube video id
    started_at     DATETIME2(0)  NOT NULL DEFAULT SYSUTCDATETIME(),
    finished_at    DATETIME2(0)  NULL,
    rows_loaded    INT           NULL,
    status         NVARCHAR(20)  NOT NULL DEFAULT N'running'  -- running | success | failed
);
GO

-- Raw Steam reviews, kept close to the API response.
-- No cleaning here: duplicates are allowed, dedup happens in the ETL step.
IF OBJECT_ID(N'stg.steam_review') IS NULL
CREATE TABLE stg.steam_review (
    stg_id                    BIGINT IDENTITY(1,1) PRIMARY KEY,
    load_id                   INT           NOT NULL REFERENCES stg.load_log(load_id),
    loaded_at                 DATETIME2(0)  NOT NULL DEFAULT SYSUTCDATETIME(),
    app_id                    INT           NOT NULL,
    game_name                 NVARCHAR(100) NOT NULL,
    recommendation_id         NVARCHAR(30)  NOT NULL,   -- Steam's unique review id
    author_steamid            NVARCHAR(30)  NULL,
    author_num_games_owned    INT           NULL,
    author_num_reviews        INT           NULL,
    author_playtime_forever   INT           NULL,       -- minutes
    author_playtime_at_review INT           NULL,       -- minutes
    language                  NVARCHAR(30)  NULL,
    review_text               NVARCHAR(MAX) NULL,
    timestamp_created         BIGINT        NULL,       -- unix seconds
    timestamp_updated         BIGINT        NULL,
    voted_up                  BIT           NULL,
    votes_up                  INT           NULL,
    votes_funny               INT           NULL,
    weighted_vote_score       FLOAT         NULL,
    comment_count             INT           NULL,
    steam_purchase            BIT           NULL,
    received_for_free         BIT           NULL,
    written_during_early_access BIT         NULL
);
GO

CREATE INDEX ix_steam_review_recid ON stg.steam_review (app_id, recommendation_id);
GO
