def run():

    import streamlit as st
    import pandas as pd
    import matplotlib.pyplot as plt

    from utils.data_loader import (
        load_data,
        get_stock_data
    )

    # =========================
    # PAGE CONFIG
    # =========================
    st.set_page_config(
        layout="wide"
    )

    # =========================
    # CSS
    # =========================
    st.markdown("""
    <style>

    .main {
        background-color: #f5f7fb;
    }

    .block-container {
        padding-top: 2rem;
    }

    .stContainer {
        background: white;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0px 2px 8px rgba(0,0,0,0.06);
        margin-bottom: 20px;
    }

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

    # =========================
    # HEADER
    # =========================
    st.title("Market Data")

    st.caption(
        """
Historical Pakistan Stock Exchange (PSX) market data
used for AI forecasting and reinforcement learning.
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
    # FILTERS
    # =========================
    with st.container():

        col1, col2 = st.columns(2)

        # STOCK
        with col1:

            selected_stock = st.selectbox(
                "Select Stock",
                stocks
            )

        # RANGE
        with col2:

            range_option = st.selectbox(
                "Historical Range",
                [
                    "Last 30 Records",
                    "Last 90 Records",
                    "Full Historical Data"
                ]
            )

    # =========================
    # GET STOCK DATA
    # =========================
    df_stock = get_stock_data(
        df,
        selected_stock
    )

    # =========================
    # RANGE FILTER
    # =========================
    if range_option == "Last 30 Records":

        df_display = df_stock.tail(30)

    elif range_option == "Last 90 Records":

        df_display = df_stock.tail(90)

    else:

        df_display = df_stock.copy()

    # RESET INDEX
    df_display = df_display.reset_index(
        drop=True
    )

    # =========================
    # DYNAMIC LATEST DATA
    # =========================
    latest = df_display.iloc[-1]

    latest_close = float(
        latest['Close']
    )

    latest_volume = (
        f"{round(latest['Volume']/1e6,2)}M"
    )

    latest_high = float(
        latest['High']
    )

    latest_low = float(
        latest['Low']
    )

    # =========================
    # TOP METRICS
    # =========================
    st.markdown("---")

    m1, m2, m3, m4 = st.columns(4)

    with m1:

        st.metric(
            "Selected Stock",
            selected_stock
        )

    with m2:

        st.metric(
            "Latest Close",
            f"PKR {latest_close:.2f}"
        )

    with m3:

        st.metric(
            "Latest High",
            f"PKR {latest_high:.2f}"
        )

    with m4:

        st.metric(
            "Trading Volume",
            latest_volume
        )

    st.markdown("---")

    # =========================
    # PRICE CHART
    # =========================
    st.subheader(
        "Historical Closing Price Trend"
    )

    fig, ax = plt.subplots(
        figsize=(12, 5)
    )

    # PLOT
    ax.plot(
        df_display.index,
        df_display['Close'],
        linewidth=2,
        color='#16a34a'
    )

    # STYLE
    ax.set_facecolor("white")

    fig.patch.set_facecolor("white")

    # LABELS
    ax.set_xlabel(
        "Historical Records"
    )

    ax.set_ylabel(
        "Closing Price (PKR)"
    )

    # GRID
    ax.grid(
        alpha=0.3
    )

    # REMOVE BORDERS
    ax.spines['top'].set_visible(False)

    ax.spines['right'].set_visible(False)

    # LESS LABELS
    step = max(
        len(df_display) // 10,
        1
    )

    ax.set_xticks(
        range(
            0,
            len(df_display),
            step
        )
    )

    ax.set_xticklabels(
        df_display['Date'].iloc[
            ::step
        ],
        rotation=45,
        ha='right'
    )

    # TITLE
    ax.set_title(
        f"{selected_stock} Historical Closing Prices",
        fontsize=14,
        fontweight='bold'
    )

    st.pyplot(fig)

    # =========================
    # OHLC TABLE
    # =========================
    st.subheader(
        f"Historical OHLC Data — {selected_stock}"
    )

    display_columns = [
        'Date',
        'Open',
        'High',
        'Low',
        'Close',
        'Volume'
    ]

    st.dataframe(
        df_display[
            display_columns
        ],
        use_container_width=True,
        height=450
    )

    # =========================
    # MARKET SUMMARY
    # =========================
    st.subheader(
        "Market Data Summary"
    )

    avg_close = round(
        df_display['Close'].mean(),
        2
    )

    max_close = round(
        df_display['Close'].max(),
        2
    )

    min_close = round(
        df_display['Close'].min(),
        2
    )

    volatility = round(
        df_display['Close'].std(),
        2
    )

    s1, s2, s3, s4 = st.columns(4)

    with s1:

        st.info(
            f"Average Close\n\nPKR {avg_close}"
        )

    with s2:

        st.success(
            f"Highest Close\n\nPKR {max_close}"
        )

    with s3:

        st.error(
            f"Lowest Close\n\nPKR {min_close}"
        )

    with s4:

        st.warning(
            f"Volatility\n\n{volatility}"
        )

    # =========================
    # DATASET INFO
    # =========================
    st.markdown("---")

    st.subheader(
        "Dataset Usage"
    )

    st.info("""
The displayed historical PSX market data is used
for feature engineering, trend analysis, deep learning
price forecasting using LSTM, and intelligent trading
decision generation using DQN reinforcement learning.

The hybrid AI system was trained using five years of
historical stock market data.
    """)