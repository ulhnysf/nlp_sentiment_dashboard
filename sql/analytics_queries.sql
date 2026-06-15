-- Sentiment percentages
SELECT predicted_sentiment,
       COUNT(*) AS total,
       ROUND(100.0 * COUNT(*) / (SELECT COUNT(*) FROM predictions), 2) AS percentage
FROM predictions
GROUP BY predicted_sentiment
ORDER BY total DESC;

-- Daily sentiment trend
SELECT DATE(classified_at) AS day,
       predicted_sentiment,
       COUNT(*) AS total
FROM predictions
GROUP BY DATE(classified_at), predicted_sentiment
ORDER BY day;

-- Average confidence by sentiment
SELECT predicted_sentiment,
       ROUND(AVG(confidence_score), 4) AS avg_confidence
FROM predictions
GROUP BY predicted_sentiment;
