from pathlib import Path
import sys

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.data_loader import _normalise_sentiment, load_reviews


def test_rating_values_are_mapped_as_star_ratings(tmp_path):
    dataset = tmp_path / "ratings.csv"
    pd.DataFrame(
        {
            "review_text": ["bad", "poor", "okay", "good", "excellent"],
            "rating": [1, 2, 3, 4, 5],
        }
    ).to_csv(dataset, index=False)

    df = load_reviews(dataset)
    assert df["sentiment"].tolist() == ["Negative", "Negative", "Neutral", "Positive", "Positive"]


def test_feedback_values_are_mapped_as_binary_feedback(tmp_path):
    dataset = tmp_path / "feedback.csv"
    pd.DataFrame(
        {
            "verified_reviews": ["did not work", "works well"],
            "feedback": [0, 1],
        }
    ).to_csv(dataset, index=False)

    df = load_reviews(dataset)
    assert df["sentiment"].tolist() == ["Negative", "Positive"]


def test_fasttext_labels_are_mapped_correctly():
    assert _normalise_sentiment("__label__1", label_column="fasttext_label") == "Negative"
    assert _normalise_sentiment("__label__2", label_column="fasttext_label") == "Positive"
