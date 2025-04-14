import os
from pathlib import Path

# Base paths
BASE_DIR = Path(__file__).parent.absolute()
CERTS_DIR = BASE_DIR / "certs"
LOG_DIR = Path("/var/log/dot_matrix_pi")

# Create log directory if it doesn't exist
os.makedirs(LOG_DIR, exist_ok=True)
os.makedirs(CERTS_DIR, exist_ok=True)

# AWS IoT Configuration
AWS_IOT_ENDPOINT = "your-aws-iot-endpoint.iot.region.amazonaws.com"  # Replace with your endpoint
AWS_IOT_PORT = 8883
AWS_IOT_TOPIC_BASE = "intelligence-briefing"
AWS_IOT_CLIENT_ID = "dot-matrix-pi"

# AWS IoT certificates
AWS_IOT_ROOT_CA = CERTS_DIR / "root-CA.crt"
AWS_IOT_CERT = CERTS_DIR / "certificate.pem.crt"
AWS_IOT_PRIVATE_KEY = CERTS_DIR / "private.pem.key"

# Printer configuration
PRINTER_NAME = "KX-P1592"  # Your dot matrix printer name in CUPS
PRINTER_PAGE_WIDTH = 80

# GPIO Configuration
BUTTON_PIN = 17
LED_PIN = 27
DEBOUNCE_TIME = 0.2  # seconds

# Temporary file locations
TEMP_DIR = Path("/tmp/dot_matrix_pi")
os.makedirs(TEMP_DIR, exist_ok=True)
TEMP_BRIEFING_FILE = TEMP_DIR / "current_briefing.txt"

# Data requirements
REQUIRED_DATA_CATEGORIES = ["weather", "market", "security"]