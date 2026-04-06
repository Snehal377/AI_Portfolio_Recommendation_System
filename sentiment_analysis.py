from transformers import pipeline
import feedparser
import os
os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"

# Load FinBERT sentiment model
sentiment_model = pipeline(
    "sentiment-analysis",
    model="ProsusAI/finbert"
)

def fetch_financial_news():

    url = "https://news.google.com/rss/search?q=indian+stock+market"

    feed = feedparser.parse(url)

    headlines = []

    for entry in feed.entries[:10]:
        headlines.append(entry.title)

    return headlines

def analyze_sentiment():

    headlines = fetch_financial_news()

    sentiments = sentiment_model(headlines)

    results = []

    for headline, sentiment in zip(headlines, sentiments):

        results.append({
            "headline": headline,
            "sentiment": sentiment["label"],
            "score": sentiment["score"]
        })

    return results

def get_market_sentiment_score():

    results = analyze_sentiment()

    score = 0

    for r in results:
        if r["sentiment"] == "positive":
            score += r["score"]
        elif r["sentiment"] == "negative":
            score -= r["score"]

    # normalize
    final_score = score / len(results)

    return final_score


if __name__ == "__main__":

    results = analyze_sentiment()

    for r in results:
        print(r)    