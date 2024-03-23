import logging
import time

import redis

import simple_trading_config

SIGNAL_TYPES = simple_trading_config.SIGNAL_TYPES
redis_client = redis.Redis(host=simple_trading_config.REDIS_HOST, port=simple_trading_config.REDIS_PORT, db=0)

logging.basicConfig(level=simple_trading_config.LOG_LEVEL)


def check_signal():
    # Assume that only one signal in demo project.
    logging.info("Signals stored in Redis ZSET:")
    for symbol, signal in redis_client.zrange(SIGNAL_TYPES[0], 0, -1, withscores=True):
        logging.info(f"{symbol.decode('utf-8')}: {signal}")

    # Fetching the first element from the result of ZSET
    result = redis_client.zrevrange(SIGNAL_TYPES[0], 0, 0, withscores=True)
    if result:
        symbol, signal = result[0]  # Unpacking the first tuple
        pre_order(symbol, signal)
    else:
        logging.info("No signals found in Redis ZSET")


def pre_order(symbol, signal):
    if float(signal) <= 0:
        logging.info("Not match, wait next good signal!")
        return

    logging.info(
        "Symbol: {symbol}, Signal: {signal} is current max. Choose this one to send order".format(symbol=symbol.decode('utf-8'),
                                                                                      signal=signal)
    )
    send_order(symbol)


def send_order(symbol):
    logging.info("[Simulate] Sending buy order to binance, symbol: %s, quantity:1", symbol)
    time.sleep(1)
    logging.info("[Simulate] Success sending buy order to binance, symbol: %s", symbol)


def main():
    try:
        while True:
            check_signal()
            time.sleep(15)

    except Exception as e:
        logging.error("Exception: {}".format(e))
    finally:
        redis_client.close()


if __name__ == '__main__':
    main()
