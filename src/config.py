from __future__ import annotations

import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
MODEL_DIR = BASE_DIR / "models"
REPORT_DIR = BASE_DIR / "reports"
FIGURE_DIR = REPORT_DIR / "figures"
SQL_DIR = BASE_DIR / "sql"

SAMPLE_DATA_PATH = RAW_DATA_DIR / "sample_reviews.csv"
PROCESSED_DATA_PATH = PROCESSED_DATA_DIR / "processed_reviews.csv"
MODEL_PATH = MODEL_DIR / "best_model.joblib"
METRICS_PATH = MODEL_DIR / "model_metrics.csv"
CONFUSION_MATRIX_PATH = FIGURE_DIR / "confusion_matrix.png"
MODEL_COMPARISON_PATH = FIGURE_DIR / "model_comparison.png"
WORD_FREQUENCY_PATH = FIGURE_DIR / "word_frequency.png"

DATABASE_URL = os.getenv("DATABASE_URL", f"sqlite:///{BASE_DIR / 'sentiment_dashboard.db'}")
CONFIDENCE_THRESHOLD = float(os.getenv("CONFIDENCE_THRESHOLD", "0.80"))
RANDOM_STATE = int(os.getenv("RANDOM_STATE", "42"))
