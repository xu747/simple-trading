import json
import logging
import socket
import simple_trading_config
import websocket
from confluent_kafka import Producer

#Config
logging.basicConfig(level=simple_trading_config.LOG_LEVEL)


# Kafka Configuration
KAFKA_BROKER = simple_trading_config.KAFKA_BROKER
KAFKA_TOPIC = simple_trading_config.KAFKA_TOPIC
BINANCE_WSS_URL = simple_trading_config.BINANCE_WSS_URL


# Symbols to track
SYMBOLS = simple_trading_config.SYMBOLS

conf = {'bootstrap.servers': KAFKA_BROKER,
        'client.id': socket.gethostname()}
producer = Producer(conf)


# add this function for pre-process binance data before sending to kafka.
def on_message(ws, data):
    logging.debug("Received message from binance: {}".format(data))
    send_to_kafka(data)


def send_to_kafka(message):
    producer.produce(KAFKA_TOPIC, value=json.dumps(message).encode('utf-8'))
    producer.flush()
    logging.debug("Sent message to kafka: {}".format(message))


def main():
    wss_endpoint = BINANCE_WSS_URL + "/".join([s.lower() + "@ticker" for s in SYMBOLS])
    ws = websocket.WebSocketApp(wss_endpoint, on_message=on_message)
    ws.run_forever()


if __name__ == "__main__":
    main()
