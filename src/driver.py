import os
import requests
from datetime import datetime
from dotenv import load_dotenv
from typing import Any

STOCK = "TSLA"
COMPANY_NAME = "Tesla"

load_dotenv()

STOCK_API_KEY = os.getenv("STOCK_API_KEY")
STOCK_ENDPOINT="https://www.alphavantage.co/query"

def get_stock() -> tuple[str, str, float]:
    stock_symbol = input("Enter the Stock name (ex. TSLA): ")
    company_name = input("Enter the company name (ex. Tesla): ")
    percent_change = input("What percent change would you like to get notified at (default. 5%): ")
    
    
    return stock_symbol, company_name, float(percent_change)

def check_price_change(yesterdays_price: float, todays_price: float) -> float:
    return ((todays_price - yesterdays_price) / yesterdays_price) * 100
    

def main() -> None:
    # When STOCK price increase/decreases by 5% between yesterday and the day before yesterday then get news.
    stock_symbol, company_name , percent_change = STOCK, COMPANY_NAME, 5   #get_info()
    stock_params = {
        'function': 'TIME_SERIES_DAILY',
        'symbol':  stock_symbol,
        'apikey': STOCK_API_KEY,
    }
  
    response = requests.get(STOCK_ENDPOINT ,params=stock_params)
    response.raise_for_status()
    data = response.json()
    time_series_data = data['Time Series (Daily)']

    todays_date = datetime.now().strftime('%Y-%m-%d')
    yesterdays_date = '2025-05-30'
    
    todays_close_price = round(float(time_series_data[todays_date]['4. close']), 2)
    yesterdays_close_price = round(float(time_series_data[yesterdays_date]['4. close']), 2)
    price_change = check_price_change(yesterdays_close_price, todays_close_price)
    
    # Checking the price threshold
    if price_change > percent_change or price_change < -percent_change:
        # Get the first 3 news pieces for the COMPANY_NAME. 
        print("Get news.")
        
        # Send a seperate message with the percentage change and each article's title and description to your phone number. 
    
    
if __name__ == "__main__":
    main()
    