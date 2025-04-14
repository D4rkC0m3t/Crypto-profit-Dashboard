# TradeProfitAnalytics - Main Entrypoint
# This file serves as the main entrypoint for the Streamlit application

import os
import sys

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

# Import the Streamlit app from the src directory
from src.app import run_app

# Run the application
if __name__ == "__main__":
    run_app()
