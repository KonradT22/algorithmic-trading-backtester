from abc import ABC, abstractmethod

class BaseStrategy(ABC):
    """
    Abstract base class for all trading strategies.
    Each strategy must inherit from this class and implement the required methods.
    """
    def __init__(self, tickers: list):
        """
        Initializes the base strategy.

        Args:
            tickers (list): A list of stock ticker symbols to trade.
        """
        self.tickers = tickers
        self.portfolio = None

    @abstractmethod
    def generate_orders(self, current_date, todays_market_data):
        """
        Generates and returns a list of Order objects.

        Args:
            current_date: The current date in the backtest loop.
            todays_market_data: A DataFrame containing market data for the current day.

        Returns:
            A list of Order objects. Can be empty if no trades are made.
        """
        pass