import os
from datetime import datetime, timedelta
import requests
import time
import json
from arbitrage_analyzer import analyze_arbitrage
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

POLYGON_API_KEY = os.getenv("POLYGON_API_KEY")
BASE_URL = "https://api.polygon.io"

# Rate limiting constants
MAX_RETRIES = 5
INITIAL_DELAY = 1  # seconds
MAX_DELAY = 32  # seconds
RATE_LIMIT_DELAY = 12  # seconds between requests

def make_request(url, retry_count=0):
    """Make a request with exponential backoff and rate limiting"""
    try:
        # Add delay between requests to respect rate limits
        time.sleep(RATE_LIMIT_DELAY)
        
        response = requests.get(url)
        
        if response.status_code == 429:  # Too Many Requests
            if retry_count < MAX_RETRIES:
                delay = min(INITIAL_DELAY * (2 ** retry_count), MAX_DELAY)
                print(f"Rate limit hit. Waiting {delay} seconds before retry...")
                time.sleep(delay)
                return make_request(url, retry_count + 1)
            else:
                print("Max retries reached. Please try again later.")
                return None
        elif response.status_code == 404:  # Not Found
            # Don't retry 404 errors, just return None
            return None
                
        response.raise_for_status()
        
        # Validate JSON response
        try:
            data = response.json()
            if not isinstance(data, dict):
                print(f"Invalid response format: expected JSON object, got {type(data)}")
                return None
            return data
        except json.JSONDecodeError as e:
            print(f"Invalid JSON response: {e}")
            return None
            
    except requests.exceptions.RequestException as e:
        if retry_count < MAX_RETRIES:
            delay = min(INITIAL_DELAY * (2 ** retry_count), MAX_DELAY)
            print(f"Request error: {e}")
            print(f"Retrying in {delay} seconds...")
            time.sleep(delay)
            return make_request(url, retry_count + 1)
        return None

def get_stock_price(ticker):
    """Get current stock price from Polygon.io"""
    url = f"{BASE_URL}/v2/aggs/ticker/{ticker}/prev?adjusted=true&apiKey={POLYGON_API_KEY}"
    data = make_request(url)
    
    if not data:
        print(f"Failed to get price data for {ticker}")
        return None
        
    if not data.get('results'):
        print(f"No price data found for {ticker}")
        return None
        
    try:
        return float(data['results'][0]['c'])  # 'c' is the closing price
    except (KeyError, IndexError, ValueError) as e:
        print(f"Error parsing price data: {e}")
        return None

def get_options_chain(ticker):
    """Get options chain from Polygon.io"""
    url = f"{BASE_URL}/v3/reference/options/contracts?underlying_ticker={ticker}&limit=1000&apiKey={POLYGON_API_KEY}"
    data = make_request(url)
    
    if not data:
        print(f"Failed to get options chain for {ticker}")
        return []
        
    if not data.get('results'):
        print(f"No options data found for {ticker}")
        return []
        
    # Group options by expiry date
    expiry_dates = set()
    for contract in data['results']:
        try:
            expiry_dates.add(contract['expiration_date'])
        except KeyError:
            print(f"Warning: Invalid contract data format: {contract}")
            continue
            
    if not expiry_dates:
        print(f"No valid expiry dates found for {ticker}")
        return []
        
    print(f"\nAvailable expiry dates for {ticker}:")
    for date in sorted(expiry_dates):
        print(f"- {date}")
        
    return data['results']

