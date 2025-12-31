import yfinance as yf
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk
import pandas as pd
from deep_translator import GoogleTranslator

#Download des Lexicons
nltk.download('vader_lexicon', quiet=True)

class SentimentAnalyzer:
    def __init__(self):
        self.analyzer = SentimentIntensityAnalyzer()

    def get_sentiment(self, ticker):
        #Die jeweiligen News abhängig vom Ticker holen zB dax
        dax = yf.Ticker(ticker)
        news = dax.news
        print(f"[*] Anzahl gefundener News für {ticker}: {len(news)}")

        if not news:
            return 0.0

        scores = []

        for article in news:
            if 'content' in article:
                data = article['content']
            else:
                data = article

            title = data.get("title", "")
            summary = data.get("summary", "")
            text = f"{title}.{summary}".strip()
            score = self.analyzer.polarity_scores(text)["compound"]
            scores.append(score)

        avg = sum(scores)/len(scores)
        print(scores)
        return avg





