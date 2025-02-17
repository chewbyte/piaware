#!/usr/bin/env python3

import json
import requests

# Load your data from the .json file
with open('/run/dump1090-fa/aircraft.json') as f:
    data = json.load(f)

# Prepare the webhook URL (you need to replace this with your actual URL)
webhook_url = ""

# Start building the message string
message = "Aircraft Information:\n"

# Loop through the aircraft data and create a message
for aircraft in data['aircraft']:
    flight = aircraft.get('flight', 'Unknown Flight')
    speed = aircraft.get('gs', 'Unknown Speed')
    altitude = aircraft.get('alt_baro', 'Unknown Altitude')
    heading = aircraft.get('track', 'Unknown Heading')
    squawk = aircraft.get('squawk', 'Unknown Squawk')
    

    message += f"**Flight Number:** {flight}\n"
message += f"**Ground Speed:** {speed} kts\n"
message += f"**Altitude:** {altitude} ft\n"
message += f"**Heading:** {heading}°\n"
message += f"**Squawk:** {squawk}\n"


# Prepare the payload to send to Discord
payload = {
    "content": message
}

# Send the message using the Discord webhook
response = requests.post(webhook_url, json=payload)

# Check if the message was sent successfully
if response.status_code == 204:
    print("Message sent successfully!")
