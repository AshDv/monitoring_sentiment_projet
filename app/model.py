from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

_analyzer = SentimentIntensityAnalyzer()

def predict_sentiment(text: str):
    scores = _analyzer.polarity_scores(text or "")
    comp = scores.get("compound", 0.0)
    if comp >= 0.05:
        label = "Positive"
    elif comp <= -0.05:
        label = "Negative"
    else:
        label = "Neutral"
    return label, float(comp)