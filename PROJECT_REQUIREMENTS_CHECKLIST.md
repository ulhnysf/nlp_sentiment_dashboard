# Proje İsterleri Kontrol Listesi

Bu dosya, IYD 328 dokümanındaki NLP Duygu Analizi Gösterge Paneli isterlerinin projede nerede karşılandığını gösterir.

| İster | Projedeki Karşılığı | Durum |
| --- | --- | --- |
| Amazon Reviews / Alexa Reviews veri seti kullanımı | `data/raw/README.md`, `src/data_loader.py`; Kaggle dosyası veya örnek veri desteklenir | Tamamlandı |
| pandas DataFrame formatında hazırlanmış veri seti | `src/data_loader.py`, `data/processed/processed_reviews.csv` | Tamamlandı |
| SQL tablolarına yükleme | `src/database.py`, `reviews` tablosu | Tamamlandı |
| Text cleaning | `src/preprocessing.py` | Tamamlandı |
| Lowercase conversion | `src/preprocessing.py` | Tamamlandı |
| Stopword kaldırma | `src/preprocessing.py` | Tamamlandı |
| Tokenization | `src/preprocessing.py` | Tamamlandı |
| TF-IDF / Bag-of-Words | TF-IDF: `src/train_models.py` | Tamamlandı |
| Logistic Regression | `src/train_models.py` | Tamamlandı |
| Naive Bayes | `src/train_models.py` | Tamamlandı |
| SVM | `src/train_models.py` | Tamamlandı |
| Accuracy | `models/model_metrics.csv` | Tamamlandı |
| Precision | `models/model_metrics.csv` | Tamamlandı |
| Recall | `models/model_metrics.csv` | Tamamlandı |
| F1-Score | `models/model_metrics.csv` | Tamamlandı |
| Confusion Matrix | `reports/figures/confusion_matrix.png` | Tamamlandı |
| Yorum metni depolama | `predictions.review_text` | Tamamlandı |
| Tahmin edilen duygu depolama | `predictions.predicted_sentiment` | Tamamlandı |
| Güven skoru depolama | `predictions.confidence_score` | Tamamlandı |
| Sınıflandırma zaman damgası | `predictions.classified_at` | Tamamlandı |
| Yeni yorum girişi | Streamlit `Tahmin` sayfası | Tamamlandı |
| Anlık tahmin sonucu | Streamlit `Tahmin` sayfası | Tamamlandı |
| Duygu dağılımı grafiği | Streamlit `Analitik` sayfası | Tamamlandı |
| Duygu istatistikleri ve eğilimleri | Streamlit `Analitik` sayfası | Tamamlandı |
| Pozitif / negatif dağılımlar | Streamlit grafikler | Tamamlandı |
| En sık kullanılan kelimeler | `reports/figures/word_frequency.png` | Tamamlandı |
| Kelime frekans analizi | `src/train_models.py` | Tamamlandı |
| Duygu yüzdeleri | Dashboard + `sql/analytics_queries.sql` | Tamamlandı |
| Model karşılaştırma grafikleri | `reports/figures/model_comparison.png` | Tamamlandı |
| Kullanıcı dostu arayüz | `app.py` | Tamamlandı |
| GitHub repo yapısı | `.gitignore`, `.github/workflows`, `GIT_COMMIT_PLAN.md` | Tamamlandı |
| Açıklayıcı README | `README.md` | Tamamlandı |
| Docker | `Dockerfile`, `docker-compose.yml` | Tamamlandı |
