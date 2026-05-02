def run():
    import streamlit as st

    st.set_page_config(layout="wide")

    # ---------------- CSS (FIXED UI) ----------------
    st.markdown("""
    <style>

    .main {
        background-color: #f5f7fb;
    }

    .block-container {
        padding-top: 2rem;
        max-width: 1150px;
    }

    /* MAIN CARD */
    div[data-testid="stContainer"] {
        border-radius: 18px !important;
        padding: 18px !important;   /* FIXED (was 4px) */
        border: 1px solid #e5e7eb !important;
        box-shadow: 0px 6px 18px rgba(0,0,0,0.06) !important;
        background: white !important;
        margin-bottom: 25px !important;
    }

    /* MODULE EQUAL HEIGHT */
    .module-card {
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }

    /* MINI TECH CARDS */
    .mini-card {
        background: #f8fafc;
        padding: 20px;
        border-radius: 14px;
        text-align: center;
        border: 1px solid #e5e7eb;
        transition: 0.3s;
    }

    .mini-card:hover {
        transform: translateY(-3px);
        box-shadow: 0px 6px 14px rgba(0,0,0,0.08);
    }

    .mini-title {
        font-weight: 600;
        margin-bottom: 6px;
    }

    .mini-sub {
        font-size: 13px;
        color: #6b7280;
    }

    </style>
    """, unsafe_allow_html=True)

    # ---------------- TITLE ----------------
    st.title("System Architecture")
    st.caption("High-level workflow and component interaction of the proposed system")

    # ---------------- FLOW ----------------
    with st.container(border=True):
        st.subheader("Overall System Flow")
        st.image("system.png", width=1000)

    # ---------------- MODULES ----------------
    col1, col2 = st.columns(2, gap="large")

    with col1:
        with st.container(border=True):
            st.markdown('<div class="module-card">', unsafe_allow_html=True)

            st.subheader("LSTM Price Prediction Module")

            st.markdown("""
            The Long Short-Term Memory (LSTM) model captures temporal patterns in historical PSX stock data.

            **Input:** Historical price sequences and derived features  
            **Output:** Predicted price movement or trend
            """)

            st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        with st.container(border=True):
            st.markdown('<div class="module-card">', unsafe_allow_html=True)

            st.subheader("DQN Decision Support Agent")

            st.markdown("""
            The Deep Q-Network (DQN) agent uses reinforcement learning to generate optimal trading decisions.

            **Actions:** Buy, Sell, Hold  
            **Objective:** Maximize long-term reward while managing market risk
            """)

            st.markdown('</div>', unsafe_allow_html=True)

    # ---------------- TECH STACK ----------------
    with st.container(border=True):
        st.subheader("Technology Stack")

        # 🔥 spacing fix
        st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)

        col1, col2, col3, col4 = st.columns(4, gap="medium")

        col1.markdown("""
        <div class="mini-card">
            <div class="mini-title">Deep Learning</div>
            <div class="mini-sub">TensorFlow, Keras</div>
        </div>
        """, unsafe_allow_html=True)

        col2.markdown("""
        <div class="mini-card">
            <div class="mini-title">Data Processing</div>
            <div class="mini-sub">Pandas, NumPy</div>
        </div>
        """, unsafe_allow_html=True)

        col3.markdown("""
        <div class="mini-card">
            <div class="mini-title">Visualization</div>
            <div class="mini-sub">Matplotlib, Plotly</div>
        </div>
        """, unsafe_allow_html=True)

        col4.markdown("""
        <div class="mini-card">
            <div class="mini-title">Web Interface</div>
            <div class="mini-sub">Streamlit</div>
        </div>
        """, unsafe_allow_html=True)

        # 🔥 bottom spacing (important fix)
        st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)