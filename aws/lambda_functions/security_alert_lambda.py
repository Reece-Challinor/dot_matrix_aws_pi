import json
import boto3
import requests
from botocore.exceptions import ClientError

# Initialize AWS clients
iot_client = boto3.client('iot-data')
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('SecurityAlerts')

def lambda_handler(event, context):
    try:
        # Query the security alert API
        response = requests.get('https://api.securityalerts.com/alerts')
        response.raise_for_status()
        alerts = response.json()

        # Process and send data to AWS IoT Core
        for alert in alerts:
            payload = json.dumps(alert)
            iot_client.publish(
                topic='security/alerts',
                qos=1,
                payload=payload
            )

            # Store a copy in DynamoDB
            table.put_item(Item=alert)

        return {
            'statusCode': 200,
            'body': json.dumps('Alerts processed successfully')
        }

    except requests.exceptions.RequestException as e:
        print(f"Error querying the security alert API: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps('Error querying the security alert API')
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
            'body': json.dumps('Unexpected error occurred')
        }