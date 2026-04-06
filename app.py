#  uesd this code 

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime
import yfinance as yf
from ag import app
from report_generator import generate_report
import seaborn as sns
from data_loader import load_market_data
from ml_predictor import get_predicted_return
from sentiment_analysis import analyze_sentiment
from rl_portfolio import train_rl_agent, get_rl_portfolio_weights
from database import add_user, login_user
import mysql.connector
import requests
from streamlit_lottie import st_lottie
import plotly.express as px
import plotly.graph_objects as go
from io import StringIO
from streamlit_autorefresh import st_autorefresh


st.markdown("""
<style>

/* Sidebar background */
[data-testid="stSidebar"]{
background: linear-gradient(180deg, #8b5cf6, #c084fc);
border-right:2px solid rgba(255,255,255,0.1);
}

/* Glass card container */
.glass-card{
    background: rgba(255,255,255,0.06);
    padding:20px;
    border-radius:16px;
    border:1px solid rgba(255,255,255,0.18);
    backdrop-filter: blur(14px);
    -webkit-backdrop-filter: blur(14px);
    margin-bottom:20px;
    color:white;
    box-shadow: 0 8px 30px rgba(0,0,0,0.4);
}
.chart-card{
    background: rgba(255,255,255,0.05);
    padding:15px;
    border-radius:12px;
    backdrop-filter: blur(10px);
    border:1px solid rgba(255,255,255,0.1);
    margin-bottom:20px;
}

/* Navigation hover effect */
.stRadio > div{
background: rgba(255,255,255,0.03);
padding:10px;
border-radius:8px;
backdrop-filter: blur(10px);
box-shadow: 0 8px 30px rgba(0,0,0,0.4);
}

</style>
""", unsafe_allow_html=True)

# ---------- LOAD ANIMATION ----------

url = "https://assets5.lottiefiles.com/packages/lf20_fcfjwiyb.json"
animation = requests.get(url).json()

st.markdown("""
<style>
.stApp{
    background: radial-gradient(circle at 20% 20%, rgba(59,130,246,0.15), transparent 40%),
                radial-gradient(circle at 80% 30%, rgba(34,197,94,0.15), transparent 40%),
                linear-gradient(#5A189A, #7B2CBF, #C77DFF);
            color:white;    
}

/* Optional subtle animation */
@keyframes moveBg {
    0% {background-position: 0% 50%;}
    50% {background-position: 100% 50%;}
    100% {background-position: 0% 50%;}
}

/* Center container */
.center-box{
display:flex;
justify-content:center;
align-items:center;
flex-direction:column;
margin-top:30px;
}

.login-card{
width:100%;
max-width:250px;
margin:auto;
padding:25px;
border-radius:15px;
background: rgba(255,255,255,0.05);
border:1px solid rgba(255,255,255,0.1);
backdrop-filter: blur(10px);
}


/* Center button */
.stButton{
text-align:center;
}

</style>
""", unsafe_allow_html=True)

st.markdown("""
<style>

*  Center ALL input elements */
[data-testid="stTextInput"], 
[data-testid="stSelectbox"]{
    max-width:200px;
    margin:10px auto;
}

/*  Center button container */
div[data-testid="stButton"]{
    display:flex;
    justify-content:center;
    margin-top:10px;
}

/* Button fix */
.stButton > button{
width:200%;
background: linear-gradient(90deg,#3b82f6,#22c55e);
color:white;
border:none;
border-radius:8px;
padding:10px;
font-weight:bold;
transition:0.3s;

}

/* Hover effect */
.stButton > button:hover{
transform:scale(1.05);
background: linear-gradient(90deg,#2563eb,#16a34a);
}

</style>
""", unsafe_allow_html=True)

st.markdown("""
<style>

.login-card{
    padding:15px;
    border-radius:15px;
    background: rgba(255,255,255,0.05);
    backdrop-filter: blur(10px);
    display:inline-block;   
    width:100%;
}

</style>
""", unsafe_allow_html=True)

# AI powered investment analytics 

st.markdown("""
<style>

.feature-box{
    padding:20px;
    border-radius:10px;
    background: rgba(255,255,255,0.05);
    border:1px solid rgba(255,255,255,0.2);
    backdrop-filter: blur(12px);
    color:white;
    text-align:left;
    margin-top:10px;
    box-shadow: 0 8px 25px rgba(0,0,0,0.3);
    min-height :180px;
    font-size:15px;
}

/* Optional hover  */
.feature-box:hover{
    transform: scale(1.02);
    transition: 0.3s;
    border:1px solid #3b82f6;
}
</style>
""", unsafe_allow_html=True)

# remove scrolling

st.markdown("""
<style>

/* Remove top space */
.block-container{
    padding-top: 0rem;
    padding-bottom: 1rem;
}

/* Remove extra gap above title */
h2{
    margin-top:0px;
}

</style>
""", unsafe_allow_html=True)

st.markdown("""
<style>

/* Target FORM buttons (important) */
div[data-testid="stFormSubmitButton"] button{
    width:200px;
    background: linear-gradient(90deg,#06b6d4,#3b82f6,#6366f1);
    color:white;
    border:none;
    border-radius:8px;
    padding:10px;
    font-weight:bold;
    transition:0.3s;
    display:block;
    margin:auto;   /* center button */
    box-shadow: 0 0 15px rgba(59,130,246,0.4);
}

/* Hover effect */
div[data-testid="stFormSubmitButton"] button:hover{
    transform:scale(1.05);
    background: linear-gradient(90deg,#2563eb,#16a34a);
    
}

</style>
""", unsafe_allow_html=True)

def premium_chart(fig, height=450):
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        margin=dict(l=10, r=10, t=40, b=10),
        height=height
    )

    fig.update_traces(
        hoverlabel=dict(
            bgcolor="black",
            font_size=14,
            font_color="white"
        )
    )

    st.plotly_chart(fig, use_container_width=True)

# select holding period 

