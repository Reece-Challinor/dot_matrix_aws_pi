import json
import boto3
import time

# Initialize AWS clients
secrets_client = boto3.client('secretsmanager', region_name='us-east-1')
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')

# Reference to the DynamoDB table
table = dynamodb.Table('IntelligenceBriefingData')

# Retrieve API key from Secrets Manager
def get_api_key(secret_name):
    secret_value = secrets_client.get_secret_value(SecretId=secret_name)
    print(f"Retrieved secret value: {secret_value}")  # Debugging statement
    return json.loads(secret_value['SecretString'])['DotMatrixKey']  # Corrected key name here

# Lambda handler function
def lambda_handler(event, context):
    try:
        # Step 1: Retrieve OpenWeatherMap API key
        secret_name = 'DotMatrixKey_openweathermap'  # The name of your secret in Secrets Manager
        api_key = get_api_key(secret_name)
        
        # Use a placeholder item until we verify successful retrieval of the key
        item = {
            'DataType': 'weather',  # Partition key for DynamoDB
            'Timestamp': str(int(time.time())),  # Unique timestamp for sorting
            'WeatherStatus': f'Using API key {api_key} to fetch data.'  # Placeholder message showing we retrieved the key
        }

        # Put the item into the DynamoDB table
        table.put_item(Item=item)

        return {
            'statusCode': 200,
            'body': json.dumps('Weather data successfully added to IntelligenceBriefingData table!')
        }

    except KeyError as e:
        return {
            'statusCode': 500,
            'body': f"KeyError: {str(e)} - Please check the key names in the secret."
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': f"Error: {str(e)}"
        }
