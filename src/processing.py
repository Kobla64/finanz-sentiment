import pandas as pd

class DataProcessor:
    def __init__(self):
        pass

    def add_moving_averages(self,df):
        df[f'MA20'] = df['Close'].rolling(20).mean()
        df[f'MA50'] = df['Close'].rolling(50).mean()
        return df

    def add_volatility(self,df):
        df['Volatility'] = (df['Close'] - df['Open']).abs() / df['Open']
        return df

    def run_all(self,df):
        df = self.add_moving_averages(df)
        df = self.add_volatility(df)
        df.to_csv("data/processed_stock_data.csv")
        return df




