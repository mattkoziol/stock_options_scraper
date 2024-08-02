import yfinance as yf
def get_stock_price(ticker):
    try:
        stock = yf.Ticker(ticker)
        stock_info = stock.info
        price = stock_info.get('currentPrice', None)
        if price is None:
            print(f"Price not available for {ticker}")
            return None
        return price
    except Exception as e:
        print(f"Error fetching price for {ticker}: {e}")
        return None

