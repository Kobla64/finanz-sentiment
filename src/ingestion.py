import yfinance as yf 
import pandas as pd 
import os 

class DataIngestor:
    def __init__(self, data_dir="data"):
        print('DEBUG TEST')
        self.data_dir = data_dir
        #erstellen von Datenordner falls nicht Existent
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)

    def fetch_data(self, ticker: str, start_date: str):
        print(f'[*] lade Daten für {ticker}')
        df = yf.download(ticker, start_date)

        #bereinigung, da wir nur den Schlusskurs wollen
        if isinstance(df.columns, pd.MultiIndex):
            df = df['Close']
        else:
            df = df[['Close']]

        df.columns = ['price']
        return df

    def save_data(self, df, filename: str):
        path = os.path.join(self.data_dir, filename)
        df.to_csv(path)
        print(f"[+] Daten erfolgreich unter {path} gespeichert.")

