# Backtesting POC

A Proof of Concept (POC) project for backtesting trading strategies using BTCUSDT price data.

## Features

- Fetches 1 year of BTCUSDT price data from Binance
- Implements a simple trading strategy using moving averages (20, 50, and 200 days)
- Generates interactive HTML charts for backtest results

## Requirements

- Python 3.10 or higher
- Required packages are listed in `requirements.txt`

## Setup

```bash
# Clone the repository
git clone https://github.com/yourusername/backtesting-poc.git
cd backtesting-poc

# Install dependencies
pip install -r requirements.txt
```

## Usage

```bash
python backtest_btc.py
```

After execution, the results will be saved as an HTML file in the `backtest_results` directory.

## Backtesting Strategy

The current strategy trades based on the following conditions:

1. Only trades when price is above the 200-day moving average (trend filter)
2. Buys when the 20-day moving average crosses above the 50-day moving average (golden cross)
3. Sells when the 50-day moving average crosses above the 20-day moving average (death cross) 