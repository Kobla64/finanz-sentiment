import yfinance as yf 
import pandas as pd 
import os 

class DataIngestor:
    def __init__(self):
        #erstellen von Datenordner falls nicht Existent
        if not os.path.exists("data"):
            os.makedirs("data")

    def fetch_data(self, ticker: str, start_date: str):
        print(f'[*] lade Daten für {ticker}')
        df = yf.download(ticker, start_date)

        # Bereinigung: Wir wählen Open und Close aus
        if isinstance(df.columns, pd.MultiIndex):
            # Falls yfinance ein MultiIndex zurückgibt (oft bei mehreren Tickern)
            # wählen wir die Spalten auf der obersten Ebene aus
            df = df.loc[:, (['Open', 'Close'], ticker)]
            df.columns = df.columns.get_level_values(0)
        else:
            # Standardfall bei einem einzelnen Ticker
            df = df[['Open', 'Close']]

        return df

    def save_data(self, df, filename: str):
        path = os.path.join("data", filename)
        df.to_csv(path)
        print(f"[+] Daten erfolgreich unter {path} gespeichert.")

    def fetch_and_save(self, ticker: str, start_date: str, filename: str):
        df = self.fetch_data(ticker, start_date)
        self.save_data(df, filename)
        return df


