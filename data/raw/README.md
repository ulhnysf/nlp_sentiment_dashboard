# Dataset Placement

The project is configured to work with the Kaggle dataset mentioned in the assignment:

- `bittlingmayer/amazonreviews`

Because Kaggle downloads usually require authentication, this folder contains `sample_reviews.csv` so the project runs immediately.

## Recommended Kaggle usage

1. Download the dataset manually from Kaggle.
2. Place one of these files in this folder:
   - `train.ft.txt.bz2`
   - `test.ft.txt.bz2`
   - a CSV file with columns such as `review_text` and `sentiment`, or `verified_reviews` and `rating`.
3. Train using:

```bash
python scripts/run_training.py --dataset data/raw/train.ft.txt.bz2 --limit 50000
```

If your file has ratings from 1 to 5, the loader maps them like this:

- 1-2: Negative
- 3: Neutral
- 4-5: Positive

If your file uses fastText labels from `bittlingmayer/amazonreviews`, the loader maps:

- `__label__1`: Negative
- `__label__2`: Positive

For binary datasets, neutral predictions are still supported through a confidence threshold in the prediction layer.
