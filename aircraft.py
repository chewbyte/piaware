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
    flight = aircraft.get('flight', 'N/A')
    speed = aircraft.get('gs', 'N/A')
    altitude = aircraft.get('alt_baro', 'N/A')
    heading = aircraft.get('track', 'N/A')
    squawk = aircraft.get('squawk', 'N/A')

    # Check if all fields are N/A, if so, skip this aircraft
    if all(value == 'N/A' for value in [flight, speed, altitude, heading, squawk]):
        continue  # Skip this aircraft if all relevant data is 'N/A'

    # Create the FlightAware URL and disable preview
    flight_url = f"https://www.flightaware.com/live/flight/{flight}" if flight != 'N/A' else "N/A"

    # Add flight number only if it's not 'N/A'
    if flight != 'N/A':
        message += f"**Flight Number:** {flight}\n"

    # Add other fields only if they are not 'N/A'
    if speed != 'N/A':
        message += f"**Ground Speed:** {speed} kts\n"
    if altitude != 'N/A':
        message += f"**Altitude:** {altitude} ft\n"
    if heading != 'N/A':
        message += f"**Heading:** {heading}°\n"
    if squawk != 'N/A':
        message += f"**Squawk:** {squawk}\n"

    message += f"**FlightAware URL:** {flight_url}\n\n"

# Function to split the message into smaller parts if it exceeds 2000 characters
def split_message(message, max_length=2000):
    # Split message in a way that it doesn't cut off data points in the middle
    chunks = []
    while len(message) > max_length:
        split_point = message.rfind('\n', 0, max_length)
        if split_point == -1:
            split_point = max_length
        chunks.append(message[:split_point])
        message = message[split_point:].lstrip()  # Remove leading newlines for next chunk
    if message:
        chunks.append(message)
    return chunks

# Split the message into smaller chunks if necessary
chunks = split_message(message)

# Send each chunk as a separate message
for chunk in chunks:
    payload = {
        "content": chunk
    }

    response = requests.post(webhook_url, json=payload)

    # Check if the message was sent successfully
    if response.status_code == 204:
        print("Message chunk sent successfully!")
    else:
        print(f"Error: Failed to send message. Status code: {response.status_code}")
        print(f"Response Text: {response.text}")
