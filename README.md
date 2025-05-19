# Stock Options Arbitrage Analyzer

## Description
The Stock Options Arbitrage Analyzer is a Python program that identifies arbitrage opportunities in stock options. It fetches real-time options data from Polygon.io, analyzes it for potential arbitrage opportunities, and provides detailed analysis of put-call parity violations, box spreads, and butterfly spreads.

## Features

- **Real-time Data**: Retrieves options data from Polygon.io API
- **Multiple Analysis Types**:
  - Put-Call Parity Violations
  - Box Spread Opportunities
  - Butterfly Spread Opportunities
- **User Input**: Analyze multiple stock tickers in one run
- **Rate Limiting**: Built-in protection against API rate limits
- **Error Handling**: Robust error handling and retry mechanisms
- **Progress Tracking**: Shows progress during data collection


## Prerequisites
- Python 3.8 or higher
- A Polygon.io API key with options data access (requires paid subscription)
- Required Python packages (see requirements.txt)

## User Manual

### Setup & Execution
1. **Navigate to the Project Directory:**
   ```bash
   cd options_scraper
   ```

2. **Create the Virtual Environment:**
   ```bash
   python -m venv venv
   ```

3. **Activate the Virtual Environment:**
   ```bash
   source venv/bin/activate   # For Unix/Linux
   ```
   ```bash
   venv\Scripts\activate      # For Windows
   ```

4. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

5. **Set up your API Key:**
   - Sign up for a Polygon.io account at https://polygon.io/
   - Subscribe to a plan that includes options data access
   - Create a `.env` file in the project directory
   - Add your API key: `POLYGON_API_KEY=your_api_key_here`

6. **Run the Program:**
   ```bash
   python main.py
   ```
   Enter stock tickers when prompted (comma-separated).

## API Key Requirements
This project requires a paid Polygon.io subscription that includes options data access. The free tier will not work as it doesn't provide options price data. Required features:
- Options contracts data
- Options quotes data
- Real-time or delayed market data

## Modules

- **arbitrage_analyzer.py**: Analyzes options data for arbitrage opportunities
- **main.py**: Main entry point for user interaction and data processing


## Libraries & Resources
### Main Libraries:
- **requests**: For making API calls to Polygon.io
- **python-dotenv**: For managing API key
- **json**: For parsing API responses
- **datetime**: For handling dates and times

### External Resources:
- **Polygon.io API**: For retrieving real-time options data
  - Documentation: https://polygon.io/docs/options
  - API Reference: https://polygon.io/docs/options/getting-started

## Note
This project is for educational purposes only. Options trading involves significant risks and requires proper understanding of the market. Always consult with financial advisors before making any investment decisions.

## Contributing
Feel free to submit issues and enhancement requests!
