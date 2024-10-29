import boto3
import json
import time
import unittest
import logging
from datetime import datetime
from botocore.exceptions import ClientError
from typing import Dict, Any
from unittest.mock import patch

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TestAWSIntegration(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Set up AWS clients and configurations once for all tests"""
        cls.iot_client = boto3.client('iot-data')
        cls.dynamodb_client = boto3.client('dynamodb')
        cls.lambda_client = boto3.client('lambda')
        cls.s3_client = boto3.client('s3')
        cls.secrets_client = boto3.client('secretsmanager')
        
        # Configuration
        cls.iot_topic = 'intelligence-briefing/test'
        cls.dynamodb_table = 'HistoricalReports'
        cls.lambda_functions = {
            'weather': 'weather_lambda',
            'market': 'market_data_lambda',
            'security': 'security_alert_lambda'
        }
        cls.s3_bucket = 'report-templates'
        cls.secret_name = 'APIKeys'

    def setUp(self):
        """Set up test-specific resources"""
        self.test_id = f"test_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        logger.info(f"Starting test with ID: {self.test_id}")

    def test_end_to_end_workflow(self):
        """Test the complete workflow from data collection to storage"""
        try:
            # 1. Trigger Lambda functions
            lambda_results = self._trigger_all_lambdas()
            self.assertTrue(all(result['StatusCode'] == 200 for result in lambda_results))

            # 2. Verify MQTT messages
            mqtt_success = self._verify_mqtt_messages()
            self.assertTrue(mqtt_success)

            # 3. Check DynamoDB storage
            dynamo_success = self._verify_dynamodb_storage()
            self.assertTrue(dynamo_success)

        except Exception as e:
            logger.error(f"End-to-end workflow test failed: {str(e)}")
            raise

    def test_secrets_manager_access(self):
        """Test access to API keys in Secrets Manager"""
        try:
            response = self.secrets_client.get_secret_value(
                SecretId=self.secret_name
            )
            self.assertIn('SecretString', response)
            secrets = json.loads(response['SecretString'])
            required_keys = ['weather_api_key', 'market_api_key']
            self.assertTrue(all(key in secrets for key in required_keys))
        except ClientError as e:
            self.fail(f"Failed to access Secrets Manager: {str(e)}")

    def test_s3_template_access(self):
        """Test access to report templates in S3"""
        try:
            response = self.s3_client.list_objects_v2(
                Bucket=self.s3_bucket,
                Prefix='templates/'
            )
            self.assertIn('Contents', response)
            self.assertTrue(any('briefing_template.txt' in obj['Key'] for obj in response['Contents']))
        except ClientError as e:
            self.fail(f"Failed to access S3 templates: {str(e)}")

    def test_lambda_error_handling(self):
        """Test Lambda functions' error handling capabilities"""
        test_payloads = {
            'invalid_data': {'invalid': 'data'},
            'missing_required': {},
            'malformed_json': 'not_json'
        }
        
        for test_case, payload in test_payloads.items():
            with self.subTest(test_case=test_case):
                try:
                    response = self.lambda_client.invoke(
                        FunctionName=self.lambda_functions['weather'],
                        InvocationType='RequestResponse',
                        Payload=json.dumps(payload)
                    )
                    response_payload = json.loads(response['Payload'].read())
                    self.assertIn('error', response_payload)
                except ClientError as e:
                    self.fail(f"Lambda error handling test failed: {str(e)}")

    def test_dynamodb_data_consistency(self):
        """Test DynamoDB data consistency and constraints"""
        test_items = [
            {
                'ReportId': {'S': f"{self.test_id}_1"},
                'Timestamp': {'N': str(int(time.time()))},
                'Data': {'S': json.dumps({'test': 'data1'})}
            },
            {
                'ReportId': {'S': f"{self.test_id}_2"},
                'Timestamp': {'N': str(int(time.time()))},
                'Data': {'S': json.dumps({'test': 'data2'})}
            }
        ]

        try:
            # Test batch write
            self._batch_write_items(test_items)
            
            # Test batch read
            response = self._batch_get_items([item['ReportId']['S'] for item in test_items])
            self.assertEqual(len(response), len(test_items))

            # Test query
            query_response = self._query_items_by_timestamp(
                int(time.time()) - 3600,  # Last hour
                int(time.time())
            )
            self.assertTrue(len(query_response) >= len(test_items))

        except ClientError as e:
            self.fail(f"DynamoDB consistency test failed: {str(e)}")
        finally:
            self._cleanup_test_items(test_items)

    def _trigger_all_lambdas(self) -> list:
        """Helper method to trigger all Lambda functions"""
        results = []
        test_payload = {
            'test': True,
            'timestamp': int(time.time())
        }
        
        for lambda_name in self.lambda_functions.values():
            response = self.lambda_client.invoke(
                FunctionName=lambda_name,
                InvocationType='RequestResponse',
                Payload=json.dumps(test_payload)
            )
            results.append(response)
        return results

    def _verify_mqtt_messages(self) -> bool:
        """Helper method to verify MQTT message delivery"""
        test_message = {
            'test_id': self.test_id,
            'timestamp': int(time.time())
        }
        
        try:
            response = self.iot_client.publish(
                topic=self.iot_topic,
                qos=1,
                payload=json.dumps(test_message)
            )
            return response['ResponseMetadata']['HTTPStatusCode'] == 200
        except ClientError:
            return False

    def _verify_dynamodb_storage(self) -> bool:
        """Helper method to verify DynamoDB storage"""
        try:
            response = self.dynamodb_client.scan(
                TableName=self.dynamodb_table,
                Limit=1
            )
            return 'Items' in response and len(response['Items']) > 0
        except ClientError:
            return False

    def _batch_write_items(self, items: list):
        """Helper method for batch writing to DynamoDB"""
        request_items = {
            self.dynamodb_table: [
                {'PutRequest': {'Item': item}} for item in items
            ]
        }
        self.dynamodb_client.batch_write_item(RequestItems=request_items)

    def _batch_get_items(self, report_ids: list) -> list:
        """Helper method for batch reading from DynamoDB"""
        keys = [{'ReportId': {'S': rid}} for rid in report_ids]
        response = self.dynamodb_client.batch_get_item(
            RequestItems={
                self.dynamodb_table: {
                    'Keys': keys
                }
            }
        )
        return response['Responses'][self.dynamodb_table]

    def _query_items_by_timestamp(self, start_time: int, end_time: int) -> list:
        """Helper method to query items by timestamp range"""
        response = self.dynamodb_client.query(
            TableName=self.dynamodb_table,
            KeyConditionExpression='#ts BETWEEN :start AND :end',
            ExpressionAttributeNames={'#ts': 'Timestamp'},
            ExpressionAttributeValues={
                ':start': {'N': str(start_time)},
                ':end': {'N': str(end_time)}
            }
        )
        return response['Items']

    def _cleanup_test_items(self, items: list):
        """Helper method to clean up test items"""
        for item in items:
            try:
                self.dynamodb_client.delete_item(
                    TableName=self.dynamodb_table,
                    Key={'ReportId': item['ReportId']}
                )
            except ClientError as e:
                logger.warning(f"Failed to clean up test item: {str(e)}")

    def tearDown(self):
        """Clean up test-specific resources"""
        logger.info(f"Cleaning up test ID: {self.test_id}")

    @classmethod
    def tearDownClass(cls):
        """Clean up shared resources"""
        pass

    def test_aws_service_availability(self):
        """Test the availability of AWS services"""
        services = {
            'IoT Data Plane': self.iot_client.describe_endpoint,
            'DynamoDB': self.dynamodb_client.list_tables,
            'Lambda': self.lambda_client.list_functions,
            'S3': self.s3_client.list_buckets,
            'Secrets Manager': self.secrets_client.list_secrets
        }
        unavailable_services = []
        for service_name, func in services.items():
            try:
                func()
            except ClientError as e:
                logger.error(f"{service_name} is unavailable: {str(e)}")
                unavailable_services.append(service_name)
        self.assertFalse(unavailable_services, f"Unavailable services: {unavailable_services}")

    def test_iot_connectivity(self):
        """Test connectivity to AWS IoT Core"""
        try:
            response = self.iot_client.get_thing_shadow(
                thingName='test_thing'
            )
            self.assertEqual(response['ResponseMetadata']['HTTPStatusCode'], 200)
        except ClientError as e:
            self.fail(f"IoT connectivity test failed: {str(e)}")

    def test_lambda_permissions(self):
        """Test that Lambda functions have correct permissions"""
        for function_name in self.lambda_functions.values():
            try:
                policy = self.lambda_client.get_policy(FunctionName=function_name)
                self.assertIn('Policy', policy)
            except ClientError as e:
                self.fail(f"Lambda permissions test failed for {function_name}: {str(e)}")

if __name__ == '__main__':
    unittest.main(verbosity=2)