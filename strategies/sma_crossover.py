import pandas as pd
from .base_strategy import BaseStrategy
from backtester.order import Order

class SmaCrossover(BaseStrategy):
    """
    A simple trading strategy based on a Simple Moving Average (SMA) crossover.
    """
    def __init__(self, tickers: list, fast_window: int = 50, slow_window: int = 200):
        """
        Initializes the SMA Crossover strategy.

        Args:
            tickers (list): List of tickers to trade.
            fast_window (int): The window size for the fast SMA.
            slow_window (int): The window size for the slow SMA.
        """
        super().__init__(tickers)
        self.fast_window = fast_window
        self.slow_window = slow_window
        self.current_positions = {}  # Track positions within the strategy

    def generate_orders(self, current_date, todays_market_data):
        """
        Generates a list of orders based on the SMA crossover signal.
        """
        orders = []

        # --- Get a history of past data needed for the moving averages ---
        # We need at least the slow_window + 1 days of history to calculate the SMAs
        history_end_date = current_date
        history_start_date = current_date - pd.Timedelta(days=self.slow_window + 1)

        # This is a key line: we get all historical data from the engine
        historical_data = self.portfolio.engine.get_historical_data(history_start_date, history_end_date)

        if historical_data is None:
            # Not enough history yet, return no orders
            return orders

        for ticker in self.tickers:
            # Get the close prices for the current ticker from the historical data
            ticker_data = historical_data.loc[(slice(None), ticker), 'Close'].droplevel('Ticker')

            # We need enough data to calculate the slow SMA
            if len(ticker_data) < self.slow_window:
                continue

            # --- Calculate the Simple Moving Averages ---
            # This uses pandas' .rolling() method, which is very efficient
            fast_sma = ticker_data.rolling(window=self.fast_window).mean().iloc[-1]
            slow_sma = ticker_data.rolling(window=self.slow_window).mean().iloc[-1]

            current_position = self.current_positions.get(ticker, 0)

            # --- Generate Buy/Sell Signals ---
            # Signal is a Buy if fast_sma crosses above slow_sma
            if fast_sma > slow_sma and current_position == 0:
                # We have a buy signal and no current position, so buy a fixed quantity
                buy_quantity = 100
                orders.append(Order(ticker, buy_quantity))
                self.current_positions[ticker] = buy_quantity

            # Signal is a Sell if fast_sma crosses below slow_sma
            elif fast_sma < slow_sma and current_position > 0:
                # We have a sell signal and we currently hold shares, so sell them all
                sell_quantity = -current_position
                orders.append(Order(ticker, sell_quantity))
                self.current_positions[ticker] = 0

        return orders