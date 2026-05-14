import pandas as pd

# =========================
# LOAD COMPLETE DATASET
# =========================
def load_data():

    df = pd.read_csv(
        "data/psx_final_dataset.csv"
    )

    # SORT DATA
    df = df.sort_values(
        by=["Symbol", "Date"]
    )

    # RESET INDEX
    df = df.reset_index(
        drop=True
    )

    return df

# =========================
# GET SINGLE STOCK DATA
# =========================
def get_stock_data(
    df,
    stock
):

    df_stock = df[
        df['Symbol'] == stock
    ].copy()

    # SORT BY DATE
    df_stock = df_stock.sort_values(
        by="Date"
    )

    # RESET INDEX
    df_stock = df_stock.reset_index(
        drop=True
    )

    return df_stock