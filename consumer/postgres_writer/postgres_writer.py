import json
import logging
import psycopg2
import simple_trading_config
from confluent_kafka import Consumer

# Config
logging.basicConfig(level=simple_trading_config.LOG_LEVEL)

KAFKA_BROKER = simple_trading_config.KAFKA_BROKER
KAFKA_TOPIC = simple_trading_config.KAFKA_TOPIC
KAFKA_CONSUMER_GROUP = 'price_consumer_pg'

POSTGRES_CONFIG = {
    'host': simple_trading_config.POSTGRES_HOST,
    'database': simple_trading_config.POSTGRES_DB,
    'user': simple_trading_config.POSTGRES_USER,
    'password': simple_trading_config.POSTGRES_PASSWORD
}

# Kafka Consumer setup
consumer = Consumer({
    'bootstrap.servers': KAFKA_BROKER,
    'group.id': KAFKA_CONSUMER_GROUP,
    'auto.offset.reset': 'latest'  # Start from latest messages
})


# If production, use connection pool instead.
def get_postgres_connection():
    if 'conn' not in globals():
        global conn
        conn = psycopg2.connect(**POSTGRES_CONFIG)
    return conn


# Get msg from kafka and store price to PG Database.
def store_price(kafka_msg):
    conn = get_postgres_connection()
    cursor = conn.cursor()

    kafka_data = json.loads(json.loads(kafka_msg))
    # unit test use
    # kafka_data = json.loads(kafka_msg)

    symbol = kafka_data["s"]
    price = float(kafka_data["c"])
    timestamp = int(kafka_data["E"])

    cursor.execute("""INSERT INTO crypto_prices (symbol, price, timestamp) VALUES (%s, %s, %s)""", (symbol, price, timestamp))
    conn.commit()

    logging.debug("Successfully Stored Symbol[{}] price[{}] timestamp[{}] To PG".format(symbol, price, timestamp))


def main():
    try:
        consumer.subscribe([KAFKA_TOPIC])

        while True:
            msg = consumer.poll(timeout=1.0)
            if msg is None:
                continue
            if msg.error():
                logging.error("Consumer error: {}".format(msg.error()))
                continue

            data = msg.value().decode('utf-8')
            store_price(data)
    except Exception as e:
        logging.error("Exception: {}".format(e))
    finally:
        consumer.close()
        conn.close()


if __name__ == '__main__':
    main()
