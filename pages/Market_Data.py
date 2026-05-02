def run():
    import streamlit as st
    import pandas as pd
    from datetime import datetime, timedelta

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

    /* Card style using container */
    section.main > div > div > div > div {
        background: transparent;
    }

    .stContainer {
        background: white;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0px 2px 8px rgba(0,0,0,0.06);
        margin-bottom: 20px;
    }

    /* Table */
    table {
        width: 100%;
        border-collapse: collapse;
    }

    th {
        text-align: left;
        padding: 10px;
        border-bottom: 1px solid #e5e7eb;
    }

    td {
        padding: 10px;
        border-bottom: 1px solid #f1f5f9;
    }

    tr:hover {
        background-color: #f9fafb;
    }

    </style>
    """, unsafe_allow_html=True)

    # ---------------- TITLE ----------------
    st.title("Market Data")
    st.caption("Historical PSX stock price data used for analysis and model input")

    # ---------------- FILTER ----------------
    with st.container():
        col1, col2 = st.columns(2)

        with col1:
            stock = st.selectbox("Select Stock", ["OGDC", "HBL", "MCB", "UBL"])

        with col2:
            range_option = st.selectbox("Date Range", ["Last 7 Days", "Last 30 Days", "Last 90 Days"])

    # ---------------- DATA ----------------
    def generate_data(days):
        dates = [datetime.today() - timedelta(days=i) for i in range(days)]
        data = []

        for i in range(days):
            data.append([
                dates[i].strftime("%Y-%m-%d"),
                180 + i,
                184 + i,
                178 + i,
                183 + i,
                f"{1.5 + i*0.2:.1f}M"
            ])

        return pd.DataFrame(data, columns=["Date", "Open", "High", "Low", "Close", "Volume"])

    if range_option == "Last 7 Days":
        df = generate_data(7)
    elif range_option == "Last 30 Days":
        df = generate_data(30)
    else:
        df = generate_data(60)

    # ---------------- TABLE ----------------
    with st.container():
        st.subheader(f"Historical OHLC Data – {stock}")
        st.dataframe(df, use_container_width=True)

        st.caption("Displayed values are sample historical records for demo purposes.")

    # ---------------- DATA USAGE ----------------
    with st.container():
        st.write("**Data Usage:** Historical data is used for analysis and prediction models.")