def run():
    import streamlit as st
    import numpy as np
    import matplotlib.pyplot as plt

    # 🔥 BACKEND IMPORTS
    from utils.data_loader import load_data, get_stock_data
    from utils.predict import get_prediction

    # ----------------------------
    # HEADER
    # ----------------------------
    st.markdown("<h1>Trading Dashboard</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color:#6b7280;'>AI-based trading decision support using historical PSX data</p>", unsafe_allow_html=True)

    # ----------------------------
    # LOAD DATA
    # ----------------------------
    df = load_data()

    stocks = df['Symbol'].unique()
    selected_stock = st.selectbox("Select Stock", stocks)

    df_stock = get_stock_data(df, selected_stock)

    # ----------------------------
    # BASIC INFO
    # ----------------------------
    latest = df_stock.iloc[-1]

    stock = selected_stock
    current_price = float(latest['Close'])

    prev_price = float(df_stock.iloc[-2]['Close'])
    movement = ((current_price - prev_price) / prev_price) * 100

    volume = f"{round(latest['Volume']/1e6,2)}M"

    # ----------------------------
    # 🔥 AI PREDICTION
    # ----------------------------
    predicted_price, decision, confidence, risk = get_prediction(selected_stock, df_stock)

    confidence = max(0, min(1, confidence))   # safety clamp
    confidence_percent = int(confidence * 100)

    # ----------------------------
    # DECISION COLOR
    # ----------------------------
    if decision == "BUY":
        color = "#16a34a"
    elif decision == "SELL":
        color = "#dc2626"
    else:
        color = "#f59e0b"

    # ----------------------------
    # TOP INFO CARD (FIXED)
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
            <div><b>Current Price</b><br>PKR {current_price:.2f}</div>
            <div><b>Predicted Price</b><br>PKR {predicted_price:.2f}</div>
            <div><b>Price Movement</b><br>{movement:.2f}%</div>
            <div><b>Trading Volume</b><br>{volume}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ----------------------------
    # AI CARDS
    # ----------------------------
    c1, c2, c3 = st.columns(3)

    # Decision
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

    # Confidence
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
        <h2>{confidence_percent}%</h2>
        <div style="height:6px; background:#e5e7eb; border-radius:5px;">
            <div style="width:{confidence_percent}%; height:6px; background:#2563eb; border-radius:5px;"></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Risk
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

    last_12 = df_stock.tail(12)

    months = last_12['Date']
    actual = last_12['Close']

    predicted = actual.copy()
    predicted.iloc[-1] = predicted_price

    fig, ax = plt.subplots(figsize=(6,3))
    ax.plot(months, actual, marker='o', label="Actual Price")
    ax.plot(months, predicted, linestyle='dashed', label="Predicted Price")

    ax.legend(fontsize=8)
    ax.tick_params(axis='x', rotation=45)

    st.pyplot(fig)

    # ----------------------------
    # FEAR & GREED INDEX
    # ----------------------------
    st.markdown("<h3>Fear & Greed Index</h3>", unsafe_allow_html=True)

    value = confidence_percent

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

    ax.set_aspect('equal')
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
    <b>Current Price:</b><br>
    PKR {current_price:.2f}<br><br>

    <b>LSTM Predicted Price:</b><br>
    PKR {predicted_price:.2f}<br><br>

    <b>Decision:</b><br>
    {decision}<br><br>

    <b>Confidence:</b><br>
    {confidence_percent}%<br><br>

    <b>Risk Level:</b><br>
    {risk}
    </div>
    """, unsafe_allow_html=True)