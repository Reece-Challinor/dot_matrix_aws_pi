import json
import boto3
import time
from typing import Dict, Any
from botocore.exceptions import ClientError

# Initialize AWS clients
secrets_client = boto3.client('secretsmanager', region_name='us-east-1')
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table('IntelligenceBriefingData')

def get_api_key(secret_name: str) -> str:
    """
    Retrieve API key from AWS Secrets Manager.
    
    Args:
        secret_name (str): Name of the secret in AWS Secrets Manager
        
    Returns:
        str: The API key
        
    Raises:
        ClientError: If there's an error retrieving the secret
        KeyError: If the expected key isn't found in the secret
    """
    try:
        secret_value = secrets_client.get_secret_value(SecretId=secret_name)
        return json.loads(secret_value['SecretString'])['DotMatrixKey']
    except ClientError as e:
        error_code = e.response['Error']['Code']
        error_message = e.response['Error']['Message']
        raise Exception(f"Failed to retrieve secret: {error_code} - {error_message}")

def store_weather_data(api_key: str) -> None:
    """
    Store weather data in DynamoDB.
    
    Args:
        api_key (str): The API key to be used for weather data retrieval
        
    Raises:
        ClientError: If there's an error writing to DynamoDB
    """
    item = {
        'DataType': 'weather',
        'Timestamp': str(int(time.time())),
        'WeatherStatus': 'API key retrieved successfully',
        'LastUpdated': time.strftime('%Y-%m-%d %H:%M:%S')
    }
    
    table.put_item(Item=item)

def create_response(status_code: int, message: str) -> Dict[str, Any]:
    """
    Create a standardized API response.
    
    Args:
        status_code (int): HTTP status code
        message (str): Response message
        
    Returns:
        Dict[str, Any]: Formatted API response
    """
    return {
        'statusCode': status_code,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        },
        'body': json.dumps({
            'message': message,
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
        })
    }

def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    Main Lambda handler function.
    
    Args:
        event (Dict[str, Any]): Lambda event data
        context (Any): Lambda context
        
    Returns:
        Dict[str, Any]: API response
    """
    try:
        # Retrieve API key
        secret_name = 'DotMatrixKey_openweathermap'
        api_key = get_api_key(secret_name)
        
        # Store data in DynamoDB
        store_weather_data(api_key)
        
        return create_response(
            200,
            'Weather data successfully added to IntelligenceBriefingData table!'
        )
        
    except ClientError as e:
        return create_response(
            500,
            f"AWS Service Error: {str(e)}"
        )
    except KeyError as e:
        return create_response(
            500,
            f"Configuration Error: Missing key {str(e)}"
        )
    except Exception as e:
        return create_response(
            500,
            f"Unexpected Error: {str(e)}"
        )