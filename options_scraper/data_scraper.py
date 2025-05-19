import os
import requests
import time
from datetime import timedelta
from dotenv import load_dotenv  # type: ignore
import yfinance as yf
import pandas as pd

load_dotenv()

def get_options_data(ticker, expiry_date):
    try:
        stock = yf.Ticker(ticker)
        opt_chain = stock.option_chain(expiry_date.strftime('%Y-%m-%d'))
        calls = opt_chain.calls.copy()
        puts = opt_chain.puts.copy()
        calls['type'] = 'call'
        puts['type'] = 'put'
        calls['expiry_date'] = expiry_date
        puts['expiry_date'] = expiry_date
        return calls.to_dict('records'), puts.to_dict('records')
    except Exception as e:
        print(f"Failed to fetch options data: {e}")
        return [], []

def scrape_options_for_month(ticker, start_date=None):
    all_data = []
    stock = yf.Ticker(ticker)
    try:
        expiry_dates = [pd.to_datetime(date).date() for date in stock.options]
    except Exception as e:
        print(f"Failed to fetch available expiry dates for {ticker}: {e}")
        return []

    for expiry_date in expiry_dates:
        print(f"Scraping data for {ticker} with expiry date {expiry_date}...")
        options_data = get_options_data(ticker, expiry_date)
        if options_data:
            calls_data, puts_data = options_data
            for call in calls_data:
                call['type'] = 'call'
                call['expiry_date'] = expiry_date
                all_data.append(call)
            for put in puts_data:
                put['type'] = 'put'
                put['expiry_date'] = expiry_date
                all_data.append(put)
        time.sleep(1)  # Add delay to avoid rate limiting
    return all_data
