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
for aircraft in data.get('aircraft', []):  # Safely iterate if 'aircraft' is not found
    flight = aircraft.get('flight', 'Unknown Flight')
    speed = aircraft.get('gs', 'Unknown Speed')
    altitude = aircraft.get('alt_baro', 'Unknown Altitude')
    heading = aircraft.get('track', 'Unknown Heading')
    squawk = aircraft.get('squawk', 'Unknown Squawk')

    # Create the FlightAware URL and disable preview
    flight_url = f"https://www.flightaware.com/live/flight/{flight}" if flight != 'Unknown Flight' else "N/A"

    message += f"**Flight Number:** {flight}\n"
    message += f"**Ground Speed:** {speed} kts\n"
    message += f"**Altitude:** {altitude} ft\n"
    message += f"**Heading:** {heading}°\n"
    message += f"**Squawk:** {squawk}\n"
    message += f"**FlightAware URL:** {flight_url}\n\n"

# Function to send message in chunks if it exceeds 2000 characters
def send_message_in_chunks(message):
    # Split the message into chunks of 2000 characters or less
    while len(message) > 2000:
        chunk = message[:2000]  # Get the first 2000 characters
        payload = {"content": chunk}
        response = requests.post(webhook_url, json=payload)

        # Check if the message was sent successfully
        if response.status_code != 204:
            print(f"Failed to send chunk. Status code: {response.status_code}, Response: {response.text}")
        message = message[2000:]  # Remove the sent chunk from the message

    # Send the remaining message if it's under 2000 characters
    if len(message) > 0:
        payload = {"content": message}
        response = requests.post(webhook_url, json=payload)
        if response.status_code == 204:
            print("Message sent successfully!")
        else:
            print(f"Failed to send message. Status code: {response.status_code}, Response: {response.text}")

# Send the message in chunks
send_message_in_chunks(message)
