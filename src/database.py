from __future__ import annotations

from datetime import datetime, timezone
from typing import Iterable, Optional

import pandas as pd
from sqlalchemy import Column, DateTime, Float, Integer, MetaData, String, Text, create_engine, text
from sqlalchemy.orm import declarative_base, sessionmaker

from src.config import DATABASE_URL

metadata = MetaData()
Base = declarative_base(metadata=metadata)


class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, autoincrement=True)
    review_text = Column(Text, nullable=False)
    clean_review = Column(Text, nullable=False)
    sentiment = Column(String(20), nullable=False, index=True)
    source = Column(String(255), nullable=True)
    loaded_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)


class Prediction(Base):
    __tablename__ = "predictions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    review_text = Column(Text, nullable=False)
    clean_review = Column(Text, nullable=False)
    predicted_sentiment = Column(String(20), nullable=False, index=True)
    confidence_score = Column(Float, nullable=False)
    model_name = Column(String(120), nullable=False)
    classified_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False, index=True)


def get_engine(database_url: str = DATABASE_URL):
    connect_args = {"check_same_thread": False} if database_url.startswith("sqlite") else {}
    return create_engine(database_url, echo=False, future=True, connect_args=connect_args)


def init_db(database_url: str = DATABASE_URL) -> None:
    engine = get_engine(database_url)
    Base.metadata.create_all(engine)


def get_session(database_url: str = DATABASE_URL):
    engine = get_engine(database_url)
    Session = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)
    return Session()


def load_reviews_to_db(df: pd.DataFrame, database_url: str = DATABASE_URL, replace: bool = True) -> int:
    init_db(database_url)
    engine = get_engine(database_url)
    if replace:
        with engine.begin() as conn:
            conn.execute(text("DELETE FROM reviews"))
    records = df[["review_text", "clean_review", "sentiment", "source"]].to_dict(orient="records")
    if not records:
        return 0
    with engine.begin() as conn:
        conn.execute(Review.__table__.insert(), records)
    return len(records)


def save_prediction(
    review_text: str,
    clean_review: str,
    predicted_sentiment: str,
    confidence_score: float,
    model_name: str,
    database_url: str = DATABASE_URL,
) -> None:
    init_db(database_url)
    session = get_session(database_url)
    try:
        row = Prediction(
            review_text=review_text,
            clean_review=clean_review,
            predicted_sentiment=predicted_sentiment,
            confidence_score=float(confidence_score),
            model_name=model_name,
            classified_at=datetime.now(timezone.utc),
        )
        session.add(row)
        session.commit()
    finally:
        session.close()


def read_table(table_name: str, database_url: str = DATABASE_URL) -> pd.DataFrame:
    init_db(database_url)
    engine = get_engine(database_url)
    try:
        return pd.read_sql_table(table_name, con=engine)
    except ValueError:
        return pd.DataFrame()
