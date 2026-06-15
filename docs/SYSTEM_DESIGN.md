# System Design

## Architecture

The system contains four main layers:

1. **Data Layer**
   - Loads Kaggle Amazon review data or the built-in sample dataset.
   - Cleans raw text and stores processed rows in `data/processed/processed_reviews.csv`.
   - Saves review and prediction records in SQL tables.

2. **NLP and Machine Learning Layer**
   - Applies text cleaning, lowercasing, tokenization, stopword removal and TF-IDF feature extraction.
   - Trains Logistic Regression, Naive Bayes and Support Vector Machine models.
   - Compares models using Accuracy, Precision, Recall and F1-Score.

3. **Database Layer**
   - `reviews` table stores prepared labeled review data.
   - `predictions` table stores new user inputs, predicted sentiment, confidence score and timestamp.

4. **Dashboard Layer**
   - Streamlit provides the user interface.
   - Users submit new comments and receive instant sentiment predictions.
   - Charts show sentiment distribution, trends, model comparison and word frequencies.

## Data Flow

```text
Kaggle Dataset / sample_reviews.csv
        ↓
Data Loader
        ↓
Text Preprocessing
        ↓
TF-IDF Feature Extraction
        ↓
ML Model Training and Evaluation
        ↓
Best Model Saved in /models
        ↓
Streamlit Dashboard
        ↓
Prediction Records Saved in SQL
```
