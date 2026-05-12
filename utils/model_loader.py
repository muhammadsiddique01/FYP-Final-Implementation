import os
from tensorflow.keras.models import load_model

MODEL_PATH = "models"

def load_lstm(stock):
    path = os.path.join(MODEL_PATH, f"lstm_{stock}.h5")
    return load_model(path)

def load_dqn(stock):
    path = os.path.join(MODEL_PATH, f"dqn_{stock}.h5")
    return load_model(path)