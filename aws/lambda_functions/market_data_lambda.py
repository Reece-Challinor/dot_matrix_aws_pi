import json
import boto3
import requests
from botocore.exceptions import ClientError

# Initialize AWS clients
dynamodb = boto3.resource('dynamodb')
iot_client = boto3.client('iot-data')

# DynamoDB table name
TABLE_NAME = 'MarketData'

# Public API URL
API_URL = 'https://api.example.com/marketdata'

def normalize_data(data):
    # Example normalization: Convert temperature to Fahrenheit if present
    if 'temperature' in data:
        data['temperature'] = data['temperature'] * 9/5 + 32
    return data

def lambda_handler(event, context):
    try:
        # Fetch market data from public API
        response = requests.get(API_URL)
        response.raise_for_status()
        market_data = response.json()

        # Normalize the data
        normalized_data = normalize_data(market_data)

        # Format the data
        formatted_data = {
            'id': normalized_data['id'],
            'price': normalized_data['price'],
            'timestamp': normalized_data['timestamp']
        }

        # Store data in DynamoDB
        table = dynamodb.Table(TABLE_NAME)
        table.put_item(Item=formatted_data)

        # Send data to AWS IoT Core
        iot_client.publish(
            topic='market/data',
            qos=1,
            payload=json.dumps(formatted_data)
        )

        return {
            'statusCode': 200,
            'body': json.dumps('Data processed successfully')
        }

    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from API: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps('Error fetching data from API')
        }
    except ClientError as e:
        print(f"Error interacting with AWS services: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps('Error interacting with AWS services')
        }
    except Exception as e:
        print(f"Unexpected error: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps('Unexpected error')
        }

# Unit tests
def test_lambda_handler_success(mocker):
    mocker.patch('requests.get', return_value=mocker.Mock(status_code=200, json=lambda: {'id': '1', 'price': '100', 'timestamp': '2023-10-01T00:00:00Z'}))
    mocker.patch('boto3.resource')
    mocker.patch('boto3.client')

    event = {}
    context = {}
    response = lambda_handler(event, context)
    assert response['statusCode'] == 200
    assert json.loads(response['body']) == 'Data processed successfully'

def test_lambda_handler_api_error(mocker):
    mocker.patch('requests.get', side_effect=requests.exceptions.RequestException('API error'))
    event = {}
    context = {}
    response = lambda_handler(event, context)
    assert response['statusCode'] == 500
    assert json.loads(response['body']) == 'Error fetching data from API'

def test_lambda_handler_aws_error(mocker):
    mocker.patch('requests.get', return_value=mocker.Mock(status_code=200, json=lambda: {'id': '1', 'price': '100', 'timestamp': '2023-10-01T00:00:00Z'}))
    mocker.patch('boto3.resource', side_effect=ClientError({'Error': {'Code': '500', 'Message': 'AWS error'}}, 'PutItem'))
    event = {}
    context = {}
    response = lambda_handler(event, context)
    assert response['statusCode'] == 500
    assert json.loads(response['body']) == 'Error interacting with AWS services'

# Integration test
def test_integration(mocker):
    mocker.patch('requests.get', return_value=mocker.Mock(status_code=200, json=lambda: {'id': '1', 'price': '100', 'timestamp': '2023-10-01T00:00:00Z'}))
    mocker.patch('boto3.resource')
    mocker.patch('boto3.client')

    event = {}
    context = {}
    response = lambda_handler(event, context)
    assert response['statusCode'] == 200
    assert json.loads(response['body']) == 'Data processed successfully'