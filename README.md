# Stock Options Arbitrage Analyzer

## Description
The Stock Options Arbitrage Analyzer is a Python program that identifies arbitrage opportunities in stock options. It fetches data from Yahoo Finance, analyzes it, and highlights potential arbitrage opportunities.

## Features
- **Data Scraping**: Retrieves options data from Yahoo Finance.
- **Data Parsing**: Extracts relevant option information.
- **Arbitrage Analysis**: Finds arbitrage opportunities using the Black-Scholes model.
- **User Input**: Analyze multiple stock tickers and specify start dates.
- **Yahoo Finance API Integration**
- **Stock Price Retrieval**: Uses the Yahoo Finance API to get current stock prices.
- **Options Data**: Fetches options data using an API key set in the .env file.
 
 ## User Manual

 ### Setup & Execution
  1. **Navigate to the Project Directory:**
   ```bash
   cd stock-options-arbitrage-analyzer
```
  2. **Create the Vitual Environment:**
```bash
python -m venv venv
 ```
  **Activate the Virtual Environment:**
```bash
source venv/bin/activate   # For Unix/Linux
```
     
```bash
venv\Scripts\activate      # For Windows
```
3. **Install Dependencies:**
```bash
pip install -r requirements.txt
```
4. **Set Up Environment Variables:**

   Create a .env file in the project directory.

   Add you Yahoo Finance API Key to the file:
```bash
API_KEY=your_yahoo_finance_api_key
  ```
  
5. **Run the Program:**
```bash
python main.py
```

  Input stock tickers and a start date when prompted.

## Modules
- **arbitrage_analyzer.py**: Analyzes options data for arbitrage.
- **data_parser.py**: Parses options data from HTML tables.
- **utils.py**: Fetches stock prices from Yahoo Finance.
- **data_scraper.py**: Scrapes options data and generates expiry dates.
- **main.py**: Main entry point for user interaction and data processing.
  
## Libraries & Resources
### Main Libraries:

- **numpy**: Used for numerical calculations.
- **pandas**: For data manipulation and analysis.
- **requests**: To handle HTTP requests for web scraping.
- **yfinance**: To fetch stock price data from Yahoo Finance.

### External Resources:

-**Yahoo Finance API**: For retrieving real-time stock and options data.
