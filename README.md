🌟 Dot Matrix Intelligence Briefing System 📜🖨️

Welcome to the Dot Matrix Intelligence Briefing System repository! This project combines modern AWS services with vintage computing to create a unique, interactive daily intelligence report, printed on a Panasonic KX-P1592 dot matrix printer via a Raspberry Pi at the press of a button. This project is designed to be an entertaining exploration of AWS architecture, IoT, and retro hardware integration. It's perfect for showing off practical AWS skills with a nostalgic flair. 🚀✨

## Project Overview 📈💡

The aim is to build an MVP that aggregates data from various open APIs (weather, security, market) using AWS services, formats the data into a daily intelligence report, and prints it via a classic dot matrix printer. This project includes the integration of modern technologies such as AWS Lambda, S3, DynamoDB, and IoT Core with the Raspberry Pi and the dot matrix printer, controlled with a simple push button.

## Project Features

- 🤖 **Automated Data Aggregation** using AWS Lambda
- 🔒 **Secure API Key Management** via AWS Secrets Manager
- 📡 **Real-Time Communication** between AWS and Raspberry Pi using AWS IoT Core
- 🖨️ **Vintage Dot Matrix Printing** for daily intelligence briefings
- ⚙️ **Retro Aesthetic**: ASCII text formatting with classic dot matrix printing

## File Structure 📂

```
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
```

## Repository Breakdown 🛠️

- **hardware/**: Contains diagrams and details of the physical components and connections.
- **raspberry_pi/**: Python scripts running on the Raspberry Pi, including the button listener, print daemon, and data aggregation logic.
- **docs/**: Guides for setting up hardware, AWS configuration, and debugging printer issues.
- **aws/**: Contains serverless code (Lambda functions) for data aggregation and IAM policies.
- **shared/**: Includes templates for formatting printed reports and utility scripts for data processing.

## Approach & Architecture 🌐🧩

### High-Level Architecture Diagram

```mermaid
graph TD;
    A[Push Button] --> B[Raspberry Pi];
    B --> C[AWS IoT Core];
    C <--> D[AWS Lambda Functions];
    B --> E[Printer];
    E <-- F[CUPS on Pi];
    F <-- G[Data from S3/DynamoDB];
```

### ASCII Diagram

```
+-------------------+
|    Push Button    |
+-------------------+
         |
         v
+-------------------+
|   Raspberry Pi    |
+-------------------+
         |
         v
+-------------------+       +-------------------+
|   AWS IoT Core    | <-->  | AWS Lambda Funcs  |
+-------------------+       +-------------------+
         |
         v
+-------------------+
|      Printer      |
+-------------------+
         ^
         |
+-------------------+
|   CUPS on Pi      |
+-------------------+
         ^
         |
+-------------------+
| Data from S3/DB   |
+-------------------+
```

## How It Works ⚙️

1. **Button Press**: A physical button press triggers the Raspberry Pi to start the daily process.
2. **Data Aggregation**: The Raspberry Pi connects to AWS IoT Core, which subscribes to MQTT topics published by Lambda functions.
3. **Data Formatting**: Aggregated data is formatted using ASCII templates.
4. **Printing**: The formatted briefing is printed by the Panasonic dot matrix printer.

## Getting Started 🏁

### Initial Setup Steps

1. **Clone the Repository**:
    ```sh
    git clone https://github.com/your-username/dot-matrix-intelligence-printer.git
    cd dot-matrix-intelligence-printer
    ```

2. **Install Dependencies**:
    ```sh
    pip install -r raspberry_pi/requirements.txt
    ```

3. **Setup Raspberry Pi**:
    - Install CUPS for printer management.
    - Set up AWS IoT credentials for Raspberry Pi.

## Contributing 🤝✨

Contributions are welcome! Please fork this repository, create a branch, make your changes, and submit a pull request. We use conventional commits for versioning.

- Tag releases with 🎉 for major changes, 🛠️ for bug fixes, and ✨ for new features.
- **Good First Issues**: Check out our beginner-friendly tasks to get started.

## Tags & Branches 🏷️

### Branches:

- **main**: Stable production code.
- **dev**: Experimental and new feature integration.

### Tags:

- **v0.1**: Initial setup and MVP testing.
- **v1.0**: First complete version with AWS integration.

## Architectural Diagrams & ASCII Drawings ✏️💻

All architectural diagrams are available in `docs/aws_configuration.md`. For that retro touch, ASCII diagrams have been provided to showcase the physical and digital flow of the project.

## License 📜

This project is licensed under the MIT License. Feel free to use, modify, and distribute it as per the license terms.

## Acknowledgments 🙌✨

Special thanks to the vintage computing community and AWS for providing the tools and inspiration to make projects like this possible. Enjoy the fun mix of old-school printing and modern cloud infrastructure! 🖨️☁️🚀