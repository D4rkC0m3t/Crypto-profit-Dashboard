import numpy as np
import pandas as pd
import datetime as dt

def generate_exchange_data():
    """
    Generate structured data for cryptocurrency exchanges.
    Generates realistic patterns but does not use real data.
    """
    # List of exchanges
    exchanges = [
        "Binance", "Coinbase", "Bybit", "Upbit", "Kraken", 
        "Kucoin", "CoinDCX", "Bitget", "OKX"
    ]
    
    # Generate data for each exchange
    exchange_data = {}
    
    # Current year and month
    current_date = dt.datetime.now()
    current_year = current_date.year
    
    for exchange in exchanges:
        # Determine exchange scale factor (some exchanges have higher volume than others)
        if exchange in ["Binance", "Coinbase"]:
            scale = np.random.uniform(8, 12)  # Larger exchanges
        elif exchange in ["Bybit", "Kraken", "Upbit"]:
            scale = np.random.uniform(4, 8)   # Medium exchanges
        else:
            scale = np.random.uniform(1, 4)   # Smaller exchanges
        
        # Monthly data - last 12 months
        months = 12
        month_dates = [(current_date - dt.timedelta(days=30*i)).strftime("%Y-%m") for i in range(months)]
        month_dates.reverse()  # Oldest first
        
        # Generate monthly volume data with realistic patterns
        base_volume = np.random.uniform(500, 2000) * scale
        monthly_volume = []
        
        for i in range(months):
            # Add some seasonality and trend
            season_factor = 1 + 0.2 * np.sin(i/6 * np.pi)
            trend_factor = 1 + (i/24)  # Slight upward trend
            
            # Add some randomness
            random_factor = np.random.uniform(0.8, 1.2)
            
            volume = base_volume * season_factor * trend_factor * random_factor
            monthly_volume.append(round(volume, 2))
        
        # Commission is typically a percentage of volume
        commission_rate = np.random.uniform(0.001, 0.003)  # 0.1% to 0.3%
        monthly_commission = [round(vol * commission_rate, 2) for vol in monthly_volume]
        
        # Yearly data - last 8 years
        years = 8
        year_list = [str(current_year - i) for i in range(years)]
        year_list.reverse()  # Oldest first
        
        # Generate yearly data
        yearly_volume = []
        yearly_commission = []
        
        for i in range(years):
            # Exchanges grow over time
            growth_factor = (1 + i/5) ** 2  # Exponential growth
            
            # Add some randomness
            random_factor = np.random.uniform(0.9, 1.1)
            
            year_volume = base_volume * 12 * growth_factor * random_factor
            yearly_volume.append(round(year_volume, 2))
            yearly_commission.append(round(year_volume * commission_rate, 2))
        
        # VIP tiers and fees
        vip_tiers = ["Regular", "VIP 1", "VIP 2", "VIP 3", "VIP 4", "VIP 5"]
        maker_fees = []
        taker_fees = []
        
        # Generate descending fee structure based on VIP level
        base_maker = np.random.uniform(0.075, 0.15)
        base_taker = base_maker * 1.5
        
        for tier in range(len(vip_tiers)):
            reduction = tier * 0.02
            maker_fees.append(round(max(0.01, base_maker - reduction), 3))
            taker_fees.append(round(max(0.02, base_taker - reduction), 3))
        
        # Store data for this exchange
        exchange_data[exchange] = {
            "monthly_dates": month_dates,
            "monthly_volume": monthly_volume,
            "monthly_commission": monthly_commission,
            "yearly_dates": year_list,
            "yearly_volume": yearly_volume,
            "yearly_commission": yearly_commission,
            "vip_tiers": vip_tiers,
            "maker_fees": maker_fees,
            "taker_fees": taker_fees
        }
    
    return exchange_data
