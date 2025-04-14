import os
import datetime as dt
import json
import pandas as pd
import numpy as np
from sqlalchemy import (
    create_engine,
    MetaData,
    Table,
    Column,
    Integer,
    String,
    Float,
    DateTime,
    Text,
    JSON,
    ForeignKey,
    select,
    func,
    insert,
    delete,
    update,
    desc
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

# Use SQLite database for local development
DATABASE_URL = 'sqlite:///crypto_exchange.db'

# Create database engine
engine = create_engine(DATABASE_URL)

# Create base class for declarative models
Base = declarative_base()

# Define database models
class Exchange(Base):
    """Model representing a cryptocurrency exchange"""
    __tablename__ = 'exchanges'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False, unique=True)
    scale_factor = Column(Float, nullable=False)
    created_at = Column(DateTime, default=dt.datetime.now)
    updated_at = Column(DateTime, default=dt.datetime.now, onupdate=dt.datetime.now)

    # Relationships
    monthly_data = relationship("MonthlyData", back_populates="exchange", cascade="all, delete-orphan")
    yearly_data = relationship("YearlyData", back_populates="exchange", cascade="all, delete-orphan")
    fee_structure = relationship("FeeStructure", back_populates="exchange", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Exchange(name='{self.name}')>"

class MonthlyData(Base):
    """Model for monthly exchange data"""
    __tablename__ = 'monthly_data'

    id = Column(Integer, primary_key=True)
    exchange_id = Column(Integer, ForeignKey('exchanges.id', ondelete='CASCADE'), nullable=False)
    month_date = Column(String(7), nullable=False)  # Format: YYYY-MM
    volume = Column(Float, nullable=False)
    commission = Column(Float, nullable=False)
    created_at = Column(DateTime, default=dt.datetime.now)
    updated_at = Column(DateTime, default=dt.datetime.now, onupdate=dt.datetime.now)

    # Relationship
    exchange = relationship("Exchange", back_populates="monthly_data")

    def __repr__(self):
        return f"<MonthlyData(exchange='{self.exchange.name}', date='{self.month_date}')>"

class YearlyData(Base):
    """Model for yearly exchange data"""
    __tablename__ = 'yearly_data'

    id = Column(Integer, primary_key=True)
    exchange_id = Column(Integer, ForeignKey('exchanges.id', ondelete='CASCADE'), nullable=False)
    year = Column(String(4), nullable=False)  # Format: YYYY
    volume = Column(Float, nullable=False)
    commission = Column(Float, nullable=False)
    created_at = Column(DateTime, default=dt.datetime.now)
    updated_at = Column(DateTime, default=dt.datetime.now, onupdate=dt.datetime.now)

    # Relationship
    exchange = relationship("Exchange", back_populates="yearly_data")

    def __repr__(self):
        return f"<YearlyData(exchange='{self.exchange.name}', year='{self.year}')>"

class FeeStructure(Base):
    """Model for exchange fee structures"""
    __tablename__ = 'fee_structures'

    id = Column(Integer, primary_key=True)
    exchange_id = Column(Integer, ForeignKey('exchanges.id', ondelete='CASCADE'), nullable=False)
    vip_tier = Column(String(50), nullable=False)
    maker_fee = Column(Float, nullable=False)
    taker_fee = Column(Float, nullable=False)
    created_at = Column(DateTime, default=dt.datetime.now)
    updated_at = Column(DateTime, default=dt.datetime.now, onupdate=dt.datetime.now)

    # Relationship
    exchange = relationship("Exchange", back_populates="fee_structure")

    def __repr__(self):
        return f"<FeeStructure(exchange='{self.exchange.name}', tier='{self.vip_tier}')>"

class CryptoPrice(Base):
    """Model for storing cryptocurrency prices"""
    __tablename__ = 'crypto_prices'

    id = Column(Integer, primary_key=True)
    crypto_id = Column(String(50), nullable=False)
    name = Column(String(100), nullable=False)
    symbol = Column(String(20), nullable=False)
    price_usd = Column(Float, nullable=False)
    change_24h = Column(Float, nullable=True)
    timestamp = Column(DateTime, default=dt.datetime.now, nullable=False)

    def __repr__(self):
        return f"<CryptoPrice(symbol='{self.symbol}', price='{self.price_usd}')>"

class NewsItem(Base):
    """Model for storing crypto news"""
    __tablename__ = 'news_items'

    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    url = Column(String(255), nullable=True)
    published_at = Column(String(50), nullable=True)
    timestamp = Column(DateTime, default=dt.datetime.now, nullable=False)

    def __repr__(self):
        return f"<NewsItem(title='{self.title[:30]}...')>"

# Create all tables in the database
def create_tables():
    Base.metadata.create_all(engine)

# Get a database session
def get_session():
    Session = sessionmaker(bind=engine)
    return Session()

# Initialize database with exchange data
def init_db_with_exchange_data(exchange_data):
    """
    Initializes the database with exchange data.
    """
    session = get_session()

    try:
        # First, check if we already have data
        existing_exchanges = session.query(Exchange).all()
        if existing_exchanges:
            print("Database already contains exchange data. Skipping initialization.")
            return

        # Add exchanges and their data
        for exchange_name, data in exchange_data.items():
            # Determine scale factor based on exchange size
            if exchange_name in ["Binance", "Coinbase"]:
                scale_factor = np.random.uniform(8, 12)  # Larger exchanges
            elif exchange_name in ["Bybit", "Kraken", "Upbit"]:
                scale_factor = np.random.uniform(4, 8)   # Medium exchanges
            else:
                scale_factor = np.random.uniform(1, 4)   # Smaller exchanges

            # Create exchange
            exchange = Exchange(name=exchange_name, scale_factor=scale_factor)
            session.add(exchange)
            session.flush()  # Get the exchange ID

            # Add monthly data
            for i, date in enumerate(data['monthly_dates']):
                # Convert numpy types to native Python types
                volume = float(data['monthly_volume'][i]) if hasattr(data['monthly_volume'][i], 'item') else data['monthly_volume'][i]
                commission = float(data['monthly_commission'][i]) if hasattr(data['monthly_commission'][i], 'item') else data['monthly_commission'][i]

                monthly = MonthlyData(
                    exchange_id=exchange.id,
                    month_date=date,
                    volume=volume,
                    commission=commission
                )
                session.add(monthly)

            # Add yearly data
            for i, year in enumerate(data['yearly_dates']):
                # Convert numpy types to native Python types
                volume = float(data['yearly_volume'][i]) if hasattr(data['yearly_volume'][i], 'item') else data['yearly_volume'][i]
                commission = float(data['yearly_commission'][i]) if hasattr(data['yearly_commission'][i], 'item') else data['yearly_commission'][i]

                yearly = YearlyData(
                    exchange_id=exchange.id,
                    year=year,
                    volume=volume,
                    commission=commission
                )
                session.add(yearly)

            # Add fee structure
            for i, tier in enumerate(data['vip_tiers']):
                # Convert numpy types to native Python types
                maker_fee = float(data['maker_fees'][i]) if hasattr(data['maker_fees'][i], 'item') else data['maker_fees'][i]
                taker_fee = float(data['taker_fees'][i]) if hasattr(data['taker_fees'][i], 'item') else data['taker_fees'][i]

                fee = FeeStructure(
                    exchange_id=exchange.id,
                    vip_tier=tier,
                    maker_fee=maker_fee,
                    taker_fee=taker_fee
                )
                session.add(fee)

        session.commit()
        print("Successfully initialized database with exchange data.")

    except Exception as e:
        session.rollback()
        print(f"Error initializing database: {str(e)}")

    finally:
        session.close()

# Store cryptocurrency prices in the database
def store_crypto_prices(crypto_prices):
    """
    Stores current cryptocurrency prices in the database.
    """
    session = get_session()

    try:
        # Clear old price data
        session.query(CryptoPrice).delete()

        # Define the list of cryptocurrencies we track
        crypto_list = [
            {"id": "bitcoin", "name": "Bitcoin", "symbol": "BTC"},
            {"id": "ethereum", "name": "Ethereum", "symbol": "ETH"},
            {"id": "ripple", "name": "XRP", "symbol": "XRP"},
            {"id": "cardano", "name": "Cardano", "symbol": "ADA"},
            {"id": "solana", "name": "Solana", "symbol": "SOL"},
            {"id": "polkadot", "name": "Polkadot", "symbol": "DOT"},
            {"id": "dogecoin", "name": "Dogecoin", "symbol": "DOGE"}
        ]

        for crypto in crypto_list:
            if crypto["id"] in crypto_prices:
                price_data = crypto_prices[crypto["id"]]
                # Convert numpy types to native Python types
                price_usd = float(price_data["usd"]) if hasattr(price_data["usd"], 'item') else price_data["usd"]
                change_24h = float(price_data.get("usd_24h_change", 0)) if hasattr(price_data.get("usd_24h_change", 0), 'item') else price_data.get("usd_24h_change", 0)

                price = CryptoPrice(
                    crypto_id=crypto["id"],
                    name=crypto["name"],
                    symbol=crypto["symbol"],
                    price_usd=price_usd,
                    change_24h=change_24h
                )
                session.add(price)

        session.commit()
        print("Successfully stored cryptocurrency prices.")

    except Exception as e:
        session.rollback()
        print(f"Error storing crypto prices: {str(e)}")

    finally:
        session.close()

# Store news items in the database
def store_news_items(news_data):
    """
    Stores cryptocurrency news items in the database.
    """
    session = get_session()

    try:
        # Clear old news data
        session.query(NewsItem).delete()

        # Add news items
        for news_item in news_data[:10]:  # Store top 10 news items
            item = NewsItem(
                title=news_item.get("title", "No title available"),
                description=news_item.get("description", "No description available"),
                url=news_item.get("url", "#"),
                published_at=news_item.get("published_at", "Unknown date")
            )
            session.add(item)

        session.commit()
        print("Successfully stored news items.")

    except Exception as e:
        session.rollback()
        print(f"Error storing news items: {str(e)}")

    finally:
        session.close()

# Retrieve all exchange data from the database
def get_all_exchange_data():
    """
    Retrieves all exchange data from the database in the same format as the original exchange_data dictionary.
    """
    session = get_session()
    result = {}

    try:
        # Get all exchanges
        exchanges = session.query(Exchange).all()

        for exchange in exchanges:
            # Get monthly data
            monthly_query = session.query(MonthlyData).filter_by(exchange_id=exchange.id).order_by(MonthlyData.month_date)
            monthly_data = monthly_query.all()

            # Get yearly data
            yearly_query = session.query(YearlyData).filter_by(exchange_id=exchange.id).order_by(YearlyData.year)
            yearly_data = yearly_query.all()

            # Get fee structure
            fee_query = session.query(FeeStructure).filter_by(exchange_id=exchange.id).order_by(FeeStructure.id)
            fee_data = fee_query.all()

            # Create result structure
            result[exchange.name] = {
                'monthly_dates': [item.month_date for item in monthly_data],
                'monthly_volume': [item.volume for item in monthly_data],
                'monthly_commission': [item.commission for item in monthly_data],
                'yearly_dates': [item.year for item in yearly_data],
                'yearly_volume': [item.volume for item in yearly_data],
                'yearly_commission': [item.commission for item in yearly_data],
                'vip_tiers': [item.vip_tier for item in fee_data],
                'maker_fees': [item.maker_fee for item in fee_data],
                'taker_fees': [item.taker_fee for item in fee_data]
            }

    except Exception as e:
        print(f"Error retrieving exchange data: {str(e)}")

    finally:
        session.close()

    return result

# Get latest cryptocurrency prices
def get_latest_crypto_prices():
    """
    Retrieves the latest cryptocurrency prices from the database.
    """
    session = get_session()
    result = {}

    try:
        # Get latest price for each cryptocurrency
        prices = session.query(CryptoPrice).all()

        for price in prices:
            result[price.crypto_id] = {
                'usd': price.price_usd,
                'usd_24h_change': price.change_24h
            }

    except Exception as e:
        print(f"Error retrieving crypto prices: {str(e)}")

    finally:
        session.close()

    return result

# Get latest news items
def get_latest_news():
    """
    Retrieves the latest news items from the database.
    """
    session = get_session()
    result = []

    try:
        # Get news items ordered by timestamp
        news_items = session.query(NewsItem).order_by(desc(NewsItem.timestamp)).all()

        for item in news_items:
            result.append({
                'title': item.title,
                'description': item.description,
                'url': item.url,
                'published_at': item.published_at
            })

    except Exception as e:
        print(f"Error retrieving news items: {str(e)}")

    finally:
        session.close()

    return result