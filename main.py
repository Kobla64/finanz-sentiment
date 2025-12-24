from src.ingestion import DataIngestor
from src.processing import volatility


def main():
    print('Hello World')
    ingestor = DataIngestor(data_dir="data") #Instanziierung des Aufnehmers

    ticker = "^GDAXI" #Wahl des tickers HIER DAX
    #Ingestion der Daten
    df_prices = ingestor.fetch_data(ticker, "2024-01-01")

    #Speichern der Rohdaten
    ingestor.save_data(df_prices, "raw_stock_data.csv")

    volatility()
if __name__ == "__main__":
    main()
