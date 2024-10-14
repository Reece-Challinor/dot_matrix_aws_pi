import json
import requests
import boto3
from botocore.exceptions import ClientError

# Initialize AWS clients
dynamodb = boto3.resource('dynamodb')
iot_client = boto3.client('iot-data')

# DynamoDB table name
DYNAMODB_TABLE = 'WeatherData'

# OpenWeatherMap API details
API_URL = 'http://api.openweathermap.org/data/2.5/weather'
API_KEY = 'your_openweathermap_api_key'
CITY = 'your_city'

def kelvin_to_fahrenheit(kelvin):
    """Convert temperature from Kelvin to Fahrenheit."""
    return (kelvin - 273.15) * 9/5 + 32

def lambda_handler(event, context):
    """AWS Lambda handler to fetch, normalize, store weather data and publish to IoT Core."""
    try:
        # Fetch weather data from OpenWeatherMap API
        response = requests.get(API_URL, params={'q': CITY, 'appid': API_KEY})
        response.raise_for_status()
        weather_data = response.json()
        
        # Normalize temperature data to Fahrenheit
        if 'main' in weather_data and 'temp' in weather_data['main']:
            weather_data['main']['temp'] = kelvin_to_fahrenheit(weather_data['main']['temp'])
        
        # Store weather data in DynamoDB
        table = dynamodb.Table(DYNAMODB_TABLE)
        table.put_item(Item={
            'City': CITY,
            'Timestamp': int(weather_data['dt']),
            'WeatherData': weather_data
        })
        
        # Publish message to AWS IoT Core
        iot_client.publish(
            topic='weather/update',
            qos=1,
            payload=json.dumps({'message': 'Weather data updated', 'city': CITY})
        )
        
        return {
            'statusCode': 200,
            'body': json.dumps('Weather data successfully retrieved, normalized, and stored.')
        }
    
    except requests.exceptions.RequestException as e:
        print(f"Error fetching weather data: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps(f'Failed to fetch weather data: {e}')
        }
    
    except ClientError as e:
        print(f"Error with AWS operation: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps(f'Failed to perform AWS operation: {e}')
        }
    
    except Exception as e:
        print(f"Unexpected error: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps(f'An unexpected error occurred: {e}')
        }