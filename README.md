# TradeProfitAnalytics

A comprehensive dashboard for analyzing cryptocurrency exchange performance, market trends, and fee structures.

## Features

- **Overview Tab**: Global cryptocurrency market data, Bitcoin dominance chart, market cap distribution, and historical trends
- **Exchange Comparison**: Compare performance metrics across multiple exchanges
- **Fee Analysis**: Analyze fee structures and compare rates across exchanges
- **Volume Analysis**: Track trading volume trends and distribution
- **Individual Exchange Tabs**: Detailed metrics for each supported exchange

## Interactive Elements

- **Dynamic Buttons**: Filter and interact with data using dynamic buttons
- **Custom Styling**: Modern UI with shadow effects and responsive design
- **Custom Cursors**: Enhanced user experience with context-aware cursors
- **Interactive Charts**: Hover for detailed information on all visualizations

## Data Sources

- Exchange fee data from public exchange documentation
- Cryptocurrency prices from CoinGecko API
- News data from CoinGecko News API
- Market data based on public trading volume

## Project Structure

```text
TradeProfitAnalytics/
├── .streamlit/
│   └── config.toml
├── README.md
├── main.py
└── src/
    ├── requirements.txt
    ├── app.py
    ├── data_fetcher.py
    ├── database.py
    └── utils.py
```

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/TradeProfitAnalytics.git
   cd TradeProfitAnalytics
   ```

2. Install required packages:

   ```bash
   pip install -r src/requirements.txt
   ```

3. Run the application:

   ```bash
   python main.py
   ```

Or directly with Streamlit:

```bash
streamlit run main.py
```

The dashboard will be available at [http://localhost:8515](http://localhost:8515)

## Requirements

- Python 3.7+
- Streamlit
- Pandas
- NumPy
- Plotly
- Requests

## License

This project is licensed under the MIT License - see the LICENSE file for details.
