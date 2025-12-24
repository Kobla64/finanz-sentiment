import pandas as pd

def volatility():
    df = pd.read_csv('data/raw_stock_data.csv', index_col=0, parse_dates=True)

    #Berechnen der Volatitilität
    #2 Ansatze für die Definition von Volatilität
    df['Volatility'] = (df['Close'] - df['Open']).abs() / df['Open']
    df['Volat2'] = (df['Close'] - df['Open']).abs()
    #Daten abspeichern
    df.to_csv("data/processed_stock_data.csv")



