import pandas as pd
import numpy as np 
from ml_predictor import get_predicted_return
from sentiment_analysis import get_market_sentiment_score
from ml_predictor import segment_investor
import warnings 
warnings.filterwarnings("ignore")

def optimize_portfolio(amount,duration,risk):
    
    top_assets = get_top_assets(risk)
    seen = set()
    unique_assets = []
    total_assets = len(top_assets)

    if total_assets == 0:
        return []
    if risk == "high":
        weights = [30, 25, 20, 15]
    elif risk == "medium":
        weights = [25, 25, 25, 25]
    else:
        weights = [40, 30, 20, 10]
    portfolio = []

    for i, (asset, pred) in enumerate(top_assets):
        allocation = weights[i] if i < len(weights) else 5  
        portfolio.append({
            "asset": asset,
            "predicted_return": round(pred, 4),
            "allocation": allocation
        })
    
    total_alloc = sum([p["allocation"] for p in portfolio])

    if total_alloc != 100:
        diff = 100 - total_alloc
        portfolio[0]["allocation"] += diff   
    return portfolio

 # monte carlo portfolio optimization    

def monte_carlo_portfolio(annual_returns, cov_matrix, assets):

    num_portfolios = 5000

    results = []

    predicted_returns={}
    for asset in assets:
        try:
            pred = get_predicted_return(asset)
            predicted_returns[asset] = pred
        except:
            predicted_returns[asset] = 0 

    # Normalize predictions
    preds = np.array(list(predicted_returns.values()))
    preds = (preds - preds.min()) / (preds.max() - preds.min() + 1e-8)

    sentiment_score = get_market_sentiment_score()

    # Convert sentiment into multiplier
    sentiment_factor = 1 + sentiment_score 

    for _ in range(num_portfolios):

        weights = np.random.random(len(assets))
        #  ML influence
        weights = weights * (1 + preds)

        #  Sentiment influence
        weights = weights * sentiment_factor

        weights /= np.sum(weights)

        port_return = np.dot(weights, annual_returns)

        port_risk = np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights)))

        sharpe = port_return / port_risk

        results.append([port_return, port_risk, sharpe, weights])

    df = pd.DataFrame(results, columns=["Return","Risk","Sharpe","Weights"])

    best = df.loc[df["Sharpe"].idxmax()]

    allocation = pd.DataFrame({

        "Asset": assets,
        "Weight": best["Weights"]
    })

    return df, best, allocation  

def get_risk_constraints(risk_level):
    """
    Returns a dictionary of weights for portfolio optimization
    based on the user's risk level.
    """

    if risk_level == "low":
        return {
            "stocks":0.30,
            "etfs":0.30,
            "bonds":0.25,
            "gold":0.10,
            "cash":0.05
        }

    elif risk_level == "medium":
        return {
            "stocks":0.45,
            "etfs":0.25,
            "bonds":0.15,
            "gold":0.10,
            "cash":0.05
        }

    else:  # high risk
        return {
            "stocks":0.65,
            "etfs":0.15,
            "bonds":0.05,
            "gold":0.10,
            "crypto":0.05
        } 

def get_top_assets(risk_level):

    if risk_level == "low":
        assets = ["HDFCBANK.NS", "ITC.NS", "LT.NS"]

    elif risk_level == "medium":
        assets = ["RELIANCE.NS", "INFY.NS", "TCS.NS", "BTC-USD"]

    else:
        assets = ["ADANIENT.NS", "TATAELXSI.NS", "BTC-USD","ETH-USD"]

    predictions = []

    for stock in assets:
        try:
            pred = get_predicted_return(stock)
            predictions.append((stock, pred))
        except Exception as e:
            print(f"Error in {stock}: ", e)
            predictions.append((stock, 0.02))
            

    # sort by predicted return
    predictions.sort(key=lambda x: x[1], reverse=True)

    return predictions    

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