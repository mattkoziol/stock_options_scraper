
Stock Options Arbitrage Analyzer
Overview
The Stock Options Arbitrage Analyzer is a Python program that identifies arbitrage opportunities in stock options. It fetches data from Yahoo Finance, analyzes it, and highlights potential arbitrage opportunities.

Features
  Data Scraping: Retrieves options data from Yahoo Finance.
  Data Parsing: Extracts relevant option information.
  Arbitrage Analysis: Finds arbitrage opportunities using the Black-Scholes model.
  User Input: Analyze multiple stock tickers and specify start dates.
  Yahoo Finance API Integration
  Stock Price Retrieval: Uses the Yahoo Finance API to get current stock prices.
  Options Data: Fetches options data using an API key set in the .env file.
  Installation
  Clone the Repository:


Copy code
git clone https://github.com/yourusername/stock-options-arbitrage-analyzer.git
cd stock-options-arbitrage-analyzer
Install Dependencies:

  python -m venv venv
  source venv/bin/activate  # On Windows use `venv\Scripts\activate`
  pip install -r requirements.txt
  Set Up Environment Variables:

Create a .env file with your Yahoo Finance API key:

  API_KEY=your_yahoo_finance_api_key

  
Usage
  Run the main script:



python main.py
Input stock tickers and a start date when prompted.

Modules
  arbitrage_analyzer.py: Analyzes options data for arbitrage.
  data_parser.py: Parses options data from HTML tables.
  utils.py: Fetches stock prices from Yahoo Finance.
  data_scraper.py: Scrapes options data and generates expiry dates.
  main.py: Main entry point for user interaction and data processing.
  
Requirements
  Python 3.7+
  numpy, pandas, requests, yfinance, python-dotenv
  
Install with:

  pip install numpy pandas requests yfinance python-dotenv
  Contributing
  Fork the Repository.
  Create a Feature Branch.
  Commit Changes.
  Push and Create a Pull Request.
