import pandas as pd

# Indian tax constants
LTCG_RATE = 0.10
STCG_RATE = 0.15
LTCG_EXEMPTION = 100000

SEC_80C_LIMIT = 150000
SEC_80D_LIMIT = 25000


def calculate_post_tax_return(allocation, annual_returns, investment=100000, holding_period="long"):

    portfolio_return = 0

    for i, row in allocation.iterrows():

        asset = row["Asset"]
        weight = row["Weight"]

        if asset in annual_returns:

            portfolio_return += weight * annual_returns[asset]

    # expected profit
    profit = portfolio_return * investment

    if holding_period == "long":

        taxable_gain = max(0, profit - LTCG_EXEMPTION)

        tax = taxable_gain * LTCG_RATE

    else:

        tax = profit * STCG_RATE

    post_tax_profit = profit - tax

    post_tax_return = post_tax_profit / investment

    return post_tax_return

def simulate_tax_savings(income, invest_80c=0, health_insurance=0):

    deduction_80c = min(invest_80c, SEC_80C_LIMIT)

    deduction_80d = min(health_insurance, SEC_80D_LIMIT)

    total_deduction = deduction_80c + deduction_80d

    taxable_income = income - total_deduction

    return {
        "taxable_income": taxable_income,
        "total_deduction": total_deduction
    }        