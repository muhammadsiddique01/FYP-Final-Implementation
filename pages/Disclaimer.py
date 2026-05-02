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

    /* BASE CARD */
    .card {
        border-radius: 16px;
        padding: 22px;
        margin-bottom: 20px;
        border: 1px solid #e5e7eb;
        box-shadow: 0px 4px 14px rgba(0,0,0,0.06);
        background: white;
    }

    /* BLUE CARD */
    .card-blue {
        border-left: 5px solid #3b82f6;
        background: #eff6ff;
    }

    /* YELLOW CARD */
    .card-yellow {
        border-left: 5px solid #f59e0b;
        background: #fffbeb;
    }

    /* GRAY CARD */
    .card-gray {
        background: #f9fafb;
    }

    /* ICON */
    .icon {
        font-size: 26px;
        margin-right: 10px;
    }

    .title {
        font-size: 30px;
        font-weight: 700;
    }

    .subtitle {
        color: #6b7280;
        margin-bottom: 20px;
    }

    </style>
    """, unsafe_allow_html=True)

    # ---------------- TITLE ----------------
    st.markdown('<div class="title">Disclaimer</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Academic and usage-related information</div>', unsafe_allow_html=True)

    # ---------------- EDUCATIONAL ----------------
    st.markdown("""
    <div class="card card-blue">
        <h4>🎓 Educational & Academic Purpose</h4>
        <p>
        This AI-Based Stock Trading Decision Support System is developed solely for academic 
        and educational purposes as part of a Final Year Project. The system demonstrates 
        the application of deep learning and reinforcement learning techniques using 
        historical stock market data.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # ---------------- NOT FINANCIAL ----------------
    st.markdown("""
    <div class="card card-yellow">
        <h4>⚠️ Not Financial Advice</h4>
        <p>
        The predictions, indicators, and trading signals presented by this system are 
        provided for academic demonstration only and do not constitute financial, investment, 
        or trading advice.
        </p>
        <ul>
            <li>The system does not execute real trades</li>
            <li>Decisions should not be based solely on system outputs</li>
            <li>Financial markets involve inherent risks</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

    # ---------------- LIMITATION ----------------
    st.markdown("""
    <div class="card card-gray">
        <h4>⚖️ Limitation of Scope</h4>
        <p>
        This system is intended as a prototype for research and learning purposes. The results 
        may vary depending on market conditions, data quality, and model assumptions. 
        No guarantees regarding prediction accuracy or trading performance are claimed.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # ---------------- FOOT NOTE ----------------
    st.markdown("""
    <div class="card card-gray" style="text-align:center;">
        This disclaimer ensures clarity regarding the academic intent and responsible use of the proposed system.
    </div>
    """, unsafe_allow_html=True)