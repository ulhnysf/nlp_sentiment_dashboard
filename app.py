from __future__ import annotations

from pathlib import Path
import sys

import pandas as pd
import plotly.express as px
import streamlit as st

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

from src.config import (
    CONFUSION_MATRIX_PATH,
    METRICS_PATH,
    MODEL_COMPARISON_PATH,
    MODEL_PATH,
    PROCESSED_DATA_PATH,
    WORD_FREQUENCY_PATH,
)
from src.database import init_db, read_table, save_prediction
from src.predict import load_model, predict_sentiment

st.set_page_config(page_title="NLP Sentiment Dashboard", page_icon="💬", layout="wide")


@st.cache_resource(show_spinner=False)
def cached_model():
    if not MODEL_PATH.exists():
        st.error("Model dosyas? bulunamad?. Terminalden `python scripts/run_training.py --dataset data/raw/train.ft.txt.bz2 --limit 10000` komutunu ?al??t?r?n.")
        st.stop()
    return load_model(MODEL_PATH)


@st.cache_data(show_spinner=False)
def load_metrics() -> pd.DataFrame:
    if METRICS_PATH.exists():
        return pd.read_csv(METRICS_PATH)
    return pd.DataFrame()


def sentiment_chart(df: pd.DataFrame, column: str, title: str):
    if df.empty or column not in df.columns:
        st.info("Grafik için henüz veri yok.")
        return
    counts = df[column].value_counts().reset_index()
    counts.columns = ["sentiment", "count"]
    fig = px.pie(counts, names="sentiment", values="count", title=title, hole=0.35)
    st.plotly_chart(fig, use_container_width=True)


def trend_chart(df: pd.DataFrame):
    if df.empty or "classified_at" not in df.columns:
        st.info("Trend grafiği için henüz tahmin kaydı yok.")
        return
    temp = df.copy()
    temp["classified_at"] = pd.to_datetime(temp["classified_at"], errors="coerce")
    temp = temp.dropna(subset=["classified_at"])
    if temp.empty:
        st.info("Trend grafiği için tarih bilgisi bulunamadı.")
        return
    temp["date"] = temp["classified_at"].dt.date
    trend = temp.groupby(["date", "predicted_sentiment"]).size().reset_index(name="count")
    fig = px.line(trend, x="date", y="count", color="predicted_sentiment", markers=True, title="Duygu Eğilimi")
    st.plotly_chart(fig, use_container_width=True)


def metrics_cards(predictions: pd.DataFrame):
    total = len(predictions)
    avg_conf = predictions["confidence_score"].mean() if not predictions.empty else 0
    positive_rate = 0
    if not predictions.empty:
        positive_rate = (predictions["predicted_sentiment"].eq("Positive").mean()) * 100
    c1, c2, c3 = st.columns(3)
    c1.metric("Toplam Sınıflandırma", f"{total}")
    c2.metric("Ortalama Güven", f"{avg_conf:.2%}")
    c3.metric("Pozitif Oran", f"{positive_rate:.1f}%")


def main():
    init_db()
    st.title("💬 NLP Projesi: Duygu Analizi Gösterge Paneli")
    st.caption("Müşteri yorumlarını Positive, Negative veya Neutral olarak sınıflandıran uçtan uca NLP + SQL + Dashboard uygulaması.")

    with st.sidebar:
        st.header("Menü")
        page = st.radio("Sayfa seç", ["Tahmin", "Analitik", "Model Performansı", "Veri Seti", "SQL Kayıtları"])
        st.divider()
        st.info("Model Kaggle verisiyle egitildi. Yeniden egitim icin terminalden scripts/run_training.py komutunu kullan.")
    if page == "Tahmin":
        st.subheader("Yeni Yorum Sınıflandır")
        review = st.text_area("Müşteri yorumu", height=140, placeholder="Örn: The sound quality is great and setup was very easy...")
        col1, col2 = st.columns([1, 3])
        with col1:
            classify = st.button("Duyguyu Tahmin Et", type="primary")
        with col2:
            st.write("Tahmin SQL veritabanındaki `predictions` tablosuna kaydedilir.")

        if classify:
            if not review.strip():
                st.warning("Lütfen bir yorum giriniz.")
            else:
                model_bundle = cached_model()
                result = predict_sentiment(review, model_bundle=model_bundle)
                save_prediction(
                    review_text=result["review_text"],
                    clean_review=result["clean_review"],
                    predicted_sentiment=result["predicted_sentiment"],
                    confidence_score=result["confidence_score"],
                    model_name=result["model_name"],
                )
                st.success(f"Tahmin edilen duygu: **{result['predicted_sentiment']}**")
                st.metric("Güven skoru", f"{result['confidence_score']:.2%}")
                if result["class_probabilities"]:
                    probs = pd.DataFrame(result["class_probabilities"].items(), columns=["sentiment", "probability"])
                    fig = px.bar(probs, x="sentiment", y="probability", title="Sınıf Olasılıkları", range_y=[0, 1])
                    st.plotly_chart(fig, use_container_width=True)

    elif page == "Analitik":
        st.subheader("Duygu İstatistikleri ve Eğilimler")
        predictions = read_table("predictions")
        metrics_cards(predictions)
        c1, c2 = st.columns(2)
        with c1:
            sentiment_chart(predictions, "predicted_sentiment", "Tahmin Edilen Duygu Dağılımı")
        with c2:
            trend_chart(predictions)
        st.divider()
        if WORD_FREQUENCY_PATH.exists():
            st.image(str(WORD_FREQUENCY_PATH), caption="En sık kullanılan kelimeler")

    elif page == "Model Performansı":
        st.subheader("Model Karşılaştırması ve Değerlendirme")
        metrics = load_metrics()
        if metrics.empty:
            st.info("Model metrikleri bulunamadi. Terminalden scripts/run_training.py komutunu calistirarak modeli egitin.")
        else:
            st.dataframe(metrics, use_container_width=True)
            if MODEL_COMPARISON_PATH.exists():
                st.image(str(MODEL_COMPARISON_PATH), caption="Accuracy, Precision, Recall, F1-Score karşılaştırması")
            if CONFUSION_MATRIX_PATH.exists():
                st.image(str(CONFUSION_MATRIX_PATH), caption="Confusion Matrix")

    elif page == "Veri Seti":
        st.subheader("Hazırlanmış Duygu Analizi Veri Seti")
        if PROCESSED_DATA_PATH.exists():
            df = pd.read_csv(PROCESSED_DATA_PATH)
            st.write(f"Toplam kayıt: **{len(df)}**")
            c1, c2 = st.columns(2)
            with c1:
                sentiment_chart(df, "sentiment", "Etiket Dağılımı")
            with c2:
                st.dataframe(df.head(30), use_container_width=True)
        else:
            st.info("İşlenmiş veri seti bulunamadı. `python scripts/prepare_dataset.py` komutunu çalıştırın.")

    elif page == "SQL Kayıtları":
        st.subheader("SQL Tabloları")
        tab1, tab2 = st.tabs(["reviews", "predictions"])
        with tab1:
            reviews = read_table("reviews")
            st.dataframe(reviews.tail(50), use_container_width=True)
        with tab2:
            predictions = read_table("predictions")
            st.dataframe(predictions.tail(50), use_container_width=True)


if __name__ == "__main__":
    main()
