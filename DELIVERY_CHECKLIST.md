# Proje Teslim Kontrol Listesi

Bu dosya, IYD 328 İş Yeri Deneyimi Faz-2 kapsamında seçilen **NLP Projesi: Duygu Analizi Gösterge Paneli** isterlerine göre hazırlanmıştır.

Amaç, proje gereksinimlerinin hangi dosyalar ve özellikler ile karşılandığını açık şekilde göstermektir.

---

## 1. Genel Teslim Durumu

| Madde                                                    | Durum      |
| -------------------------------------------------------- | ---------- |
| GitHub deposu oluşturuldu                                | Tamamlandı |
| Proje GitHub'a yüklendi                                  | Tamamlandı |
| README dosyası hazırlandı                                | Tamamlandı |
| README içinde sistem tasarımı açıklandı                  | Tamamlandı |
| README içinde veri seti açıklandı                        | Tamamlandı |
| README içinde model seçim gerekçesi açıklandı            | Tamamlandı |
| README içinde eğitim süreci açıklandı                    | Tamamlandı |
| README içinde değerlendirme sonuçları açıklandı          | Tamamlandı |
| README içinde kurulum talimatları verildi                | Tamamlandı |
| README içinde dashboard ekran görüntüleri eklendi        | Tamamlandı |
| Büyük veri dosyaları `.gitignore` ile dışarıda bırakıldı | Tamamlandı |
| Model dosyasının neden GitHub'a yüklenmediği açıklandı   | Tamamlandı |
| Dockerfile sağlandı                                      | Tamamlandı |
| docker-compose.yml sağlandı                              | Tamamlandı |
| .dockerignore sağlandı                                   | Tamamlandı |

---

## 2. Veri Seti Gereksinimleri

| İster                                             | Durum      | Açıklama                                                     |
| ------------------------------------------------- | ---------- | ------------------------------------------------------------ |
| Kaggle Amazon Reviews veri seti kullanımı         | Tamamlandı | `train.ft.txt.bz2` veri dosyası kullanıldı                   |
| Veri setinin pandas DataFrame olarak işlenmesi    | Tamamlandı | Veri eğitim pipeline içinde DataFrame formatına dönüştürüldü |
| Veri setinin sorgulanabilir yapıya dönüştürülmesi | Tamamlandı | İşlenmiş veri ve SQL kayıtları desteklendi                   |
| Büyük veri dosyalarının GitHub dışında tutulması  | Tamamlandı | `data/raw/*.bz2` `.gitignore` içine eklendi                  |
| Veri setinin nereye konulacağının açıklanması     | Tamamlandı | `data/raw/README.md` eklendi                                 |

---

## 3. NLP Ön İşleme Gereksinimleri

| İster                     | Durum      |
| ------------------------- | ---------- |
| Text cleaning             | Tamamlandı |
| Lowercase conversion      | Tamamlandı |
| Stopword removal          | Tamamlandı |
| Tokenization              | Tamamlandı |
| TF-IDF feature extraction | Tamamlandı |

---

## 4. Makine Öğrenmesi Model Gereksinimleri

| Model                  | Durum      |
| ---------------------- | ---------- |
| Logistic Regression    | Tamamlandı |
| Naive Bayes            | Tamamlandı |
| Support Vector Machine | Tamamlandı |

Final eğitim sonucunda en iyi model:

```text
Support Vector Machine
```

---

## 5. Model Değerlendirme Gereksinimleri

| Metrik           | Durum      |
| ---------------- | ---------- |
| Accuracy         | Tamamlandı |
| Precision        | Tamamlandı |
| Recall           | Tamamlandı |
| F1-Score         | Tamamlandı |
| Confusion Matrix | Tamamlandı |

Final model karşılaştırma sonuçları:

| Model                  | Accuracy | Precision Macro | Recall Macro | F1 Macro |
| ---------------------- | -------: | --------------: | -----------: | -------: |
| Support Vector Machine |     0.89 |            0.89 |         0.89 |     0.89 |
| Logistic Regression    |     0.88 |            0.88 |         0.88 |     0.88 |
| Naive Bayes            |     0.87 |            0.87 |         0.87 |     0.87 |

---

## 6. SQL Veritabanı Gereksinimleri

| SQL'de Saklanması İstenen Bilgi | Durum      |
| ------------------------------- | ---------- |
| Yorum metni                     | Tamamlandı |
| Tahmin edilen duygu             | Tamamlandı |
| Güven skoru                     | Tamamlandı |
| Sınıflandırma zaman damgası     | Tamamlandı |

Ek olarak dashboard içinde SQL kayıtlarını görüntüleyen ayrı bir sayfa bulunmaktadır.

---

## 7. Dashboard Gereksinimleri

