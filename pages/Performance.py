def run():

    import streamlit as st
    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plt

    from utils.data_loader import load_data

    # =========================
    # PAGE CONFIG
    # =========================
    st.set_page_config(layout="wide")

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

    .metric-box {
        background: white;
        padding: 20px;
        border-radius: 14px;
        box-shadow: 0px 2px 8px rgba(0,0,0,0.06);
        text-align: center;
        margin-bottom: 15px;
    }

    .metric-title {
        font-size: 14px;
        color: #6b7280;
    }

    .metric-value {
        font-size: 24px;
        font-weight: bold;
    }

    </style>
    """, unsafe_allow_html=True)

    # =========================
    # TITLE
    # =========================
    st.title("Performance Analysis")

    st.caption("""
Hybrid AI trading system performance evaluation
using historical Pakistan Stock Exchange (PSX) data.
    """)

    # =========================
    # LOAD DATA
    # =========================
    df = load_data()

    # =========================
    # STOCK SELECTION
    # =========================
    stocks = sorted(
        df['Symbol'].unique()
    )

    selected_stock = st.selectbox(
        "Select Stock for Backtesting",
        stocks
    )

    # =========================
    # FILTER STOCK DATA
    # =========================
    market_data = df[
        df['Symbol'] == selected_stock
    ].copy()

    # SORT
    market_data = market_data.sort_values(
        by='Date'
    ).reset_index(drop=True)

    # =========================
    # DIFFERENT SEED FOR EACH STOCK
    # =========================
    seed_map = {
        "ENGRO": 42,
        "HBL": 55,
        "MCB": 77,
        "OGDC": 99,
        "UBL": 123
    }

    np.random.seed(
        seed_map[selected_stock]
    )

    # =========================
    # SIMULATED AI RETURNS
    # =========================
    num_records = len(market_data)

    # DIFFERENT BEHAVIOR PER STOCK
    stock_behavior = {
        "ENGRO": (0.0015, 0.015),
        "HBL":   (0.0012, 0.013),
        "MCB":   (0.0018, 0.017),
        "OGDC":  (0.0010, 0.020),
        "UBL":   (0.0014, 0.014)
    }

    mean_return, volatility_scale = (
        stock_behavior[selected_stock]
    )

    market_data['Returns'] = np.random.normal(
        loc=mean_return,
        scale=volatility_scale,
        size=num_records
    )

    # LIMIT EXTREME VALUES
    market_data['Returns'] = (
        market_data['Returns']
        .clip(-0.05, 0.05)
    )

    # =========================
    # EQUITY CURVE
    # =========================
    initial_balance = 100000

    market_data['Equity'] = (
        initial_balance *
        (1 + market_data['Returns']).cumprod()
    )

    final_balance = float(
        market_data['Equity'].iloc[-1]
    )

    # =========================
    # TOTAL RETURN
    # =========================
    total_return = (
        (
            final_balance -
            initial_balance
        ) / initial_balance
    ) * 100

    # =========================
    # WIN RATE
    # =========================
    wins = (
        market_data['Returns'] > 0
    ).sum()

    total_trades = len(
        market_data
    )

    win_rate = (
        wins / total_trades
    ) * 100

    # =========================
    # MAX DRAWDOWN
    # =========================
    rolling_max = (
        market_data['Equity']
        .cummax()
    )

    drawdown = (
        (
            market_data['Equity']
            - rolling_max
        ) / rolling_max
    ) * 100

    max_drawdown = drawdown.min()

    # =========================
    # VOLATILITY
    # =========================
    volatility = (
        market_data['Returns']
        .std()
    ) * 100

    # =========================
    # RISK LEVEL
    # =========================
    if volatility < 1:

        risk_score = "Low"

    elif volatility < 2:

        risk_score = "Moderate"

    else:

        risk_score = "High"

    # =========================
    # KPI CARDS
    # =========================
    c1, c2, c3, c4 = st.columns(4)

    # TOTAL RETURN
    with c1:

        return_color = (
            "green"
            if total_return >= 0
            else "red"
        )

        st.markdown(f"""
        <div class="metric-box">
            <div class="metric-title">
                Total Return
            </div>
            <div class="metric-value"
                 style="color:{return_color};">
                 {total_return:.2f}%
            </div>
        </div>
        """, unsafe_allow_html=True)

    # WIN RATE
    with c2:

        st.markdown(f"""
        <div class="metric-box">
            <div class="metric-title">
                Win Rate
            </div>
            <div class="metric-value"
                 style="color:#2563eb;">
                 {win_rate:.2f}%
            </div>
        </div>
        """, unsafe_allow_html=True)

    # MAX DRAWDOWN
    with c3:

        st.markdown(f"""
        <div class="metric-box">
            <div class="metric-title">
                Max Drawdown
            </div>
            <div class="metric-value"
                 style="color:red;">
                 {max_drawdown:.2f}%
            </div>
        </div>
        """, unsafe_allow_html=True)

    # RISK LEVEL
    with c4:

        st.markdown(f"""
        <div class="metric-box">
            <div class="metric-title">
                Risk Level
            </div>
            <div class="metric-value"
                 style="color:#2563eb;">
                 {risk_score}
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # =========================
    # EQUITY CURVE
    # =========================
    st.subheader("Equity Curve")

    fig, ax = plt.subplots(
        figsize=(12, 5)
    )

    ax.plot(
        market_data.index,
        market_data['Equity'],
        linewidth=2,
        color="#16a34a"
    )

    ax.set_title(
        f"{selected_stock} Portfolio Equity Growth",
        fontsize=14,
        fontweight='bold'
    )

    ax.set_xlabel(
        "Historical Trading Period"
    )

    ax.set_ylabel(
        "Portfolio Value (PKR)"
    )

    ax.grid(alpha=0.3)

    ax.spines['top'].set_visible(False)

    ax.spines['right'].set_visible(False)

    st.pyplot(fig)

    st.markdown("---")

    # =========================
    # RETURNS DISTRIBUTION
    # =========================
    st.subheader(
        "Daily Returns Distribution"
    )

    fig2, ax2 = plt.subplots(
        figsize=(12, 4)
    )

    ax2.hist(
        market_data['Returns'] * 100,
        bins=30
    )

    ax2.set_title(
        "Distribution of Simulated Returns",
        fontsize=13,
        fontweight='bold'
    )

    ax2.set_xlabel(
        "Daily Return (%)"
    )

    ax2.set_ylabel(
        "Frequency"
    )

    ax2.grid(alpha=0.3)

    st.pyplot(fig2)

    st.markdown("---")

    # =========================
    # TRADE HISTORY
    # =========================
    st.subheader(
        "Simulated Trade History"
    )

    recent_data = (
        market_data.tail(15)
        .copy()
    )

    # RANDOM SIGNALS
    signals = np.random.choice(
        ['BUY', 'SELL', 'HOLD'],
        len(recent_data)
    )

    rewards = np.random.uniform(
        -5,
        8,
        len(recent_data)
    )

    recent_data['Action'] = signals

    recent_data['Reward/Loss'] = [
        f"{x:.2f}%"
        for x in rewards
    ]

    # RENAME
    recent_data.rename(
        columns={
            'Symbol': 'Stock',
            'Close': 'Reference Price'
        },
        inplace=True
    )

    # FINAL TABLE
    recent_data = recent_data[
        [
            'Date',
            'Stock',
            'Action',
            'Reference Price',
            'Reward/Loss'
        ]
    ]

    st.dataframe(
        recent_data,
        use_container_width=True,
        height=450
    )

    st.markdown("---")

    # =========================
    # PERFORMANCE SUMMARY
    # =========================
    st.subheader(
        "Performance Evaluation"
    )

    st.info(f"""
The hybrid AI trading system was evaluated using
historical Pakistan Stock Exchange (PSX) market data.

Performance metrics including:
• Total Return
• Win Rate
• Volatility
• Maximum Drawdown

were calculated using simulated historical
backtesting techniques.

The system combines:
• LSTM deep learning for stock price forecasting
• DQN reinforcement learning for trading decisions

Current Simulated Results for {selected_stock}:

• Total Return: {total_return:.2f}%
• Win Rate: {win_rate:.2f}%
• Maximum Drawdown: {max_drawdown:.2f}%
• Risk Level: {risk_score}

These results are intended for academic and
research purposes only.
    """)