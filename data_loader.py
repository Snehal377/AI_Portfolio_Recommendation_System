import yfinance as yf
import pandas as pd
import datetime
import time


def load_market_data():

    stocks = [
        "TCS.NS",
        "INFY.NS",
        "RELIANCE.NS",
        "HDFCBANK.NS",
        "ICICIBANK.NS"
    ]

    etfs = [
        "NIFTYBEES.NS",
        "GOLDBEES.NS"
    ]

    reits = [
        "MINDSPACE.NS",
        "EMBASSY.NS"
    ]

    international = [
        "SPY",
        "QQQ"
    ]

    bonds = [
        "TLT",
        "IEF"
    ]
    safe_assets = {
        "PPF": 0.071,
        "EPF": 0.081,
        "GSEC": 0.065
    }

    all_assets = stocks + etfs + reits + international + bonds 

    end = datetime.datetime.today()
    start = end - datetime.timedelta(days=365)

    for attempt in range(3):

        try:

            data = yf.download(all_assets, start=start, end=end)["Close"]

            #  Flatten multi index columns
            data.columns = ['_'.join(col).strip() for col in data.columns.values]

            #  Keep only Close prices
            close_cols = [col for col in data.columns if col.startswith("Close")]
            data = data[close_cols]

            returns = data.pct_change().dropna()

            annual_returns = returns.mean() * 252

            for asset, rate in safe_assets.items():
                annual_returns[asset] = rate

            cov_matrix = returns.cov() * 252
            
            
            return data, returns, annual_returns, cov_matrix, all_assets

        except Exception as e:

            print("Data fetch failed. Retrying...", e)

            time.sleep(3)

    raise Exception("Market data could not be loaded.")