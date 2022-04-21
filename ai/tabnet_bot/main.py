from .tabnet_trader import TabNetBybitTrader

if __name__ == '__main__':
    bybit_cred = {
        "api_key": "",
        "api_secret": "",
    }
    telegram_cred = {
        "token": "",
        "chat_id": "",
    }
    trader = TabNetBybitTrader(
        symbol="BTC/USDT",
        bybit_credential=bybit_cred,
        telegram_credential=telegram_cred,
        tabnet_zip_dir="trained/TabNetClassifier_Binance.zip"
    )
    trader.execute_trade()
