import os
import requests
import time
from datetime import timedelta, datetime
from dotenv import load_dotenv  # type: ignore

load_dotenv()

API_KEY = os.getenv('API_KEY')  # Load your API key from the environment

def get_options_data(ticker, expiry_date):
    headers = {
        'Authorization': f'Bearer {API_KEY}'  # Use API key in the header
    }
    params = {
        'ticker': ticker,
        'expiry_date': expiry_date.strftime('%Y-%m-%d')  # Convert date to string format
    }

    print(f"Fetching data for {ticker} with expiry date {expiry_date}...")

    try:
        response = requests.get("YOUR_API_ENDPOINT_HERE", headers=headers, params=params)  # Replace with actual endpoint
        response.raise_for_status()  # Raise an HTTPError for bad responses
    except requests.RequestException as e:
        print(f"Request failed: {e}")
        return None

    data = response.json()  # Parse the JSON response
    calls_data = data.get('calls', [])  # Extract calls data
    puts_data = data.get('puts', [])    # Extract puts data

    return calls_data, puts_data

def scrape_options_for_month(ticker, start_date):
    all_data = []
    expiry_dates = generate_expiry_dates(start_date)

    for expiry_date in expiry_dates:
        print(f"Scraping data for {ticker} with expiry date {expiry_date}...")

        options_data = get_options_data(ticker, expiry_date)  # Pass expiry_date as datetime.date
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

        time.sleep(1)  # Avoid hitting the API rate limit

    return all_data

def generate_expiry_dates(start_date):
    expiry_dates = []
    for i in range(30):
        current_date = start_date + timedelta(days=i)
        if current_date.weekday() == 4:  # Check for Friday
            expiry_dates.append(current_date)
    return expiry_dates
