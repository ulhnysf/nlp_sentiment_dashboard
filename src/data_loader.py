from __future__ import annotations

import bz2
from pathlib import Path
from typing import Optional

import pandas as pd

from src.config import PROCESSED_DATA_PATH, SAMPLE_DATA_PATH
from src.preprocessing import clean_text

TEXT_COLUMN_CANDIDATES = [
    "review_text", "review", "reviews", "verified_reviews", "text", "content", "summary"
]
LABEL_COLUMN_CANDIDATES = [
    "sentiment", "label", "feedback", "rating", "score", "overall"
]


def _normalise_sentiment(value) -> Optional[str]:
    """Map common Kaggle label/rating formats to Positive/Negative/Neutral."""
    if pd.isna(value):
        return None

    value_str = str(value).strip().lower()

    if value_str in {"positive", "pos", "p", "__label__2", "2", "1.0"}:
        # In the Amazon Reviews fastText dataset, __label__2 means positive.
        return "Positive"
    if value_str in {"negative", "neg", "n", "__label__1", "0", "0.0"}:
        # In the Amazon Reviews fastText dataset, __label__1 means negative.
        return "Negative"
    if value_str in {"neutral", "neu", "3", "3.0"}:
        return "Neutral"

    try:
        rating = float(value_str)
        if rating <= 2:
            return "Negative"
        if rating == 3:
            return "Neutral"
        if rating >= 4:
            return "Positive"
    except ValueError:
        return None

    return None


def _read_fasttext_file(path: Path, limit: Optional[int] = None) -> pd.DataFrame:
    """Read files like train.ft.txt / test.ft.txt from the bittlingmayer Amazon Reviews dataset."""
    opener = bz2.open if path.suffix == ".bz2" else open
    records = []
    with opener(path, "rt", encoding="utf-8", errors="ignore") as handle:
        for idx, line in enumerate(handle):
            if limit is not None and idx >= limit:
                break
            line = line.strip()
            if not line:
                continue
            if line.startswith("__label__"):
                label, _, text = line.partition(" ")
                records.append({"review_text": text, "sentiment": _normalise_sentiment(label), "source": path.name})
    return pd.DataFrame(records)


def _detect_text_column(df: pd.DataFrame) -> str:
    for col in TEXT_COLUMN_CANDIDATES:
        if col in df.columns:
            return col
    object_cols = [col for col in df.columns if df[col].dtype == "object"]
    if object_cols:
        return object_cols[0]
    raise ValueError("No text column found. Rename your review column to 'review_text'.")


def _detect_label_column(df: pd.DataFrame) -> str:
    for col in LABEL_COLUMN_CANDIDATES:
        if col in df.columns:
            return col
    raise ValueError("No label/rating column found. Use 'sentiment', 'label', 'feedback' or 'rating'.")


def load_reviews(path: Optional[str | Path] = None, limit: Optional[int] = None) -> pd.DataFrame:
    """Load sample data, Alexa-style CSV data, or Amazon Reviews fastText files."""
    path = Path(path) if path else SAMPLE_DATA_PATH
    if not path.exists():
        raise FileNotFoundError(f"Dataset not found: {path}")

    if path.suffix in {".txt", ".bz2"} or path.name.endswith(".txt.bz2"):
        df = _read_fasttext_file(path, limit=limit)
    else:
        df = pd.read_csv(path)
        text_col = _detect_text_column(df)
        label_col = _detect_label_column(df)
        df = df[[text_col, label_col]].rename(columns={text_col: "review_text", label_col: "sentiment"})
        df["sentiment"] = df["sentiment"].apply(_normalise_sentiment)
        df["source"] = path.name
        if limit:
            df = df.head(limit)

    df = df.dropna(subset=["review_text", "sentiment"]).copy()
    df["review_text"] = df["review_text"].astype(str).str.strip()
    df = df[df["review_text"].str.len() > 0]
    df["clean_review"] = df["review_text"].apply(clean_text)
    df = df[df["clean_review"].str.len() > 0]
    df = df.drop_duplicates(subset=["review_text"])
    return df.reset_index(drop=True)


def save_processed_dataset(df: pd.DataFrame, path: Path = PROCESSED_DATA_PATH) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False)
    return path
