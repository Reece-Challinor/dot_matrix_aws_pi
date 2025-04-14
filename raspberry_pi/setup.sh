#!/bin/bash
# Setup script for Dot Matrix Intelligence Briefing System
# Run this on your Raspberry Pi to set up dependencies and configuration

echo "===== Dot Matrix Intelligence Briefing System Setup ====="

# Check for root privileges
if [ "$EUID" -ne 0 ]; then
  echo "Please run as root (use sudo)"
  exit 1
fi

# Install dependencies
echo "Installing dependencies..."
apt-get update
apt-get install -y python3-pip cups cups-bsd wiringpi

# Install Python dependencies
echo "Installing Python packages..."
pip3 install paho-mqtt requests

# Create necessary directories
echo "Creating directories..."
mkdir -p /var/log/dot_matrix_pi
mkdir -p ./certs

# Set permissions
echo "Setting permissions..."
chmod 755 *.py
chmod +x test_printer.py setup.sh

# Configure CUPS service
echo "Ensuring CUPS is running..."
systemctl enable cups
systemctl start cups

# Setup complete
echo ""
echo "Setup complete! Next steps:"
echo "1. Update config.py with your AWS IoT Core endpoint and credentials"
echo "2. Copy your AWS IoT certificates to the ./certs directory:"
echo "   - root-CA.crt"
echo "   - certificate.pem.crt"
echo "   - private.pem.key"
echo "3. Configure your printer in CUPS: http://localhost:631"
echo "4. Run the test script: sudo python3 test_printer.py"
echo "5. Start the system: sudo python3 button_listener.py"
echo ""
echo "For more information, see the documentation in the docs directory."