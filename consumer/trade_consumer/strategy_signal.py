import logging

import strategy_indicator_rsi15
import strategy_indicator_rsi5

# RSI threshold values
RSI15_THRESHOLD = 50
RSI5_THRESHOLD = 80


# 在DEMO中用rsi5和rsi15来模拟真实的指标，并根据和阈值的差作为信号强度
# 不满足的时候整体取反，是为了让DEMO的测试数据更加明显
def signal_rsi(data):
    rsi5 = strategy_indicator_rsi5.cal(data)
    rsi15 = strategy_indicator_rsi15.cal(data)

    if rsi5 <= RSI5_THRESHOLD or rsi15 <= RSI15_THRESHOLD:
        return -rsi5 + -rsi15

    return rsi5 - RSI5_THRESHOLD + rsi15 - RSI15_THRESHOLD


def default_signal():
    return 0


def get_signal(data, signal_type):
    match signal_type:
        case 'RSI':
            return signal_rsi(data)
        case _:
            return default_signal()
