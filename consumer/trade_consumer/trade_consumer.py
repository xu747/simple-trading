import json
import logging
import pandas as pd
import redis
from datetime import datetime
from confluent_kafka import Consumer

import simple_trading_config
import strategy_signal

logging.basicConfig(level=simple_trading_config.LOG_LEVEL)

# Configuration
KAFKA_BROKER = simple_trading_config.KAFKA_BROKER
KAFKA_TOPIC = simple_trading_config.KAFKA_TOPIC
KAFKA_CONSUMER_GROUP = 'trade_consumer'

SYMBOLS = simple_trading_config.SYMBOLS
SIGNAL_TYPES = simple_trading_config.SIGNAL_TYPES

df_symbol_data = {}  # Dataframe to store tick binance data for each symbol

redis_client = redis.Redis(host=simple_trading_config.REDIS_HOST, port=simple_trading_config.REDIS_PORT, db=0)


# Update signal for each symbol and store in redis
def update_signal():
    for symbol in SYMBOLS:
        for signal_type in SIGNAL_TYPES:
            logging.debug("Updating signal_type {} for {}".format(signal_type, symbol))
            new_signal = strategy_signal.get_signal(df_symbol_data[symbol], signal_type)
            logging.debug("symbol: {}, signal: {} signal_type {}".format(symbol, new_signal, signal_type))
            redis_client.zadd(signal_type, {symbol: new_signal})


# Process incoming Kafka messages and update the DataFrame with the latest data for each symbol.
def process_messages(msg):
    # Parse the message
    message_data = json.loads(json.loads(msg.value()))
    symbol = message_data['s']
    timestamp = datetime.fromtimestamp(message_data['E'] / 1000.0)
    last_price = message_data['c']

    logging.debug("Get new data, symbol: {}, price: {}, timestamp: {}".format(symbol, last_price, timestamp))

    # """
    # {
    #   "e": "24hrTicker",  // Event type
    #   "E": 1672515782136, // Event time
    #   "s": "BNBBTC",      // Symbol
    #   "p": "0.0015",      // Price change
    #   "P": "250.00",      // Price change percent
    #   "w": "0.0018",      // Weighted average price
    #   "x": "0.0009",      // First trade(F)-1 price (first trade before the 24hr rolling window)
    #   "c": "0.0025",      // Last price
    #   "Q": "10",          // Last quantity
    #   "b": "0.0024",      // Best bid price
    #   "B": "10",          // Best bid quantity
    #   "a": "0.0026",      // Best ask price
    #   "A": "100",         // Best ask quantity
    #   "o": "0.0010",      // Open price
    #   "h": "0.0025",      // High price
    #   "l": "0.0010",      // Low price
    #   "v": "10000",       // Total traded base asset volume
    #   "q": "18",          // Total traded quote asset volume
    #   "O": 0,             // Statistics open time
    #   "C": 86400000,      // Statistics close time
    #   "F": 0,             // First trade ID
    #   "L": 18150,         // Last trade Id
    #   "n": 18151          // Total number of trades
    # }
    # """

    # 在df中存储所有数据, 方便后续有新策略需要使用
    new_entry = {
        'timestamp': timestamp,
        'price_change': message_data['p'],
        'price_change_percent': message_data['P'],
        'weighted_average_price': message_data['w'],
        'last_price': message_data['c'],
        'last_quantity': message_data['Q'],
        'best_bid_price': message_data['b'],
        'best_bid_quantity': message_data['B'],
        'best_ask_price': message_data['a'],
        'best_ask_quantity': message_data['A'],
        'open_price': message_data['o'],
        'high_price': message_data['h'],
        'low_price': message_data['l'],
        'total_traded_base_asset_volume': message_data['v'],
        'total_traded_quote_asset_volume': message_data['q']
    }

    # Check if the symbol is already in the DataFrame
    if symbol not in df_symbol_data:
        df_symbol_data[symbol] = pd.DataFrame(columns=new_entry.keys())

    # Convert the new entry to a DataFrame
    new_entry_df = pd.DataFrame([new_entry])

    # Append the new data
    if df_symbol_data[symbol].empty:
        df_symbol_data[symbol] = new_entry_df
    else:
        # Ensure that the new entry has the same dtypes as the existing data
        new_entry_df = new_entry_df.astype(df_symbol_data[symbol].dtypes)
        df_symbol_data[symbol] = pd.concat([df_symbol_data[symbol], new_entry_df], ignore_index=True)

    # Keep only the last 30 minutes of data
    time_cutoff = timestamp - pd.Timedelta(minutes=30)
    df_symbol_data[symbol] = df_symbol_data[symbol][df_symbol_data[symbol]['timestamp'] > time_cutoff]

    # logging.debug("df_symbol_data[{}]: {}".format(symbol, df_symbol_data[symbol].tail(1)))

    return df_symbol_data


def main():
    consumer = Consumer({
        'bootstrap.servers': KAFKA_BROKER,
        'group.id': KAFKA_CONSUMER_GROUP,
        'auto.offset.reset': 'latest'  # Start from latest messages
    })
    consumer.subscribe([KAFKA_TOPIC])

    msg_count = 0

    try:
        while True:
            msg = consumer.poll(1.0)
            if msg is not None:
                process_messages(msg)
                msg_count += 1

            # After 15 new prices, update signal.
            if msg_count % (len(SYMBOLS) * 15) == 0 and msg_count > 0:
                msg_count = 0
                update_signal()

    except Exception as e:
        logging.error("Exception: {}".format(e))
    finally:
        consumer.close()
        redis_client.close()


if __name__ == '__main__':
    main()