| Dashboard Özelliği                       | Durum      |
| ---------------------------------------- | ---------- |
| Yeni yorum girişi                        | Tamamlandı |
| Tahmin edilen duygu sonucunu görüntüleme | Tamamlandı |
| Güven skoru gösterimi                    | Tamamlandı |
| Duygu dağılımlarını görselleştirme       | Tamamlandı |
| Duygu istatistiklerini inceleme          | Tamamlandı |
| Model performansını görüntüleme          | Tamamlandı |
| SQL kayıtlarını görüntüleme              | Tamamlandı |
| Kullanıcı dostu arayüz                   | Tamamlandı |

Kullanılan dashboard teknolojisi:

```text
Streamlit
```

---

## 8. Görselleştirme Gereksinimleri

| Görselleştirme                       | Durum      |
| ------------------------------------ | ---------- |
| Pozitif ve negatif yorum dağılımları | Tamamlandı |
| En sık kullanılan kelimeler          | Tamamlandı |
| Kelime frekans analizi               | Tamamlandı |
| Duygu yüzdeleri                      | Tamamlandı |
| Model karşılaştırma grafikleri       | Tamamlandı |
| Confusion Matrix görseli             | Tamamlandı |

Oluşturulan temel görsel dosyalar:

```text
reports/figures/confusion_matrix.png
reports/figures/model_comparison.png
reports/figures/word_frequency.png
```

Dashboard ekran görüntüleri:

```text
docs/screenshots/
```

---

## 9. Neutral Sınıfı Açıklaması

Kullanılan Kaggle Amazon Reviews veri seti doğrudan Neutral etiketi içermemektedir. Veri setindeki etiketler temel olarak şu şekildedir:

```text
__label__1 -> Negative
__label__2 -> Positive
```

Proje isterinde Positive, Negative ve Neutral sınıflandırması beklendiği için Neutral sınıfı şu yaklaşımla uygulanmıştır:

* Model tahmin güveni yüksekse sonuç Positive veya Negative olarak gösterilir.
* Model tahmin güveni düşükse sonuç Neutral olarak gösterilir.
* Confidence threshold değeri 0.80 olarak ayarlanmıştır.
* Türkçe açık duygu ifadeleri için ek kural tabanlı kontrol uygulanmıştır.

Örnekler:

| Yorum                                       | Çıktı    |
| ------------------------------------------- | -------- |
| This product is amazing.                    | Positive |
| The product stopped working after two days. | Negative |
| The product is okay.                        | Neutral  |
| Berbat!                                     | Negative |
| Mükemmel!                                   | Positive |
| İdare eder.                                 | Neutral  |

---

## 10. GitHub ve Commit Süreci

GitHub deposu:

```text
https://github.com/ulhnysf/nlp_sentiment_dashboard
```

Anlamlı commit mesajları kullanılmıştır. Örnek commitler:

```text
Complete final NLP sentiment dashboard project
Add Docker configuration
```

Bu commitler ile proje dosyaları, README, dashboard ekran görüntüleri, Docker yapılandırması ve proje dokümantasyonu GitHub'a yüklenmiştir.

---

## 11. Docker Durumu

Projede Docker desteği için aşağıdaki dosyalar sağlanmıştır:

```text
Dockerfile
docker-compose.yml
.dockerignore
```

Docker yapılandırması, uygulamanın container ortamında çalıştırılabilmesini hedefler.

Not: Yerel bilgisayarda Docker kurulu olmadığı için Docker çalıştırma testi yapılamamıştır. Ancak Docker yapılandırma dosyaları projeye eklenmiş ve GitHub'a gönderilmiştir.

---

## 12. GitHub'a Yüklenmeyen Dosyalar

Aşağıdaki dosyalar bilinçli olarak GitHub dışında bırakılmıştır:

```text
.venv/
data/raw/train.ft.txt.bz2
data/raw/test.ft.txt.bz2
archive.zip
sentiment_dashboard.db
data/processed/processed_reviews.csv
models/best_model.joblib
```

Gerekçeler:

* `.venv/`: Yerel sanal ortamdır.
* Raw Kaggle dosyaları: Büyük veri dosyalarıdır.
* `sentiment_dashboard.db`: Çalışma zamanı veritabanıdır.
* `processed_reviews.csv`: Eğitim sürecinde yeniden üretilebilir.
* `best_model.joblib`: GitHub'ın 100 MB tek dosya sınırını aştığı için repoya eklenmemiştir.

Model dosyası şu komutla yeniden üretilebilir:

```bash
python scripts/run_training.py --dataset data/raw/train.ft.txt.bz2 --limit 100000
```

---

## 13. Genel Sonuç

Bu proje, IYD 328 Faz-2 NLP Projesi isterlerini karşılayacak şekilde geliştirilmiştir.

Tamamlanan ana bileşenler:

* NLP veri ön işleme
* Üç farklı makine öğrenmesi modeli
* Model performans karşılaştırması
* SQL veritabanı entegrasyonu
* Streamlit dashboard
* Görselleştirmeler
* Dashboard ekran görüntüleri
* Detaylı README
* GitHub reposu
* Docker yapılandırma dosyaları
* Teslim kontrol dokümantasyonu

Proje teknik olarak teslim edilebilir durumdadır.
