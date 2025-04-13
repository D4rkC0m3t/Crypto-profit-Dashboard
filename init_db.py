import sys
from data_fetcher import fetch_real_time_data, fetch_crypto_news, fetch_current_prices
from database import create_tables, init_db_with_exchange_data, store_crypto_prices, store_news_items

def main():
    """Initialize the database with exchange data, crypto prices, and news."""
    print("Creating database tables...")
    create_tables()
    
    print("Fetching real-time exchange data...")
    exchange_data = fetch_real_time_data()
    
    print("Initializing database with exchange data...")
    init_db_with_exchange_data(exchange_data)
    
    print("Fetching and storing cryptocurrency prices...")
    crypto_prices = fetch_current_prices()
    store_crypto_prices(crypto_prices)
    
    print("Fetching and storing news items...")
    news_data = fetch_crypto_news()
    store_news_items(news_data)
    
    print("Database initialization complete!")

if __name__ == "__main__":
    main()