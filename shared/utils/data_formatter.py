import json
from datetime import datetime

def format_data_for_printing(weather_data, market_data, security_alerts, template_path):
    """
    Formats the aggregated data into a printable ASCII report based on the briefing template.

    Args:
        weather_data (dict): Data from the weather API.
        market_data (dict): Data from the market API.
        security_alerts (list): List of security alerts.
        template_path (str): Path to the briefing template file.

    Returns:
        str: Formatted report as a string.
    """
    with open(template_path, 'r') as template_file:
        template = template_file.read()

    # Format the current date and time
    current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Format weather data
    weather_section = (
        f"Weather Report:\n"
        f"Temperature: {weather_data['temperature']}°C\n"
        f"Humidity: {weather_data['humidity']}%\n"
        f"Condition: {weather_data['condition']}\n"
    )

    # Format market data
    market_section = (
        f"Market Data:\n"
        f"Stock Index: {market_data['stock_index']}\n"
        f"Current Value: {market_data['current_value']}\n"
        f"Change: {market_data['change']}%\n"
    )

    # Format security alerts
    security_section = "Security Alerts:\n"
    for alert in security_alerts:
        security_section += f"- {alert['title']}: {alert['description']}\n"

    # Combine all sections into the final report
    report = template.format(
        datetime=current_datetime,
        weather=weather_section,
        market=market_section,
        security=security_section
    )

    return report

# Example usage
if __name__ == "__main__":
    # Mock data for testing
    weather_data = {
        "temperature": 22,
        "humidity": 60,
        "condition": "Sunny"
    }
    market_data = {
        "stock_index": "NASDAQ",
        "current_value": 15000,
        "change": 1.2
    }
    security_alerts = [
        {"title": "Alert 1", "description": "Description of alert 1"},
        {"title": "Alert 2", "description": "Description of alert 2"}
    ]

    template_path = "shared/templates/briefing_template.txt"
    formatted_report = format_data_for_printing(weather_data, market_data, security_alerts, template_path)
    print(formatted_report)