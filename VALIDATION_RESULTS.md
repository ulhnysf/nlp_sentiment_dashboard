# Validation Results

Son kontrol tarihi: 2026-06-15

Bu dosya, proje klasörü üzerinde yapılan teknik doğrulama çıktılarının özetidir.

## 1. Python syntax / compile check

Komut:

```bash
python -m compileall app.py src scripts
```

Sonuç: Başarılı. `app.py`, `src/` ve `scripts/` altındaki Python dosyalarında syntax hatası bulunmadı.

## 2. Veri yükleme ve etiket eşleştirme testi

Kontrol edilen durumlar:

- `rating=1` ve `rating=2` -> `Negative`
- `rating=3` -> `Neutral`
- `rating=4` ve `rating=5` -> `Positive`
- `feedback=0` -> `Negative`
- `feedback=1` -> `Positive`
- `__label__1` -> `Negative`
- `__label__2` -> `Positive`

Sonuç: Başarılı.

## 3. Otomatik testler

Komut:

```bash
pytest -q
```

Sonuç:

```text
3 passed
```

## 4. Model eğitim testi

Komut:

```bash
python scripts/run_training.py --no-db
```

Sonuç: Başarılı.

Örnek veri setiyle eğitilen modeller:

- Logistic Regression
- Naive Bayes
- Support Vector Machine

Üretilen çıktılar:

- `models/best_model.joblib`
- `models/model_metrics.csv`
- `reports/figures/model_comparison.png`
- `reports/figures/confusion_matrix.png`
- `reports/figures/word_frequency.png`

## 5. SQL kontrolü

SQLite veritabanında beklenen tablolar mevcut:

- `reviews`
- `predictions`

Son paket temizliği sırasında test amaçlı tahmin kayıtları silindi. `predictions` tablosu kullanıcı dashboard üzerinden yeni yorum gönderdiğinde dolacaktır.

## 6. Not

Streamlit paketi mevcut proje bağımlılıklarında `requirements.txt` içinde yer almaktadır. Bu çalışma ortamında Streamlit yüklü olmadığı için arayüz canlı olarak başlatılmadı; ancak Docker/Python kurulum adımlarında paket otomatik kurulacak şekilde tanımlanmıştır.
