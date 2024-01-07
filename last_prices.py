# https://pypi.org/project/websocket_client/
import websocket
import os
from utils import logger
from dotenv import load_dotenv

load_dotenv()

logger = logger(stream=False)

finnhub_api_key = os.getenv("FINNHUB_API_KEY")


def on_message(ws, message):
    logger.info(message)


def on_error(ws, error):
    logger.error(error)


def on_close(ws):
    logger.info("### closed ###")


def on_open(ws):
    logger.info(ws.send('{"type":"subscribe","symbol":"AAPL"}'))
    logger.info(ws.send('{"type":"subscribe","symbol":"AMZN"}'))
    logger.info(ws.send('{"type":"subscribe","symbol":"BINANCE:BTCUSDT"}'))
    logger.info(ws.send('{"type":"subscribe","symbol":"IC MARKETS:1"}'))


if __name__ == "__main__":
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp(
        f"wss://ws.finnhub.io?token={finnhub_api_key}",
        on_message=on_message,
        on_error=on_error,
        on_close=on_close,
        on_open=on_open,
    )
    ws.run_forever()
