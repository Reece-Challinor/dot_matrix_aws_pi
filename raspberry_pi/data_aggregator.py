import datetime
from typing import Dict, List, Any
import json
import threading
import time
import paho.mqtt.client as mqtt

class BriefingFormatter:
    def __init__(self):
        self.box_chars = {
            'horizontal': '─',
            'vertical': '│',
            'top_left': '┌',
            'top_right': '┐',
            'bottom_left': '└',
            'bottom_right': '┘',
            'left_intersection': '├',
            'right_intersection': '┤',
            'top_intersection': '┬',
            'bottom_intersection': '┴',
            'cross': '┼'
        }

    def create_header(self, text: str, width: int = 50) -> str:
        border = "=" * width
        padding = (width - len(text)) // 2
        return f"{border}\n{' ' * padding}{text}\n{border}"

    def create_section_header(self, text: str, width: int = 50) -> str:
        stars = "*" * ((width - len(text) - 2) // 2)
        return f"{stars} {text} {stars}"

    def create_table(self, headers: List[str], data: List[List[Any]], col_widths: List[int]) -> str:
        result = []
        
        # Create top border
        top_border = self.box_chars['top_left']
        for i, width in enumerate(col_widths):
            top_border += self.box_chars['horizontal'] * width
            top_border += self.box_chars['top_right'] if i == len(col_widths)-1 else self.box_chars['top_intersection']
        result.append(top_border)
        
        # Add headers
        header_row = self.box_chars['vertical']
        for header, width in zip(headers, col_widths):
            header_row += f"{header:<{width}}"
            header_row += self.box_chars['vertical']
        result.append(header_row)
        
        # Add separator
        separator = self.box_chars['left_intersection']
        for i, width in enumerate(col_widths):
            separator += self.box_chars['horizontal'] * width
            separator += self.box_chars['right_intersection'] if i == len(col_widths)-1 else self.box_chars['cross']
        result.append(separator)
        
        # Add data rows
        for row in data:
            data_row = self.box_chars['vertical']
            for value, width in zip(row, col_widths):
                data_row += f"{str(value):<{width}}"
                data_row += self.box_chars['vertical']
            result.append(data_row)
        
        # Add bottom border
        bottom_border = self.box_chars['bottom_left']
        for i, width in enumerate(col_widths):
            bottom_border += self.box_chars['horizontal'] * width
            bottom_border += self.box_chars['bottom_right'] if i == len(col_widths)-1 else self.box_chars['bottom_intersection']
        result.append(bottom_border)
        
        return "\n".join(result)

    def create_bar_chart(self, value: float, max_value: float, width: int = 10) -> str:
        filled_blocks = int((value / max_value) * width)
        return "▇" * filled_blocks

    def format_briefing(self, data: Dict[str, Any]) -> str:
        # Initialize the briefing with the main header
        briefing = [
            self.create_header("DAILY SECURITY INTELLIGENCE BRIEFING"),
            f"Date: {datetime.datetime.now().strftime('%Y-%m-%d')}             Location: {data.get('location', 'N/A')}",
            f"Classification: {data.get('classification', 'CONFIDENTIAL')}",
            "=" * 50,
            ""
        ]

        # Strategic Overview
        briefing.extend([
            self.create_section_header("STRATEGIC OVERVIEW"),
            f"- Today's sentiment: {data.get('sentiment', 'N/A')}",
            f"- Weather affecting transportation: {data.get('weather_impact', 'N/A')}",
            f"- Security alerts: {data.get('security_level', 'N/A')}",
            "*" * 50,
            ""
        ])

        # Market Analysis
        if 'market_data' in data:
            briefing.extend([
                self.create_section_header("MARKET ANALYSIS"),
                "-- STOCK INDICES --"
            ])
            
            # Create market data table
            headers = ["Index", "Current", "Change"]
            market_data = [
                ["Dow Jones", data['market_data'].get('dow_value', 'N/A'), data['market_data'].get('dow_change', 'N/A')],
                ["S&P 500", data['market_data'].get('sp_value', 'N/A'), data['market_data'].get('sp_change', 'N/A')],
                ["NASDAQ", data['market_data'].get('nasdaq_value', 'N/A'), data['market_data'].get('nasdaq_change', 'N/A')]
            ]
            briefing.append(self.create_table(headers, market_data, [12, 10, 10]))
            
            # Add commodity trends
            briefing.extend([
                "-- COMMODITY TREND --",
                f"Gold: ${data['market_data'].get('gold_price', 'N/A')}/oz {self.create_bar_chart(float(data['market_data'].get('gold_trend', 0)), 100, 7)} {data['market_data'].get('gold_direction', 'N/A')}",
                f"Crude Oil: ${data['market_data'].get('oil_price', 'N/A')}/bbl {self.create_bar_chart(float(data['market_data'].get('oil_trend', 0)), 100, 5)} {data['market_data'].get('oil_direction', 'N/A')}",
                "*" * 50,
                ""
            ])

        # Add remaining sections with proper formatting
        sections = [
            ('SUPPLY CHAIN & LOGISTICS', 'supply_chain'),
            ('MILITARY DEVELOPMENTS', 'military'),
            ('GLOBAL HEADLINES', 'headlines'),
            ('ACTIONABLE RECOMMENDATIONS', 'recommendations')
        ]

        for section_title, key in sections:
            if key in data:
                briefing.extend([
                    self.create_section_header(section_title),
                    *[f"- {item}" for item in data[key]],
                    "*" * 50,
                    ""
                ])

        # Add footer
        briefing.extend([
            "=" * 50,
            "End of Briefing - Confidential Information",
            "For inquiries contact: security@yourdomain.com",
            "*" * 50
        ])

        return "\n".join(briefing)


class DataAggregator:
    def __init__(self):
        self.latest_data = None
        self.mqtt_client = None
        self.setup_mqtt()

    def setup_mqtt(self):
        """Set up MQTT client to connect to AWS IoT Core."""
        self.mqtt_client = mqtt.Client()
        self.mqtt_client.tls_set(
            ca_certs="AmazonRootCA1.pem",
            certfile="device.pem.crt",
            keyfile="private.pem.key"
        )
        self.mqtt_client.on_connect = self.on_connect
        self.mqtt_client.on_message = self.on_message
        # Replace 'your-endpoint' with your AWS IoT endpoint
        self.mqtt_client.connect("your-endpoint.amazonaws.com", 8883)
        # Start the MQTT client in a separate thread
        threading.Thread(target=self.mqtt_client.loop_forever, daemon=True).start()

    def on_connect(self, client, userdata, flags, rc):
        """Callback when the client connects to AWS IoT Core."""
        if rc == 0:
            # Connection successful
            client.subscribe("your/iot/topic")
        else:
            # Connection failed
            print(f"Failed to connect, return code {rc}")

    def on_message(self, client, userdata, msg):
        """Callback when a message is received from the MQTT topic."""
        try:
            message = json.loads(msg.payload.decode())
            self.latest_data = message
        except json.JSONDecodeError:
            print("Received invalid JSON payload")

    def get_latest_data(self) -> Dict[str, Any]:
        """Retrieve the most recent data from the MQTT topic."""
        # Wait until data is received
        while self.latest_data is None:
            time.sleep(0.1)
        return self.latest_data


def format_data_for_printing() -> str:
    """
    Format the intelligence briefing data with data from AWS IoT MQTT topic.

    Returns:
        str: Formatted briefing ready for printing
    """
    aggregator = DataAggregator()
    data = aggregator.get_latest_data()
    formatter = BriefingFormatter()
    return formatter.format_briefing(data)


# Example usage
if __name__ == "__main__":
    # Fetch data and print formatted briefing
    briefing_content = format_data_for_printing()
    print(briefing_content)