st.markdown("""
<style>

/* Selectbox main container */
div[data-baseweb="select"] > div {
    background: rgba(255,255,255,0.05) !important;
    border: 1px solid rgba(255,255,255,0.2) !important;
    backdrop-filter: blur(10px) !important;
    border-radius: 10px !important;
    color: white !important;
}

/* Dropdown text */
div[data-baseweb="select"] span {
    color: white !important;
}

/* Dropdown menu */
ul[role="listbox"] {
    background: rgba(0,0,0,0.8) !important;
    backdrop-filter: blur(10px);
    border-radius: 10px;
}

/* Hover option */
li[role="option"]:hover {
    background: rgba(59,130,246,0.3) !important;
}

</style>
""", unsafe_allow_html=True)    

st.markdown("""
<style>

/* Reduce space between sections */
h1, h2, h3 {
    margin-top: 10px !important;
    margin-bottom: 5px !important;
}

/* Reduce block spacing */
.block-container {
    padding-top: 1rem;
    padding-bottom: 0rem;
}

/* Reduce space between elements */
div[data-testid="stVerticalBlock"] > div {
    gap: 0.5rem;
}

</style>
""", unsafe_allow_html=True)

#Safe Investment (PPF / EPF)
st.markdown("""
<style>

/* Selectbox main container */
div[data-testid="stSelectbox"] > div {
    background: linear-gradient(90deg, #7c3aed, #a855f7) !important;
    border-radius: 10px !important;
    border: 1px solid rgba(255,255,255,0.2) !important;
    padding: 4px;
}

/* Inner select field */
div[data-testid="stSelectbox"] div[data-baseweb="select"] > div {
    background: transparent !important;
    color: white !important;
}

/* Text inside */
div[data-testid="stSelectbox"] span {
    color: white !important;
    font-weight: 500;
}

/* Dropdown arrow */
div[data-testid="stSelectbox"] svg {
    fill: white !important;
}

/* Label */
div[data-testid="stSelectbox"] label {
    color: white !important;
    font-weight: 600;
}

/* Hover effect */
div[data-testid="stSelectbox"]:hover > div {
    box-shadow: 0 0 10px rgba(168,85,247,0.5);
}

</style>
""", unsafe_allow_html=True)

# Annual income 

st.markdown("""
<style>

/* FULL number input container */
div[data-testid="stNumberInput"] > div {
    background: linear-gradient(90deg, #7c3aed, #a855f7) !important;
    border-radius: 10px !important;
    border: 1px solid rgba(255,255,255,0.2) !important;
    padding: 4px;
    display: flex;
    align-items: center;
}

/* INPUT FIELD FIX (REMOVE BLACK AREA) */
div[data-testid="stNumberInput"] input {
    background: transparent !important;
    border: none !important;
    color: white !important;
    font-weight: 600;
    width: 100%;
}

/* REMOVE INNER BLACK WRAPPER */
div[data-testid="stNumberInput"] div[data-baseweb="input"] {
    background: transparent !important;
}

/* FIX BUTTON AREA */
div[data-testid="stNumberInput"] button {
    background: transparent !important;
    border: none !important;
    color: white !important;
}

/* REMOVE SPLIT LOOK */
div[data-testid="stNumberInput"] div {
    background: transparent !important;
}

/* LABEL */
div[data-testid="stNumberInput"] label {
    color: white !important;
    font-weight: 600;
}

/* HOVER GLOW */
div[data-testid="stNumberInput"]:hover > div {
    box-shadow: 0 0 10px rgba(168,85,247,0.5);
}

/* FOCUS GLOW */
div[data-testid="stNumberInput"]:focus-within > div {
    box-shadow: 0 0 12px rgba(168,85,247,0.7);
}

</style>
""", unsafe_allow_html=True)

# Download pdf report 

st.markdown("""
<style>

/* Download button style (same as your normal buttons) */
div[data-testid="stDownloadButton"] button {
    width: 200px;
    background: linear-gradient(90deg,#3b82f6,#22c55e) !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
    padding: 10px !important;
    font-weight: bold !important;
    transition: 0.3s;
    display: block;
    margin: auto;
}

/* Hover effect */
div[data-testid="stDownloadButton"] button:hover {
    transform: scale(1.05);
    background: linear-gradient(90deg,#2563eb,#16a34a) !important;
}

</style>
""", unsafe_allow_html=True)

# investment goal 

st.markdown("""
<style>

/* TEXT AREA CONTAINER */
div[data-testid="stTextArea"] > div {
    background: linear-gradient(90deg, #7c3aed, #a855f7) !important;
    border-radius: 10px !important;
    border: 1px solid rgba(255,255,255,0.2) !important;
    padding: 6px;
    display :flex;
}

/* TEXT AREA INPUT FIELD */
div[data-testid="stTextArea"] textarea {
    background: transparent !important;
    border: none !important;
    color: white !important;
    font-weight: 500;
    width: 100%;
}

/* REMOVE INNER BLACK AREA */
div[data-testid="stTextArea"] div[data-baseweb="textarea"] {
    background: transparent !important;
}

/* FIX BUTTON AREA */
div[data-testid="stTextArea"] button {
    background: transparent !important;
    border: none !important;
    color: white !important;
}
/* REMOVE SPLIT LOOK */
div[data-testid="stTextArea"] div {
    background: transparent !important;
}

/* LABEL */
div[data-testid="stTextArea"] label {
    color: white !important;
    font-weight: 600;
}

/* HOVER EFFECT */
div[data-testid="stTextArea"]:hover > div {
    box-shadow: 0 0 10px rgba(168,85,247,0.5);
}

/* FOCUS EFFECT */
div[data-testid="stTextArea"]:focus-within > div {
    box-shadow: 0 0 12px rgba(168,85,247,0.7);
}

</style>
""", unsafe_allow_html=True)

# Login and Register page

