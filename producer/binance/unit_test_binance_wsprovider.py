import unittest
from unittest.mock import patch, MagicMock
import producer.binance.binance_wsprovider as ws_provider


class TestWSS(unittest.TestCase):
    @patch('producer.binance.binance_wsprovider.send_to_kafka')
    def test_on_message(self, mock_send_to_kafka):
        # Create a mock WebSocket instance
        mock_ws = MagicMock()

        # Mock data
        data = {'price': '100', 'symbol': 'BTCUSDT'}

        # Call the on_message function with mock WebSocket and data
        ws_provider.on_message(mock_ws, data)

        # Assert that the send_to_kafka function was called with the correct parameters
        mock_send_to_kafka.assert_called_with(data)


if __name__ == '__main__':
    unittest.main()
