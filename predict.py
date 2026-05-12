import numpy as np
from utils.model_loader import load_lstm, load_dqn

WINDOW_SIZE = 10
FEATURES = ['Open', 'High', 'Low', 'Close', 'Volume']

def prepare_input(df_stock):
    last_data = df_stock[FEATURES].values[-WINDOW_SIZE:]
    return np.expand_dims(last_data, axis=0)

def get_prediction(stock, df_stock):
    lstm_model = load_lstm(stock)
    dqn_model = load_dqn(stock)

    X = prepare_input(df_stock)

    # LSTM prediction
    pred = lstm_model.predict(X, verbose=0)
    predicted_price = float(pred[0][0])

    # DQN decision
    q_values = dqn_model.predict(X, verbose=0)
    action = np.argmax(q_values)

    decision_map = {0: "SELL", 1: "HOLD", 2: "BUY"}
    decision = decision_map.get(action, "HOLD")

    confidence = float(np.max(q_values))

    return predicted_price, decision, confidence