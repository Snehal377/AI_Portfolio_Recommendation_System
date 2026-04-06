import pandas as pd
import numpy as np

print("Loading financial metrics...")

# Load expected returns
returns = pd.read_csv("expected_returns.csv", index_col=0)

# Load covariance matrix
cov_matrix = pd.read_csv("covariance_matrix.csv", index_col=0)

returns = returns.squeeze()

num_assets = len(returns)
num_portfolios = 10000

results = []

print("Running Monte Carlo Simulation...")

for i in range(num_portfolios):

    # Generate random weights
    weights = np.random.random(num_assets)
    weights /= np.sum(weights)

    # Portfolio return
    portfolio_return = np.dot(weights, returns)

    # Portfolio risk
    portfolio_risk = np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights)))

    # Sharpe Ratio
    sharpe_ratio = portfolio_return / portfolio_risk

    results.append([
        portfolio_return,
        portfolio_risk,
        sharpe_ratio,
        weights.tolist()
    ])

portfolio_results = pd.DataFrame(results, columns=[
    "Return",
    "Risk",
    "Sharpe",
    "Weights"
])

# Best portfolio
best_portfolio = portfolio_results.loc[portfolio_results["Sharpe"].idxmax()]

print("\nBest Portfolio Found")

print("\nExpected Return:", best_portfolio["Return"])
print("Risk:", best_portfolio["Risk"])
print("Sharpe Ratio:", best_portfolio["Sharpe"])

print("\nOptimal Weights:")

assets = returns.index.tolist()

for asset, weight in zip(assets, best_portfolio["Weights"]):
    print(asset, ":", round(weight * 100, 2), "%")

portfolio_results.to_csv("monte_carlo_portfolios.csv")

print("\nSimulation completed.")