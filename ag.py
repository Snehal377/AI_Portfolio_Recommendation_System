from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os
from prompts import *
from optimizer import optimize_portfolio, get_risk_constraints
from tool import market_research
from langgraph.graph import StateGraph, END
from typing import TypedDict
from ml_predictor import segment_investor
load_dotenv()

# Initialize LLM
llm = ChatGroq(
    model="llama-3.1-8b-instant",
    api_key=os.getenv("GROQ_API_KEY")
)

# Safe Risk Function 
def get_final_risk(user_risk, amount, duration):
    try:
        if user_risk:
            return user_risk.lower().strip()
        return segment_investor(amount, duration)
    except:
        return "medium"

# Agent State 

class AgentState(TypedDict):
    input: str
    market_analysis: str
    risk_report: str
    risk_level: str
    risk :str
    final_recommendation: str
    portfolio_review: str
    amount: float
    duration: int
    scenario_summary: dict
    portfolio_metrics: dict
    allocation: list

# Market Analyst Agent

def market_analyst(state):
    user_query = state["input"]
    research = market_research(user_query)
    clean_research = research.split("Recent Market Data")[0] if "Recent Market Data" in research else research

    prompt = f"""
{MARKET_ANALYST_PROMPT}

User Query:
{user_query}

Market Research Data:
{research}

Clean Research:
{clean_research}
"""
    response = llm.invoke(prompt)
    state["market_analysis"] = f"Market Analysis for: {user_query}\nAI Market Interpretation:\n{response.content}"
    return state

# Risk Analyst Agent

def risk_analyst(state):
    market_data = state["market_analysis"]
    user_risk = state["risk"]

    prompt = f"""
{RISK_ANALYST_PROMPT}

IMPORTANT: User has selected risk level = {user_risk}.
You MUST strictly follow this risk level.
Do NOT override it.

Based on the following market analysis, determine the investment risk level.

Market Data:
{market_data}

Classify the overall investment risk as:
LOW RISK
MEDIUM RISK
HIGH RISK
"""
    response = llm.invoke(prompt)
    state["risk_report"] = response.content
   
    return state

# Scenario Simulation 

def simulate_scenarios(portfolio):
    crash_total = 0
    bull_total = 0
    current_total = 0
    results = []

    for asset in portfolio:
        investment = asset["investment_₹"]
        crash_value = investment * 0.8
        bull_value = investment * 1.15
        crash_total += crash_value
        bull_total += bull_value
        current_total += investment
        results.append({
            "asset": asset["asset"],
            "current": investment,
            "crash": round(crash_value, 2),
            "bull": round(bull_value, 2)
        })

    summary = {
        "current_total": round(current_total, 2),
        "crash_total": round(crash_total, 2),
        "bull_total": round(bull_total, 2)
    }

    return results, summary

# ---------------- ESG Score Function ----------------
def get_esg_score(asset):
    esg_scores = {
        "TCS.NS": 85,
        "INFY.NS": 80,
        "RELIANCE.NS": 65,
        "HDFCBANK.NS": 75,
        "BTC-USD": 50,
        "ETH-USD": 55
    }
    return esg_scores.get(asset, 60)
# Portfolio Consultant Agent

