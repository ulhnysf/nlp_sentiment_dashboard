# Models Directory

Bu klasör model eğitimi sonucunda oluşan model ve metrik dosyaları için kullanılır.

## Neden `best_model.joblib` GitHub'a yüklenmedi?

Final eğitim sonucunda oluşan `best_model.joblib` dosyası yaklaşık 110 MB boyutundadır. GitHub tek dosya için 100 MB sınırı uyguladığı için bu model dosyası repoya eklenmemiştir.

Model dosyası yerel bilgisayarda üretilebilir. Bunun için önce Kaggle Amazon Reviews veri setindeki `train.ft.txt.bz2` dosyası `data/raw/` klasörüne yerleştirilmelidir.

Ardından şu komut çalıştırılır:

```bash
python scripts/run_training.py --dataset data/raw/train.ft.txt.bz2 --limit 100000
```

Bu komut çalıştırıldığında aşağıdaki dosyalar yeniden oluşturulur:

* `models/best_model.joblib`
* `models/model_metrics.csv`
* `reports/figures/confusion_matrix.png`
* `reports/figures/model_comparison.png`
* `reports/figures/word_frequency.png`

## Final Model

Final eğitim sonucunda en iyi model:

```text
Support Vector Machine
```

Final test başarımı yaklaşık olarak:

```text
Accuracy: 0.89
Macro F1-Score: 0.89
```

## Not

Model dosyasının GitHub reposunda bulunmaması projenin eksik olduğu anlamına gelmez. Model dosyası büyük olduğu için repoya eklenmemiştir. Projeyi çalıştırmak isteyen kullanıcı, README dosyasında verilen eğitim komutunu çalıştırarak modeli yeniden üretebilir.
