def run():
    import streamlit as st
    import numpy as np
    import matplotlib.pyplot as plt

    # ----------------------------
    # HEADER (NO ANCHOR ICON)
    # ----------------------------
    st.markdown("<h1>Trading Dashboard</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color:#6b7280;'>AI-based trading decision support using historical PSX data</p>", unsafe_allow_html=True)

    # ----------------------------
    # STOCK DATA
    # ----------------------------
    stocks_data = {
        "OGDC": {"price": 192.5, "movement": 2.35, "volume": "2.4M"},
        "HBL": {"price": 145.2, "movement": -1.2, "volume": "1.8M"},
        "UBL": {"price": 120.8, "movement": 0.8, "volume": "1.2M"},
        "ENGRO": {"price": 310.5, "movement": 1.5, "volume": "900K"},
        "PSO": {"price": 210.3, "movement": -0.6, "volume": "1.1M"}
    }

    # ----------------------------
    # DROPDOWN
    # ----------------------------
    selected_stock = st.selectbox("Select Stock", list(stocks_data.keys()))
    data = stocks_data[selected_stock]

    stock = selected_stock
    price = data["price"]
    movement = data["movement"]
    volume = data["volume"]

    # ----------------------------
    # AI LOGIC (DUMMY)
    # ----------------------------
    prediction = np.random.uniform(-3, 3)
    accuracy = np.random.uniform(0.6, 0.9)

    if accuracy > 0.7 and prediction > 0:
        decision = "BUY"
        color = "#16a34a"
    elif accuracy > 0.7 and prediction < 0:
        decision = "SELL"
        color = "#dc2626"
    else:
        decision = "HOLD"
        color = "#f59e0b"

    risk = "Low" if accuracy > 0.8 else "Medium" if accuracy > 0.6 else "High"

    # ----------------------------
    # TOP INFO CARD
    # ----------------------------
    st.markdown(f"""
    <div style="
        background:#f8fafc;
        padding:20px;
        border-radius:12px;
        border:1px solid #e5e7eb;
        margin-bottom:20px;
    ">
        <div style="display:flex; justify-content:space-between;">
            <div><b>Selected Stock</b><br>{stock}</div>
            <div><b>Reference Price</b><br>PKR {price}</div>
            <div><b>Price Movement</b><br>{movement:.2f}%</div>
            <div><b>Trading Volume</b><br>{volume}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ----------------------------
    # AI CARDS
    # ----------------------------
    c1, c2, c3 = st.columns(3)

    c1.markdown(f"""
    <div style="
        border:2px solid #16a34a;
        border-radius:12px;
        padding:25px;
        text-align:center;
        height:180px;
    ">
        <div style="font-size:28px;">📈</div>
        <div style="color:#6b7280;">AI Decision</div>
        <h2 style="color:{color}; margin-top:10px;">{decision}</h2>
    </div>
    """, unsafe_allow_html=True)

    c2.markdown(f"""
    <div style="
        background:#f8fafc;
        border:2px solid #16a34a;
        border-radius:12px;
        padding:25px;
        text-align:center;
        height:180px;
    ">
        <div style="font-size:28px;">🎯</div>
        <div style="color:#6b7280;">Confidence Score</div>
        <h2>{int(accuracy*100)}%</h2>
        <div style="height:6px; background:#e5e7eb; border-radius:5px;">
            <div style="width:{int(accuracy*100)}%; height:6px; background:#2563eb; border-radius:5px;"></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    c3.markdown(f"""
    <div style="
        background:#f8fafc;
        border:2px solid #16a34a;
        border-radius:12px;
        padding:25px;
        text-align:center;
        height:180px;
    ">
        <div style="font-size:28px;">⚠️</div>
        <div style="color:#6b7280;">Risk Level</div>
        <h2 style="color:#f59e0b;">{risk}</h2>
    </div>
    """, unsafe_allow_html=True)

    # ----------------------------
    # PRICE CHART
    # ----------------------------
    st.markdown("<h3>Price Chart - Historical vs Predicted</h3>", unsafe_allow_html=True)

    months = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]

    actual = np.linspace(150, 190, 12)
    predicted = actual + np.random.normal(0, 2, 12)

    fig, ax = plt.subplots(figsize=(6,3))
    ax.plot(months, actual, marker='o', label="Actual Price")
    ax.plot(months, predicted, linestyle='dashed', label="Predicted Price")

    ax.set_ylim(0, 200)
    ax.set_yticks([0,50,100,150,200])
    ax.legend(fontsize=8)

    st.pyplot(fig)

    # ----------------------------
    # 🔥 FINAL PERFECT GAUGE (NO CUT)
    # ----------------------------
    st.markdown("<h3>Fear & Greed Index</h3>", unsafe_allow_html=True)

    value = int(accuracy * 100)

    fig, ax = plt.subplots(figsize=(6,4))

    theta = np.linspace(np.pi, 2*np.pi, 300)

    for i in range(len(theta)-1):
        color = plt.cm.RdYlGn(i / len(theta))
        ax.plot([np.cos(theta[i]), np.cos(theta[i+1])],
                [np.sin(theta[i]), np.sin(theta[i+1])],
                linewidth=12,
                color=color)

    angle = np.pi + (value/100) * np.pi
    x = np.cos(angle)
    y = np.sin(angle)

    ax.plot([0, x], [0, y], linewidth=3, color="black")
    ax.scatter(0, 0, s=80, color="black")

    ax.text(0, -0.35, f"{value}", ha='center', fontsize=20, fontweight='bold')

    ax.text(-1.2, -0.55, "Fear", fontsize=11)
    ax.text(0, -0.55, "Neutral", fontsize=11, ha='center')
    ax.text(1.2, -0.55, "Greed", fontsize=11, ha='right')

    ax.set_aspect('equal')
    ax.set_xlim(-1.5, 1.5)
    ax.set_ylim(-1.4, 0.8)

    plt.subplots_adjust(left=0.05, right=0.95, top=10.0, bottom=0.2)

    ax.axis('off')

    col1, col2, col3 = st.columns([1,3,1])
    with col2:
        st.pyplot(fig, use_container_width=True)

    # ----------------------------
    # EXPLANATION
    # ----------------------------
    st.markdown("<h3>AI Decision Explanation</h3>", unsafe_allow_html=True)

    st.markdown(f"""
    <div style="
        background:#f8fafc;
        padding:20px;
        border-radius:12px;
        border:1px solid #e5e7eb;
    ">
    <b>LSTM Price Prediction:</b><br>
    Model predicts <b>{prediction:.2f}% change</b><br><br>

    <b>DQN Decision:</b><br>
    Recommends <b>{decision}</b><br><br>

    <b>Key Factors:</b><br>
    • RSI: 58<br>
    • MACD: Bullish<br>
    </div>
    """, unsafe_allow_html=True)