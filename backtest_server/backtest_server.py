import ccxt
import pandas as pd
from datetime import datetime, timedelta
from backtesting import Backtest, Strategy
from backtesting.lib import crossover
import os
from typing import Any
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("backtest_server")

def SMA(values, n):
    return pd.Series(values).rolling(n).mean()

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

@mcp.tool()
async def run_backtest(
    symbol: str = "BTC/USDT",
    timeframe: str = "1d",
    days: int = 365,
    initial_cash: float = 1000000,
    commission: float = 0.002
) -> dict[str, Any]:
    """Run a backtest for the specified cryptocurrency.

    Args:
        symbol: Trading pair symbol (e.g. BTC/USDT)
        timeframe: Timeframe for the data (e.g. 1d, 4h, 1h)
        days: Number of days of historical data to fetch
        initial_cash: Initial capital for backtesting
        commission: Trading commission rate
    """
    # Fetch data
    exchange = ccxt.binance()
    since = int((datetime.now() - timedelta(days=days)).timestamp() * 1000)
    ohlcv = exchange.fetch_ohlcv(symbol, timeframe, since=since)
    
    # Convert to DataFrame
    df = pd.DataFrame(ohlcv, columns=['Timestamp', 'Open', 'High', 'Low', 'Close', 'Volume'])
    df['Timestamp'] = pd.to_datetime(df['Timestamp'], unit='ms')
    df.set_index('Timestamp', inplace=True)
    
    # Run backtest
    bt = Backtest(df, SimpleStrategy, commission=commission, cash=initial_cash)
    results = bt.run()
    
    # Format results
    return {
        "period": f"{results['Start']} to {results['End']}",
        "return": f"{results['Return [%]']:.2f}%",
        "max_drawdown": f"{results['Max. Drawdown [%]']:.2f}%",
        "number_of_trades": results['# Trades'],
        "win_rate": f"{results['Win Rate [%]']:.2f}%",
        "average_trade": f"{results['Avg. Trade [%]']:.2f}%",
        "sharpe_ratio": f"{results['Sharpe Ratio']:.2f}",
        "trades": results._trades.to_dict('records')
    }

if __name__ == '__main__':
    # Initialize and run the server
    mcp.run(transport='stdio')
