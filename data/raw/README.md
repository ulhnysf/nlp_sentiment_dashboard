# Raw Dataset Directory

Bu klasör, Kaggle Amazon Reviews veri seti dosyalarının yerleştirileceği klasördür.

## Kullanılan Veri Seti

Projede Kaggle üzerinde bulunan Amazon Reviews veri seti kullanılmıştır:

```text
bittlingmayer/amazonreviews
```

Kaggle arşivi açıldığında aşağıdaki dosyalar elde edilir:

```text
train.ft.txt.bz2
test.ft.txt.bz2
```

Bu dosyalar fastText formatındadır. Veri setindeki etiketler şu şekilde yorumlanır:

```text
__label__1 -> Negative
__label__2 -> Positive
```

## Neden Kaggle Dosyaları GitHub'a Yüklenmedi?

`train.ft.txt.bz2` ve `test.ft.txt.bz2` dosyaları büyük boyutlu veri dosyalarıdır. Bu nedenle GitHub reposuna eklenmemiştir.

Projeyi çalıştırmak isteyen kullanıcı bu dosyaları Kaggle'dan indirip bu klasöre yerleştirmelidir.

Beklenen dosya yolları:

```text
data/raw/train.ft.txt.bz2
data/raw/test.ft.txt.bz2
```

## Örnek Veri

Projede hızlı testler için küçük bir `sample_reviews.csv` dosyası da bulunmaktadır.

Bu dosya:

* Proje yapısını hızlı test etmek
* Docker senaryosunda küçük veriyle model oluşturmak
* Dashboard'u hızlı şekilde çalıştırmak

için kullanılabilir.

Ancak final model eğitimi için asıl kullanılan veri seti Kaggle Amazon Reviews veri setidir.

## Final Eğitim Komutu

Final model eğitimi için kullanılan komut:

```bash
python scripts/run_training.py --dataset data/raw/train.ft.txt.bz2 --limit 100000
```

Bu komut çalıştırıldığında:

* Veri seti okunur
* Etiketler Positive ve Negative olarak dönüştürülür
* NLP ön işleme süreci uygulanır
* TF-IDF özellik çıkarımı yapılır
* Logistic Regression, Naive Bayes ve Support Vector Machine modelleri eğitilir
* Model sonuçları karşılaştırılır
* En iyi model `models/best_model.joblib` olarak oluşturulur
* Model metrikleri ve grafikler yeniden üretilir