st.markdown("""
<style>

/* TARGET ONLY LOGIN + REGISTER FORMS */
div[data-testid="stForm"] {
    background: rgba(255,255,255,0.05);
    padding: 30px;
    border-radius: 30px;
    backdrop-filter: blur(12px);
    border: 1px solid rgba(255,255,255,0.15);
    max-width: 800px;
    margin: auto;
}

/* TEXT INPUT + PASSWORD */
div[data-testid="stTextInput"] input {
    background: rgba(255,255,255,0.08) !important;
    border: 1px solid rgba(255,255,255,0.25) !important;
    border-radius: 10px !important;
    color: white !important;
}

/* SELECTBOX (Role) */
/* Outer container */
div[data-testid="stSelectbox"] > div {
    background: rgba(255,255,255,0.08) !important;
    border: 1px solid rgba(255,255,255,0.25) !important;
    border-radius: 8px !important;
    padding: 2px;

}
div[data-testid="stSelectbox"] div[data-baseweb="select"] { border: 1px solid black !important; }
/* Inner select field (MAIN FIX) */
div[data-testid="stSelectbox"] div[data-baseweb="select"] > div {
    background: transparent !important;
    border: none !important;
    color: white !important;
}

/* Text */
div[data-testid="stSelectbox"] span {
    color: white !important;
}

/* Arrow icon */
div[data-testid="stSelectbox"] svg {
    fill: white !important;
}


/* REMOVE extra inner border (IMPORTANT FIX) */
div[data-testid="stSelectbox"] div {
    border: none !important;
}
/* Hover */
div[data-testid="stSelectbox"]:hover > div {
    border: 1px solid #3b82f6 !important;
}

/* Focus */
div[data-testid="stSelectbox"]:focus-within > div {
    box-shadow: 0 0 10px rgba(59,130,246,0.5);
}

/* LABELS */
label {
    color: white !important;
    font-weight: 600;
}

/* REMOVE SPLIT LOOK */
div[data-testid="stTextInput"] div {
    background: transparent !important;
}

/* HOVER EFFECT */
div[data-testid="stTextInput"]:hover input> div {
    border: 1px solid #3b82f6 !important;
}

/* FOCUS EFFECT */
div[data-testid="stTextInput"]:focus-within input> div {
    box-shadow: 0 0 10px rgba(59,130,246,0.5);
}

/* BUTTON CENTER + STYLE */
div[data-testid="stFormSubmitButton"] button {
    width: 100%;
    background: linear-gradient(90deg,#3b82f6,#22c55e);
    color: white;
    border-radius: 10px;
    border: none;
    padding: 10px;
    font-weight: bold;
}

</style>
""", unsafe_allow_html=True)

st.set_page_config(page_title="AI Portfolio Dashboard", layout="wide")

# auto refresh 
if st.button("🔄 Refresh Data"):
    st.cache_data.clear()
# session start 
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "role" not in st.session_state:
    st.session_state.role = None    

# log and register page 
if not st.session_state.logged_in:

    st.markdown("""
    <div style='text-align:center'>

    <h2>🤖 AI Portfolio Intelligence System</h2>
    <p>Smart AI Powered Investment Platform</p>

    </div>
    """, unsafe_allow_html=True)

    #select page 
    tab_choice = st.radio("", ["Login", "Register"], horizontal=True)

    # -------- BACKGROUND CHANGE --------
    if tab_choice == "Login":
        st.markdown("""
        <style>
        .stApp{
            background: linear-gradient(#03045E,#0077B6,#1e3a8a,#e2e8f0);
        }
        </style>
        """, unsafe_allow_html=True)

    else:
        st.markdown("""
        <style>
        .stApp{
            background: linear-gradient(#1B4079,#7F9C96,#8FAD88, #CBDF90);
        }
        </style>
        """, unsafe_allow_html=True)

    # Center animation 
    if animation is not None:
        col1, col2, = st.columns([1,2])
        with col1:
            if animation:
                st_lottie(animation, height=230) 
        
        with col2 :
            st.markdown("""
            <div class="feature-box">
            <h4>AI powered investment analytics platform.</h4>
            <p>✔ Machine Learning Predictions</p>
            <p>✔ Portfolio Optimization</p>
            <p>✔ Reinforcement Learning Allocation</p>
            <p>✔ Generative AI</p>
            </div>
            """, unsafe_allow_html=True)

    else:
        st.markdown("<br>", unsafe_allow_html=True)  
    
    # ---------------- LOGIN ----------------
    if tab_choice =="Login":
        col1, col2, col3 = st.columns([1,2,1]) 
        with col2:
                
            with st.form("login_form"):
                st.session_state.login_user = st.text_input("Username")
                st.session_state.login_pass = st.text_input("Password", type="password")
                
                login_btn = st.form_submit_button("Login")

            if login_btn:
                username = st.session_state.login_user
                password = st.session_state.login_pass
                
                result = login_user(username, password)
                if result:
                    st.session_state.logged_in = True
                    
                    st.session_state.username = result[1]
                    
                    st.session_state.role = result[3]

                    st.success("Login Successful")
                    st.rerun()

                else:
                    st.error("Invalid Username or Password")
                
    # ---------------- REGISTER ----------------
    else:
        col1, col2, col3 = st.columns([1,2,1])
        with col2:
            with st.form("register_form"):
                new_user = st.text_input("New Username")
                new_password = st.text_input("New Password", type="password")

                role = st.selectbox("Role", ["Investor","Admin"])
                register_btn = st.form_submit_button("Register")
            if register_btn:
                add_user(new_user,new_password,role)
                st.success("Account Created Successfully")

    st.stop() 
# after login 
st.title("AI Portfolio Optimization Dashboard")

st.write(f"Welcome **{st.session_state.username}**")       

# ---------------- SIDEBAR ----------------
with st.sidebar:
    
        url = "https://assets2.lottiefiles.com/packages/lf20_qp1q7mct.json"
        animation = requests.get(url).json()
        st_lottie(animation, height=110)

        st.markdown("""
        <div class="glass-card">
        <h3>🤖 AI Portfolio System</h3>
        <p>Investment Intelligence System</p>

        </div>
        """, unsafe_allow_html=True)
    
        if st.session_state.role =="Investor":
            page = st.radio(
                "Navigation",
                [
                    "AI Portfolio Advisor",
                    "Market Analysis",
                    "Portfolio Optimization",
                    "Investment Simulator",
                    "Portfolio Report"
                ]
            )
            st.markdown("---")
            st.markdown("""
            <div class="glass-card">
            AI Portfolio System v1.0
            </div>
            """, unsafe_allow_html=True)
        elif st.session_state.role =="Admin":
            page = st.radio(
                "Admin Panel",
                [
                    "User Management",
                    "System Analytics"
                ]
            )    
            st.markdown("---")
   
        if st.sidebar.button("Logout"):
            st.session_state.logged_in = False
            st.rerun()    

