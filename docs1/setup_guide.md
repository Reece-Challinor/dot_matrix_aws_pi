# Dot Matrix Intelligence Briefing System Setup Guide

Welcome to the comprehensive setup guide for the Dot Matrix Intelligence Briefing System. This guide will walk you through the step-by-step process of setting up the Raspberry Pi, the dot matrix printer, AWS services, and the physical setup.

## Table of Contents
1. [Hardware Setup](#hardware-setup)
2. [Raspberry Pi Configuration](#raspberry-pi-configuration)
3. [AWS Configuration](#aws-configuration)
4. [Connecting Everything](#connecting-everything)
5. [Testing and Debugging](#testing-and-debugging)

## Hardware Setup

### Components Needed
- Raspberry Pi (any model with GPIO pins)
- Panasonic KX-P1592 dot matrix printer
- Push button
- Breadboard and jumper wires
- Power supply for Raspberry Pi

### Wiring Diagram
```
[Push Button] --> [GPIO Pin on Raspberry Pi]
[Printer] <--> [USB-to-Parallel Adapter] <--> [Raspberry Pi]
```

Refer to `hardware/wiring_diagram.png` for a detailed wiring diagram.

### Component List
Refer to `hardware/component_list.txt` for a detailed list of components.

## Raspberry Pi Configuration

### Initial Setup
1. **Install Raspbian OS**: Follow the official [Raspberry Pi OS installation guide](https://www.raspberrypi.org/documentation/installation/installing-images/).
2. **Update and Upgrade**:
    ```bash
    sudo apt-get update
    sudo apt-get upgrade
    ```

### Install Dependencies
1. **Clone the Repository**:
    ```bash
    git clone https://github.com/your-username/dot-matrix-intelligence-printer.git
    cd dot-matrix-intelligence-printer
    ```
2. **Install Python Dependencies**:
    ```bash
    pip install -r raspberry_pi/requirements.txt
    ```

### Setup CUPS for Printer Management
1. **Install CUPS**:
    ```bash
    sudo apt-get install cups
    ```
2. **Add User to lpadmin Group**:
    ```bash
    sudo usermod -aG lpadmin pi
    ```
3. **Configure Printer**:
    - Access CUPS web interface at `http://localhost:631`.
    - Add the Panasonic KX-P1592 printer.

### Configure AWS IoT Credentials
1. **Install AWS CLI**:
    ```bash
    sudo apt-get install awscli
    ```
2. **Configure AWS CLI**:
    ```bash
    aws configure
    ```
3. **Set Up IoT Credentials**:
    - Follow the instructions in `docs/aws_configuration.md`.

## AWS Configuration

### Create AWS Resources
1. **Create IAM Roles and Policies**:
    - Use the policy defined in `aws/iam_policies/lambda_execution_policy.json`.
2. **Set Up AWS IoT Core**:
    - Create a new IoT thing and configure certificates.
3. **Deploy Lambda Functions**:
    - Deploy the Lambda functions located in `aws/lambda_functions/`.

### Configure AWS Services
1. **S3 Buckets**:
    - Create an S3 bucket for storing report templates.
2. **DynamoDB Tables**:
    - Create DynamoDB tables for storing historical data.

## Connecting Everything

### High-Level Architecture Diagram
```
[Push Button] --> [Raspberry Pi] --> [AWS IoT Core] <--> [AWS Lambda Functions]
   |                                                |
[Printer] <-- [CUPS on Pi] <-- [Data from S3/DynamoDB]
```

### How It Works
1. **Button Press**: A physical button press triggers the Raspberry Pi to start the data aggregation process.
2. **Data Aggregation**: The Raspberry Pi connects to AWS IoT Core, which subscribes to MQTT topics published by Lambda functions.
3. **Data Formatting**: Aggregated data is formatted using ASCII templates.
4. **Printing**: The formatted briefing is printed by the Panasonic dot matrix printer.

## Testing and Debugging

### Initial Tests
1. **Test Button Listener**:
    ```bash
    python raspberry_pi/button_listener.py
    ```
2. **Test Print Daemon**:
    ```bash
    python raspberry_pi/print_daemon.py
    ```

### Debugging Tips
- Check the logs in AWS CloudWatch for Lambda function errors.
- Use `raspberry_pi/printing_debugging.md` for troubleshooting printer issues.

## Contributing

Contributions are welcome! Please fork this repository, create a branch, make your changes, and submit a pull request. We use conventional commits for versioning.

### Good First Issues
Check out our beginner-friendly tasks to get started.

### Tags & Branches
- **Branches**:
  - `main`: Stable production code.
  - `dev`: Experimental and new feature integration.
- **Tags**:
  - `v0.1`: Initial setup and MVP testing.
  - `v1.0`: First complete version with AWS integration.

Happy coding! 🚀✨