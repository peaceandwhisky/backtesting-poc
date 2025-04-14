import ccxt
import pandas as pd
from datetime import datetime, timedelta
from backtesting import Backtest, Strategy
from backtesting.lib import crossover
import os

class SimpleStrategy(Strategy):
    def init(self):
        # 移動平均線の計算
        self.sma20 = self.I(SMA, self.data.Close, 20)
        self.sma50 = self.I(SMA, self.data.Close, 50)
        self.sma200 = self.I(SMA, self.data.Close, 200)  # 長期トレンドの確認用

    def next(self):
        # 長期トレンドが上昇の場合のみ取引
        if self.data.Close[-1] > self.sma200[-1]:
            # ゴールデンクロスで買い、デッドクロスで売り
            if crossover(self.sma20, self.sma50):
                self.buy()
            elif crossover(self.sma50, self.sma20):
                self.sell()

def SMA(values, n):
    return pd.Series(values).rolling(n).mean()

def fetch_ohlcv_data():
    # Binanceからデータを取得
    exchange = ccxt.binance()
    
    # 過去1年分の日足データを取得
    since = int((datetime.now() - timedelta(days=365)).timestamp() * 1000)
    ohlcv = exchange.fetch_ohlcv('BTC/USDT', '1d', since=since)
    
    # DataFrameに変換
    df = pd.DataFrame(ohlcv, columns=['Timestamp', 'Open', 'High', 'Low', 'Close', 'Volume'])
    df['Timestamp'] = pd.to_datetime(df['Timestamp'], unit='ms')
    df.set_index('Timestamp', inplace=True)
    
    return df

def main():
    # データの取得
    data = fetch_ohlcv_data()
    
    # バックテストの実行
    initial_cash = 1000000  # 1,000,000 USDT
    bt = Backtest(data, SimpleStrategy, commission=.002, cash=initial_cash)
    results = bt.run()
    
    # 結果の表示
    print("\n=== バックテスト結果 ===")
    print(f"期間: {results['Start']} から {results['End']}")
    print(f"リターン: {results['Return [%]']:.2f}%")
    print(f"最大ドローダウン: {results['Max. Drawdown [%]']:.2f}%")
    print(f"取引回数: {results['# Trades']}")
    print(f"勝率: {results['Win Rate [%]']:.2f}%")
    print(f"平均取引利益: {results['Avg. Trade [%]']:.2f}%")
    print(f"シャープレシオ: {results['Sharpe Ratio']:.2f}")
    
    # 取引履歴の表示
    print("\n=== 取引履歴 ===")
    print(results._trades)
    
    # HTMLチャートの保存
    output_dir = 'backtest_results'
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, 'backtest_results.html')
    
    # バックテストの結果をHTMLとして保存（バージョン0.2.0用の修正）
    try:
        bt.plot(filename=output_file)
        print(f"\nインタラクティブなチャートを {output_file} に保存しました。")
        print("このファイルをブラウザで開いて結果を確認してください。")
    except Exception as e:
        print(f"プロットエラー: {e}")
        print("テキストベースの結果を表示します:")
        print(results._trades)

if __name__ == '__main__':
    main() 