# Initialize session variables
if "best_portfolio" not in st.session_state:
    st.session_state.best_portfolio = None

if "allocation" not in st.session_state:
    st.session_state.allocation = None 

if "ai_result" not in st.session_state:
    st.session_state.ai_result = None    

# ---------------- MONTE CARLO PORTFOLIO ----------------
@st.cache_data
def run_monte_carlo(assets,annual_returns,cov_matrix):
    num_portfolios = 5000
    results = []

    for _ in range(num_portfolios):
        weights = np.random.random(len(assets))
        weights /= np.sum(weights)
        port_return = np.dot(weights, annual_returns)
        port_risk = np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights)))
        sharpe_ratio = port_return / port_risk
        results.append([port_return, port_risk, sharpe_ratio, weights.tolist()])

    portfolios = pd.DataFrame(results, columns=["Return","Risk","Sharpe","Weights"])
    best = portfolios.loc[portfolios["Sharpe"].idxmax()]

    allocation = pd.DataFrame({
        "Asset": assets,
        "Weight": best["Weights"],

    })

# Save in session_state
    st.session_state['allocation'] = allocation.copy()
    st.session_state['best_portfolio'] = best
    #return portfolios 
    st.session_state["portfolios"] = portfolios
    return portfolios

# ---------------- LOAD LIVE DATA ----------------
@st.cache_data(ttl=3600)
def load_live_data():
    # Assets
    stocks = ["TCS.NS","INFY.NS","RELIANCE.NS","HDFCBANK.NS","ICICIBANK.NS"]
    etfs = ["NIFTYBEES.NS","GOLDBEES.NS"]
    reits = ["MINDSPACE.NS","EMBASSY.NS"]
    international = ["SPY","QQQ"]

    all_assets = stocks + etfs + reits + international
    safe_assets = {
        "PPF":0.071,
        "EPF":0.081,
        "GSEC":0.065
    }

    try :
        # Fetch 1 year data
        end_date = datetime.datetime.today()
        start_date = end_date - datetime.timedelta(days=365)
        data = yf.download(all_assets, start=start_date, end=end_date)["Close"]
        # Daily returns
        returns = data.pct_change().dropna()
        # Annualized metrics
        annual_returns = returns.mean() * 252
        cov_matrix = returns.cov() * 252
    except Exception as e:
        st.warning(f"Market data could not be loaded: {e}")
    return data, returns, annual_returns, cov_matrix, all_assets, safe_assets

data, daily_returns, annual_returns, cov_matrix, assets , safe_assets = load_live_data()

# Generate Monte Carlo portfolio if not already
if st.session_state.best_portfolio is None or st.session_state.allocation is None:
    portfolios = run_monte_carlo(assets, annual_returns, cov_matrix)
else:
    portfolios = st.session_state.get("portfolios")

# Train RL model
clean_returns = daily_returns.replace([np.inf, -np.inf], np.nan).dropna()
clean_returns = (clean_returns - clean_returns.mean()) / clean_returns.std()
@st.cache_resource
def get_rl_model(returns):
    return train_rl_agent(returns)
    

rl_model = get_rl_model(clean_returns)

# Get portfolio weights from RL
rl_weights = get_rl_portfolio_weights(rl_model, daily_returns)


# ---------------- ENSURE MONTE CARLO DATA ----------------
if st.session_state.get("best_portfolio") is None or st.session_state.get("allocation") is None:
    st.info("Generating Monte Carlo portfolio for simulator and optimization...")
    portfolios = run_monte_carlo(assets, annual_returns, cov_matrix)
else:
    portfolios = st.session_state.get("portfolios")
    
# ---------------- ML RETURN PREDICTION ----------------

predicted_returns = {}

for asset in assets:
    try:
        predicted_returns[asset] = get_predicted_return(asset)
    except:
        predicted_returns[asset] = annual_returns.get(asset, 0)

ml_returns = pd.Series(predicted_returns)

sector_map = {
    "HDFCBANK.NS": "Banking",
    "ICICIBANK.NS": "Banking",
    "ITC.NS": "FMCG",
    "LT.NS": "Infrastructure",
    "Gold": "Commodities",
    "Fixed Income (Bonds)": "Fixed Income",
    "Mutual Funds": "Mutual Funds",
    "International ETFs": "International Funds",
    "TATAELXSI.NS": "IT",
    "ADANIENT.NS": "IT",
    "TCS.NS": "IT",
    "INFY.NS": "IT",
    "RELIANCE.NS": "Energy",

}  

# ---------------- PAGE 1: AI ADVISOR ----------------
if st.session_state.role =="Investor":
    if page == "AI Portfolio Advisor":
        st.header(" AI Portfolio Advisor")
        
        goal = st.text_area(
            "Describe your investment goal",
            value=st.session_state.get("goal", "I want long term wealth creation high Risk")
        )

        amount = st.number_input(
            "Enter Investment Amount (₹)",
            value=st.session_state.get("amount", 500000)
        )

        duration = st.slider(
            "Investment Duration (Years)",
            1, 15,
            value=st.session_state.get("duration", 10)
        )

        risk = st.selectbox(
            "Risk Level",
            ["Low", "Medium", "High"],
            index=["Low", "Medium", "High"].index(st.session_state.get("risk", "Medium"))
        )
        if st.button("Generate AI Portfolio"):
            st.session_state.goal=goal
            st.session_state.amount=amount
            st.session_state.duration=duration
            st.session_state.risk=risk
            
            with st.spinner("AI analyzing your portfolio..."):
                try :
                    result = app.invoke({"input": goal,"amount": amount,"duration": duration,"risk": risk})
                
                    if result is None:
                        st.error("AI failed to generate portfolio. Try again.")
                    else:
                        result = app.invoke({"input": goal,"amount": amount,"duration": duration,"risk": risk})
                        if result is None:
                            st.error("AI failed to generate portfolio. Try again.")
                         
                        # ------------------ ADD ALLOCATION DATAFRAME HERE ------------------
    
                        # Prepare allocation DataFrame from final_recommendation
                        allocation_data = result.get("allocation")
                        if allocation_data:
                            allocation_df = pd.DataFrame(allocation_data)
                            esg_map = {
                                "TCS.NS": 85,
                                "INFY.NS": 80,
                                "RELIANCE.NS": 65,
                                "HDFCBANK.NS": 75,
                                "BTC-USD": 50,
                                "ETH-USD": 55
                            }
                            allocation_df["ESG Score"] = allocation_df["Asset"].map(esg_map).fillna(60)

                            st.session_state["allocation"] = allocation_df
                            st.session_state["ai_result"] = result
                            
                            st.success("AI Portfolio generated!")
                            
                except Exception as e :
                    st.error(f"AI Portfolio analysis failed: {e}")
  
        # --- Always show AI Portfolio if already generated ---
        if st.session_state.get("ai_result") is not None:
            result = st.session_state["ai_result"]
            st.subheader("AI Portfolio Recommendation")
            st.text(result["final_recommendation"])
            st.subheader("Portfolio Critique")
            st.write(result["portfolio_review"])

