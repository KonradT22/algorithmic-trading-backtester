# This is the main script to run your backtest

import pandas as pd
import matplotlib.pyplot as plt
from backtester.engine import Engine
from strategies.sma_crossover import SmaCrossover

# --- Backtest Configuration ---
tickers = ["AAPL", "MSFT", "GOOGL"]
start_date = "2020-01-01"
end_date = "2023-12-31"
initial_cash = 100000.0

# --- Main Execution Block ---
if __name__ == "__main__":
    print("Starting backtest...")

    # 1. Instantiate the trading strategy
    strategy = SmaCrossover(tickers=tickers, fast_window=50, slow_window=200)

    # 2. Instantiate the backtesting engine with all the necessary components
    backtester = Engine(
        tickers=tickers,
        start_date=start_date,
        end_date=end_date,
        initial_cash=initial_cash,
        strategy=strategy
    )

    # 3. Run the backtest and get the results
    results = backtester.run()

    # 4. Print and visualize the results
    print("\n--- Backtest Results ---")
    print(results.tail())

    # Plot the equity curve
    plt.style.use('dark_background') # For a nice dark theme
    plt.figure(figsize=(12, 8))
    
    # Ensure 'Date' is datetime and set as index for plotting
    results['Date'] = pd.to_datetime(results['Date'])
    results.set_index('Date', inplace=True)
    
    # Ensure 'Total' is numeric for plotting
    results['Total'] = pd.to_numeric(results['Total'])

    results['Total'].plot(title='Equity Curve')
    plt.xlabel('Date')
    plt.ylabel('Portfolio Value')
    plt.grid(True)
    plt.show()

    print("\nBacktest finished.")