def get_options_data(ticker, expiry_date):
    """Get detailed options data for a specific expiry date"""
    # Get the contract information with last trade data
    url = f"{BASE_URL}/v3/reference/options/contracts?underlying_ticker={ticker}&expiration_date={expiry_date}&limit=1000&apiKey={POLYGON_API_KEY}"
    print(f"Fetching options data for {expiry_date}...")
    contracts_data = make_request(url)
    
    if not contracts_data or not contracts_data.get('results'):
        print(f"No options contracts found for {expiry_date}")
        return [], []
    
    calls = []
    puts = []
    total_contracts = len(contracts_data['results'])
    
    # Debug: Print first contract to check data structure
    if total_contracts > 0:
        print("\nSample contract data:")
        print(json.dumps(contracts_data['results'][0], indent=2))
    
    # Process each contract
    for i, contract in enumerate(contracts_data['results'], 1):
        try:
            # Show progress
            if i % 10 == 0 or i == total_contracts:
                print(f"Processing contract {i}/{total_contracts}...")
            
            # Get the last price from the contract data
            last_price = float(contract.get('last_trade_price', 0))
            
            # Debug: Print non-zero prices
            if last_price > 0:
                print(f"Found non-zero price: {contract['contract_type']} {contract['strike_price']} @ ${last_price}")
            
            option_data = {
                'strike': float(contract['strike_price']),
                'expiry_date': contract['expiration_date'],
                'type': 'call' if contract['contract_type'] == 'call' else 'put',
                'lastPrice': last_price,
                'impliedVolatility': float(contract.get('implied_volatility', 0.2))
            }
            
            if contract['contract_type'] == 'call':
                calls.append(option_data)
            else:
                puts.append(option_data)
                
        except (KeyError, ValueError) as e:
            print(f"Warning: Invalid contract data format: {e}")
            continue
        except Exception as e:
            print(f"Warning: Error processing contract: {e}")
            continue
            
    print(f"\nFound {len(calls)} calls and {len(puts)} puts for {expiry_date}")
    print(f"Number of options with non-zero prices: {sum(1 for opt in calls + puts if opt['lastPrice'] > 0)}")
    return calls, puts

def main():
    print("Note: This program requires a valid Polygon.io API key with options data access.")
    print("If you see 403 errors, please verify your API key is valid and has the correct permissions.")
    print("\nYou can get a free API key at: https://polygon.io/")
    print("Make sure to enable options data access in your subscription.")
    print("\nNote: The program will respect API rate limits and may take some time to complete.")
    print("Please be patient as it processes the data...\n")
    
    # Get user input for stock ticker
    tickers = input("Enter the tickers of the stocks you would like to analyze, separated by commas: ").split(',')

    for ticker in tickers:
        ticker = ticker.strip().upper()  # Clean up ticker symbol
        print(f"\nProcessing {ticker}...")
        
        try:
            # Get current stock price
            current_price = get_stock_price(ticker)
            if current_price is None:
                print(f"Could not get current price for {ticker}. Skipping...")
                continue
                
            print(f"Current price for {ticker}: ${current_price:.2f}")
            
            # Get available expiry dates
            options_chain = get_options_chain(ticker)
            if not options_chain:
                print(f"No options data available for {ticker}.")
                continue
                
            # Get options data for each expiry date
            all_options_data = []
            processed_dates = set()  # Track processed dates to avoid duplicates
            
            for contract in options_chain:
                expiry_date = contract['expiration_date']
                if expiry_date in processed_dates:
                    continue
                    
                print(f"\nProcessing expiry date {expiry_date}...")
                processed_dates.add(expiry_date)
                
                calls, puts = get_options_data(ticker, expiry_date)
                if calls or puts:  # Only extend if we got valid data
                    all_options_data.extend(calls)
                    all_options_data.extend(puts)
            
            # Analyze for arbitrage opportunities
            if all_options_data:
                print(f"\nAnalyzing {len(all_options_data)} options for arbitrage opportunities...")
                print(f"Using current price of ${current_price:.2f} for analysis")
                analyze_arbitrage(all_options_data, ticker, current_price)
            else:
                print(f"No valid options data available for {ticker}.")
                
        except KeyboardInterrupt:
            print("\nOperation cancelled by user.")
            break
        except Exception as e:
            print(f"Error processing {ticker}: {str(e)}")
            print("This might be due to:")
            print("1. Invalid ticker symbol")
            print("2. Network connectivity issues")
            print("3. API rate limiting")
            print("4. Invalid or expired API key")
            print("\nPlease try again in a few minutes.")
            continue

if __name__ == "__main__":
    main()
