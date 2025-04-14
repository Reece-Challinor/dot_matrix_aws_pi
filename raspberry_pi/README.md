# Raspberry Pi Components for Dot Matrix Intelligence Briefing System

This directory contains the code that runs on your Raspberry Pi to connect with AWS IoT Core and control the dot matrix printer.

## Components

- **button_listener.py**: Monitors a physical button connected to the Raspberry Pi GPIO pins and triggers the print process when pressed
- **data_aggregator.py**: Collects data from AWS IoT Core and formats it for printing
- **print_daemon.py**: Handles communication with the printer and manages the print queue
- **printer_interface.py**: Provides an interface to the dot matrix printer via CUPS
- **config.py**: Contains configuration settings for the system
- **test_printer.py**: Test script to verify printer setup and functionality
- **setup.sh**: Setup script to install dependencies and configure the system

## Hardware Requirements

- Raspberry Pi (model 3 or newer recommended)
- Push button
- LED (optional, for status indication)
- Panasonic KX-P1592 dot matrix printer (or similar)
- USB to parallel adapter (if your printer uses a parallel port)

## Setup Instructions

1. **Copy Files**:
   - Copy all files in this directory to your Raspberry Pi

2. **Run Setup Script**:
   ```bash
   sudo chmod +x setup.sh
   sudo ./setup.sh
   ```

3. **Configure Settings**:
   - Edit `config.py` with your AWS IoT Core endpoint and settings
   - Place your AWS IoT certificates in the `certs` directory

4. **Set Up Printer**:
   - Connect your dot matrix printer to the Raspberry Pi
   - Configure the printer in CUPS (http://localhost:631)
   - The default printer name in the code is "KX-P1592" - update in config.py if yours is different

5. **Run Tests**:
   ```bash
   sudo python3 test_printer.py
   ```

6. **Start the System**:
   ```bash
   sudo python3 button_listener.py
   ```

## Troubleshooting

- **Printer Not Found**: Verify printer is configured in CUPS with `lpstat -p`
- **MQTT Connection Issues**: Check AWS IoT Core credentials and endpoint
- **GPIO Errors**: Verify wiring and GPIO pin configuration in config.py

## Operating Instructions

1. Press the button to trigger the intelligence briefing process
2. The system will:
   - Connect to AWS IoT Core
   - Retrieve the latest data
   - Format a briefing document
   - Send it to the printer

The LED will indicate status:
- Solid: Processing
- Blink twice: Success
- Rapid blinking: Error

## Logs

Logs are stored in `/var/log/dot_matrix_pi/` and include:
- button_controller.log
- data_aggregator.log
- print_daemon.log