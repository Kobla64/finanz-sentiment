import yfinance as yf
import pandas as pd

# Konfiguration
TICKER = "^GDAXI"  # Symbol für den DAX
START_DATE = "2023-01-01"
OUTPUT_FILE = "dax_prices.csv"

def download_data():
    print(f"Lade Daten für {TICKER} ab {START_DATE} herunter...")
    
    # Daten von Yahoo Finance laden
    df = yf.download(TICKER, start=START_DATE)
    
    # Wir brauchen nur den Schlusskurs ('Close')
    # yfinance liefert oft Multi-Level-Spalten, wir vereinfachen das:
    if isinstance(df.columns, pd.MultiIndex):
        df = df['Close']
    else:
        df = df[['Close']]
        
    # Spalte umbenennen für Klarheit
    df.columns = ['Close']
    
    # Speichern
    df.to_csv(OUTPUT_FILE)
    print(f"Erfolg! {len(df)} Zeilen in '{OUTPUT_FILE}' gespeichert.")
    print(df.tail()) # Die letzten 5 Zeilen anzeigen

if __name__ == "__main__":
    download_data()