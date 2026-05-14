import os
import numpy as np
import pandas as pd
import joblib

from tensorflow.keras.models import load_model

# ======================
# PATHS
# ======================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MODEL_DIR = os.path.join(
    BASE_DIR,
    "..",
    "models"
)

# ======================
# DATA PATH
# ======================
DATA_PATH = os.path.join(
    BASE_DIR,
    "..",
    "data",
    "psx_final_dataset.csv"
)

# ======================
# SETTINGS
# ======================
STOCKS = [
    "ENGRO",
    "HBL",
    "MCB",
    "OGDC",
    "UBL"
]

FEATURES = [
    'Open',
    'High',
    'Low',
    'Close',
    'Volume',
    'Return',
    'MA_5',
    'MA_10'
]

WINDOW_SIZE = 20

# ======================
# FEATURE ENGINEERING
# ======================
def add_features(df):

    df = df.copy()

    # ======================
    # SAFE CLOSE
    # ======================
    df['Close'] = df['Close'].replace(
        0,
        np.nan
    )

    # ======================
    # RETURNS
    # ======================
    df['Return'] = df['Close'].pct_change()

    # ======================
    # MOVING AVERAGES
    # ======================
    df['MA_5'] = df['Close'].rolling(5).mean()

    df['MA_10'] = df['Close'].rolling(10).mean()

    # ======================
    # REMOVE INF
    # ======================
    df.replace(
        [np.inf, -np.inf],
        np.nan,
        inplace=True
    )

    # ======================
    # FILL NaN
    # ======================
    df = df.ffill().bfill()

    # ======================
    # FINAL SAFETY
    # ======================
    df = df.dropna()

    return df

# ======================
# CREATE SEQUENCES
# ======================
def create_sequences(data):

    X = []

    y = []

    for i in range(
        WINDOW_SIZE,
        len(data)
    ):

        X.append(
            data[i-WINDOW_SIZE:i]
        )

        y.append(
            data[i, FEATURES.index('Close')]
        )

    return (
        np.array(X),
        np.array(y)
    )

# ======================
# LOAD DATA
# ======================
df = pd.read_csv(
    DATA_PATH
)

print("=" * 70)
print("LSTM MODEL TESTING")
print("=" * 70)

# ======================
# LOOP
# ======================
for stock in STOCKS:

    print("\n" + "=" * 50)
    print(f"📈 TESTING {stock}")
    print("=" * 50)

    # ----------------------
    # FILTER STOCK
    # ----------------------
    df_stock = df[
        df['Symbol'] == stock
    ].copy()

    # ----------------------
    # FEATURE ENGINEERING
    # ----------------------
    df_stock = add_features(
        df_stock
    )

    # ----------------------
    # LOAD SCALER
    # ----------------------
    scaler = joblib.load(
        os.path.join(
            MODEL_DIR,
            f"scaler_{stock}.pkl"
        )
    )

    # ----------------------
    # SCALE DATA
    # ----------------------
    scaled_data = scaler.transform(
        df_stock[FEATURES]
    )

    # ----------------------
    # CREATE SEQUENCES
    # ----------------------
    X, y = create_sequences(
        scaled_data
    )

    # ----------------------
    # TRAIN / TEST SPLIT
    # ----------------------
    split = int(
        len(X) * 0.7
    )

    X_test = X[split:]

    y_test = y[split:]

    # ----------------------
    # LOAD MODEL
    # ----------------------
    model = load_model(
        os.path.join(
            MODEL_DIR,
            f"lstm_{stock}.h5"
        ),
        compile=False
    )

    # ----------------------
    # PREDICT
    # ----------------------
    preds = model.predict(
        X_test,
        verbose=0
    )

    # ----------------------
    # INVERSE SCALE
    # ----------------------
    actual_prices = []

    predicted_prices = []

    for i in range(len(preds)):

        # ACTUAL
        dummy_actual = np.zeros(
            (1, len(FEATURES))
        )

        dummy_actual[
            0,
            FEATURES.index('Close')
        ] = y_test[i]

        actual = scaler.inverse_transform(
            dummy_actual
        )[0][FEATURES.index('Close')]

        # PREDICTED
        dummy_pred = np.zeros(
            (1, len(FEATURES))
        )

        dummy_pred[
            0,
            FEATURES.index('Close')
        ] = preds[i][0]

        pred = scaler.inverse_transform(
            dummy_pred
        )[0][FEATURES.index('Close')]

        actual_prices.append(actual)

        predicted_prices.append(pred)

    # ----------------------
    # CONVERT
    # ----------------------
    actual_prices = np.array(
        actual_prices
    )

    predicted_prices = np.array(
        predicted_prices
    )

    # ----------------------
    # METRICS
    # ----------------------
    mae = np.mean(
        np.abs(
            actual_prices - predicted_prices
        )
    )

    rmse = np.sqrt(
        np.mean(
            (
                actual_prices - predicted_prices
            ) ** 2
        )
    )

    bias = np.mean(
        predicted_prices - actual_prices
    )

    # ----------------------
    # PRINT RESULTS
    # ----------------------
    print(f"\nMAE   : {mae:.2f}")

    print(f"RMSE  : {rmse:.2f}")

    print(f"BIAS  : {bias:.2f}")

    # ----------------------
    # VERDICT
    # ----------------------
    if bias > 10:

        verdict = "UPWARD BIAS"

    elif bias < -10:

        verdict = "DOWNWARD BIAS"

    else:

        verdict = "GOOD"

    print(f"🎯 Verdict: {verdict}")

print("\n" + "=" * 70)