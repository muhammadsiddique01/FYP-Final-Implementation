import os
import numpy as np
import joblib
from tensorflow.keras.models import load_model

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_DIR = os.path.join(BASE_DIR, "..", "models")

# ✅ MUST MATCH TRAINING
FEATURES = [
    'Open','High','Low','Close','Volume',
    'Return','MA_5','MA_10'
]

WINDOW_SIZE = 10

# ======================
# LOAD MODEL + SCALER
# ======================
def load_lstm(stock):
    return load_model(os.path.join(MODEL_DIR, f"lstm_{stock}.h5"), compile=False)

def load_scaler(stock):
    return joblib.load(os.path.join(MODEL_DIR, f"scaler_{stock}.pkl"))

# ======================
# FEATURE ENGINEERING (CRITICAL FIX)
# ======================
def add_features(df):
    df = df.copy()

    df['Return'] = df['Close'].pct_change()
    df['MA_5']   = df['Close'].rolling(5).mean()
    df['MA_10']  = df['Close'].rolling(10).mean()

    # clean NaNs
    df.replace([np.inf, -np.inf], np.nan, inplace=True)
    df = df.ffill().bfill()

    return df

# ======================
# CREATE SEQUENCE
# ======================
def create_sequence(df):
    data = df[FEATURES].values
    return np.array([data[-WINDOW_SIZE:]])

# ======================
# MAIN FUNCTION
# ======================
def get_prediction(stock, df_stock):

    df_stock = df_stock.sort_values("Date")

    if len(df_stock) < WINDOW_SIZE:
        return None, "Not enough data", 0, "Unknown"

    # ======================
    # 🔥 ADD FEATURES (FIX)
    # ======================
    df_stock = add_features(df_stock)

    # ======================
    # LOAD SCALER
    # ======================
    scaler = load_scaler(stock)

    df_scaled = df_stock.copy()

    # ======================
    # SCALE INPUT
    # ======================
    df_scaled[FEATURES] = scaler.transform(df_scaled[FEATURES])

    # ======================
    # LSTM PREDICTION
    # ======================
    lstm_model = load_lstm(stock)
    X = create_sequence(df_scaled)

    pred_scaled = lstm_model.predict(X, verbose=0)[0][0]

    # ======================
    # 🔥 INVERSE TRANSFORM
    # ======================
    dummy = np.zeros((1, len(FEATURES)))
    dummy[0, FEATURES.index('Close')] = pred_scaled

    predicted_price = scaler.inverse_transform(dummy)[0][FEATURES.index('Close')]

    # ======================
    # CURRENT PRICE
    # ======================
    current_price = float(df_stock.iloc[-1]['Close'])

    # ======================
    # CHANGE %
    # ======================
    change_pct = (predicted_price - current_price) / current_price

    # ======================
    # DECISION
    # ======================
    if change_pct > 0.03:
        decision = "BUY"
    elif change_pct < -0.03:
        decision = "SELL"
    else:
        decision = "HOLD"

    # ======================
    # CONFIDENCE
    # ======================
    confidence = min(abs(change_pct) * 10, 1.0)
    confidence = round(confidence * 100, 2)

    # ======================
    # RISK
    # ======================
    if abs(change_pct) < 0.02:
        risk = "Low"
    elif abs(change_pct) < 0.05:
        risk = "Moderate"
    else:
        risk = "High"

    return float(predicted_price), decision, confidence, risk