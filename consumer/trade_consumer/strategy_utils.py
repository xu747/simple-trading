import logging

import simple_trading_config

logging.basicConfig(level=simple_trading_config.LOG_LEVEL)


def calculate_rsi(prices, period=1):
    # Convert to floats
    prices = [float(price) for price in prices if isinstance(price, (int, float, str)) and price not in ['', ' ', None]]

    if len(prices) < period:
        return 0

    gains = losses = 0.0
    for i in range(1, period - 1):
        change = prices[i] - prices[i - 1]
        if change > 0:
            gains += change
        else:
            losses -= change
    average_gain = gains / period
    average_loss = losses / period
    if average_loss == 0:
        return 100
    rs = average_gain / average_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi
