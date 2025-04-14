# Backtesting POC

BTCUSDTの価格データを使用したバックテスティングのPOC（Proof of Concept）プロジェクトです。

## 機能

- Binanceから過去1年分のBTCUSDTの価格データを取得
- 移動平均線（20日、50日、200日）を使用した簡単な取引戦略
- バックテスト結果のインタラクティブなHTMLチャート生成

## 必要条件

- Python 3.10以上
- 必要なパッケージは`requirements.txt`に記載

## セットアップ

```bash
# リポジトリのクローン
git clone https://github.com/yourusername/backtesting-poc.git
cd backtesting-poc

# 依存パッケージのインストール
pip install -r requirements.txt
```

## 使用方法

```bash
python backtest_btc.py
```

実行後、`backtest_results`ディレクトリに結果のHTMLファイルが生成されます。

## バックテスト戦略

現在の戦略は以下の条件で取引を行います：

1. 200日移動平均線を上回っている場合のみ取引（トレンドフィルター）
2. 20日移動平均線が50日移動平均線を上抜けた場合に買い（ゴールデンクロス）
3. 50日移動平均線が20日移動平均線を上抜けた場合に売り（デッドクロス） 