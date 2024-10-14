🌟 Dot Matrix Intelligence Briefing System 📜🖨️

Welcome to the Dot Matrix Intelligence Briefing System repository! This project combines modern AWS services with vintage computing to create a unique, interactive daily intelligence report, printed on a Panasonic KX-P1592 dot matrix printer via a Raspberry Pi at the press of a button. This project is designed to be an entertaining exploration of AWS architecture, IoT, and retro hardware integration. It's perfect for showing off practical AWS skills with a nostalgic flair. 🚀✨

Project Overview 📈💡

The aim is to build an MVP that aggregates data from various open APIs (weather, security, market) using AWS services, formats the data into a daily intelligence report, and prints it via a classic dot matrix printer. This project includes the integration of modern technologies such as AWS Lambda, S3, DynamoDB, and IoT Core with the Raspberry Pi and the dot matrix printer, controlled with a simple push button.

Project Features

🤖 Automated Data Aggregation using AWS Lambda

🔒 Secure API Key Management via AWS Secrets Manager

📡 Real-Time Communication between AWS and Raspberry Pi using AWS IoT Core

🖨️ Vintage Dot Matrix Printing for daily intelligence briefings

⚙️ Retro Aesthetic: ASCII text formatting with classic dot matrix printing

File Structure 📂

dot-matrix-intelligence-printer/
├── README.md
├── hardware/
│   ├── wiring_diagram.png
│   └── component_list.txt
├── raspberry_pi/
│   ├── button_listener.py
│   ├── print_daemon.py
│   ├── printer_interface.py
│   ├── data_aggregator.py
│   ├── config.py
│   └── requirements.txt
├── docs/
│   ├── setup_guide.md
│   ├── aws_configuration.md
│   └── printing_debugging.md
├── aws/
│   ├── lambda_functions/
│   │   ├── weather_lambda.py
│   │   ├── market_data_lambda.py
│   │   ├── security_alert_lambda.py
│   └── iam_policies/
│       └── lambda_execution_policy.json
└── shared/
    ├── templates/
    │   └── briefing_template.txt
    └── utils/
        └── data_formatter.py

Repository Breakdown 🛠️

hardware/: Contains diagrams and details of the physical components and connections.

raspberry_pi/: Python scripts running on the Raspberry Pi, including the button listener, print daemon, and data aggregation logic.

docs/: Guides for setting up hardware, AWS configuration, and debugging printer issues.

aws/: Contains serverless code (Lambda functions) for data aggregation and IAM policies.

shared/: Includes templates for formatting printed reports and utility scripts for data processing.

Approach & Architecture 🌐🧩

High-Level Architecture Diagram

[Push Button] --> [Raspberry Pi] --> [AWS IoT Core] <--> [AWS Lambda Functions]
                |                                     |
            [Printer] <-- [CUPS on Pi] <-- [Data from S3/DynamoDB]

Push Button: Triggers the Raspberry Pi to start the data aggregation process.

Raspberry Pi: Runs scripts to pull data from AWS and initiate the printing process.

AWS Lambda: Collects data from various open-source APIs and pushes it to AWS IoT Core.

AWS IoT Core: Facilitates real-time communication between Lambda and the Raspberry Pi.

S3 & DynamoDB: Stores historical data and report templates for use in report generation.

How It Works ⚙️

Button Press: A physical button press triggers the Raspberry Pi to start the daily process.

Data Aggregation: The Raspberry Pi connects to AWS IoT Core, which subscribes to MQTT topics published by Lambda functions.

Data Formatting: Aggregated data is formatted using ASCII templates.

Printing: The formatted briefing is printed by the Panasonic dot matrix printer.

Getting Started 🏁

Initial Setup Steps

Clone the Repository:

git clone https://github.com/your-username/dot-matrix-intelligence-printer.git
cd dot-matrix-intelligence-printer

Install Dependencies:

Install Python requirements:

pip install -r raspberry_pi/requirements.txt

Setup Raspberry Pi:

Install CUPS for printer management.

Set up AWS IoT credentials for Raspberry Pi.

Contributing 🤝✨

Contributions are welcome! Please fork this repository, create a branch, make your changes, and submit a pull request. We use conventional commits for versioning.

Tag releases with 🎉 for major changes, 🛠️ for bug fixes, and ✨ for new features.

Good First Issues: Check out our beginner-friendly tasks to get started.

Tags & Branches 🏷️

Branches:

main: Stable production code.

dev: Experimental and new feature integration.

Tags:

v0.1: Initial setup and MVP testing.

v1.0: First complete version with AWS integration.

Architectural Diagrams & ASCII Drawings ✏️💻

All architectural diagrams are available in docs/aws_configuration.md.

For that retro touch, ASCII diagrams have been provided to showcase the physical and digital flow of the project.

Prompts for GitHub Copilot 💡🤖

Below is a set of prompts for generating code using GitHub Copilot, based on the core components outlined above.

1. Lambda Function for Data Aggregation (Weather, Market, Security)

Prompt: "Write a Python AWS Lambda function that pulls data from an open-source API (e.g., OpenWeatherMap). Use boto3 to store the results in DynamoDB, and publish a message to AWS IoT Core for MQTT communication. Include error handling for failed API calls and AWS operations."

2. Button Listener Script (button_listener.py)

Prompt: "Create a Python script for the Raspberry Pi using WiringPi to listen for a button press on GPIO 17. When pressed, turn on an LED (GPIO 27), trigger another script (print_daemon.py), and turn off the LED when done. The script should handle debouncing the button input."

3. Print Daemon Script (print_daemon.py)