# ---------------- PAGE 2: MARKET ANALYSIS ----------------
    elif page == "Market Analysis":
            st.subheader("Market News Sentiment")
            try:
                sentiments = analyze_sentiment()
                sentiment_df = pd.DataFrame(sentiments)
               
                fig = go.Figure(data=[go.Table(
                    header=dict(
                        values=list(sentiment_df.columns),
                        fill_color='rgba(0,0,0,0.4)',
                        font=dict(color='white', size=14),
                        align='center'
                    ),
                    cells=dict(
                        values=[sentiment_df[col] for col in sentiment_df.columns],
                        fill_color='rgba(0,0,0,0)',
                        font=dict(color='white', size=13),
                        align='center'
                    )
                )])
                fig.update_layout(
                    paper_bgcolor='rgba(0,0,0,0)',
                )
                st.plotly_chart(fig, use_container_width=True)

                sentiment_counts = sentiment_df["sentiment"].value_counts()
                df_chart = sentiment_counts.reset_index()
                df_chart.columns = ["Sentiment", "Count"]
                fig = px.bar(
                    df_chart, 
                    x="Sentiment", 
                    y="Count",
                    color="Sentiment",   
                    color_discrete_map={
                        "Positive": "#22c55e",   
                        "Negative": "#ef4444",   
                        "Neutral": "#3b82f6"     
                    }
                    
                )

                fig.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(color='white')
                )
                st.plotly_chart(fig, use_container_width=True)

            except Exception as e:
                st.warning("Sentiment analysis could not be loaded.") 
            st.header("📊 Market Insights")
            # Show AI market analysis
           
            if st.session_state.get("ai_result") is not None :
                result = st.session_state["ai_result"]
                st.write(result["market_analysis"])
            else:
                st.info("Generate AI Portfolio first.")
            #  Show recent NIFTY ETF data in table format
            st.subheader("Recent Market Data (NIFTY ETF)")
            try:
                data = yf.download("NIFTYBEES.NS", period="1mo")
                data = data.reset_index()
               
                if data.empty:
                    st.warning("no data found")
                else:
                    
                    if isinstance(data.columns, pd.MultiIndex):
                        data.columns = data.columns.get_level_values(0)
                    
                    fig = go.Figure(data=[go.Table(
                        header=dict(
                            values=list(data.columns),
                            fill_color='rgba(0,0,0,0.4)',
                            font=dict(color='white', size=14),
                            align='center'
                        ),
                        cells=dict(
                            values=[data[col] for col in data.columns],
                            fill_color='rgba(0,0,0,0)',
                            font=dict(color='white', size=12),
                            align='center'
                        )
                    )])
                    fig.update_layout(
                        paper_bgcolor='rgba(0,0,0,0)',
                        margin=dict(l=0, r=0, t=10, b=0)
                    )
                    st.plotly_chart(fig, use_container_width=True)
                   
                    st.subheader("NIFTY ETF Price Trend")
                    fig2 = px.line(data, x="Date", y="Close")

                    fig2.update_layout(
                        plot_bgcolor='rgba(0,0,0,0)',
                        paper_bgcolor='rgba(0,0,0,0)',
                        font=dict(color='white')
                    )
                    st.plotly_chart(fig2, use_container_width=True)
            except Exception as e:
                st.warning(f"NIFTY ETF data could not be loaded: {e}")


# ---------------- PAGE 3: PORTFOLIO OPTIMIZATION ----------------
    elif page == "Portfolio Optimization":
            st.header("Portfolio Optimization")

            allocation = st.session_state.get("allocation")
            best = st.session_state.get("best_portfolio")

            if allocation is None or best is None:
                st.warning("Please generate portfolio first.")
                st.stop()
            allocation = allocation.copy()
    # ---------------- RISK CONTRIBUTION ----------------

            weights = np.array(best["Weights"])

            portfolio_variance = np.dot(weights.T, np.dot(cov_matrix, weights))
            portfolio_risk = np.sqrt(portfolio_variance)

            marginal_risk = np.dot(cov_matrix, weights)
            risk_contribution = weights * marginal_risk / portfolio_risk

            risk_df = pd.DataFrame({
                "Asset": assets,
                 "Risk Contribution": risk_contribution
            })
