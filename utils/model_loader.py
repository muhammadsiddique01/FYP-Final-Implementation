import os

from tensorflow.keras.models import load_model

# =========================
# BASE PATH
# =========================
BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

MODEL_PATH = os.path.join(
    BASE_DIR,
    "..",
    "models"
)

# =========================
# LOAD LSTM MODEL
# =========================
def load_lstm(stock):

    path = os.path.join(
        MODEL_PATH,
        f"lstm_{stock}.h5"
    )

    return load_model(
        path,
        compile=False
    )

# =========================
# LOAD DQN MODEL
# =========================
def load_dqn(stock):

    path = os.path.join(
        MODEL_PATH,
        f"dqn_{stock}.h5"
    )

    return load_model(
        path,
        compile=False
    )