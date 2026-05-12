import os
import numpy as np
from tensorflow.keras.models import load_model

# ======================
# PATH
# ======================
BASE_DIR  = os.path.dirname(os.path.abspath(__file__))
MODEL_DIR = os.path.join(BASE_DIR, "..", "models")

STOCKS = ["ENGRO", "HBL", "MCB", "OGDC", "UBL"]

print("=" * 60)
print("  DQN MODEL TESTING (CONSISTENT WITH CHECK_MODELS)")
print("=" * 60)

# ======================
# ACTIONS
# ======================
actions = ["BUY", "HOLD", "SELL"]

# ======================
# SAME STATES AS check_models
# ======================
s_up     = np.array([[ 0.034,  0.100,  0.066, 0.20]])
s_down   = np.array([[-0.032, -0.100, -0.068, 0.15]])
s_stable = np.array([[ 0.002,  0.003,  0.001, 0.18]])

# ======================
# LOOP
# ======================
for stock in STOCKS:

    path = os.path.join(MODEL_DIR, f"dqn_{stock}.h5")

    if not os.path.exists(path):
        print(f"\n{stock}: MODEL NOT FOUND")
        continue

    print("\n" + "="*50)
    print(f"📈 TESTING {stock}")
    print("="*50)

    model = load_model(path, compile=False)

    # ======================
    # PREDICTIONS
    # ======================
    q_up     = model.predict(s_up,     verbose=0)[0]
    q_down   = model.predict(s_down,   verbose=0)[0]
    q_stable = model.predict(s_stable, verbose=0)[0]

    # ======================
    # OUTPUT
    # ======================
    def show(name, q):
        print(f"\n📊 {name}")
        print(f"Q-values : {np.round(q, 3)}")
        print(f"Decision : {actions[np.argmax(q)]}")

    show("UP TREND", q_up)
    show("DOWN TREND", q_down)
    show("STABLE", q_stable)

    # ======================
    # VERDICT (same logic)
    # ======================
    up_ok     = np.argmax(q_up)     == 0
    down_ok   = np.argmax(q_down)   == 2
    stable_ok = np.argmax(q_stable) == 1

    verdict = "PASS" if (up_ok and down_ok and stable_ok) else "NOT PERFECT"

    print(f"\n🎯 Verdict: {verdict}")

print("\n" + "=" * 60)