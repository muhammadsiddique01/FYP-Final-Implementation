def run():
    import streamlit as st

    st.set_page_config(layout="wide")

    # ---------------- CSS ----------------
    st.markdown("""
    <style>

    .main {
        background-color: #f5f7fb;
    }

    .block-container {
        padding-top: 2rem;
        max-width: 1100px;
    }

    /* CARD */
    div[data-testid="stContainer"] {
        border-radius: 16px !important;
        padding: 22px !important;
        border: 1px solid #e5e7eb !important;
        box-shadow: 0px 4px 14px rgba(0,0,0,0.06) !important;
        background: white !important;
        margin-bottom: 20px !important;
    }

    /* CITATION BOX */
    .citation {
        background: #f1f5f9;
        padding: 14px;
        border-radius: 12px;
        margin-bottom: 10px;
    }

    /* BADGE */
    .badge {
        background: #eef2f7;
        padding: 10px 14px;
        border-radius: 12px;
        text-align: center;
        font-size: 14px;
        border: 1px solid #e5e7eb;
    }

    </style>
    """, unsafe_allow_html=True)

    # ---------------- TITLE ----------------
    st.title("References")
    st.caption("Research papers, data sources, and related platforms")

    # ---------------- RESEARCH PAPERS ----------------
    with st.container(border=True):
        st.subheader("📄 Research Paper Citations")

        st.markdown("""
        <div class="citation">
        Awad, M. et al. (2023). <i>Stock Market Prediction Using Deep Reinforcement Learning</i>. Applied System Innovation.
        </div>

        <div class="citation">
        IEEE Access (2024). <i>A Multifaceted Approach to Stock Market Trading Using Reinforcement Learning</i>. IEEE Access.
        </div>
        """, unsafe_allow_html=True)

    # ---------------- DATA SOURCES ----------------
    with st.container(border=True):
        st.subheader("📊 Data Sources")

        st.markdown("""
        • Pakistan Stock Exchange (PSX) – Historical Stock Data  
        • PSX Data Portal (DPS) – Downloaded CSV Files  
        """)

        st.caption("*Only historical data is used for academic analysis. No real-time or paid data sources are integrated.")

    # ---------------- PLATFORMS ----------------
    with st.container(border=True):
        st.subheader("🌐 Related Trading Platforms")

        col1, col2, col3 = st.columns(3, gap="medium")

        col1.markdown('<div class="badge">TradingView</div>', unsafe_allow_html=True)
        col2.markdown('<div class="badge">QuantConnect</div>', unsafe_allow_html=True)
        col3.markdown('<div class="badge">MetaTrader</div>', unsafe_allow_html=True)

        st.caption("*These platforms are listed solely for feature comparison and are not used in the system implementation.")