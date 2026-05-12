"""
STEP 1 — Run this BEFORE retraining.
It tells you exactly which model files exist, when they were saved,
and whether they were trained under the old or new reward signal.
"""

import os
import numpy as np
from datetime import datetime
from tensorflow.keras.models import load_model

BASE_DIR  = os.path.dirname(os.path.abspath(__file__))
MODEL_DIR = os.path.join(BASE_DIR, "..", "models")
STOCKS    = ["ENGRO", "HBL", "MCB", "OGDC", "UBL"]

print("=" * 60)
print("  MODEL FILE DIAGNOSTIC")
print("=" * 60)

for stock in STOCKS:
    path = os.path.join(MODEL_DIR, f"dqn_{stock}.h5")

    if not os.path.exists(path):
        print(f"\n  {stock}: FILE NOT FOUND — {path}")
        continue

    mtime     = os.path.getmtime(path)
    dt        = datetime.fromtimestamp(mtime).strftime("%Y-%m-%d %H:%M:%S")
    size_kb   = os.path.getsize(path) / 1024

    print(f"\n  {stock}")
    print(f"    Path      : {path}")
    print(f"    Saved at  : {dt}")
    print(f"    Size      : {size_kb:.1f} KB")

    # Load and probe Q-values on 3 canonical states
    try:
        model = load_model(path, compile=False)

        # UP TREND state
        s_up     = np.array([[ 0.034,  0.100,  0.066, 0.20]])
        # DOWN TREND state
        s_down   = np.array([[-0.032, -0.100, -0.068, 0.15]])
        # STABLE state
        s_stable = np.array([[ 0.002,  0.003,  0.001, 0.18]])

        q_up     = model.predict(s_up,     verbose=0)[0]
        q_down   = model.predict(s_down,   verbose=0)[0]
        q_stable = model.predict(s_stable, verbose=0)[0]

        def fmt(q): return f"BUY={q[0]:+.3f}  HOLD={q[1]:+.3f}  SELL={q[2]:+.3f}"

        print(f"    UP    Q: {fmt(q_up)}  → {['BUY','HOLD','SELL'][np.argmax(q_up)]}")
        print(f"    DOWN  Q: {fmt(q_down)}  → {['BUY','HOLD','SELL'][np.argmax(q_down)]}")
        print(f"    STABLE Q: {fmt(q_stable)}  → {['BUY','HOLD','SELL'][np.argmax(q_stable)]}")

        # Verdict
        up_ok     = np.argmax(q_up)     == 0   # expects BUY
        down_ok   = np.argmax(q_down)   == 2   # expects SELL
        stable_ok = np.argmax(q_stable) == 1   # expects HOLD

        verdict = "PASS" if (up_ok and down_ok and stable_ok) else "NEEDS RETRAINING"
        print(f"    Verdict   : {verdict}")

    except Exception as e:
        print(f"    ERROR loading model: {e}")

print("\n" + "=" * 60)
print("  If any model shows NEEDS RETRAINING:")
print("  → Run train_dqn_v2.py to retrain with fixed reward")
print("  → Then re-run test_dqn.py")
print("=" * 60)