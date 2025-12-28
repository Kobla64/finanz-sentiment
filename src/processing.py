import pandas as pd

def volatility():
    df = pd.read_csv('data/raw_stock_data.csv', index_col=0, parse_dates=True)

    #Berechnen der Volatitilität
    #2 Ansatze für die Definition von Volatilität
    df['Volatility'] = (df['Close'] - df['Open']).abs() / df['Open']
    df['MA20'] = df['Close'].rolling(20).mean()
    df['MA50'] = df['Close'].rolling(50).mean()

    #Daten abspeichern
    df.to_csv("data/processed_stock_data.csv")



