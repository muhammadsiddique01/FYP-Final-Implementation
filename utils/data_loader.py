import pandas as pd

def load_data():
    df = pd.read_csv("data/psx_final_dataset.csv")
    return df

def get_stock_data(df, stock):
    df_stock = df[df['Symbol'] == stock]
    df_stock = df_stock.sort_values(by="Date")
    return df_stock