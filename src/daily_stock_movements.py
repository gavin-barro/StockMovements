import os
import requests
from datetime import datetime, timedelta
from dotenv import load_dotenv

STOCK = "TSLA"
COMPANY_NAME = "Tesla"

load_dotenv()

STOCK_API_KEY = os.getenv("STOCK_API_KEY")
STOCK_ENDPOINT="https://www.alphavantage.co/query"

NEWS_API_KEY = os.getenv("NEWS_API_KEY")
NEWS_ENDPOINT="https://newsapi.org/v2/everything"

def get_stock() -> tuple[str, str, float]:
    # Default values
    DEFAULT_STOCK = "TSLA"
    DEFAULT_COMPANY_NAME = "Tesla"
    DEFAULT_PERCENT = 5.0

    # Get stock symbol
    stock_symbol = input("Enter the Stock name (ex. TSLA): ").strip().upper()
    if not stock_symbol or not stock_symbol.isalnum():
        print(f"Invalid stock symbol. Using default: {DEFAULT_STOCK}")
        stock_symbol = DEFAULT_STOCK

    # Get company name
    company_name = input("Enter the company name (ex. Tesla): ").strip()
    if not company_name:
        print(f"Invalid company name. Using default: {DEFAULT_COMPANY_NAME}")
        company_name = DEFAULT_COMPANY_NAME

    # Get percent change
    percent_change_input = input("What percent change would you like to get notified at (default 5%): ").strip()
    try:
        percent_change = float(percent_change_input)
        if percent_change <= 0:
            print(f"Percent change must be positive. Using default: {DEFAULT_PERCENT}%")
            percent_change = DEFAULT_PERCENT
    except ValueError:
        print(f"Invalid percent change. Using default: {DEFAULT_PERCENT}%")
        percent_change = DEFAULT_PERCENT

    return stock_symbol, company_name, percent_change

def get_valid_dates() -> tuple[str, str]:
    # Get today's date
    today = datetime.now().date()
    
    # Check if today is a weekday (Monday=0, Friday=4)
    if today.weekday() >= 5:  # Saturday (5) or Sunday (6)
        # Adjust to previous Friday
        days_to_subtract = today.weekday() - 4  # 5 -> 1, 6 -> 2
        today = today - timedelta(days=days_to_subtract)
    
    # Get yesterday (previous weekday)
    if today.weekday() == 0:  # Today is Monday
        yesterday = today - timedelta(days=3)  # Previous Friday
    else:
        yesterday = today - timedelta(days=1)  # Previous weekday
    
    # Format dates as YYYY-MM-DD
    todays_date = today.strftime('%Y-%m-%d')
    yesterdays_date = yesterday.strftime('%Y-%m-%d')
    
    return todays_date, yesterdays_date

def check_price_change(yesterdays_price: float, todays_price: float) -> float:
    return ((todays_price - yesterdays_price) / yesterdays_price) * 100

def get_news(stock_name: str, today_date: str) -> list[str]:
    three_days_from_today = '2025-05-28'
    
    news_params = {
        'q': stock_name,
        'searchIn': 'title',
        'apiKey': NEWS_API_KEY,
        'from': three_days_from_today,
        'to': today_date
    }
    response = requests.get(NEWS_ENDPOINT, params=news_params)
    response.raise_for_status()
    news_data = response.json()

    article1 = news_data["articles"][0]
    # Key info
    # print(f"Name : {name}")
    
    return ["", "", ""]
    

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
    print(data)
    time_series_data = data['Time Series (Daily)']

    todays_date, yesterdays_date = get_valid_dates()
    todays_date = datetime.now().strftime('%Y-%m-%d')
    yesterdays_date = '2025-05-30'
    
    todays_close_price = round(float(time_series_data[todays_date]['4. close']), 2)
    yesterdays_close_price = round(float(time_series_data[yesterdays_date]['4. close']), 2)
    price_change = check_price_change(yesterdays_close_price, todays_close_price)
    
    # Checking the price threshold
    # if price_change > percent_change or price_change < -percent_change:
        # Get the first 3 news pieces for the COMPANY_NAME. 
    get_news(stock_symbol, todays_date)
        
        # Send a seperate message with the percentage change and each article's title and description to your phone number. 
    
    
if __name__ == "__main__":
    main()
    