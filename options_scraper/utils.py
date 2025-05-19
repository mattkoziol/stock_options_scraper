import os
import requests
from dotenv import load_dotenv  # type: ignore
import yfinance as yf
import numpy as np

load_dotenv()

API_KEY = os.getenv('API_KEY')  # Load your API key from the environment

def get_stock_price(ticker):
    try:
        stock = yf.Ticker(ticker)
        price = stock.history(period="1d")['Close'].iloc[-1]
        return price
    except Exception as e:
        print(f"Failed to fetch stock price: {e}")
        return None

# Black-Scholes formula for European options
def black_scholes_price(S, K, T, r, sigma, option_type='call'):
    """
    S: current stock price
    K: strike price
    T: time to expiration in years
    r: risk-free interest rate
    sigma: volatility (annualized std dev of log returns)
    option_type: 'call' or 'put'
    """
    from scipy.stats import norm
    d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    if option_type == 'call':
        price = S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
    else:
        price = K * np.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)
    return price
