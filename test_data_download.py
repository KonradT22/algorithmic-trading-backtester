import yfinance as yf
import pandas as pd
import os

print("Hello from your trading backtester project!")

# Define a stock ticker and date range
ticker = "AAPL"
start_date = "2023-01-01"
end_date = "2023-12-31"

print(f"\nAttempting to download {ticker} data from {start_date} to {end_date}...")

try:
    data = yf.download(ticker, start=start_date, end=end_date)
    if not data.empty:
        print(f"Successfully downloaded {len(data)} rows of data for {ticker}.")
        print("First 5 rows:")
        print(data.head())

        # Optional: Save to a CSV for later use (will be ignored by .gitignore)
        data_dir = "data"
        os.makedirs(data_dir, exist_ok=True) # Create data directory if it doesn't exist
        file_path = os.path.join(data_dir, f"{ticker}_daily.csv")
        data.to_csv(file_path)
        print(f"Data saved to {file_path}")
    else:
        print(f"No data found for {ticker} in the specified range.")
except Exception as e:
    print(f"An error occurred during data download: {e}")

print("\nSetup complete for initial data test!")