def portfolio_consultant(state):

    user_query = state.get("input", "")
    amount = state["amount"]
    duration = state["duration"]
    user_risk= state.get("risk")
 
    risk = get_final_risk(user_risk,amount,duration)
    print("final risk :",risk)

    # Step 2: ML risk
    ml_risk = segment_investor(amount, duration)
    ml_risk = ml_risk.lower().replace(" risk", "").strip()
    # Step 3: Final decision priority
    
    # Risk-based allocation 
    risk = risk.lower().strip()
    if risk == "low":
        allocation_split = {"stocks": 0.4, "gold": 0.1, "fixed_income": 0.2, "mutual_funds": 0.2, "international": 0.1}
    elif risk == "high":
        allocation_split = {"stocks": 0.7, "gold": 0.05, "fixed_income": 0.05, "mutual_funds": 0.1, "international": 0.1}
    else:
        print("⚠️ Invalid risk input, defaulting to MEDIUM")
        allocation_split = {"stocks": 0.5, "gold": 0.1, "fixed_income": 0.15, "mutual_funds": 0.15, "international": 0.1}

    stock_budget = amount * allocation_split["stocks"]
    portfolio = optimize_portfolio(amount,duration,risk)
    
    # Convert % allocation to actual investment
    detailed_portfolio = []
    for asset in portfolio:
        allocation_value = (asset["allocation"] / 100) * stock_budget
        detailed_portfolio.append({
            "asset": asset["asset"],
            "allocation_%": round(asset["allocation"] * allocation_split["stocks"], 2),
            "investment_₹": round(allocation_value, 2),
            "predicted_return": float(round(asset["predicted_return"], 4)),
            "esg_score" : get_esg_score(asset["asset"])
        })

    # Add other asset classes
    other_assets = [
        {"asset": "Gold", "allocation_%": allocation_split["gold"] * 100},
        {"asset": "Fixed Income (Bonds)", "allocation_%": allocation_split["fixed_income"] * 100},
        {"asset": "Mutual Funds", "allocation_%": allocation_split["mutual_funds"] * 100},
        {"asset": "International ETFs", "allocation_%": allocation_split["international"] * 100},
    ]
    for asset in other_assets:
        investment = (asset["allocation_%"] / 100) * amount
        detailed_portfolio.append({
            "asset": asset["asset"],
            "allocation_%": asset["allocation_%"],
            "investment_₹": round(investment, 2),
            "predicted_return": 0.08
        })

    scenario_results, summary = simulate_scenarios(detailed_portfolio)
    state["scenario_summary"] = summary

    # Portfolio explanation prompt
    prompt = f"""
{PORTFOLIO_CONSULTANT_PROMPT}

User Goal:
{user_query}

Investment Amount: ₹{amount}
Duration: {duration} years

Risk Level:
{risk}

Portfolio Data (Use This Only):
{detailed_portfolio}

Task:
1. Explain this portfolio EXACTLY as it is.
2. Do Not suggest rebalancing or adjustments.
3. Describe expected returns.

"""
    response = llm.invoke(prompt)

    portfolio_text = ""
    for p in detailed_portfolio:
        portfolio_text += f"""
📌 Asset: {p['asset']}
Allocation: {p['allocation_%']}%
Investment: ₹{p['investment_₹']}
Expected Return: {p['predicted_return']}
ESG Score :{p.get('esg_score','N/A')}
-----------------------------------
"""

    scenario_text = ""
    for s in scenario_results:
        scenario_text += f"""
📊 {s['asset']}
Current: ₹{s['current']}
Crash Value: ₹{s['crash']}
Bull Value: ₹{s['bull']}
-----------------------------------
"""
    state["final_recommendation"] = f"""
===== 📊 PORTFOLIO =====
{portfolio_text}

===== 📉📈 SCENARIO ANALYSIS =====
Total Investment: ₹{summary['current_total']}
After Market Crash (-20%): ₹{summary['crash_total']}
After Bull Run (+15%): ₹{summary['bull_total']}

{scenario_text}

=====  AI ANALYSIS =====
{response.content}
"""

    # Portfolio metrics
    import numpy as np
    returns = [0.02, 0.01, -0.015]
    volatility = np.std(returns)
    sharpe_ratio = np.mean(returns) / volatility if volatility != 0 else 0
    beta = 1.2
    coin_beta =1.5
    state["portfolio_metrics"] = {
        "volatility": float(volatility), 
        "sharpe_ratio": float(sharpe_ratio), 
        "beta": float(beta),
        "coin_beta" : float(coin_beta)}
    
    # Allocation for reference
    allocation_list = [
        {
            "Asset": asset["asset"],
            "Weight": asset["allocation_%"]/100,
            "current_weight": asset["allocation_%"]/100,
            "ESG Score":asset.get("esg_score",None)
        } 
        for asset in detailed_portfolio
    ]
    state["allocation"] = allocation_list

    return state

# Portfolio Critic Agent

def portfolio_critic(state):
    portfolio = state["final_recommendation"]
    prompt = f"{PORTFOLIO_CRITIC_PROMPT}\nPortfolio Recommendation:\n{portfolio}"
    response = llm.invoke(prompt)
    state["portfolio_review"] = response.content
    return state

# Workflow Setup

workflow = StateGraph(AgentState)
workflow.add_node("market_analyst", market_analyst)
workflow.add_node("risk_analyst", risk_analyst)
workflow.add_node("portfolio_consultant", portfolio_consultant)
workflow.add_node("portfolio_critic", portfolio_critic)

workflow.set_entry_point("market_analyst")
workflow.add_edge("market_analyst", "risk_analyst")
workflow.add_edge("risk_analyst", "portfolio_consultant")
workflow.add_edge("portfolio_consultant", "portfolio_critic")
workflow.add_edge("portfolio_critic", END)

app = workflow.compile()

# Run Agent

if __name__ == "__main__":
    user_input = input("Enter your investment goal: ")
    amount = float(input("Enter investment amount (₹): "))
    duration = int(input("Enter investment duration (years): "))
    risk = input("Enter your risk (low/medium/high): ")

    result = app.invoke({"input": user_input, "amount": amount, "duration": duration, "risk": risk})
    print("\n===== FINAL PORTFOLIO RECOMMENDATION =====\n")
    print(result["final_recommendation"])