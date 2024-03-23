import logging

BINANCE_WSS_URL = "wss://stream.binance.com:9443/ws/"
# if you run this program in US, use the link below
# BINANCE_WSS_URL = "wss://stream.binance.us:9443/ws/"

# PG Credentials
POSTGRES_HOST = "postgres"
POSTGRES_PORT = 5432
POSTGRES_USER = "postgres"
POSTGRES_PASSWORD = "postgres"
POSTGRES_DB = "simple-trading"

# Kafka Configuration (replace if your Kafka cluster details differ)
KAFKA_BROKER = "kafka:9092"
KAFKA_TOPIC = "crypto_prices"

SYMBOLS = ["BTCUSDT", "ETHUSDT", "BNBUSDT"]
SIGNAL_TYPES = ['RSI']

LOG_LEVEL = logging.DEBUG

REDIS_HOST = "redis"
REDIS_PORT = 6379
