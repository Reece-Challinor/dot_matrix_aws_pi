import subprocess
import json
import time
import logging
from typing import Dict, Any
import paho.mqtt.client as mqtt
from datetime import datetime
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/var/log/print_daemon.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('print_daemon')

class PrintDaemon:
    def __init__(self):
        # MQTT Configuration
        self.mqtt_broker = "your-aws-iot-endpoint.iot.region.amazonaws.com"
        self.mqtt_port = 8883  # Standard AWS IoT Core MQTT port
        self.mqtt_topic = "intelligence-briefing/#"
        
        # Printer Configuration
        self.printer_name = "KX-P1592"  # Your dot matrix printer name in CUPS
        self.page_width = 80  # Standard dot matrix page width
        self.temp_file = Path("/tmp/current_briefing.txt")
        
        # Data Storage
        self.current_data: Dict[str, Any] = {}
        
        # Initialize MQTT Client
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.on_disconnect = self.on_disconnect
        
        # AWS IoT Core Certificate Configuration
        self.client.tls_set(
            ca_certs="/path/to/root-CA.crt",
            certfile="/path/to/certificate.pem.crt",
            keyfile="/path/to/private.pem.key"
        )

    def check_printer_status(self) -> bool:
        """Check if printer is ready and online"""
        try:
            result = subprocess.run(
                ['lpstat', '-p', self.printer_name],
                capture_output=True,
                text=True
            )
            return "enabled" in result.stdout and "idle" in result.stdout
        except subprocess.SubProcessError as e:
            logger.error(f"Error checking printer status: {e}")
            return False

    def format_header(self) -> str:
        """Create ASCII header for the report"""
        now = datetime.now()
        header = "=" * self.page_width + "\n"
        header += "DAILY INTELLIGENCE BRIEFING\n"
        header += f"Generated: {now.strftime('%Y-%m-%d %H:%M:%S')}\n"
        header += "=" * self.page_width + "\n\n"
        return header

    def format_section(self, title: str, data: Dict[str, Any]) -> str:
        """Format a section of the report"""
        section = f"\n{title.upper()}\n"
        section += "-" * len(title) + "\n"
        
        for key, value in data.items():
            # Format key-value pairs, handling multi-line values
            if isinstance(value, (dict, list)):
                section += f"{key}:\n"
                formatted_value = json.dumps(value, indent=2)
                # Indent multi-line values
                section += "\n".join(f"  {line}" for line in formatted_value.split("\n"))
                section += "\n"
            else:
                section += f"{key}: {value}\n"
        
        return section + "\n"

    def format_report(self) -> str:
        """Format the complete report with all sections"""
        report = self.format_header()
        
        # Add sections based on available data
        sections = {
            "Weather Information": self.current_data.get("weather", {}),
            "Market Updates": self.current_data.get("market", {}),
            "Security Alerts": self.current_data.get("security", {}),
        }
        
        for title, data in sections.items():
            if data:  # Only add section if data exists
                report += self.format_section(title, data)
        
        report += "\n" + "=" * self.page_width + "\n"
        report += "End of Report\n"
        return report

    def send_to_printer(self, report: str) -> bool:
        """Send the formatted report to the dot matrix printer"""
        try:
            # Save report to temporary file
            self.temp_file.write_text(report)
            
            # Configure print options for dot matrix printer
            print_options = [
                'lp',
                '-d', self.printer_name,
                '-o', 'raw',  # Send raw text to printer
                '-o', 'cpi=10',  # Characters per inch
                '-o', 'lpi=6',  # Lines per inch
                str(self.temp_file)
            ]
            
            # Send to printer
            result = subprocess.run(print_options, capture_output=True, text=True)
            
            if result.returncode == 0:
                logger.info("Report successfully sent to printer")
                return True
            else:
                logger.error(f"Printer error: {result.stderr}")
                return False
                
        except Exception as e:
            logger.error(f"Error sending to printer: {e}")
            return False
        finally:
            # Cleanup temporary file
            if self.temp_file.exists():
                self.temp_file.unlink()

    def on_connect(self, client, userdata, flags, rc):
        """Callback when connected to MQTT broker"""
        if rc == 0:
            logger.info("Connected to MQTT broker")
            client.subscribe(self.mqtt_topic)
        else:
            logger.error(f"Failed to connect to MQTT broker with code: {rc}")

    def on_message(self, client, userdata, msg):
        """Handle incoming MQTT messages"""
        try:
            topic = msg.topic
            payload = json.loads(msg.payload.decode())
            
            # Extract category from topic (e.g., "intelligence-briefing/weather" -> "weather")
            category = topic.split('/')[-1]
            
            # Update current data for this category
            self.current_data[category] = payload
            logger.info(f"Received {category} data")
            
            # Check if we have all required data categories
            required_categories = {"weather", "market", "security"}
            if required_categories.issubset(self.current_data.keys()):
                if self.check_printer_status():
                    report = self.format_report()
                    if self.send_to_printer(report):
                        # Clear current data after successful print
                        self.current_data.clear()
                else:
                    logger.error("Printer not ready")
                    
        except json.JSONDecodeError as e:
            logger.error(f"Error decoding message: {e}")
        except Exception as e:
            logger.error(f"Error processing message: {e}")

    def on_disconnect(self, client, userdata, rc):
        """Handle MQTT disconnection"""
        logger.warning("Disconnected from MQTT broker")
        if rc != 0:
            logger.error(f"Unexpected disconnection. Reconnecting...")
            self.connect()

    def connect(self):
        """Connect to MQTT broker"""
        try:
            self.client.connect(self.mqtt_broker, self.mqtt_port, 60)
        except Exception as e:
            logger.error(f"Connection error: {e}")
            time.sleep(5)  # Wait before retry
            self.connect()

    def run(self):
        """Main loop for the print daemon"""
        logger.info("Starting print daemon...")
        self.connect()
        try:
            self.client.loop_forever()
        except KeyboardInterrupt:
            logger.info("Shutting down print daemon...")
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
        finally:
            self.client.disconnect()

if __name__ == "__main__":
    daemon = PrintDaemon()
    daemon.run()