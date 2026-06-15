-- SQLite schema for the NLP Sentiment Dashboard
CREATE TABLE IF NOT EXISTS reviews (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    review_text TEXT NOT NULL,
    clean_review TEXT NOT NULL,
    sentiment VARCHAR(20) NOT NULL,
    source VARCHAR(255),
    loaded_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_reviews_sentiment ON reviews(sentiment);

CREATE TABLE IF NOT EXISTS predictions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    review_text TEXT NOT NULL,
    clean_review TEXT NOT NULL,
    predicted_sentiment VARCHAR(20) NOT NULL,
    confidence_score REAL NOT NULL,
    model_name VARCHAR(120) NOT NULL,
    classified_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_predictions_sentiment ON predictions(predicted_sentiment);
CREATE INDEX IF NOT EXISTS idx_predictions_classified_at ON predictions(classified_at);
