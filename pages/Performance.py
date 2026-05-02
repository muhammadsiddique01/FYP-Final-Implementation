def run():
    import streamlit as st
    import pandas as pd
    import numpy as np

    st.set_page_config(layout="wide")

    # ---------------- CSS ----------------
    st.markdown("""
    <style>

    .main {
        background-color: #f5f7fb;
    }

    .block-container {
        padding-top: 2rem;
    }

    /* CARD */
    .stContainer {
        background: white;
        padding: 20px;
        border-radius: 14px;
        box-shadow: 0px 2px 8px rgba(0,0,0,0.06);
        margin-bottom: 20px;
    }

    /* KPI BOX */
    .metric-box {
        background: white;
        padding: 20px;
        border-radius: 14px;
        box-shadow: 0px 2px 8px rgba(0,0,0,0.06);
        text-align: center;
    }

    .metric-title {
        font-size: 14px;
        color: #6b7280;
    }

    .metric-value {
        font-size: 22px;
        font-weight: bold;
    }

    </style>
    """, unsafe_allow_html=True)

    # ---------------- TITLE ----------------
    st.title("Performance Analysis")
    st.caption("Backtesting results based on historical PSX data")

    # ---------------- KPI CARDS ----------------
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown("""
        <div class="metric-box">
            <div class="metric-title">Total Return (Simulated)</div>
            <div class="metric-value" style="color:green;">+12.4%</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="metric-box">
            <div class="metric-title">Win Rate</div>
            <div class="metric-value" style="color:#2563eb;">61.8%</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="metric-box">
            <div class="metric-title">Max Drawdown</div>
            <div class="metric-value" style="color:red;">-6.5%</div>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown("""
        <div class="metric-box">
            <div class="metric-title">Risk-Adjusted Score</div>
            <div class="metric-value" style="color:#2563eb;">Moderate</div>
        </div>
        """, unsafe_allow_html=True)

    # ---------------- EQUITY CURVE ----------------
    with st.container():
        st.subheader("Equity Curve")

        # Dummy data
        months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
                  "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        equity = np.cumsum(np.random.randint(-5000, 8000, 12)) + 100000

        chart_data = pd.DataFrame({
            "Month": months,
            "Equity": equity
        })

        st.line_chart(chart_data.set_index("Month"))

    # ---------------- TRADE HISTORY ----------------
    with st.container():
        st.subheader("Simulated Trade History")

        data = pd.DataFrame({
            "Date": ["2024-01-15", "2024-01-12", "2024-01-10", "2024-01-08", "2024-01-05"],
            "Stock": ["OGDC", "PPL", "ENGRO", "HBL", "LUCK"],
            "Action": ["BUY", "SELL", "BUY", "SELL", "BUY"],
            "Reference Price": [185.50, 92.75, 245.00, 78.50, 520.25],
            "Position": ["-", "-", "-", "-", "-"],
            "Reward/Loss": ["+3.2%", "-1.5%", "+2.8%", "-0.9%", "+4.1%"]
        })

        # Color BUY/SELL
        def color_action(val):
            if val == "BUY":
                return "color: green"
            elif val == "SELL":
                return "color: red"
            return ""

        st.dataframe(data, use_container_width=True)

        st.caption("*All results shown are simulated for academic purposes.")