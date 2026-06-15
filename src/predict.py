from __future__ import annotations

from pathlib import Path
from typing import Dict

import joblib
import numpy as np

from src.config import CONFIDENCE_THRESHOLD, MODEL_PATH
from src.preprocessing import clean_text


def load_model(model_path: str | Path = MODEL_PATH) -> Dict:
    model_path = Path(model_path)
    if not model_path.exists():
        raise FileNotFoundError(
            f"Model file not found: {model_path}. Run `python scripts/run_training.py` first."
        )
    return joblib.load(model_path)


def predict_sentiment(review_text: str, model_bundle: Dict | None = None, threshold: float = CONFIDENCE_THRESHOLD) -> Dict:
    """Predict Positive, Negative or Neutral sentiment and return confidence."""
    if model_bundle is None:
        model_bundle = load_model()

    model = model_bundle["model"]
    model_name = model_bundle.get("model_name", "Unknown Model")
    classes = list(model.classes_)

    probabilities = None
    if hasattr(model, "predict_proba"):
        probabilities = model.predict_proba([review_text])[0]
        best_idx = int(np.argmax(probabilities))
        predicted = classes[best_idx]
        confidence = float(probabilities[best_idx])
    else:
        predicted = str(model.predict([review_text])[0])
        confidence = 1.0

    # If the model is uncertain, present the result as Neutral. This also supports
    # binary Amazon Reviews files where the original dataset has no explicit neutral class.
    if confidence < threshold:
        displayed_sentiment = "Neutral"
    else:
        displayed_sentiment = predicted

    return {
        "review_text": review_text,
        "clean_review": clean_text(review_text),
        "predicted_sentiment": displayed_sentiment,
        "raw_model_sentiment": predicted,
        "confidence_score": round(confidence, 4),
        "model_name": model_name,
        "class_probabilities": dict(zip(classes, [round(float(p), 4) for p in probabilities])) if probabilities is not None else {},
    }
