import streamlit as st

st.set_page_config(layout="wide")

# ================= SESSION =================
if "page" not in st.session_state:
    st.session_state.page = "Home"

def set_page(page):
    st.session_state.page = page

# ================= CSS =================
st.markdown("""
<style>

/* REMOVE STREAMLIT ANCHOR LINK ICON */
a.anchor-link {
    display: none !important;
}

/* SIDEBAR BUTTON WIDTH */
section[data-testid="stSidebar"] div.stButton > button {
    width: 100%;
}

/* SIDEBAR FIXED */
section[data-testid="stSidebar"] {
    position: fixed !important;
    width: 250px !important;
    height: 100vh !important;
    background-color: #f9fafb;
    border-right: 1px solid #e5e7eb;
}

/* REMOVE ALL SCROLL */
section[data-testid="stSidebar"] > div {
    overflow: hidden !important;
    height: 100vh !important;
}

/* REMOVE INTERNAL SCROLL */
section[data-testid="stSidebar"] div[data-testid="stVerticalBlock"] {
    overflow: hidden !important;
}

/* REMOVE DEFAULT NAV */
[data-testid="stSidebarNav"] {display:none;}

/* SHOW SIDEBAR TOGGLE BUTTON */
button[kind="header"] {
    display: block !important;
}

/* REMOVE FOOTER */
footer {visibility: hidden;}

/* FLEX SIDEBAR */
section[data-testid="stSidebar"] > div {
    display: flex;
    flex-direction: column;
    height: 100vh !important;
    justify-content: space-between;
    padding-top: 0.5rem;
}

/* MAIN CONTENT SHIFT */
.block-container {
    margin-left: 260px;
    padding-top: 1rem;
    max-width: 1100px;
}

/* ===== SIDEBAR BUTTON STYLE ONLY ===== */
section[data-testid="stSidebar"] div.stButton > button {
    width: 100%;
    text-align: left;
    background: transparent;
    color: black;
    border: none;
    padding: 7px 10px;
    border-radius: 8px;
    font-size: 14px;
}

/* HOVER (SIDEBAR ONLY) */
section[data-testid="stSidebar"] div.stButton > button:hover {
    background-color: #e5e7eb;
}

/* ===== HOME BUTTON (CENTER) ===== */
div[data-testid="column"]:nth-of-type(2) div.stButton > button {
    display: block;
    margin: 0 auto;

    background-color: transparent !important;
    color: #2563eb !important;

    padding: 12px 30px !important;
    border-radius: 10px !important;

    border: 2px solid #2563eb !important;   /* 🔥 FIX */
    font-size: 16px !important;
    font-weight: 600 !important;
    width: 250px !important;
}

/* HOVER */
div[data-testid="column"]:nth-of-type(2) div.stButton > button:hover {
    background-color: #2563eb !important;
    color: white !important;
}

/* ACTIVE */
.active-btn {
    background-color: #2563eb;
    color: white;
    padding: 7px 10px;
    border-radius: 8px;
    margin-bottom: 4px;
}

/* DIVIDER */
.divider {
    height: 1px;
    background-color: #e5e7eb;
    margin: 6px 0;
}

/* CARD */
.card {
    padding: 20px;
    border-radius: 15px;
    background: #f1f5f9;
    margin-bottom: 20px;
}

/* TITLE */
.main-title {
    text-align: center;
    font-size: 40px;
    font-weight: 700;
}

/* SUBTEXT */
.sub-text {
    text-align: center;
    color: #6b7280;
}

/* BOTTOM BOX */
.bottom-box {
    background: #f3f4f6;
    padding: 20px;
    border-radius: 12px;
    text-align: center;
    margin-top: 30px;
}

</style>
""", unsafe_allow_html=True)

# ================= SIDEBAR HEADER =================
import base64

# Read and encode PNG image
with open("logo.png", "rb") as f:
    data = f.read()
    encoded = base64.b64encode(data).decode()

st.sidebar.markdown(f"""
<div style="display:flex; align-items:center; gap:10px;">
    <div>
        <img src="data:image/png;base64,{encoded}" width="60" style="display:block;">
    </div>
    <div>
        <div style="font-size:20px; font-weight:700;">QuantSight</div>
        <div style="font-size:12px; color:#6b7280;">Decision Support</div>
    </div>
</div>
""", unsafe_allow_html=True)

st.sidebar.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# ================= ICONS =================
icons = {
    "Home": "🏠",
    "Dashboard": "📊",
    "Market Data": "📈",
    "Performance": "📉",
    "System Architecture": "⚙️",
    "About Project": "ℹ️",
    "References": "📚",
    "Disclaimer": "⚠️"
}

# ================= MENU =================
pages = list(icons.keys())

