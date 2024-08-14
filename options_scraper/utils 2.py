import os
import requests
from dotenv import load_dotenv  # type: ignore

load_dotenv()

API_KEY = os.getenv('API_KEY')  # Load your API key from the environment

def get_stock_price(ticker):
    headers = {
        'Authorization': f'Bearer {API_KEY}'  # Use API key in the header
    }
    params = {
        'ticker': ticker
    }

    try:
        response = requests.get("YOUR_STOCK_PRICE_API_ENDPOINT_HERE", headers=headers, params=params)  # Replace with actual endpoint
        response.raise_for_status()  # Raise an HTTPError for bad responses
    except requests.RequestException as e:
        print(f"Failed to fetch stock price: {e}")
        return None

    data = response.json()
    return data.get('price')  # Adjust based on your API's response structure
