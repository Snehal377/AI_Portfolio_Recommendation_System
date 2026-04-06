import pandas as pd
import yfinance as yf


def load_portfolio_data():
    return pd.read_csv("portfolio_data.csv")

def get_stock_data(ticker="NIFTYBEES.NS"):
    try:
        if "USD" in ticker:
            data =yf.download(ticker,period="2d",interval="1h",progress=False)
        else:
            data =yf.download(ticker,period="5d",interval="1h",progress=False)

        if data is None or data.empty:
            return None

        latest_price = data["Close"].iloc[-1]
        change = data["Close"].pct_change().iloc[-1]

        return {
            "price": round(latest_price, 2),
            "change": round(change * 100, 2)
        }

    except Exception as e:
        print("Market fetch error:", e)
        return None

def market_research(query):

    #  mapping
    if "crypto" in query.lower() or "bitcoin" in query.lower():
        ticker = "BTC-USD"
    elif "ethereum" in query.lower():
        ticker = "ETH-USD"
    elif "bank" in query.lower():
        ticker = "BANKBEES.NS"
    elif "it" in query.lower():
        ticker = "ITBEES.NS"
    elif "gold" in query.lower():
        ticker = "GOLDBEES.NS"
    else:
        ticker = "NIFTYBEES.NS"

    data = get_stock_data(ticker)

    if data is None:
        return "Market data unavailable"

    return f"""
Market Analysis for: {query}

Asset: {ticker}
Current Price: {data['price']}
Change: {data['change']}%

Insights:
- Positive change indicates bullish trend
- Negative change indicates bearish movement
"""



            