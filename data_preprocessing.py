import pandas as pd
import numpy as np

print("Loading collected data...")

# Load stock data
stock_data = pd.read_csv("live_stock_data.csv", index_col="Date", parse_dates=True)

# Load gold data
gold_data = pd.read_csv("live_gold_data.csv", index_col="Date", parse_dates=True)

# Rename gold column
gold_data.columns = ["Gold"]

# Combine stocks and gold
data = pd.concat([stock_data, gold_data], axis=1)

print("\nCombined Asset Data:")
print(data.head())

# Remove missing values
data = data.dropna()

print("\nCalculating Daily Returns...")

# Daily returns
returns = data.pct_change().dropna()

print(returns.head())

# Expected annual return
annual_returns = returns.mean() * 252

# Risk (volatility)
annual_volatility = returns.std() * np.sqrt(252)

# Covariance matrix
cov_matrix = returns.cov() * 252

print("\nExpected Annual Returns:")
print(annual_returns)

print("\nAnnual Risk (Volatility):")
print(annual_volatility)

print("\nCovariance Matrix:")
print(cov_matrix)

# Save outputs
returns.to_csv("asset_daily_returns.csv")
annual_returns.to_csv("expected_returns.csv")
annual_volatility.to_csv("asset_risk.csv")
cov_matrix.to_csv("covariance_matrix.csv")

print("\nFeature Engineering Completed.")
print("Files saved successfully.")