import json
import boto3
import requests
import time
import os

# Initialize AWS clients
secrets_client = boto3.client('secretsmanager', region_name='us-east-1')
dynamodb_client = boto3.resource('dynamodb', region_name='us-east-1')

# Reference to the DynamoDB table
table = dynamodb_client.Table('IntelligenceBriefingData')

# Retrieve API key from Secrets Manager
def get_api_key(secret_name):
    secret_value = secrets_client.get_secret_value(SecretId=secret_name)
    return json.loads(secret_value['SecretString'])['DotMatrixKey_openweathermap']

# Lambda handler function
def lambda_handler(event, context):
    try:
        # Define the secret name
        secret_name = 'DotMatrixKey_openweathermap'  # The name of your secret in Secrets Manager

        # Call get_api_key function with secret_name as the argument
        api_key = get_api_key(secret_name)
        
        # Make API call to fetch weather data
        city = "Dallas"
        response = requests.get(f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}')
        
        # Check for a successful response
        if response.status_code != 200:
            raise Exception(f"API request failed with status code {response.status_code}")

        weather_data = response.json()

        # Format the data for DynamoDB storage
        item = {
            'DataType': 'weather',
            'Timestamp': str(int(time.time())),
            'Location': city,
            'Temperature': weather_data['main']['temp'],
            'Description': weather_data['weather'][0]['description']
        }

        # Store the data in DynamoDB
        table.put_item(Item=item)

        return {
            'statusCode': 200,
            'body': json.dumps('Weather data successfully stored in DynamoDB!')
        }
    
    except requests.exceptions.RequestException as e:
        return {
            'statusCode': 500,
            'body': f"API Request Error: {str(e)}"
        }
    
    except Exception as e:
        return {
            'statusCode': 500,
            'body': f"Error: {str(e)}"
        }