for p in pages:
    label = f"{icons[p]}  {p}"

    if st.session_state.page == p:
        st.sidebar.markdown(f'<div class="active-btn">{label}</div>', unsafe_allow_html=True)
    else:
        if st.sidebar.button(label):
            set_page(p)
            st.rerun()

st.sidebar.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# ================= FOOTER =================
st.sidebar.markdown("""
<div style="padding:12px; text-align:center; color:#6b7280;">
Final Year Project
</div>
""", unsafe_allow_html=True)

# ================= HOME =================
if st.session_state.page == "Home":

    # TOP BADGE
    st.markdown("""
    <div style="text-align:center; margin-bottom:10px;">
        <span style="
            background:#e0f2fe;
            color:#2563eb;
            padding:6px 14px;
            border-radius:20px;
            font-size:13px;
            font-weight:500;">
            ⚙️ Final Year Project
        </span>
    </div>
    """, unsafe_allow_html=True)

    # MAIN TITLE (NO ANCHOR ICON)
    st.markdown("""
    <div style="
        text-align:center;
        font-size:50px;
        font-weight:800;
        margin-bottom:10px;">
        AI-Based Stock Trading Decision Support System for PSX
    </div>
    """, unsafe_allow_html=True)

    # DESCRIPTION
    st.markdown("""
    <p style="
        text-align:center;
        color:#6b7280;
        font-size:18px;
        max-width:750px;
        margin:auto;">
        An AI-based decision support system leveraging deep learning models 
        (LSTM and DQN) to analyze historical data and assist trading decisions 
        for Pakistan Stock Exchange securities.
    </p>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

# BUTTON (CLEAN + SINGLE)
    col1, col2, col3 = st.columns([1,1,1])

    with col2:
        st.markdown("""
        <style>
        /* Button container ko center karne ke liye */
        div.stButton {
            display: flex;
            justify-content: center;
        }

        /* Specific Home Button ki Styling */
        button[data-testid="baseButton-home_btn"] {
            background-color: #2563eb !important; /* Blue color */
            color: white !important;
            padding: 12px 30px !important;
            border-radius: 10px !important;
            border: none !important;
            font-size: 16px !important;
            font-weight: 600 !important;
            width: 250px !important; /* Button ki width */
            transition: 0.3s;
        }

        /* Hover effect */
        button[data-testid="baseButton-home_btn"]:hover {
            background-color: #1e40af !important; /* Darker blue on hover */
            border: none !important;
        }
        </style>
        """, unsafe_allow_html=True)

        btn = st.button("Go to Dashboard →", key="home_btn")

        if btn:
            set_page("Dashboard")
            st.rerun()
        

    st.markdown("<br><br>", unsafe_allow_html=True)

    # CARDS
    col1, col2 = st.columns(2)
    col3, col4 = st.columns(2)

    def card(icon, title, desc):
        st.markdown(f"""
        <div style="
            padding:22px;
            border-radius:16px;
            background:#f8fafc;
            box-shadow: 0 2px 6px rgba(0,0,0,0.05);
            margin-bottom:20px;
        ">
            <div style="font-size:22px; margin-bottom:10px;">{icon}</div>
            <h4 style="margin-bottom:5px;">{title}</h4>
            <p style="color:#6b7280; font-size:14px;">{desc}</p>
        </div>
        """, unsafe_allow_html=True)

    with col1:
        card("🧠", "AI-Based Analysis", "LSTM neural networks for stock price trend prediction")

    with col2:
        card("📈", "Trading Decision Support", "DQN-based Buy, Sell, and Hold signal generation")

    with col3:
        card("📊", "Performance Evaluation", "Historical backtesting and strategy performance analysis")

    with col4:
        card("🛡️", "Risk & Sentiment Awareness", "Fear & Greed Index and risk level indicators")

    # DISCLAIMER
    st.markdown("""
    <div style="
        background:#f1f5f9;
        padding:20px;
        border-radius:14px;
        text-align:center;
        margin-top:20px;
        color:#475569;">
        This system is developed strictly for academic and educational purposes. 
        It does not perform real-time trading or provide financial advice.
    </div>
    """, unsafe_allow_html=True)

# ================= ROUTING =================
elif st.session_state.page == "Dashboard":
    import pages.Dashboard as Dashboard
    Dashboard.run()

elif st.session_state.page == "Market Data":
    import pages.Market_Data as Market_Data
    Market_Data.run()

elif st.session_state.page == "Performance":
    import pages.Performance as Performance
    Performance.run()

elif st.session_state.page == "System Architecture":
    import pages.System_Architecture as System_Architecture
    System_Architecture.run()

elif st.session_state.page == "About Project":
    import pages.About as About
    About.run()

elif st.session_state.page == "References":
    import pages.References as References
    References.run()

elif st.session_state.page == "Disclaimer":
    import pages.Disclaimer as Disclaimer
    Disclaimer.run()