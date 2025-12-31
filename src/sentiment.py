import pandas as pd
import feedparser
from groq import Groq
from dotenv import load_dotenv
import os

class SentimentAnalyzer:
    def __init__(self):
        load_dotenv()
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        self.model = "llama-3.1-8b-instant"

    def get_google_news_headlines(self, ticker):
        """Holt ca. 50-100 Schlagzeilen von Google News"""
        # Wir suchen nach dem Ticker und dem Begriff 'Stock'
        url = f"https://news.google.com/rss/search?q={ticker}+stock+when:2d&hl=en-US&gl=US&ceid=US:en"
        feed = feedparser.parse(url)
        headlines = [entry.title for entry in feed.entries]
        print(f"[*] {len(headlines)} Schlagzeilen von Google News geladen.")
        return headlines

    def get_sentiment(self, ticker):
        headlines = self.get_google_news_headlines(ticker)

        if not headlines:
            return 0.0

        #bündeln Schlagzeilen zu einem langen Text, um API-Calls zu sparen
        text_block = "\n".join(headlines[:50])  # Die ersten 50 Schlagzeilen

        prompt = f"""
        Analysiere das Sentiment der folgenden Schlagzeilen für den Ticker {ticker}.
        Antworte NUR mit einer einzigen Zahl zwischen -1.0 (sehr negativ) und 1.0 (sehr positiv).
        0.0 ist neutral. Gib keinen Text oder Erklärungen aus.

        Schlagzeilen:
        {text_block}
        """

        try:
            chat_completion = self.client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model=self.model,
                temperature=0.0  # Für konsistente Ergebnisse
            )

            response = chat_completion.choices[0].message.content.strip()
            #Antwort in float umwandeln -> Hoffnung das auch wirklich nur eine Zahl zurückgegeben wurde
            score = float(response)
            return score
        except Exception as e:
            print(f"[!] Fehler bei der Groq-Analyse: {e}")
            return 0.0





