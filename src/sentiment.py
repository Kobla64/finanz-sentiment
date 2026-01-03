import pandas as pd
import feedparser
from groq import Groq
from dotenv import load_dotenv
import os

class SentimentAnalyzer:
    def __init__(self):
        load_dotenv()
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        self.model = "meta-llama/llama-4-scout-17b-16e-instruct"

    def get_google_news_headlines(self, ticker):
        """Holt ca. 50-100 Schlagzeilen von Google News"""
        # Wir suchen nach dem Ticker und dem Begriff 'Stock'
        url = f"https://news.google.com/rss/search?q={ticker}+stock+when:3d&hl=en-US&gl=US&ceid=US:en"
        feed = feedparser.parse(url)
        headlines = [entry.title for entry in feed.entries]
        print(f"[*] {len(headlines)} Schlagzeilen von Google News geladen.")
        return headlines

    def get_sentiment(self, ticker):
        headlines = self.get_google_news_headlines(ticker)

        if not headlines:
            return 0.0

        #bündeln Schlagzeilen zu einem langen Text, um API-Calls zu sparen
        text_block = "\n".join(headlines[:75])  # Die ersten 75 Schlagzeilen

        prompt = f"""
        Analyze the overall market sentiment for {ticker} based on these headlines.
        
        Rules:
        - Output ONLY a float between -1.0 and 1.0.
        - -1.0 = Extreme Fear/Crash
        - 1.0 = Extreme Bullish/Greed
        - Use the full scale (e.g., 0.15, -0.42), do not just stay at 0.0.
        - AND PLEASE ONLY OUTPUT A SINGLE FLOAT AND NOTHING ELSE
        
        Examples:
        "S&P 500 hits new all-time high" -> 0.8
        "Fed signals interest rate hikes" -> -0.4
        "Markets trade sideways in low volume" -> 0.0

        Headlines:
        {text_block}
        """
        prompt_for_summary = f"""
        Hier sind aktuelle Schlagzeilen zu {ticker}:
        {text_block}
        Fasse die wichtigsten Entwicklungen der letzten 2 Tage in genau 2 prägnanten deutschen Sätzen zusammen.
        Antworte nur mit der Zusammenfassung, ohne Einleitung. 
        Verwende NUR deutsche Zeichen und Buchstaben.
        """
        try:
            #1. API call
            chat_completion = self.client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model=self.model,
                temperature=0.0  # Für konsistente Ergebnisse
            )

            response = chat_completion.choices[0].message.content.strip()
            #Antwort in float umwandeln -> Hoffnung das auch wirklich nur eine Zahl zurückgegeben wurde
            score = float(response)

            #2. API call für die Zusammenfassung
            completion_summary = self.client.chat.completions.create(
                messages=[{"role": "user", "content": prompt_for_summary}],
                model=self.model,
                temperature=0.5  # Etwas mehr Kreativität für den Text erlaubt
            )
            summary = completion_summary.choices[0].message.content.strip()
            print(f'Score ist: {response}')
            print(f'Summary is: {summary}')
            return score, summary
        except Exception as e:
            print(f"[!] Fehler bei der Groq-Analyse: {e}")
            return 0.0





