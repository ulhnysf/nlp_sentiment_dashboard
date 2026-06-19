# Git Commit ve Geliştirme Süreci

Bu dosya, projenin Git ve GitHub üzerinde nasıl yönetildiğini açıklamak için hazırlanmıştır.

IYD 328 İş Yeri Deneyimi Faz-2 NLP Projesi kapsamında geliştirilen bu proje, GitHub deposu üzerinden sürüm kontrolüne alınmıştır. Proje geliştirme sürecinde anlamlı commit mesajları kullanılmış ve kod, dokümantasyon, dashboard ekran görüntüleri ve Docker yapılandırmaları GitHub üzerinde saklanmıştır.

---

## 1. GitHub Deposu

Proje GitHub üzerinde aşağıdaki repoda yayınlanmıştır:

```text id="nrxxql"
https://github.com/ulhnysf/nlp_sentiment_dashboard
```

---

## 2. Kullanılan Branch

Proje ana geliştirme branch'i olarak aşağıdaki branch kullanılmıştır:

```text id="hnbx71"
main
```

---

## 3. Commit Mesajları

Projede açıklayıcı commit mesajları kullanılmaya çalışılmıştır.

Örnek commit mesajları:

```text id="pnvhew"
Complete final NLP sentiment dashboard project
Add Docker configuration
```

Teslim öncesi dokümantasyon güçlendirmeleri için ayrıca şu mantıkta commit mesajları kullanılmıştır:

```text id="gdka6f"
docs: add delivery checklist and project documentation
```

Bu commitler, yapılan değişikliğin amacını kısa ve anlaşılır şekilde ifade eder.

---

## 4. Geliştirme Süreci Özeti

Proje geliştirme süreci genel olarak aşağıdaki adımlardan oluşmuştur:

1. Proje klasör yapısı oluşturuldu.
2. Python sanal ortamı hazırlandı.
3. Gerekli Python paketleri `requirements.txt` üzerinden kuruldu.
4. Kaggle Amazon Reviews veri seti proje yapısına uygun şekilde yerleştirildi.
5. Veri yükleme ve dönüştürme modülleri hazırlandı.
6. NLP ön işleme süreci geliştirildi.
7. TF-IDF feature extraction yapısı kuruldu.
8. Logistic Regression modeli eğitildi.
9. Naive Bayes modeli eğitildi.
10. Support Vector Machine modeli eğitildi.
11. Modeller Accuracy, Precision, Recall, F1-Score ve Confusion Matrix ile değerlendirildi.
12. En iyi model seçildi.
13. Streamlit dashboard geliştirildi.
14. SQL veritabanı entegrasyonu yapıldı.
15. Dashboard üzerinden yeni yorum tahmini ve SQL kayıt sistemi test edildi.
16. Duygu dağılımları, kelime frekansları ve model karşılaştırma grafikleri oluşturuldu.
17. Dashboard ekran görüntüleri `docs/screenshots/` klasörüne eklendi.
18. README dosyası detaylandırıldı.
19. Büyük veri dosyaları `.gitignore` ile GitHub dışında bırakıldı.
20. Dockerfile, docker-compose.yml ve .dockerignore dosyaları düzenlendi.
21. Proje GitHub'a yüklendi.
22. Teslim kontrol listesi ve ek açıklama dokümanları eklendi.

---

## 5. GitHub'a Eklenmeyen Dosyalar

Aşağıdaki dosyalar bilinçli olarak GitHub dışında bırakılmıştır:

```text id="3i2ttv"
.venv/
data/raw/train.ft.txt.bz2
data/raw/test.ft.txt.bz2
archive.zip
sentiment_dashboard.db
data/processed/processed_reviews.csv
models/best_model.joblib
```

Bu dosyaların eklenmemesinin nedenleri:

* `.venv/` klasörü kişisel sanal ortamdır.
* `train.ft.txt.bz2` ve `test.ft.txt.bz2` büyük Kaggle veri dosyalarıdır.
* `sentiment_dashboard.db` çalışma sırasında yeniden üretilebilen veritabanı dosyasıdır.
* `processed_reviews.csv` eğitim sürecinde yeniden oluşturulabilir.
* `best_model.joblib` dosyası yaklaşık 110 MB olduğu için GitHub'ın 100 MB tek dosya sınırını aşmaktadır.

---

## 6. Modelin Yeniden Üretilmesi

GitHub reposunda `best_model.joblib` dosyası yer almadığı için modeli yeniden üretmek isteyen kullanıcı önce Kaggle veri setini `data/raw/` klasörüne yerleştirmelidir.

Ardından şu komut çalıştırılır:

```bash id="zowxwm"
python scripts/run_training.py --dataset data/raw/train.ft.txt.bz2 --limit 100000
```

Bu komut çalıştırıldığında model, metrik dosyaları ve grafikler yeniden oluşturulur.

---

## 7. Docker Yapılandırması

Projede Docker desteği için aşağıdaki dosyalar sağlanmıştır:

```text id="jqm6fl"
Dockerfile
docker-compose.yml
.dockerignore
```

Docker ile çalıştırmak için README dosyasında verilen komut kullanılabilir:

```bash id="4m8kd4"
docker compose up --build
```

Not: Yerel bilgisayarda Docker kurulu olmadığı için Docker çalıştırma testi yapılamamıştır. Ancak Docker yapılandırma dosyaları projeye eklenmiş ve GitHub'a gönderilmiştir.

---

## 8. Sonuç

Bu proje GitHub üzerinde sürüm kontrolüne alınmış, açıklayıcı commit mesajları ile güncellenmiş ve teslim sürecini destekleyen ek dokümantasyon dosyaları ile güçlendirilmiştir.

Proje deposu, kod dosyalarını, README dosyasını, dashboard ekran görüntülerini, model sonuçlarını, Docker yapılandırmasını ve teslim kontrol dokümantasyonunu içermektedir.
