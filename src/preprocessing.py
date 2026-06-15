from __future__ import annotations

import re
from typing import Iterable, List

from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS

CUSTOM_STOPWORDS = {
    "product", "device", "amazon", "alexa", "review", "reviews", "really", "very"
}
STOPWORDS = set(ENGLISH_STOP_WORDS).union(CUSTOM_STOPWORDS)


def clean_text(text: str) -> str:
    """Clean, lowercase, tokenize and remove stopwords from a review."""
    if text is None:
        return ""
    text = str(text).lower()
    text = re.sub(r"http\S+|www\.\S+", " ", text)
    text = re.sub(r"[^a-zA-Z\s]", " ", text)
    tokens = re.findall(r"[a-zA-Z]{2,}", text)
    tokens = [token for token in tokens if token not in STOPWORDS]
    return " ".join(tokens)


def tokenize(text: str) -> List[str]:
    """Return cleaned tokens for word-frequency analysis."""
    return clean_text(text).split()


def batch_clean(texts: Iterable[str]) -> List[str]:
    return [clean_text(text) for text in texts]
