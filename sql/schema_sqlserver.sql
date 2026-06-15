-- SQL Server compatible schema for students who want to deploy on Microsoft SQL Server
IF OBJECT_ID('dbo.predictions', 'U') IS NOT NULL DROP TABLE dbo.predictions;
IF OBJECT_ID('dbo.reviews', 'U') IS NOT NULL DROP TABLE dbo.reviews;
GO

CREATE TABLE dbo.reviews (
    id INT IDENTITY(1,1) PRIMARY KEY,
    review_text NVARCHAR(MAX) NOT NULL,
    clean_review NVARCHAR(MAX) NOT NULL,
    sentiment NVARCHAR(20) NOT NULL,
    source NVARCHAR(255) NULL,
    loaded_at DATETIME2 NOT NULL DEFAULT SYSUTCDATETIME()
);
GO

CREATE INDEX IX_reviews_sentiment ON dbo.reviews(sentiment);
GO

CREATE TABLE dbo.predictions (
    id INT IDENTITY(1,1) PRIMARY KEY,
    review_text NVARCHAR(MAX) NOT NULL,
    clean_review NVARCHAR(MAX) NOT NULL,
    predicted_sentiment NVARCHAR(20) NOT NULL,
    confidence_score FLOAT NOT NULL,
    model_name NVARCHAR(120) NOT NULL,
    classified_at DATETIME2 NOT NULL DEFAULT SYSUTCDATETIME()
);
GO

CREATE INDEX IX_predictions_sentiment ON dbo.predictions(predicted_sentiment);
CREATE INDEX IX_predictions_classified_at ON dbo.predictions(classified_at);
GO
