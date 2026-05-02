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

    /* TITLE */
    h1 {
        font-size: 30px !important;
        font-weight: 700 !important;
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

    /* NUMBER CIRCLE */
    .circle {
        background: #e0f2fe;
        color: #0369a1;
        border-radius: 50%;
        width: 26px;
        height: 26px;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        font-size: 13px;
        margin-right: 10px;
        font-weight: 600;
    }

    </style>
    """, unsafe_allow_html=True)

    # ---------------- TITLE ----------------
    st.title("About Project")
    st.caption("Research background, objectives, and academic contribution")

    # ---------------- PROBLEM ----------------
    with st.container(border=True):
        st.subheader("🎯 Problem Statement")

        st.markdown("""
        Traditional stock trading largely depends on manual analysis and subjective decision-making, 
        which is often time-consuming and influenced by emotional biases. The Pakistan Stock Exchange (PSX), 
        as an emerging market, exhibits high volatility and limited availability of intelligent decision 
        support tools for individual investors, motivating the need for AI-assisted trading analysis.
        """)

    # ---------------- OBJECTIVES ----------------
    with st.container(border=True):
        st.subheader("💡 Research Objectives")

        st.markdown("""
        <div><span class="circle">1</span>Develop an LSTM-based model for forecasting stock price trends using historical PSX data</div><br>
        <div><span class="circle">2</span>Design a DQN-based trading decision support agent for Buy, Sell, and Hold recommendations</div><br>
        <div><span class="circle">3</span>Develop an interactive web dashboard to visualize predictions, decisions, and risk indicators</div><br>
        <div><span class="circle">4</span>Evaluate system effectiveness through historical backtesting and performance analysis</div>
        """, unsafe_allow_html=True)

    # ---------------- CONTRIBUTION ----------------
    with st.container(border=True):
        st.subheader("🏆 Research Contribution")

        st.markdown("""
        • Proposing an AI-based trading decision support system tailored for PSX market characteristics  
        • Integrating deep learning (LSTM) with reinforcement learning (DQN) for informed trading decisions  
        • Emphasizing explainability and risk awareness in trading signals  
        • Providing an academic prototype suitable for emerging market studies  
        """)

    # ---------------- TOOLS ----------------
    with st.container(border=True):
        st.subheader("🛠 Tools & Technologies")

        col1, col2, col3 = st.columns(3, gap="medium")

        col1.markdown('<div class="badge">Python 3.x</div>', unsafe_allow_html=True)
        col2.markdown('<div class="badge">TensorFlow / Keras</div>', unsafe_allow_html=True)
        col3.markdown('<div class="badge">Pandas</div>', unsafe_allow_html=True)

        col1, col2, col3 = st.columns(3, gap="medium")

        col1.markdown('<div class="badge">NumPy</div>', unsafe_allow_html=True)
        col2.markdown('<div class="badge">Scikit-learn</div>', unsafe_allow_html=True)
        col3.markdown('<div class="badge">Matplotlib</div>', unsafe_allow_html=True)

        col1, col2, col3 = st.columns(3, gap="medium")

        col1.markdown('<div class="badge">Plotly</div>', unsafe_allow_html=True)
        col2.markdown('<div class="badge">Streamlit</div>', unsafe_allow_html=True)
        col3.markdown('<div class="badge">Jupyter Notebook</div>', unsafe_allow_html=True)