Prompt: "Write a Python script that subscribes to an AWS IoT MQTT topic, receives aggregated data, formats it into a plain text ASCII report, and sends it to the default printer on the system using CUPS. Use the paho-mqtt library for MQTT and subprocess to interact with CUPS."

4. AWS IoT Core Setup and MQTT Communication

Prompt: "Guide me through creating a Python script that connects to AWS IoT Core using the MQTT protocol. Include steps for authenticating with X.509 certificates and subscribing to a topic for receiving messages. Use the paho-mqtt library."

5. Data Formatter Utility (data_formatter.py)

Prompt: "Develop a Python utility script to take JSON input and format it into an ASCII layout for printing. It should support headers, footers, and structured sections, similar to an intelligence briefing. Include examples for formatting different types of data, such as tables and bullet points."

6. Soldering and Physical Setup Documentation (setup_guide.md)

Prompt: "Write step-by-step instructions for connecting a physical button to GPIO pins on a Raspberry Pi. Include a wiring diagram, the components needed, and best practices for soldering and insulation."

7. Error Handling and Debugging Print Issues (printing_debugging.md)

Prompt: "Document common issues that might arise when using a dot matrix printer with CUPS on a Raspberry Pi. Include troubleshooting steps for driver issues, incorrect formatting, and failed print jobs."

Appendix: GitHub Copilot Prompt Plan 🧩📜

This appendix outlines a comprehensive prompt plan and Copilot prompt library, serving as an overview for Copilot to understand the full project scope, structure, and architecture. Use this as a base to generate the code, unit tests, integration tests, and handle potential errors.

Project Overview Prompt

Prompt: "Provide an overview of a project that integrates AWS services with vintage computing to create a daily intelligence briefing printed using a dot matrix printer. The solution includes data aggregation, real-time communication, and physical interaction using Raspberry Pi GPIOs. File structure, Lambda functions, and the end-to-end workflow should be clearly explained."

GitHub Repository Structure and Initial Commit

Prompt: "Outline the initial commit for a GitHub repository that includes separate folders for hardware diagrams, AWS Lambda functions, Raspberry Pi scripts, documentation, and shared utilities. The project aims to create a daily intelligence briefing system using AWS, Raspberry Pi, and a vintage dot matrix printer. Include README, .gitignore, and necessary Python scripts."

Lambda Functions Prompt Plan

Weather Data Aggregation: "Create a Lambda function that calls the OpenWeatherMap API, processes the JSON response, and writes the results to DynamoDB. Publish the data to an AWS IoT Core MQTT topic for Raspberry Pi to retrieve."

Market Data Lambda: "Write a Lambda function in Python that fetches market data from a public API, formats it, stores it in DynamoDB, and sends it to AWS IoT Core. Include appropriate error handling."

Security Alerts Lambda: "Develop a Lambda function that queries a security alert API, processes the data, and sends it to AWS IoT Core. Store a copy in DynamoDB for historical reference."

Raspberry Pi Script Prompt Plan

Button Listener Script: "Develop a script that uses WiringPi to monitor GPIO 17 for a button press. When pressed, turn on an LED indicator, trigger the print daemon, and handle any button press debouncing."

Print Daemon Script: "Write a script that subscribes to MQTT topics on AWS IoT Core, processes the received data, formats it into an ASCII report, and uses CUPS to print the report on a dot matrix printer. Include error handling for network or print-related issues."

Printer Interface Script: "Create a Python script to interact with the CUPS server to manage print jobs. Include commands for checking the status of the printer and retrying failed print jobs."

Documentation Prompt Plan

Setup Guide: "Document the setup process for connecting physical hardware components like a button and LED to the Raspberry Pi. Include the wiring diagram, recommended tools, and soldering best practices."

AWS Configuration: "Write a guide on setting up AWS services for this project, including Lambda functions, IoT Core, Secrets Manager, and DynamoDB. Explain IAM roles and security best practices."

Printing Debugging: "List common issues and fixes for connecting and using a Panasonic dot matrix printer with CUPS on a Raspberry Pi. Include steps for diagnosing driver errors, print format issues, and physical connection problems."

Unit Testing & Integration Tests Prompt Plan

Unit Tests for Lambda Functions: "Create unit tests using pytest for the Lambda functions. Ensure each function correctly processes API responses and stores data in DynamoDB. Include mock API calls."

Integration Tests for AWS Services: "Write integration tests that verify the data flow between Lambda, IoT Core, and DynamoDB. Use boto3 to confirm the successful creation of items and correct MQTT topic publishing."

Raspberry Pi Scripts Testing: "Develop a testing script that validates the GPIO connections for button and LED. Simulate button presses and confirm the LED behavior, and validate that the print daemon is triggered appropriately."

Error Handling & Best Practices

Lambda Functions: "Incorporate retries and exponential backoff for failed API calls in Lambda functions. Add CloudWatch logging to monitor execution success and failures."

Raspberry Pi Print Daemon: "Implement try-except blocks around MQTT communication and print commands. Log errors to a local file and add retry logic for failed print jobs."

Connection Issues: "Document handling for network interruptions, particularly between Raspberry Pi and AWS IoT Core. Include code to detect connectivity issues and attempt reconnection."

License 📜

This project is licensed under the MIT License. Feel free to use, modify, and distribute it as per the license terms.

Acknowledgments 🙌✨

Special thanks to the vintage computing community and AWS for providing the tools and inspiration to make projects like this possible. Enjoy the fun mix of old-school printing and modern cloud infrastructure! 🖨️☁️🚀
