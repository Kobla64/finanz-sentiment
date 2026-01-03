from src.ingestion import DataIngestor
from src.processing import DataProcessor
import subprocess
import json
from src.sentiment import SentimentAnalyzer


def main():
    #Instanziierung von den Bestandteilen der Pipelinearchitektur
    ingestor = DataIngestor()
    processor = DataProcessor()
    analyzer = SentimentAnalyzer()

    ticker = "^GSPC" #Wahl des tickers HIER SP500

    df = ingestor.fetch_and_save(ticker, "2025-01-01", "raw_stock_data.csv")
    df = processor.run_all(df)

    score,summary = analyzer.get_sentiment(ticker)
    df['Sentiment'] = score
    df.to_csv("data/evaluated_processed_stock_data.csv")

    metadata = {
        "ticker": ticker,
        "sentiment_score": score,
        "summary": summary
    }
    with open("data/sentiment_metadata.json", "w", encoding="utf-8") as f:
        json.dump(metadata, f, ensure_ascii=False, indent=4)
    print("[*] Analyse abgeschlossen und Metadaten gespeichert.")

    subprocess.run(["streamlit", "run", "src/dashboard.py"])
if __name__ == "__main__":
    main()
