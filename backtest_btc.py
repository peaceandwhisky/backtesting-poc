import ccxt
import pandas as pd
from datetime import datetime, timedelta
from backtesting import Backtest, Strategy
from backtesting.lib import crossover
import os

class SimpleStrategy(Strategy):
    def init(self):
        # Calculate moving averages
        self.sma20 = self.I(SMA, self.data.Close, 20)
        self.sma50 = self.I(SMA, self.data.Close, 50)
        self.sma200 = self.I(SMA, self.data.Close, 200)  # For long-term trend confirmation

    def next(self):
        # Only trade when long-term trend is bullish
        if self.data.Close[-1] > self.sma200[-1]:
            # Buy on golden cross, sell on death cross
            if crossover(self.sma20, self.sma50):
                self.buy()
            elif crossover(self.sma50, self.sma20):
                self.sell()

def SMA(values, n):
    return pd.Series(values).rolling(n).mean()

def fetch_ohlcv_data():
    # Fetch data from Binance
    exchange = ccxt.binance()
    
    # Get 1 year of daily data
    since = int((datetime.now() - timedelta(days=365)).timestamp() * 1000)
    ohlcv = exchange.fetch_ohlcv('BTC/USDT', '1d', since=since)
    
    # Convert to DataFrame
    df = pd.DataFrame(ohlcv, columns=['Timestamp', 'Open', 'High', 'Low', 'Close', 'Volume'])
    df['Timestamp'] = pd.to_datetime(df['Timestamp'], unit='ms')
    df.set_index('Timestamp', inplace=True)
    
    return df

def main():
    # Fetch data
    data = fetch_ohlcv_data()
    
    # Run backtest
    initial_cash = 1000000  # 1,000,000 USDT
    bt = Backtest(data, SimpleStrategy, commission=.002, cash=initial_cash)
    results = bt.run()
    
    # Display results
    print("\n=== Backtest Results ===")
    print(f"Period: {results['Start']} to {results['End']}")
    print(f"Return: {results['Return [%]']:.2f}%")
    print(f"Max Drawdown: {results['Max. Drawdown [%]']:.2f}%")
    print(f"Number of Trades: {results['# Trades']}")
    print(f"Win Rate: {results['Win Rate [%]']:.2f}%")
    print(f"Average Trade: {results['Avg. Trade [%]']:.2f}%")
    print(f"Sharpe Ratio: {results['Sharpe Ratio']:.2f}")
    
    # Display trade history
    print("\n=== Trade History ===")
    print(results._trades)
    
    # Save HTML chart
    output_dir = 'backtest_results'
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, 'backtest_results.html')
    
    # Save backtest results as HTML (modified for version 0.2.0)
    try:
        bt.plot(filename=output_file)
        print(f"\nInteractive chart saved to {output_file}")
        print("Please open this file in your browser to view the results.")
    except Exception as e:
        print(f"Plot error: {e}")
        print("Displaying text-based results:")
        print(results._trades)

if __name__ == '__main__':
    main() 