# ------------benchmark & portfolio returns --------------
            try:
                # portfolio returns 
                portfolio_returns = daily_returns.dot(weights)
                portfolio_cum = (1 + portfolio_returns).cumprod()
                if "NIFTYBEES.NS" in data.columns:
                    benchmark = data["NIFTYBEES.NS"]
                    benchmark_returns = benchmark.pct_change().dropna()
                    benchmark_cum = (1 + benchmark_returns).cumprod()

                #comarsion dataframe 
                    comparison = pd.DataFrame({
                        "Portfolio": portfolio_cum,
                        "NIFTY Benchmark": benchmark_cum
                    })
                else:
                    st.warning("NIFTYBEES data not available")
                    comparison = pd.DataFrame({
                        "Portfolio": portfolio_cum
                    })    
            except Exception as e :
                st.warning(f"Portfolio or benchmark returns could not be calculated: {e}")
                comparison = pd.DataFrame()

            col1, col2, col3= st.columns(3)
            def glass_metric(title,value):
                return f"""
                <div style="
                    background: rgba(255,255,255,0.05);
                    border:1px solid rgba(255,255,255,0.15);
                    backdrop-filter: blur(10px);
                    padding:15px;
                    border-radius:12px;
                    text-align:center;
                    width:250px;
                    height:120px;
                    margin:auto;
                    display:flex;
                    flex-direction:column;
                    align-items:center;
                    justify-content:center;
                    backdrop-filter: blur(10px);
                    gap:10px;
                    box-shadow: 0 8px 25px rgba(0,0,0,0.3);
                ">
                    <span style="color:white; font-weight:bold; font-size:18px;">
                        {title}
                    </span>
                    <span style="color:#38bdf8; font-weight:bold;font-size:18px;">
                        {value}
                    </span>
                </div>
                """
            with col1:
                st.markdown(glass_metric("Return", f"{round(best['Return']*100,2)}%"), unsafe_allow_html=True)

            with col2:
                st.markdown(glass_metric("Risk", f"{round(best['Risk']*100,2)}%"), unsafe_allow_html=True)

            with col3:
                st.markdown(glass_metric("Sharpe", f"{round(best['Sharpe'],2)}"), unsafe_allow_html=True)
   
            # ---------------- ESG SCORE ----------------
            allocation = st.session_state.get("allocation")
            st.subheader("🌱 ESG Score Analysis")
            if allocation is not None and "ESG Score" in allocation.columns:
                avg_esg = allocation["ESG Score"].mean()
                if avg_esg >= 70:
                    st.success(f"🌱 Strong ESG Score: {round(avg_esg,2)}")
                elif avg_esg >= 50:
                    st.warning(f"🌿 Moderate ESG Score: {round(avg_esg,2)}")
                else:
                    st.error(f"⚠️ Low ESG Score: {round(avg_esg,2)}")
            else:
                st.warning("ESG data not available")
# ---------------- Portfolio Risk Metrics ----------------
            st.subheader("📊 Portfolio Risk Metrics")

            metrics ={} 

            if "result" in locals() and result is not None:
                metrics = result.get("portfolio_metrics", {})
               
            if not metrics:
                import numpy as np
                returns = [0.02, 0.01, -0.015] 
                volatility = np.std(returns)
                sharpe_ratio = np.mean(returns) / volatility if volatility != 0 else 0
                beta = 1.2
                coin_beta = 1.0
                metrics = {
                    "volatility": volatility,
                    "sharpe_ratio": sharpe_ratio,
                    "beta": beta,
                    "coin_beta": coin_beta
                }
            col4,col5,col6,col7 =st.columns(4)
            with col4:
                st.markdown(glass_metric("Portfolio Beta", metrics.get("beta", "N/A")), unsafe_allow_html=True)

            with col5:
                if "coin_beta" in metrics:
                    st.markdown(glass_metric("Crypto Beta", metrics.get("coin_beta", "N/A")), unsafe_allow_html=True)

            with col6:
                st.markdown(glass_metric("Volatility", round(metrics.get("volatility", 0), 4)), unsafe_allow_html=True)

            with col7:
                st.markdown(glass_metric("Sharpe Ratio", round(metrics.get("sharpe_ratio", 0), 4)), unsafe_allow_html=True)

            
            st.subheader("🚨 Alerts & Risk Monitoring")
            if st.session_state.get("ai_result") is not None:
                result = st.session_state["ai_result"]
              
                summary = result.get("scenario_summary", None)
                if summary:
                    current = summary.get("current_total", 1)
                    crash = summary.get("crash_total", 0)
                    risk_level = result.get("risk_level", "").lower()
                    loss_pct = ((current - crash) / current) * 100

                    if loss_pct > 15 and risk_level =="low":
                        st.error("🚨 Inconsistency: AI marked LOW risk but crash loss is HIGH!")
                    elif loss_pct > 8 and risk_level=="high":
                        st.warning("⚠️ Inconsistency: AI marked HIGH risk but portfolio looks safe")
                    else:
                        st.success(f"✅ Low Risk: Only {loss_pct:.2f}% drop expected")
                else:
                    st.warning("⚠️ Scenario data not available")

                # ------------- Rebalancing Alert------------------
                allocation_data = result.get("allocation", [])
                if allocation_data is not None:
                    allocation = pd.DataFrame(allocation_data)
                    for _, row in allocation.iterrows():
                        deviation = abs(row["current_weight"] - row["Weight"])
                        if deviation > 0.05:
                            st.warning(f"⚠️ Rebalancing needed for {row['Asset']}")
                else:
                    st.info("ℹ️ Allocation data not available yet")
                # ------------------- RISK THRESHOLD ALERT -------------------
                metrics = result.get("portfolio_metrics",{})
                if metrics and isinstance(metrics, dict):
                    if metrics.get("volatility", 0) > 0.15:  
                        st.error(f"🚨 High volatility alert: {metrics['volatility']*100:.2f}%")
                    if metrics.get("sharpe_ratio", 0) < 0.8: 
                        st.warning(f"⚠️ Low Sharpe Ratio: {metrics['sharpe_ratio']:.2f}")
                    if metrics.get("beta", 0) > 1.2: 
                        st.error(f"🚨 High Beta alert: {metrics['beta']:.2f}")
                else:
                    st.info("ℹ️ Portfolio metrics not available")

            # post tax returns 
            st.subheader("Post-Tax Expected Return")

            holding_period = st.selectbox(
                "Select Holding Period",
                ["Short Term (<1 year)", "Long Term (>1 year)"]
            )
            expected_return = best["Return"]

        # Capital gains tax
            if holding_period == "Short Term (<1 year)":
                tax_rate = 0.15    
            else:
                tax_rate = 0.10    

            post_tax_return = expected_return * (1 - tax_rate)

            col_left, col_right = st.columns([1,2])
            with col_left:
                st.markdown(f"""
                <div style="
                    background: rgba(255,255,255,0.06);
                    border:0.9px solid rgba(255,255,255,0.2);
                    backdrop-filter: blur(12px);
                    padding:8px;
                    border-radius:8px;
                    text-align:center;
                    box-shadow: 0 8px 25px rgba(0,0,0,0.3);
                ">
                    <h4 style="color:white; margin-bottom:3px;">
                        Post-Tax Return
                    </h4>
                    <h2 style="color:#38bdf8;">
                        {round(post_tax_return*100,2)}%
                    </h2>
                </div>
                """, unsafe_allow_html=True)

    # Portfolio vs NIFTY Benchmark Performance

            st.subheader(" Portfolio vs NIFTY Benchmark Performance") 
            try:
                portfolio_return = portfolio_cum.iloc[-1] - 1
                benchmark_return = benchmark_cum.iloc[-1] - 1

                st.write("Portfolio Return:", round(portfolio_return*100,2), "%")
                st.write("NIFTY Benchmark Return:", round(benchmark_return*100,2), "%")       

                if portfolio_return > benchmark_return:
                    st.success("Portfolio outperformed the NIFTY benchmark.")
                else:
                    st.warning("Portfolio underperformed the NIFTY benchmark.")
            except :
                st.info("Portfolio benchmark comparison not available.")

        # portfolio value trends 
            st.subheader("Portfolio Value Trend")
            days = 30
            trend_data = np.cumsum(np.random.normal(200, 100, days)) + 200000
            
            trend_df = pd.DataFrame({
                "Day": range(days),
                "Portfolio Value": trend_data
            })
            fig = px.line(
                trend_df,
                x="Day",
                y="Portfolio Value"
            )

            fig.update_traces(
                line=dict(width=3)  
            )
            premium_chart(fig)
    # ------- Asset Allocation --------------------

            cols1 , cols2 = st.columns(2)
            with cols1 :
                st.subheader("Optimal Asset Allocation")
                
                fig = go.Figure(data=[go.Table(
                    header=dict(
                        values=list(allocation.columns),
                        fill_color='rgba(0,0,0,0.4)',
                        font=dict(color='white', size=14),
                        align='center'
                    ),
                    cells=dict(
                        values=[allocation[col] for col in allocation.columns],
                        fill_color='rgba(0,0,0,0)',
                        font=dict(color='white', size=13),
                        align='center'
                    )
                )])
                premium_chart(fig, height=300)
                
            with cols2:
                
                st.subheader("Allocation Distribution")

                allocation_sorted = allocation.sort_values("Weight", ascending=False)

                fig = px.pie(
                    allocation_sorted,
                    names="Asset",
                    values="Weight",
                    hole=0.55,   
                )

                premium_chart(fig)    
