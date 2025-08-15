# utils/sentiment_analyzer.py

from textblob import TextBlob

def analyze_sentiment(text):
    if not text.strip():
        return "Neutral"

    blob = TextBlob(text)
    polarity = blob.sentiment.polarity

    if polarity > 0.1:
        return "Positive"
    elif polarity < -0.1:
        return "Negative"
    else:
        return "Neutral"

