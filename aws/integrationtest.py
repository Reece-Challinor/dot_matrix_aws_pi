import boto3
import json
import time
import unittest
from botocore.exceptions import ClientError

class TestAWSIntegration(unittest.TestCase):

    def setUp(self):
        self.iot_client = boto3.client('iot-data')
        self.dynamodb_client = boto3.client('dynamodb')
        self.lambda_client = boto3.client('lambda')
        self.iot_topic = 'your/iot/topic'
        self.dynamodb_table = 'YourDynamoDBTable'
        self.lambda_function_name = 'YourLambdaFunction'

    def test_mqtt_publish(self):
        payload = {
            'message': 'Test message'
        }
        try:
            response = self.iot_client.publish(
                topic=self.iot_topic,
                qos=1,
                payload=json.dumps(payload)
            )
            self.assertEqual(response['ResponseMetadata']['HTTPStatusCode'], 200)
        except ClientError as e:
            self.fail(f"Failed to publish to MQTT topic: {e}")

    def test_lambda_invocation(self):
        payload = {
            'key': 'value'
        }
        try:
            response = self.lambda_client.invoke(
                FunctionName=self.lambda_function_name,
                InvocationType='RequestResponse',
                Payload=json.dumps(payload)
            )
            response_payload = json.loads(response['Payload'].read())
            self.assertEqual(response['StatusCode'], 200)
            self.assertIn('status', response_payload)
            self.assertEqual(response_payload['status'], 'success')
        except ClientError as e:
            self.fail(f"Failed to invoke Lambda function: {e}")

    def test_dynamodb_insertion(self):
        item = {
            'PrimaryKey': {'S': 'TestKey'},
            'Attribute': {'S': 'TestValue'}
        }
        try:
            response = self.dynamodb_client.put_item(
                TableName=self.dynamodb_table,
                Item=item
            )
            self.assertEqual(response['ResponseMetadata']['HTTPStatusCode'], 200)
        except ClientError as e:
            self.fail(f"Failed to insert item into DynamoDB: {e}")

    def test_dynamodb_retrieval(self):
        key = {
            'PrimaryKey': {'S': 'TestKey'}
        }
        try:
            response = self.dynamodb_client.get_item(
                TableName=self.dynamodb_table,
                Key=key
            )
            self.assertIn('Item', response)
            self.assertEqual(response['Item']['Attribute']['S'], 'TestValue')
        except ClientError as e:
            self.fail(f"Failed to retrieve item from DynamoDB: {e}")

    def tearDown(self):
        # Clean up DynamoDB table
        key = {
            'PrimaryKey': {'S': 'TestKey'}
        }
        try:
            self.dynamodb_client.delete_item(
                TableName=self.dynamodb_table,
                Key=key
            )
        except ClientError as e:
            print(f"Failed to clean up DynamoDB table: {e}")

if __name__ == '__main__':
    unittest.main()