# ------------ charts -----------------------
            coll1,coll2 =st.columns(2)
            with coll1:
                
                st.subheader("Risk vs Return")
                
                df_plot = portfolios.copy()
                fig = px.scatter(
                    df_plot,
                    x="Risk",
                    y="Return",
                    color="Sharpe",
                    color_continuous_scale="viridis"
                )
                premium_chart(fig)
            with coll2 :
                st.subheader("Efficient Frontier")
            
                fig = px.scatter(
                    portfolios,
                    x="Risk",
                    y="Return",
                    color="Sharpe",
                    color_continuous_scale="plasma"
                )

                fig.add_scatter(
                    x=[best["Risk"]],
                    y=[best["Return"]],
                    mode="markers",
                    marker=dict(size=14, color="red"),
                    name="Best Portfolio"
                )
                premium_chart(fig)
            
            colls1,colls2=st.columns(2)
            with colls1:
                st.subheader("Asset Correlation Heatmap")
                fig = px.imshow(
                    daily_returns.corr(),
                    text_auto=True,
                    color_continuous_scale="RdBu"
                )
                premium_chart(fig, height=500)
                
            with colls2:
                st.subheader("Monte Carlo Portfolio Returns Distribution")
                fig = px.histogram(
                    portfolios,
                    x="Return",
                    nbins=50,
                    opacity=0.7,
                )
               
                fig.add_vline(
                    x=best["Return"],
                    line_dash="dash",
                    line_color="red"
                )
                premium_chart(fig)

    #---- rolling volatility and sector ---------------
            col1 ,col2 = st.columns(2)
            with col1:
                st.subheader("Rolling 30-Day Volatility")
                rolling_vol = daily_returns.rolling(window=30).std() * np.sqrt(252)
                
                fig = px.line(rolling_vol)
                premium_chart(fig) 
    
            with col2:
                allocation["Sector"] = allocation["Asset"].map(sector_map)
                sector_allocation = (
                    allocation
                    .groupby("Sector")["Weight"]
                    .sum()
                    .reset_index()
                )
                st.subheader("Sector Allocation")
                
                fig = px.pie(
                    sector_allocation,
                    names="Sector",
                    values="Weight",
                    hole=0.5  
                )
                premium_chart(fig)
# ------risk contribution by ASSET-------------------
            col1,col2=st.columns(2)
            with col1 :
                st.subheader("Top Risk Contributors")
                top5_risk = risk_df.sort_values(by="Risk Contribution", ascending=False).head(5)
                fig = px.bar(
                    top5_risk,
                    x="Asset",
                    y="Risk Contribution",
                    color="Risk Contribution",
                    color_continuous_scale=["#06b6d4", "#3b82f6"]
                )
                premium_chart(fig)
                
            with col2:
                st.subheader("Portfolio vs NIFTY Benchmark")
                if not comparison.empty:
                   
                    fig = go.Figure()
                    
                    fig.add_trace(go.Scatter(
                        x=comparison.index,
                        y=comparison["Portfolio"],
                        mode='lines',
                        name='Portfolio'
                    ))

                    fig.add_trace(go.Scatter(
                        x=comparison.index,
                        y=comparison["NIFTY Benchmark"],
                        mode='lines',
                        name='Benchmark'
                    ))

                    premium_chart(fig)
                else:
                    st.info("Comparison not available")
               

            st.subheader("Reinforcement Learning Portfolio Allocation")
            rl_df = pd.DataFrame({
                "Asset": assets,
               "Weight": rl_weights
            })
            
            fig = px.bar(
                rl_df,
                x="Asset",
                y="Weight",
                color="Weight",
                color_continuous_scale=["#00f5ff", "#6366f1", "#8b5cf6"]
            )
            premium_chart(fig)   

