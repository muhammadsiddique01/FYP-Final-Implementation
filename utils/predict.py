import os
import numpy as np
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
# FEATURES
# ======================
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

# ======================
# WINDOW SIZE
# ======================
WINDOW_SIZE = 20

# ======================
# LOAD LSTM MODEL
# ======================
def load_lstm(stock):

    return load_model(
        os.path.join(
            MODEL_DIR,
            f"lstm_{stock}.h5"
        ),
        compile=False
    )

# ======================
# LOAD DQN MODEL
# ======================
def load_dqn(stock):

    return load_model(
        os.path.join(
            MODEL_DIR,
            f"dqn_{stock}.h5"
        ),
        compile=False
    )

# ======================
# LOAD SCALER
# ======================
def load_scaler(stock):

    return joblib.load(
        os.path.join(
            MODEL_DIR,
            f"scaler_{stock}.pkl"
        )
    )

# ======================
# FEATURE ENGINEERING
# ======================
def add_features(df):

    df = df.copy()

    # SAFE CLOSE
    df['Close'] = df['Close'].replace(
        0,
        np.nan
    )

    # RETURNS
    df['Return'] = df['Close'].pct_change()

    # MOVING AVERAGES
    df['MA_5'] = df['Close'].rolling(5).mean()

    df['MA_10'] = df['Close'].rolling(10).mean()

    # REMOVE INF
    df.replace(
        [np.inf, -np.inf],
        np.nan,
        inplace=True
    )

    # FILL NaN
    df = df.ffill().bfill()

    # DROP NaN
    df = df.dropna()

    return df

# ======================
# CREATE LSTM SEQUENCE
# ======================
def create_sequence(df):

    data = df[FEATURES].values

    return np.array([
        data[-WINDOW_SIZE:]
    ])

# ======================
# MAIN PREDICTION FUNCTION
# ======================
def get_prediction(
    stock,
    df_stock,
    latest_close
):

    # ======================
    # SORT DATA
    # ======================
    df_stock = df_stock.sort_values(
        "Date"
    )

    # ======================
    # CHECK MINIMUM DATA
    # ======================
    if len(df_stock) < WINDOW_SIZE:

        return (
            None,
            "Not enough data",
            0,
            "Unknown"
        )

    # ======================
    # FEATURE ENGINEERING
    # ======================
    df_stock = add_features(
        df_stock
    )

    # ======================
    # LOAD SCALER
    # ======================
    scaler = load_scaler(
        stock
    )

    # ======================
    # SCALE FEATURES
    # ======================
    df_scaled = df_stock.copy()

    df_scaled[FEATURES] = scaler.transform(
        df_scaled[FEATURES]
    )

    # ======================
    # CREATE LSTM INPUT
    # ======================
    X = create_sequence(
        df_scaled
    )

    # ======================
    # LOAD LSTM
    # ======================
    lstm_model = load_lstm(
        stock
    )

    # ======================
    # PREDICT NEXT PRICE
    # ======================
    pred_scaled = lstm_model.predict(
        X,
        verbose=0
    )[0][0]

    # ======================
    # INVERSE TRANSFORM
    # ======================
    dummy = np.zeros(
        (1, len(FEATURES))
    )

    dummy[
        0,
        FEATURES.index('Close')
    ] = pred_scaled

    predicted_price = scaler.inverse_transform(
        dummy
    )[0][FEATURES.index('Close')]

    predicted_price = float(
        predicted_price
    )

    # ======================
    # HISTORICAL MARKET STATE
    # ======================
    prev_close = float(
        df_stock.iloc[-2]['Close']
    )

    latest_volume = float(
        df_stock.iloc[-1]['Volume']
    )

    # ======================
    # MARKET MOVEMENT
    # ======================
    historical_change = (
        latest_close - prev_close
    ) / (prev_close + 1e-8)

    predicted_change = (
        predicted_price - latest_close
    ) / (latest_close + 1e-8)

    trend_strength = (
        predicted_change - historical_change
    )

    # ======================
    # NORMALIZED VOLUME
    # ======================
    volume = latest_volume / 1e6

    # ======================
    # CREATE DQN STATE
    # ======================
    state = np.array([[

        np.clip(
            historical_change,
            -0.1,
            0.1
        ),

        np.clip(
            predicted_change,
            -0.1,
            0.1
        ),

        np.clip(
            trend_strength,
            -0.1,
            0.1
        ),

        np.clip(
            volume,
            0,
            10
        )

    ]])

    # ======================
    # LOAD DQN MODEL
    # ======================
    dqn_model = load_dqn(
        stock
    )

    # ======================
    # DQN PREDICTION
    # ======================
    q_values = dqn_model.predict(
        state,
        verbose=0
    )

    action = np.argmax(
        q_values[0]
    )

    # ======================
    # RL SIGNAL
    # ======================
    if action == 0:

        rl_signal = "BUY"

    elif action == 2:

        rl_signal = "SELL"

    else:

        rl_signal = "HOLD"

    # ======================
    # EXPECTED MOVEMENT %
    # ======================
    movement_percent = (
        (predicted_price - latest_close)
        / (latest_close + 1e-8)
    ) * 100

    # ======================
    # FINAL HYBRID DECISION
    # ======================
    if (
        movement_percent > 1.5
        and rl_signal == "BUY"
    ):

        decision = "BUY"

    elif (
        movement_percent < -1.5
        and rl_signal == "SELL"
    ):

        decision = "SELL"

    elif movement_percent > 5:

        decision = "BUY"

    elif movement_percent < -5:

        decision = "SELL"

    else:

        decision = "HOLD"

    # ======================
    # CONFIDENCE SCORE
    # ======================
    confidence = min(
        abs(movement_percent) * 2,
        100
    )

    confidence = round(
        confidence,
        2
    )

    # ======================
    # RISK LEVEL
    # ======================
    if abs(movement_percent) < 2:

        risk = "Low"

    elif abs(movement_percent) < 5:

        risk = "Moderate"

    else:

        risk = "High"

    # ======================
    # RETURN RESULTS
    # ======================
    return (
        round(predicted_price, 2),
        decision,
        confidence,
        risk
    )