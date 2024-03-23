import unittest
import unittest.mock as mock
import json
from trade_consumer import (
    process_messages,
    df_symbol_data
)


class TestTradeConsumer(unittest.TestCase):

    def setUp(self):
        # Reset any shared data structures before each test
        df_symbol_data.clear()

    @mock.patch('redis.Redis')
    def test_process_messages(self, mock_redis):
        # Create a mock message with the demo data
        sample_data = {
            "e": "24hrTicker",
            "E": 1672515782136,
            "s": "BNBBTC",
            "p": "0.0015",
            "P": "250.00",
            "w": "0.0018",
            "x": "0.0009",
            "c": "0.0025",
            "Q": "10",
            "b": "0.0024",
            "B": "10",
            "a": "0.0026",
            "A": "100",
            "o": "0.0010",
            "h": "0.0025",
            "l": "0.0010",
            "v": "10000",
            "q": "18",
            "O": 0,
            "C": 86400000,
            "F": 0,
            "L": 18150,
            "n": 18151
        }

        mock_msg = mock.Mock()
        mock_msg.value.return_value = json.dumps(json.dumps(sample_data))

        # Call the function
        df_result = process_messages(mock_msg)

        # Assert data in df
        assert 'BNBBTC' in df_result
        assert not df_result['BNBBTC'].empty

        # Assert data correct
        last_price = df_result['BNBBTC'].iloc[-1]['last_price']
        assert float(last_price) == float(sample_data['c'])


if __name__ == '__main__':
    unittest.main()
