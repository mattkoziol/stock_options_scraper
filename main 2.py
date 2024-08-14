import os

print("Current directory:", os.getcwd())
from options_scraper.data_scraper import scrape_options_for_month
from options_scraper.arbitrage_analyzer import analyze_arbitrage
from datetime import datetime, date

def main():
    tickers_input = input("Enter the tickers of the stocks you would like to analyze, separated by commas: ")
    
    # Process the input to create a list of tickers
    tickers = [ticker.strip() for ticker in tickers_input.split(',')]
    
    # Prompt the user for the start date
    start_date_input = input("Enter the start date (YYYY-MM-DD): ")
    start_date = datetime.strptime(start_date_input, '%Y-%m-%d').date()
    

    for ticker in tickers:
        print(f"Processing {ticker}...")
        options_data = scrape_options_for_month(ticker, start_date)
        if options_data:
            analyze_arbitrage(options_data, ticker)

if __name__ == "__main__":
    main()