# ---------------- PAGE 4: INVESTMENT SIMULATOR ----------------
    elif page == "Investment Simulator":
            st.subheader("💰 Investment Allocation Simulator")
            allocation = st.session_state['allocation']
            best = st.session_state['best_portfolio']

            investment = st.slider("Investment Amount (₹)", 10000, 1000000, 100000)
            allocation['Investment'] = allocation['Weight'] * investment
           
            fig_table = go.Figure(data=[go.Table(
                header=dict(
                    values=list(allocation.columns),
                    fill_color='rgba(0,0,0,0.4)',
                    font=dict(color='white', size=14),
                    align='center'
                ),
                cells=dict(
                    values=[allocation[col] for col in allocation.columns],
                    fill_color='rgba(0,0,0,0)',
                    font=dict(color='white', size=12),
                    align='center'
                )
            )])
            fig_table.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                margin=dict(l=0, r=0, t=10, b=0)
            )
            st.plotly_chart(fig_table, use_container_width=True)
            
            st.subheader("Portfolio Growth Simulator")
            years = st.slider("Investment Horizon (Years)", 1, 30, 10)
            value = investment
            growth = []
            expected_return = best['Return']

            for year in range(years):
                value *= (1 + expected_return)
                growth.append(value)

            growth_df = pd.DataFrame({"Year": list(range(1, years+1)), "Portfolio Value": growth})
            
            fig_growth = px.line(
                growth_df,
                x="Year",
                y="Portfolio Value"
            )

            fig_growth.update_traces(
                line=dict(color="#06b6d4", width=3)
            )

            fig_growth.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white')
            )
            st.plotly_chart(fig_growth, use_container_width=True)

            st.metric("Final Portfolio Value", f"₹{int(growth[-1]):,}")
    
            st.header("Tax Saving Simulation")
            col1, col2 = st.columns(2)
            with col1:
                annual_income = st.number_input(
                    "Annual Income (₹)",
                    min_value=100000,
                    max_value=5000000,
                    value=800000
                )

            investment_80c = st.slider(
                "80C Investment (PPF / ELSS)",
                0,
                150000,
                50000
            )

            health_insurance = st.slider(
                "Health Insurance (80D)",
                0,
                25000,
                10000
            )

            with col2:
                total_deduction = investment_80c + health_insurance
                taxable_income = max(0,annual_income - total_deduction)

                st.metric("Total Deduction", f"₹{total_deduction:,}")
            st.metric("Taxable Income", f"₹{taxable_income:,}")

            #  tax calculation

            if taxable_income <= 250000:
                tax = 0

            elif taxable_income <= 500000:
                tax = (taxable_income - 250000) * 0.05
            elif taxable_income <= 1000000:
                tax = 12500 + (taxable_income - 500000) * 0.20
            else:
                tax = 112500 + (taxable_income - 1000000) * 0.30

            st.metric("Estimated Tax Payable", f"₹{int(tax):,}")    
    
            coll1,coll2 = st.columns(2)
            with coll1:
                st.subheader("Tax Saving Impact")

                df_tax = pd.DataFrame({
                    "Type": ["Before Deduction", "After Deduction"],
                    "Amount": [annual_income, taxable_income]
                })
                
                fig_tax = px.bar(
                    df_tax,
                    x="Type",
                    y="Amount",
                    color="Amount",
                    color_continuous_scale=["#06b6d4", "#3b82f6"]
                )

                fig_tax.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(color='white'),
                    coloraxis_showscale=False
                )
                st.plotly_chart(fig_tax, use_container_width=True)

            st.subheader("Safe Investment (PPF / EPF)")
            safe_choice = st.selectbox(
                "Select Safe Asset",
                list(safe_assets.keys())
            )
            safe_rate = safe_assets[safe_choice]
            years = st.slider("Investment Years",1,30,10)
            safe_value = investment * (1 + safe_rate) ** years
            st.metric(
                f"{safe_choice} Final Value",
                f"₹{int(safe_value):,}"
            )
# ---------------- PAGE 5: PORTFOLIO REPORT ----------------
    elif page == "Portfolio Report":
            st.header("📄 Download Portfolio Report")
        
            if st.session_state.get("ai_result") is None:
                st.warning("Generate AI Portfolio first.")
                st.stop()

            if st.button("Generate Portfolio Report"):
                try :
                    result = st.session_state['ai_result']
                    allocation = st.session_state['allocation']
                    filename = generate_report(
                        "User Investment Goal",
                        result.get("final_recommendation", ""),
                        result.get("portfolio_review", ""),
                        allocation
                    )
                    with open(filename, "rb") as file:
                        st.download_button(
                        label="Download PDF Report",
                        data=file,
                        file_name="AI_Portfolio_Report.pdf",
                        mime="application/pdf"
                    )
                except Exception as e:
                    st.error(f"Report generation failed: {e}")
            
        
        # ---------------- ADMIN PANEL ----------------

elif st.session_state.role == "Admin":
            st.header("Admin Dashboard")
            if page == "User Management":
                st.subheader("Registered Users")
                conn = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    password="root",
                    database="portfolio_db"
                )
                cursor = conn.cursor()
                cursor.execute("SELECT id, username, role FROM users")
                users = cursor.fetchall()
                df = pd.DataFrame(users, columns=["ID","Username","Role"])
                
                fig = go.Figure(data=[go.Table(
                    header=dict(
                        values=list(df.columns),
                        fill_color='rgba(0,0,0,0.4)',
                        font=dict(color='white', size=14),
                        align='center'
                    ),
                    cells=dict(
                        values=[df[col] for col in df.columns],
                        fill_color='rgba(0,0,0,0)',
                        font=dict(color='white', size=13),
                        align='center'
                    )
                )])
                fig.update_layout(
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    margin=dict(l=0, r=0, t=10, b=0)
                )
                st.plotly_chart(fig, use_container_width=True)
            
            elif page == "System Analytics":
                st.subheader("System Analytics")

                conn = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    password="root",
                    database="portfolio_db"
                )
                cursor = conn.cursor()
                cursor.execute("SELECT count(*) from users")
                total_users = cursor.fetchone()[0]

                st.metric("Total Users", total_users)
    