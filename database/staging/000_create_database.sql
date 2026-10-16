-- Run this first, connected to the master database (SSMS default).
IF DB_ID(N'PlayerFeedbackDW') IS NULL
    CREATE DATABASE PlayerFeedbackDW;
GO
