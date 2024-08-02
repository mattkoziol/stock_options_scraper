import numpy as np
import pandas as pd
from datetime import date
from .utils import get_stock_price

RISK_FREE_RATE = 0.05  # Annual risk-free interest rate

def analyze_arbitrage(data, ticker):
    current_stock_price = get_stock_price(ticker)

    df = pd.DataFrame(data)
    call_data = df[df['type'] == 'call']
    put_data = df[df['type'] == 'put']

    merged_data = pd.merge(call_data, put_data, on=['strike', 'expiry_date'], suffixes=('_call', '_put'))

    arbitrage_opportunities = []

    for _, row in merged_data.iterrows():
        C = row['last_price_call']
        P = row['last_price_put']
        S = current_stock_price
        X = row['strike']
        T = (row['expiry_date'] - date.today()).days / 365.0

        theoretical_call = P + S - X * np.exp(-RISK_FREE_RATE * T)

        if C > theoretical_call:
            arbitrage_opportunities.append({
                'strike': X,
                'expiry_date': row['expiry_date'],
                'market_call_price': C,
                'theoretical_call_price': theoretical_call,
                'arbitrage_amount': C - theoretical_call
            })

    if arbitrage_opportunities:
        arbitrage_df = pd.DataFrame(arbitrage_opportunities)
        print(f"Arbitrage opportunities for {ticker}:")
        print(arbitrage_df)
    else:
        print(f"No arbitrage opportunities found for {ticker}.")
