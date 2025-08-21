class Order:
    """
    Represents a simple market order.
    """
    def __init__(self, ticker: str, quantity: int):
        """
        Initializes an Order object.

        Args:
            ticker (str): The stock ticker symbol.
            quantity (int): The number of shares to buy (positive) or sell (negative).
        """
        self.ticker = ticker
        self.quantity = quantity