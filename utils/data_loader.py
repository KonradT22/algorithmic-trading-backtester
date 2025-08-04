import yfinance as yf
import pandas as pd
import os
import datetime

# Define the directory where raw data will be stored
RAW_DATA_DIR = os.path.join('data', 'raw')

# Ensure the raw data directory exists
# os.makedirs(path, exist_ok=True) creates the directory if it doesn't exist.
# If it already exists, it does nothing, preventing errors.
os.makedirs(RAW_DATA_DIR, exist_ok=True)

# --- Functions for Data Ingestion ---

def download_stock_data(ticker: str, start_date: str, end_date: str) -> pd.DataFrame:
    """
    Purpose: Downloads historical stock data for a given ticker from Yahoo Finance.

    Args:
        ticker (str): The stock ticker symbol (e.g., 'AAPL', 'MSFT').
        start_date (str): The start date for data download in 'YYYY-MM-DD' format.
        end_date (str): The end date for data download in 'YYYY-MM-DD' format.

    Returns:
        pd.DataFrame: A DataFrame containing the historical stock data
                      with columns: 'Date', 'Open', 'High', 'Low', 'Close', 'Volume', 'Adj Close'.
                      The 'Date' column will be the DataFrame index.
    """
    print(f"Downloading data for {ticker} from {start_date} to {end_date}...")
    try:
        data = yf.download(ticker, start=start_date, end=end_date)
        if data.empty:
            print(f"Warning: No data found for {ticker} in the specified range.")
        else:
            print(f"Successfully downloaded {len(data)} rows for {ticker}.")
        return data
    except Exception as e:
        print(f"Error downloading data for {ticker}: {e}")
        return pd.DataFrame() # Return an empty DataFrame on error
    
def save_data_to_csv(data: pd.DataFrame, ticker: str, directory: str = RAW_DATA_DIR):
    """
    Purpose: Saves a Pandas DataFrame to a CSV file in the specified directory.

    Args:
        data (pd.DataFrame): The DataFrame to save.
        ticker (str): The stock ticker symbol, used for naming the file.
        directory (str): The directory where the CSV file will be saved.
                         Defaults to RAW_DATA_DIR.
    """
    # Check if the DataFrame is empty before attempting to save
    if data.empty:
        print(f"No data to save for {ticker}.")
        return # Exit the function if there's no data

    # Construct the full file name (e.g., "AAPL_daily.csv")
    file_name = f"{ticker}_daily.csv"

    # Combine the directory path and the file name to get the complete file path
    # (e.g., "data/raw/AAPL_daily.csv")
    file_path = os.path.join(directory, file_name)

    # Use a try-except block for robust error handling during file saving
    try:
        print(f"Saving {ticker}'s data to: {file_path}") # More specific print
        data.to_csv(file_path, index=True)
        print(f"Data for {ticker} saved successfully.") # Confirmation
    except Exception as e:
        print(f"Error saving data for {ticker} to {file_path}: {e}")

# --- Example Usage (This part runs when the script is executed directly) ---
if __name__ == "__main__":
    # Define tickers and date range for demonstration
    tickers = ["AAPL", "MSFT", "GOOGL"]
    # Get today's date
    today = datetime.date.today()
    # Set end date to today
    end_date = today.strftime('%Y-%m-%d')
    # Set start date to 5 years ago from today
    start_date = (today - datetime.timedelta(days=5*365)).strftime('%Y-%m-%d')

    print(f"Starting data ingestion for multiple tickers from {start_date} to {end_date}...")

    for ticker in tickers:
        # 1. Download the data
        stock_data = download_stock_data(ticker, start_date, end_date)

        # 2. Save the downloaded data
        save_data_to_csv(stock_data, ticker)
        print("-" * 30) # Separator for readability

    print("\nData ingestion process completed.")