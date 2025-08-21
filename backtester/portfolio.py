import pandas as pd

class Portfolio:
    """
    Manages the simulated trading portfolio, including cash, positions,
    and calculating portfolio value.
    """
    def __init__(self, initial_cash: float = 100000.0):
        """
        Initializes the portfolio with a starting cash balance.

        Args:
            initial_cash (float): The starting amount of cash in the portfolio.
        """
        self.initial_cash = initial_cash
        self.cash = initial_cash
        self.positions = {}  # Dictionary to store {ticker: quantity}
        self.holdings = pd.DataFrame(columns=['Date', 'Cash', 'Equity', 'Total'])

    def update_holdings(self, current_date, market_data):
        """
        Calculates and records the portfolio's total value at the end of each day.

        Args:
            current_date: The current date of the backtest.
            market_data: A DataFrame containing the latest market prices for all tickers.
        """
        equity = 0.0
        for ticker, quantity in self.positions.items():
            if ticker in market_data.index:
                close_price = market_data.loc[ticker, 'Close']
                equity += close_price * quantity
        
        total_value = self.cash + equity
        
        # Create a new row (a dictionary) with the latest holdings data
        new_row = {
            'Date': current_date,
            'Cash': self.cash,
            'Equity': equity,
            'Total': total_value
        }
        
        # Append the new row to the holdings DataFrame
        # pd.concat handles appending a single dictionary as a new row
        self.holdings = pd.concat([self.holdings, pd.DataFrame([new_row])], ignore_index=True)

    def transact(self, ticker: str, price: float, quantity: int):
        """
        Processes a buy or sell transaction and updates cash and positions.
        A positive quantity indicates a buy, a negative quantity indicates a sell.

        Args:
            ticker (str): The stock ticker symbol.
            price (float): The execution price of the trade.
            quantity (int): The number of shares to trade. Positive for buy, negative for sell.
        """
        transaction_value = price * quantity
        self.cash -= transaction_value

        if ticker not in self.positions:
            self.positions[ticker] = 0
        
        self.positions[ticker] += quantity
        
        print(f"Transaction: {'BUY' if quantity > 0 else 'SELL'} {abs(quantity)} shares of {ticker} at ${price:.2f}.")
        print(f"New cash balance: ${self.cash:.2f}")
