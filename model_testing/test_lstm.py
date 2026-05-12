import os
import pandas as pd
import numpy as np
import joblib
from tensorflow.keras.models import load_model

# ======================
# PATHS (FIXED)
# ======================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 🔥 CHANGE ONLY IF YOUR DATA LOCATION IS DIFFERENT
DATA_PATH = r"C:\UNIVERSITY\FYP\FYP DATASET\data\splits\test.csv"

MODEL_PATH = os.path.join(BASE_DIR, "../models/lstm_ENGRO.h5")
SCALER_PATH = os.path.join(BASE_DIR, "../models/scaler_ENGRO.pkl")

# ======================
# FEATURES (SAME AS TRAINING)
# ======================
FEATURES = [
    'Open','High','Low','Close','Volume',
    'Return','MA_5','MA_10'
]

WINDOW_SIZE = 20

# ======================
# FEATURE ENGINEERING
# ======================
def add_features(df):
    df = df.copy()

    df['Return'] = df['Close'].pct_change()
    df['MA_5'] = df['Close'].rolling(5).mean()
    df['MA_10'] = df['Close'].rolling(10).mean()

    df = df.dropna()
    return df

# ======================
# LOAD DATA
# ======================
df = pd.read_csv(DATA_PATH)
df = df[df['Symbol'] == 'ENGRO'].sort_values("Date")

df = add_features(df)

# ======================
# LOAD MODEL + SCALER
# ======================
model = load_model(MODEL_PATH, compile=False)
scaler = joblib.load(SCALER_PATH)

# ======================
# SCALE INPUT
# ======================
df_scaled = df.copy()
df_scaled[FEATURES] = scaler.transform(df_scaled[FEATURES])

data = df_scaled[FEATURES].values

print("\n🔍 Testing LSTM (REAL PRICES)...\n")

# ======================
# TEST LOOP
# ======================
for i in range(WINDOW_SIZE, len(data)):

    # INPUT WINDOW
    X = np.array([data[i-WINDOW_SIZE:i]])

    # PREDICTION (scaled)
    pred_scaled = model.predict(X, verbose=0)[0][0]

    # ======================
    # INVERSE TRANSFORM
    # ======================
    dummy = np.zeros((1, len(FEATURES)))
    dummy[0, 3] = pred_scaled  # Close index

    pred_real = scaler.inverse_transform(dummy)[0][3]

    # ======================
    # ACTUAL PRICE
    # ======================
    actual_real = df.iloc[i]['Close']

    print(f"Predicted: {pred_real:.2f} PKR | Actual: {actual_real:.2f} PKR")