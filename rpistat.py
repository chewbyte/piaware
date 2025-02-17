#!/usr/bin/env python3

import json
import requests

# Load the status data from the .json file
with open('/run/piaware/status.json') as f:
    status_data = json.load(f)

# Prepare the webhook URL (replace with your actual webhook URL)
webhook_url = ""

# Function to generate message for system status from the new JSON structure
def generate_system_status_message(status):
    #message = "RPI System Status:\n"
    message = ""

    # CPU info
    message += f"\n**CPU Load:** {status.get('cpu_load_percent', 'N/A')}%\n"
    message += f"**CPU Temperature:** {status.get('cpu_temp_celcius', 'N/A')}°C\n"
    message += f"**System Uptime:** {status.get('system_uptime', 'N/A')} seconds\n"

    return message

# Build the message content
message = generate_system_status_message(status_data)

# Prepare the payload to send to Discord
payload = {
    "content": message
}

# Send the message using the Discord webhook
response = requests.post(webhook_url, json=payload)

# Check if the message was sent successfully
if response.status_code == 204:
    print("Message sent successfully!")
else:
    print(f"Failed to send message. Status code: {response.status_code}")
