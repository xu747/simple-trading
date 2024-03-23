import json
import unittest
from unittest.mock import patch, MagicMock
from postgres_writer import store_price, get_postgres_connection


@patch('postgres_writer.Consumer')
@patch('postgres_writer.get_postgres_connection')
class TestStorePrice(unittest.TestCase):
    def test_store_price(self, mock_get_conn, mock_kafka_consumer):
        # Set up the mock connection and cursor for PostgreSQL
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_conn.commit = MagicMock()
        mock_get_conn.return_value = mock_conn

        # Set up the mock Kafka consumer
        mock_consumer = MagicMock()
        mock_kafka_consumer.return_value = mock_consumer
        mock_consumer.poll.return_value = None  # Simulate no message being polled

        # Example Kafka message
        kafka_msg = """
        {"s": "BTCUSDT","c": "50000", "E": "1609459200000"}
        """.encode('utf-8')

        # Call the function
        store_price(kafka_msg)

        # Assert if the cursor executed with the correct query and data
        mock_cursor.execute.assert_called_once_with(
            """INSERT INTO crypto_prices (symbol, price, timestamp) VALUES (%s, %s, %s)""",
            ("BTCUSDT", 50000.0, 1609459200000))

        # Assert if the commit was called once
        self.assertTrue(mock_conn.commit.called)


if __name__ == '__main__':
    unittest.main()
