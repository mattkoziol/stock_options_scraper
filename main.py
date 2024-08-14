import os
from datetime import datetime
from options_scraper.data_scraper import scrape_options_for_month
from options_scraper.arbitrage_analyzer import analyze_arbitrage
from dotenv import load_dotenv  # type: ignore

# Load environment variables
load_dotenv()

def main():
    # Get user input for stock ticker and start date
    tickers = input("Enter the tickers of the stocks you would like to analyze, separated by commas: ").split(',')
    start_date_str = input("Enter the start date (YYYY-MM-DD): ")
    start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()

    for ticker in tickers:
        ticker = ticker.strip().upper()  # Clean up ticker symbol
        print(f"Processing {ticker}...")

        # Scrape options data for the specified month
        options_data = scrape_options_for_month(ticker, start_date)

        # Analyze for arbitrage opportunities
        if options_data:
            analyze_arbitrage(options_data, ticker)
        else:
            print(f"No options data available for {ticker}.")

if __name__ == "__main__":
    main()
