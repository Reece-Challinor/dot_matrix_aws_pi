import subprocess
import json

import paho.mqtt.client as mqtt

# MQTT settings
MQTT_BROKER = "your_broker_address"
MQTT_PORT = 1883
MQTT_TOPIC = "your/topic"

# Callback when the client receives a message from the broker
def on_message(client, userdata, msg):
    try:
        data = json.loads(msg.payload.decode())
        report = format_report(data)
        send_to_printer(report)
    except Exception as e:
        print(f"Error processing message: {e}")

# Format the received data into a plain text ASCII report
def format_report(data):
    report = "Aggregated Data Report\n"
    report += "=" * 30 + "\n"
    for key, value in data.items():
        report += f"{key}: {value}\n"
    return report

# Send the formatted report to the default printer using CUPS
def send_to_printer(report):
    try:
        process = subprocess.Popen(['lp'], stdin=subprocess.PIPE)
        process.communicate(input=report.encode())
    except Exception as e:
        print(f"Error sending to printer: {e}")

# Setup MQTT client
client = mqtt.Client()
client.on_message = on_message

client.connect(MQTT_BROKER, MQTT_PORT, 60)
client.subscribe(MQTT_TOPIC)

# Blocking call that processes network traffic, dispatches callbacks and handles reconnecting
client.loop_forever()