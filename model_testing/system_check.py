import os
import traceback
import pandas as pd
import numpy as np
from tensorflow.keras.models import load_model

print("=" * 70)
print("FYP HYBRID TRADING SYSTEM - FINAL SYSTEM VERIFICATION")
print("=" * 70)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# =========================================================
# PATHS
# =========================================================
ROOT_DIR = os.path.abspath(os.path.join(BASE_DIR, ".."))

DATA_PATH = os.path.join(ROOT_DIR, "data", "psx_final_dataset.csv")
MODELS_DIR = os.path.join(ROOT_DIR, "models")
PAGES_DIR = os.path.join(ROOT_DIR, "pages")

STOCKS = ["ENGRO", "HBL", "MCB", "OGDC", "UBL"]

results = []


def add_result(module, status, message):
    results.append({
        "Module": module,
        "Status": status,
        "Message": message
    })


# =========================================================
# DATASET CHECK
# =========================================================
print("\n[1] CHECKING DATASET")
print("-" * 70)

try:

    if os.path.exists(DATA_PATH):

        df = pd.read_csv(DATA_PATH)

        print("Dataset Loaded Successfully")
        print(f"Total Records : {len(df)}")
        print(f"Columns       : {list(df.columns)}")

        required_cols = [
            "Date",
            "Symbol",
            "Open",
            "High",
            "Low",
            "Close",
            "Volume"
        ]

        missing = [c for c in required_cols if c not in df.columns]

        if len(missing) == 0:
            print("All required columns exist")
            add_result("Dataset", "PASS", "Dataset loaded")

        else:
            print(f"Missing columns: {missing}")
            add_result("Dataset", "FAIL", "Missing columns")

    else:
        print("Dataset NOT FOUND")
        add_result("Dataset", "FAIL", "Dataset missing")

except Exception as e:

    print(f"Dataset Error: {e}")
    add_result("Dataset", "FAIL", str(e))


# =========================================================
# MODEL CHECK
# =========================================================
print("\n[2] CHECKING MODELS")
print("-" * 70)

for stock in STOCKS:

    lstm_path = os.path.join(MODELS_DIR, f"lstm_{stock}.h5")
    dqn_path = os.path.join(MODELS_DIR, f"dqn_{stock}.h5")

    # LSTM
    try:

        if os.path.exists(lstm_path):

            load_model(lstm_path, compile=False)

            print(f"LSTM {stock} : OK")
            add_result(f"LSTM {stock}", "PASS", "Loaded")

        else:

            print(f"LSTM {stock} : NOT FOUND")
            add_result(f"LSTM {stock}", "FAIL", "Missing")

    except Exception as e:

        print(f"LSTM {stock} ERROR : {e}")
        add_result(f"LSTM {stock}", "FAIL", str(e))

    # DQN
    try:

        if os.path.exists(dqn_path):

            load_model(dqn_path, compile=False)

            print(f"DQN {stock} : OK")
            add_result(f"DQN {stock}", "PASS", "Loaded")

        else:

            print(f"DQN {stock} : NOT FOUND")
            add_result(f"DQN {stock}", "FAIL", "Missing")

    except Exception as e:

        print(f"DQN {stock} ERROR : {e}")
        add_result(f"DQN {stock}", "FAIL", str(e))


# =========================================================
# PAGE CHECK
# =========================================================
print("\n[3] CHECKING STREAMLIT PAGES")
print("-" * 70)

required_pages = [
    "Dashboard.py",
    "Market_Data.py",
    "Performance.py"
]

for page in required_pages:

    path = os.path.join(PAGES_DIR, page)

    if os.path.exists(path):

        print(f"{page} : FOUND")
        add_result(page, "PASS", "Exists")

    else:

        print(f"{page} : MISSING")
        add_result(page, "FAIL", "Missing")


# =========================================================
# STOCK DATA CHECK
# =========================================================
print("\n[4] CHECKING STOCK RECORDS")
print("-" * 70)

try:

    df = pd.read_csv(DATA_PATH)

    for stock in STOCKS:

        stock_df = df[df["Symbol"] == stock]

        if len(stock_df) > 0:

            print(f"{stock} : {len(stock_df)} records")
            add_result(f"DATA {stock}", "PASS", "Records found")

        else:

            print(f"{stock} : NO DATA")
            add_result(f"DATA {stock}", "FAIL", "No records")

except Exception as e:

    print(f"Stock Data Error : {e}")
    add_result("Stock Data", "FAIL", str(e))


# =========================================================
# PREDICTION TEST
# =========================================================
print("\n[5] TESTING DQN PREDICTIONS")
print("-" * 70)

actions = ["BUY", "HOLD", "SELL"]

states = {
    "UP": np.array([[0.03, 0.10, 0.06, 0.20]]),
    "DOWN": np.array([[-0.03, -0.10, -0.06, 0.15]]),
    "STABLE": np.array([[0.001, 0.002, 0.001, 0.18]])
}

for stock in STOCKS:

    try:

        dqn_path = os.path.join(MODELS_DIR, f"dqn_{stock}.h5")

        model = load_model(dqn_path, compile=False)

        print(f"\n{stock}")

        for name, state in states.items():

            q = model.predict(state, verbose=0)[0]

            decision = actions[np.argmax(q)]

            print(f"{name:10} -> {decision}")

        add_result(f"PREDICTION {stock}", "PASS", "Prediction working")

    except Exception as e:

        print(f"{stock} Prediction Error : {e}")
        traceback.print_exc()

        add_result(f"PREDICTION {stock}", "FAIL", str(e))


# =========================================================
# FINAL SUMMARY
# =========================================================
print("\n")
print("=" * 70)
print("FINAL SUMMARY")
print("=" * 70)

summary_df = pd.DataFrame(results)

print(summary_df.to_string(index=False))

pass_count = len(summary_df[summary_df["Status"] == "PASS"])
fail_count = len(summary_df[summary_df["Status"] == "FAIL"])

print("\n" + "=" * 70)
print(f"TOTAL PASS : {pass_count}")
print(f"TOTAL FAIL : {fail_count}")
print("=" * 70)

if fail_count == 0:

    print("\nSYSTEM STATUS : FULLY WORKING")

else:

    print("\nSYSTEM STATUS : NEEDS FIXES")

print("\nVerification Complete")