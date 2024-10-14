import json
import unittest
from unittest.mock import patch, MagicMock
from aws.lambda_functions.security_alert_lambda import lambda_handler

class TestLambdaHandler(unittest.TestCase):

    @patch('aws.lambda_functions.security_alert_lambda.requests.get')
    @patch('aws.lambda_functions.security_alert_lambda.iot_client.publish')
    @patch('aws.lambda_functions.security_alert_lambda.table.put_item')
    def test_lambda_handler_success(self, mock_put_item, mock_publish, mock_get):
        # Mock the API response
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = [
            {'temperature': 25, 'unit': 'C', 'alert': 'Intrusion detected'}
        ]

        # Mock the context object
        context = MagicMock()

        # Call the lambda handler
        event = {}
        response = lambda_handler(event, context)

        # Assertions
        self.assertEqual(response['statusCode'], 200)
        self.assertEqual(json.loads(response['body']), 'Alerts processed successfully')
        mock_publish.assert_called_once()
        mock_put_item.assert_called_once()

    @patch('aws.lambda_functions.security_alert_lambda.requests.get')
    def test_lambda_handler_api_failure(self, mock_get):
        # Mock the API response to raise an exception
        mock_get.side_effect = requests.exceptions.RequestException("API failure")

        # Mock the context object
        context = MagicMock()

        # Call the lambda handler
        event = {}
        response = lambda_handler(event, context)

        # Assertions
        self.assertEqual(response['statusCode'], 500)
        self.assertEqual(json.loads(response['body']), 'Error querying the security alert API')

    @patch('aws.lambda_functions.security_alert_lambda.requests.get')
    @patch('aws.lambda_functions.security_alert_lambda.iot_client.publish')
    @patch('aws.lambda_functions.security_alert_lambda.table.put_item')
    def test_lambda_handler_aws_failure(self, mock_put_item, mock_publish, mock_get):
        # Mock the API response
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = [
            {'temperature': 25, 'unit': 'C', 'alert': 'Intrusion detected'}
        ]

        # Mock AWS service to raise an exception
        mock_publish.side_effect = boto3.exceptions.Boto3Error("AWS IoT Core failure")

        # Mock the context object
        context = MagicMock()

        # Call the lambda handler
        event = {}
        response = lambda_handler(event, context)

        # Assertions
        self.assertEqual(response['statusCode'], 500)
        self.assertEqual(json.loads(response['body']), 'Error interacting with AWS services')

    @patch('aws.lambda_functions.security_alert_lambda.requests.get')
    @patch('aws.lambda_functions.security_alert_lambda.iot_client.publish')
    @patch('aws.lambda_functions.security_alert_lambda.table.put_item')
    def test_lambda_handler_unexpected_failure(self, mock_put_item, mock_publish, mock_get):
        # Mock the API response
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = [
            {'temperature': 25, 'unit': 'C', 'alert': 'Intrusion detected'}
        ]

        # Mock an unexpected exception
        mock_publish.side_effect = Exception("Unexpected error")

        # Mock the context object
        context = MagicMock()

        # Call the lambda handler
        event = {}
        response = lambda_handler(event, context)

        # Assertions
        self.assertEqual(response['statusCode'], 500)
        self.assertEqual(json.loads(response['body']), 'Unexpected error occurred')

if __name__ == '__main__':
    unittest.main()