# AWS Configuration Overview

## Introduction
This document provides a detailed overview of the AWS services used in the Dot Matrix Intelligence Briefing System project. It covers the resources, their connections, data aggregation methods, integration testing, and AWS Well-Architected best practices.

## AWS Resources

### 1. AWS Lambda
- **Purpose**: Executes code in response to triggers such as changes in data or system state.
- **Functions**:
    - `weather_lambda.py`: Fetches weather data from an open API.
    - `market_data_lambda.py`: Retrieves market data.
    - `security_alert_lambda.py`: Collects security alerts.

### 2. AWS IoT Core
- **Purpose**: Facilitates real-time communication between AWS services and IoT devices.
- **Components**:
    - IoT Thing: Represents the Raspberry Pi.
    - MQTT Topics: Used for communication between Lambda functions and the Raspberry Pi.

### 3. AWS S3
- **Purpose**: Stores report templates and aggregated data.
- **Buckets**:
    - `report-templates`: Stores ASCII templates for the daily intelligence report.
    - `historical-data`: Archives past reports and data.

### 4. AWS DynamoDB
- **Purpose**: Provides a NoSQL database for storing historical data.
- **Tables**:
    - `HistoricalReports`: Stores metadata and content of past reports.

### 5. AWS Secrets Manager
- **Purpose**: Manages and retrieves API keys securely.
- **Secrets**:
    - `APIKeys`: Stores keys for accessing various open APIs.

## Architecture Diagram

```plaintext
[Push Button] --> [Raspberry Pi] --> [AWS IoT Core] <--> [AWS Lambda Functions]
                                                                            |                |
                                                                            v                v
                                                                    [Printer] <-- [CUPS on Pi] <-- [Data from S3/DynamoDB]
```

## Data Aggregation Process

1. **Button Press**: A physical button press triggers the Raspberry Pi to start the data aggregation process.
2. **Data Collection**: The Raspberry Pi connects to AWS IoT Core, which subscribes to MQTT topics published by Lambda functions.
3. **Data Formatting**: Aggregated data is formatted using ASCII templates stored in S3.
4. **Printing**: The formatted briefing is printed by the Panasonic dot matrix printer.

## Integration Testing

- **Unit Tests**: Each Lambda function includes unit tests to verify data retrieval and processing.
- **End-to-End Tests**: Simulate button presses and verify the complete flow from data aggregation to printing.
- **Mocking**: Use mock data to test the system without relying on external APIs.

## AWS Well-Architected Best Practices

### 1. Security
- Use IAM roles and policies to restrict access.
- Store API keys in AWS Secrets Manager.

### 2. Reliability
- Implement retries and error handling in Lambda functions.
- Use CloudWatch for monitoring and logging.

### 3. Performance Efficiency
- Optimize Lambda function code for quick execution.
- Use DynamoDB for fast data retrieval.

### 4. Cost Optimization
- Use AWS Free Tier where possible.
- Schedule Lambda functions to run only when needed.

### 5. Operational Excellence
- Automate deployments using AWS CloudFormation.
- Regularly review and update IAM policies.

## Additional Notes

- **Images and Diagrams**: Include architectural diagrams and wiring diagrams in the `docs/` directory.
- **Explainer GIFs**: Add GIFs to demonstrate the setup and operation process.

## Conclusion

This document provides a comprehensive overview of the AWS configuration for the Dot Matrix Intelligence Briefing System. Follow the best practices and guidelines to ensure a secure, reliable, and efficient setup.
