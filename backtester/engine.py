import pandas as pd
import yfinance as yf
from .portfolio import Portfolio
from .order import Order

class Engine:
    """
    The core backtesting engine that simulates the trading process.
    """
    def __init__(self, tickers: list, start_date: str, end_date: str, initial_cash: float, strategy):
        """
        Initializes the engine with market data and a portfolio.

        Args:
            tickers (list): A list of stock ticker symbols to backtest.
            start_date (str): The start date for the backtest.
            end_date (str): The end date for the backtest.
            initial_cash (float): The starting cash for the portfolio.
            strategy: The trading strategy object to use.
        """
        self.tickers = tickers
        self.start_date = start_date
        self.end_date = end_date
        self.portfolio = Portfolio(initial_cash)
        self.market_data = None
        self.orders = []

        # Connect the strategy and portfolio to the engine
        self.strategy = strategy
        self.portfolio.engine = self  # Give the portfolio a reference to its engine
        self.strategy.portfolio = self.portfolio # Give the strategy a reference to its portfolio

    def get_historical_data(self, start_date, end_date):
        """
        Retrieves a slice of market data for a given date range.
        """
        try:
            return self.market_data.loc[(slice(start_date, end_date), slice(None)), :]
        except KeyError:
            print("Warning: Not enough historical data to fulfill strategy request.")
            return None

    def run(self):
        """
        Runs the backtest by iterating through each day and executing trades.
        """
        # --- Step 1: Download all market data for the backtest period ---
        all_data = pd.DataFrame()
        for ticker in self.tickers:
            data = yf.download(ticker, start=self.start_date, end=self.end_date)
            # CRUCIAL FIX: Convert the Date index to a column
            data.reset_index(inplace=True)
            # Add a 'Ticker' column to identify the stock
            data['Ticker'] = ticker
            all_data = pd.concat([all_data, data])

        # Drop any rows with missing data
        all_data.dropna(inplace=True)
        # We need a MultiIndex to easily access data by Date and Ticker
        self.market_data = all_data.set_index(['Date', 'Ticker']).sort_index()

        # --- Step 2: Start the simulation loop ---
        unique_dates = self.market_data.index.get_level_values('Date').unique()
        for current_date in unique_dates:
            # Tell the strategy to generate orders for the day
            todays_market_data = self.market_data.loc[current_date]
            self.orders = self.strategy.generate_orders(current_date, todays_market_data)

            # --- Execute orders from the strategy ---
            if len(self.orders) > 0:
                for order in self.orders:
                    # Get the stock's closing price for the day
                    execution_price = todays_market_data.loc[order.ticker, 'Close']
                    # Execute the transaction
                    self.portfolio.transact(order.ticker, execution_price, order.quantity)
                # Clear the orders list after execution
                self.orders = []

            # --- Update the portfolio's total value at the end of the day ---
            self.portfolio.update_holdings(current_date, todays_market_data)

        print("\nBacktest completed.")
        return self.portfolio.holdings
