import yfinance as yf 
import pandas as pd 
import os 

class DataIngestor:
    def __init__(self, data_dir="data"):
        self.data_dir = data_dir
        #erstellen von Datenordner falls nicht Existent
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)

    def fetch_data(self, ticker: str, start_date: str):
        print(f'[*] lade Daten für {ticker}')
        df = yf.download(ticker, start_date)

        # Bereinigung: Wir wählen Open und Close aus
        if isinstance(df.columns, pd.MultiIndex):
            # Falls yfinance ein MultiIndex zurückgibt (oft bei mehreren Tickern)
            # wählen wir die Spalten auf der obersten Ebene aus
            df = df.loc[:, (['Open', 'Close'], ticker)]
            # Optional: MultiIndex glätten, damit die CSV sauberer aussieht
            df.columns = df.columns.get_level_values(0)
        else:
            # Standardfall bei einem einzelnen Ticker
            df = df[['Open', 'Close']]

        # Optional: Wenn du die Spalten für den Chart umbenennen willst
        # df.columns = ['open_price', 'close_price']

        return df
    def save_data(self, df, filename: str):
        path = os.path.join(self.data_dir, filename)
        df.to_csv(path)
        print(f"[+] Daten erfolgreich unter {path} gespeichert.")

