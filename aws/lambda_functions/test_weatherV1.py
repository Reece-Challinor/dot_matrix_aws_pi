
import unittest
from unittest.mock import patch, MagicMock
from weatherV1 import get_api_key, store_weather_data, create_response, lambda_handler

class TestWeatherV1(unittest.TestCase):
    @patch('weatherV1.secrets_client')
    def test_get_api_key_success(self, mock_secrets_client):
        # Mock the response from AWS Secrets Manager
        mock_secrets_client.get_secret_value.return_value = {
            'SecretString': json.dumps({'DotMatrixKey': 'test_api_key'})
        }
        api_key = get_api_key('test_secret')
        self.assertEqual(api_key, 'test_api_key')

    @patch('weatherV1.secrets_client')
    def test_get_api_key_failure(self, mock_secrets_client):
        # Simulate an exception when retrieving the secret
        mock_secrets_client.get_secret_value.side_effect = Exception('Error')
        with self.assertRaises(Exception):
            get_api_key('test_secret')

    @patch('weatherV1.table')
    def test_store_weather_data(self, mock_table):
        # Mock the DynamoDB table
        mock_table.put_item.return_value = {}
        store_weather_data('test_api_key')
        mock_table.put_item.assert_called_once()

    def test_create_response(self):
        response = create_response(200, 'Success')
        self.assertEqual(response['statusCode'], 200)
        self.assertIn('Success', response['body'])

    @patch('weatherV1.get_api_key')
    @patch('weatherV1.store_weather_data')
    def test_lambda_handler_success(self, mock_store_weather_data, mock_get_api_key):
        mock_get_api_key.return_value = 'test_api_key'
        mock_store_weather_data.return_value = None
        response = lambda_handler({}, {})
        self.assertEqual(response['statusCode'], 200)

if __name__ == '__main__':
    unittest.main()
