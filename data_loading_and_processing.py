from google.colab import drive
import os
import yfinance as yf
import pandas as pd
from datetime import datetime
import numpy as np

# Mounting google drive
drive.mount('/content/drive', force_remount=True)

# Defining the directory path
directory_path = '/content/drive/My Drive/Model Thinking/Stock Market Analysis/Stock Data'

# Creating the directory if it doesn't exist
if not os.path.exists(directory_path):
    os.makedirs(directory_path)

#Download data

# List of stock tickers
stock_tickers = [
    "RELIANCE.NS",
    "INFY",
    "TCS.NS",
    "HINDUNILVR.NS",
    "ITC.NS",
    "HDFCBANK.NS",
    "BHARTIARTL.NS",
    "M&M.NS",
    "LT.NS",
    "ASIANPAINT.NS"
]


# Fetching historical data for each stock
stock_data = {}
for ticker in stock_tickers:
    stock_data[ticker] = yf.download(ticker, start="2004-01-01", end="2024-01-01")

# Extracting daily closing values
closing_values = {}
for ticker, data in stock_data.items():
    closing_values[ticker] = data['Close']

# Write closing values to CSV and store in Google Drive
for ticker, closes in closing_values.items():
    file_name = f"{ticker}_closing_values.csv"
    closes.to_csv(f"/content/drive/My Drive/Model Thinking/Stock Market Analysis/Stock Data/{file_name}")

# Splitting data into annual files
def split_into_annual_files(stock_data, directory_path):
    # Iterate over each stock's data
    for ticker, data in stock_data.items():
        print(f"Processing data for {ticker}...")

        # Create folder for the stock if it doesn't exist
        stock_folder = os.path.join(directory_path, ticker)
        if not os.path.exists(stock_folder):
            os.makedirs(stock_folder)

        # Split data into annual stock values and save as separate files
        for year in range(data.index.year.min(), data.index.year.max() + 1):
            annual_data = data[str(year)]
            file_name = f"{year}_closing_values.csv"
            file_path = os.path.join(stock_folder, file_name)
            annual_data.to_csv(file_path)

split_into_annual_files(stock_data, '/content/drive/My Drive/Model Thinking/Stock Market Analysis/Stock Data')

# Computing and storing annual returns and risks

def compute_returns_risks(stock_data, directory_path):
    returns_data = pd.DataFrame()

    for ticker, data in stock_data.items():
        print(f"Processing data for {ticker}...")

        annual_returns_daily = []
        annual_risk = []  # List to store annualized risk for each year

        years = range(data.index.year.min(), data.index.year.max() + 1)

        for year in years:
            # Subset data for the current year
            year_data = data.loc[str(year)]

            # Daily Returns
            daily_returns = year_data['Close'].pct_change()

            # Annualized Return based on Daily Returns
            annual_return_daily = daily_returns.mean() * 252
            annual_returns_daily.append(annual_return_daily)

            # Annualized Risk (Standard Deviation of Daily Returns)
            annual_risk_daily = daily_returns.std() * (252 ** 0.5)
            annual_risk.append(annual_risk_daily)

        # Create a DataFrame for the results
        results_df = pd.DataFrame({
            'Year': years,
            'Annualized Return': annual_returns_daily,
            'Annualized Risk': annual_risk
        })

        # Save results to CSV file
        file_name = f"{ticker}_returns_risk.csv"
        file_path = os.path.join(directory_path, file_name)
        results_df.to_csv(file_path, index=False)
        print(f"Results saved to {file_path}")


compute_returns_risks(stock_data, directory_path)

