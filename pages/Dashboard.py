def run():

    import streamlit as st
    import numpy as np
    import matplotlib.pyplot as plt

    # =========================
    # BACKEND IMPORTS
    # =========================
    from utils.data_loader import (
        load_data,
        get_stock_data
    )

    from utils.predict import (
        get_prediction
    )

    # =========================
    # HEADER
    # =========================
    st.markdown("# Trading Dashboard")

    st.markdown(
        """
AI-based hybrid trading decision support system
using LSTM forecasting and DQN reinforcement learning
for Pakistan Stock Exchange (PSX).
        """
    )

    # =========================
    # LOAD DATA
    # =========================
    df = load_data()

    stocks = sorted(
        df['Symbol'].unique()
    )

    # =========================
    # INPUT SECTION
    # =========================
    col1, col2, col3 = st.columns(
        [2, 2, 1]
    )

    # =========================
    # STOCK SELECT
    # =========================
    with col1:

        selected_stock = st.selectbox(
            "Select Stock",
            stocks
        )

    # =========================
    # GET STOCK DATA
    # =========================
    df_stock = get_stock_data(
        df,
        selected_stock
    )

    latest = df_stock.iloc[-1]

    # =========================
    # LATEST HISTORICAL CLOSE
    # =========================
    with col2:

        latest_close = float(
            latest['Close']
        )

        st.metric(
            "Latest Historical Close",
            f"PKR {latest_close:.2f}"
        )

    # =========================
    # PREDICT BUTTON
    # =========================
    with col3:

        st.markdown(
            "<br>",
            unsafe_allow_html=True
        )

        predict_btn = st.button(
            "Run AI Prediction",
            use_container_width=True
        )

    # =========================
    # RUN AI PREDICTION
    # =========================
    if predict_btn:

        # =========================
        # BASIC METRICS
        # =========================
        stock = selected_stock

        volume = (
            f"{round(latest['Volume']/1e6,2)}M"
        )

        # =========================
        # AI PREDICTION
        # =========================
        predicted_price, decision, confidence, risk = get_prediction(
            selected_stock,
            df_stock,
            latest_close
        )

        # =========================
        # SAFETY CHECK
        # =========================
        if predicted_price is None:

            st.error(
                "Prediction failed."
            )

            return

        # =========================
        # PRICE MOVEMENT
        # =========================
        movement = (
            (predicted_price - latest_close)
            / (latest_close + 1e-8)
        ) * 100

        # =========================
        # CONFIDENCE FIX
        # =========================
        confidence = max(
            0,
            min(confidence, 100)
        )

        confidence_percent = int(
            confidence
        )

        # =========================
        # TOP METRICS
        # =========================
        st.markdown("---")

        m1, m2, m3, m4, m5 = st.columns(5)

        # STOCK
        with m1:

            st.metric(
                "Selected Stock",
                stock
            )

        # HISTORICAL CLOSE
        with m2:

            st.metric(
                "Latest Historical Close",
                f"PKR {latest_close:.2f}"
            )

        # PREDICTED PRICE
        with m3:

            st.metric(
                "Predicted Next Close",
                f"PKR {predicted_price:.2f}"
            )

        # MOVEMENT
        with m4:

            st.metric(
                "Expected Movement",
                f"{movement:.2f}%"
            )

        # VOLUME
        with m5:

            st.metric(
                "Trading Volume",
                volume
            )

        st.markdown("---")

        # =========================
        # AI RESULT CARDS
        # =========================
        c1, c2, c3 = st.columns(3)

        # =========================
        # DECISION CARD
        # =========================
        if decision == "BUY":

            c1.success(
                f"AI Decision: {decision}"
            )

        elif decision == "SELL":

            c1.error(
                f"AI Decision: {decision}"
            )

        else:

            c1.warning(
                f"AI Decision: {decision}"
            )

        # =========================
        # CONFIDENCE CARD
        # =========================
        c2.info(
            f"Confidence Score: {confidence_percent}%"
        )

        # =========================
        # RISK CARD
        # =========================
        if risk == "Low":

            c3.success(
                f"Risk Level: {risk}"
            )

        elif risk == "Moderate":

            c3.warning(
                f"Risk Level: {risk}"
            )

        else:

            c3.error(
                f"Risk Level: {risk}"
            )

        # =========================
        # PRICE CHART
        # =========================
        st.subheader(
            "Historical vs Predicted Price"
        )

        last_20 = df_stock.tail(20)

        dates = last_20['Date']

        actual = last_20['Close']

        # CREATE PREDICTION LINE
        predicted = actual.copy()

        predicted.iloc[-1] = predicted_price

        fig, ax = plt.subplots(
            figsize=(10, 4)
        )

        # ACTUAL LINE
        ax.plot(
            dates,
            actual,
            marker='o',
            linewidth=2,
            label="Historical Close"
        )

        # PREDICTED LINE
        ax.plot(
            dates,
            predicted,
            linestyle='dashed',
            linewidth=2,
            label="Predicted Next Close"
        )

        ax.legend(
            fontsize=8
        )

        ax.tick_params(
            axis='x',
            rotation=45
        )

        st.pyplot(fig)

        # =========================
        # FEAR & GREED INDEX
        # =========================
        st.subheader(
            "Fear & Greed Index"
        )

        value = confidence_percent

        fig2, ax2 = plt.subplots(
            figsize=(6, 4)
        )

        theta = np.linspace(
            np.pi,
            2*np.pi,
            300
        )

        # COLOR ARC
        for i in range(len(theta)-1):

            color_arc = plt.cm.RdYlGn(
                i / len(theta)
            )

            ax2.plot(
                [
                    np.cos(theta[i]),
                    np.cos(theta[i+1])
                ],
                [
                    np.sin(theta[i]),
                    np.sin(theta[i+1])
                ],
                linewidth=12,
                color=color_arc
            )

        # NEEDLE
        angle = np.pi + (
            value / 100
        ) * np.pi

        x = np.cos(angle)

        y = np.sin(angle)

        ax2.plot(
            [0, x],
            [0, y],
            linewidth=3,
            color="black"
        )

        ax2.scatter(
            0,
            0,
            s=80,
            color="black"
        )

        # VALUE TEXT
        ax2.text(
            0,
            -0.35,
            f"{value}",
            ha='center',
            fontsize=20,
            fontweight='bold'
        )

        ax2.set_aspect('equal')

        ax2.axis('off')

        col_a, col_b, col_c = st.columns(
            [1, 3, 1]
        )

        with col_b:

            st.pyplot(
                fig2,
                use_container_width=True
            )

        # =========================
        # AI EXPLANATION
        # =========================
        st.subheader(
            "AI Decision Explanation"
        )

        st.info(f"""
Latest Historical Close: PKR {latest_close:.2f}

LSTM Predicted Next Close: PKR {predicted_price:.2f}

Expected Price Movement: {movement:.2f}%

DQN Trading Decision: {decision}

Confidence Score: {confidence_percent}%

Risk Level: {risk}

The hybrid AI system uses five years of historical
Pakistan Stock Exchange (PSX) data.

The LSTM deep learning model forecasts the next
future stock price using historical sequential
patterns, while the DQN reinforcement learning
agent generates intelligent BUY, HOLD, or SELL
trading decisions based on market state analysis.
        """)