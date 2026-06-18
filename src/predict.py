from __future__ import annotations

from pathlib import Path
from typing import Dict, Optional, Tuple
import unicodedata

import joblib
import numpy as np

from src.config import CONFIDENCE_THRESHOLD, MODEL_PATH
from src.preprocessing import clean_text


TURKISH_NEGATIVE_TERMS = {
    "berbat", "kotu", "k?t?", "cok kotu", "?ok k?t?", "rezalet", "begenmedim",
    "hic begenmedim", "hayal kirikligi", "ise yaramaz",
    "bozuk", "kalitesiz", "pismanim", "nefret", "vasat",
    "sorunlu", "korkunc", "iade", "memnun kalmadim"
}

TURKISH_POSITIVE_TERMS = {
    "harika", "mukemmel", "m?kemmel", "cok iyi", "super", "begendim",
    "tavsiye ederim", "memnun kaldim", "kaliteli", "basarili",
    "guzel", "efsane", "muthis", "sorunsuz", "sevdim"
}

TURKISH_NEUTRAL_TERMS = {
    "idare eder", "?dare eder", "orta", "ortalama", "normal", "fena degil",
    "eh iste", "siradan", "ne iyi ne kotu"
}


def normalize_for_rules(text: str) -> str:
    value = str(text).casefold()
    value = value.replace("?", "i").replace("?", "i")
    value = value.replace("?", "c").replace("?", "g")
    value = value.replace("?", "o").replace("?", "s")
    value = value.replace("?", "u")
    value = unicodedata.normalize("NFKD", value)
    value = "".join(ch for ch in value if not unicodedata.combining(ch))
    return value


def load_model(model_path: str | Path = MODEL_PATH) -> Dict:
    model_path = Path(model_path)
    if not model_path.exists():
        raise FileNotFoundError(
            f"Model file not found: {model_path}. Run `python scripts/run_training.py` first."
        )
    return joblib.load(model_path)


def rule_based_turkish_sentiment(text: str) -> Tuple[Optional[str], Optional[float]]:
    normalized = normalize_for_rules(text)

    neutral_hits = sum(1 for term in TURKISH_NEUTRAL_TERMS if term in normalized)
    negative_hits = sum(1 for term in TURKISH_NEGATIVE_TERMS if term in normalized)
    positive_hits = sum(1 for term in TURKISH_POSITIVE_TERMS if term in normalized)

    if neutral_hits > 0 and negative_hits == 0 and positive_hits == 0:
        return "Neutral", 0.80

    if negative_hits > positive_hits and negative_hits > 0:
        return "Negative", 0.95

    if positive_hits > negative_hits and positive_hits > 0:
        return "Positive", 0.95

    if neutral_hits > 0:
        return "Neutral", 0.80

    return None, None


def predict_sentiment(
    review_text: str,
    model_bundle: Dict | None = None,
    threshold: float = CONFIDENCE_THRESHOLD
) -> Dict:
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

    rule_sentiment, rule_confidence = rule_based_turkish_sentiment(review_text)

    if rule_sentiment is not None:
        displayed_sentiment = rule_sentiment
        confidence = max(confidence, rule_confidence or confidence)
    elif confidence < threshold:
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
