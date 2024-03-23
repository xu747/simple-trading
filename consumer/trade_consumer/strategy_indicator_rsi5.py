import strategy_utils

PERIOD = 5


def cal(data):
    return strategy_utils.calculate_rsi(data['last_price'].tail(PERIOD).tolist(), period=PERIOD)
