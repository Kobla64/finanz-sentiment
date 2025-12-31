from src.ingestion import DataIngestor
from src.processing import DataProcessor
import subprocess

from src.sentiment import SentimentAnalyzer


def main():
    #Instanziierung von den Bestandteilen der Pipelinearchitektur
    ingestor = DataIngestor()
    processor = DataProcessor()
    analyzer = SentimentAnalyzer()

    ticker = "^GSPC" #Wahl des tickers HIER SP500

    df = ingestor.fetch_and_save(ticker, "2025-01-01", "raw_stock_data.csv")
    df = processor.run_all(df)
    df['Sentiment'] = analyzer.get_sentiment(ticker)
    df.to_csv("data/evaluated_processed_stock_data.csv")


    subprocess.run(["streamlit", "run", "src/dashboard.py"])
if __name__ == "__main__":
    main()
