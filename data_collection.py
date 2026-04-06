import yfinance as yf
import pandas as pd
import datetime
import requests
from io import StringIO
import warnings
warnings.filterwarnings("ignore")

# Define Assets

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

all_assets = stocks + etfs

# Date Range

end_date = datetime.datetime.today()
start_date = end_date - datetime.timedelta(days=365)

# Download Stock / ETF Data

print("Downloading stock data...")

data = yf.download(
    all_assets,
    start=start_date,
    end=end_date
)

# Extract closing prices
stock_data = data["Close"]

print(stock_data.head())

# Save Stock Data

stock_data.to_csv("live_stock_data.csv")

# Download Gold Data

print("Downloading gold data...")

gold_data = yf.download(
    "GOLDBEES.NS",
    start=start_date,
    end=end_date
)

gold_data = gold_data["Close"]

gold_data.to_csv("live_gold_data.csv")

# Download Mutual Fund NAV

print("Downloading mutual fund NAV data...")

url = "https://www.amfiindia.com/spages/NAVAll.txt"

response = requests.get(url, verify=False)

data = response.text.split("\n")

clean_rows = []

for row in data:
    parts = row.split(";")

    if len(parts) == 6:
        clean_rows.append(parts)

mf_data = pd.DataFrame(clean_rows, columns=[
    "Scheme Code",
    "Scheme Name",
    "ISIN Div Payout",
    "ISIN Div Reinvestment",
    "NAV",
    "Date"
])

mf_data.to_csv("live_mutual_funds.csv", index=False)

print("Mutual fund data downloaded successfully.")