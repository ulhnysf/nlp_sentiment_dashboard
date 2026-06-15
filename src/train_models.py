from __future__ import annotations

import argparse
from pathlib import Path
from typing import Dict, Tuple

import joblib
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.calibration import CalibratedClassifierCV
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    ConfusionMatrixDisplay,
    accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
)
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.svm import LinearSVC
from sklearn.feature_extraction.text import TfidfVectorizer

from src.config import (
    CONFUSION_MATRIX_PATH,
    FIGURE_DIR,
    METRICS_PATH,
    MODEL_COMPARISON_PATH,
    MODEL_DIR,
    MODEL_PATH,
    PROCESSED_DATA_PATH,
    RANDOM_STATE,
    WORD_FREQUENCY_PATH,
)
from src.data_loader import load_reviews, save_processed_dataset
from src.database import load_reviews_to_db
from src.preprocessing import clean_text, tokenize

MODEL_DEFINITIONS = {
    "Logistic Regression": LogisticRegression(max_iter=1000, class_weight="balanced", random_state=RANDOM_STATE),
    "Naive Bayes": MultinomialNB(),
    "Support Vector Machine": CalibratedClassifierCV(LinearSVC(class_weight="balanced", random_state=RANDOM_STATE)),
}


def build_pipeline(model_name: str) -> Pipeline:
    return Pipeline(
        steps=[
            ("tfidf", TfidfVectorizer(preprocessor=clean_text, tokenizer=str.split, token_pattern=None, ngram_range=(1, 2), min_df=1)),
            ("classifier", MODEL_DEFINITIONS[model_name]),
        ]
    )


def _safe_stratify(y: pd.Series):
    counts = y.value_counts()
    return y if len(counts) > 1 and counts.min() >= 2 else None


def evaluate_models(df: pd.DataFrame) -> Tuple[Dict[str, Pipeline], pd.DataFrame, str, pd.Series, pd.Series]:
    X = df["review_text"]
    y = df["sentiment"]
    stratify = _safe_stratify(y)
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.25,
        random_state=RANDOM_STATE,
        stratify=stratify,
    )

    trained_models: Dict[str, Pipeline] = {}
    rows = []
    for name in MODEL_DEFINITIONS:
        model = build_pipeline(name)
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        rows.append(
            {
                "model": name,
                "accuracy": accuracy_score(y_test, y_pred),
                "precision_macro": precision_score(y_test, y_pred, average="macro", zero_division=0),
                "recall_macro": recall_score(y_test, y_pred, average="macro", zero_division=0),
                "f1_macro": f1_score(y_test, y_pred, average="macro", zero_division=0),
            }
        )
        report = classification_report(y_test, y_pred, zero_division=0)
        print(f"\n{name}\n{report}")
        trained_models[name] = model

    metrics = pd.DataFrame(rows).sort_values(by="f1_macro", ascending=False).reset_index(drop=True)
    best_model_name = metrics.iloc[0]["model"]
    return trained_models, metrics, best_model_name, X_test, y_test


def save_model_comparison(metrics: pd.DataFrame, path: Path = MODEL_COMPARISON_PATH) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    ax = metrics.set_index("model")[["accuracy", "precision_macro", "recall_macro", "f1_macro"]].plot(kind="bar", figsize=(10, 6))
    ax.set_title("Model Performance Comparison")
    ax.set_ylabel("Score")
    ax.set_ylim(0, 1)
    ax.legend(loc="lower right")
    plt.xticks(rotation=20, ha="right")
    plt.tight_layout()
    plt.savefig(path, dpi=160)
    plt.close()


def save_confusion_matrix(model: Pipeline, X_test: pd.Series, y_test: pd.Series, path: Path = CONFUSION_MATRIX_PATH) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    labels = sorted(y_test.unique())
    y_pred = model.predict(X_test)
    cm = confusion_matrix(y_test, y_pred, labels=labels)
    disp = ConfusionMatrixDisplay(cm, display_labels=labels)
    disp.plot(cmap=None, values_format="d")
    plt.title("Confusion Matrix - Best Model")
    plt.tight_layout()
    plt.savefig(path, dpi=160)
    plt.close()


def save_word_frequency(df: pd.DataFrame, path: Path = WORD_FREQUENCY_PATH, top_n: int = 20) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tokens = []
    for text in df["review_text"]:
        tokens.extend(tokenize(text))
    freq = pd.Series(tokens).value_counts().head(top_n).sort_values()
    ax = freq.plot(kind="barh", figsize=(9, 7))
    ax.set_title("Most Frequent Words")
    ax.set_xlabel("Frequency")
    plt.tight_layout()
    plt.savefig(path, dpi=160)
    plt.close()


def train_and_save(dataset_path: str | None = None, limit: int | None = None, load_db: bool = True) -> dict:
    MODEL_DIR.mkdir(parents=True, exist_ok=True)
    FIGURE_DIR.mkdir(parents=True, exist_ok=True)

    df = load_reviews(dataset_path, limit=limit)
    save_processed_dataset(df, PROCESSED_DATA_PATH)
    if load_db:
        load_reviews_to_db(df)

    trained_models, metrics, best_model_name, X_test, y_test = evaluate_models(df)
    best_model = trained_models[best_model_name]
    joblib.dump({"model": best_model, "model_name": best_model_name, "labels": sorted(df["sentiment"].unique())}, MODEL_PATH)
    metrics.to_csv(METRICS_PATH, index=False)
    save_model_comparison(metrics)
    save_confusion_matrix(best_model, X_test, y_test)
    save_word_frequency(df)

    return {
        "rows": len(df),
        "labels": df["sentiment"].value_counts().to_dict(),
        "best_model": best_model_name,
        "model_path": str(MODEL_PATH),
        "metrics_path": str(METRICS_PATH),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Train sentiment analysis models and save the best model.")
    parser.add_argument("--dataset", type=str, default=None, help="Path to CSV, TXT, or TXT.BZ2 dataset.")
    parser.add_argument("--limit", type=int, default=None, help="Optional row limit for large Kaggle files.")
    parser.add_argument("--no-db", action="store_true", help="Do not load processed reviews into SQL database.")
    args = parser.parse_args()
    summary = train_and_save(args.dataset, args.limit, load_db=not args.no_db)
    print("Training completed:", summary)


if __name__ == "__main__":
    main()
