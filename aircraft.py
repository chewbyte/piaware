#!/usr/bin/env python3

import json
import requests

# Load your data from the .json file
with open('/run/dump1090-fa/aircraft.json') as f:
    data = json.load(f)

# Prepare the webhook URL (you need to replace this with your actual URL)
webhook_url = ""

# Function to convert heading to a cardinal direction
def heading_to_cardinal(heading):
    if heading is None or heading == 'N/A':
        return 'N/A'
    heading = float(heading)

    if heading >= 337.5 or heading < 22.5:
        return 'N'
    elif heading >= 22.5 and heading < 67.5:
        return 'NE'
    elif heading >= 67.5 and heading < 112.5:
        return 'E'
    elif heading >= 112.5 and heading < 157.5:
        return 'SE'
    elif heading >= 157.5 and heading < 202.5:
        return 'S'
    elif heading >= 202.5 and heading < 247.5:
        return 'SW'
    elif heading >= 247.5 and heading < 292.5:
        return 'W'
    elif heading >= 292.5 and heading < 337.5:
        return 'NW'

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

    # Start aircraft data
    aircraft_message = ""

    # Add flight number only if it's not 'N/A'
    if flight != 'N/A':
        aircraft_message += f"**Flight Number:** {flight}\n"
    if speed != 'N/A':
        aircraft_message += f"**Ground Speed:** {speed} kts\n"
    if altitude != 'N/A':
        aircraft_message += f"**Altitude:** {altitude} ft\n"

    # Add heading with cardinal direction if available
    if heading != 'N/A':
        cardinal_direction = heading_to_cardinal(heading)
        aircraft_message += f"**Heading:** {heading}° ({cardinal_direction})\n"

    if squawk != 'N/A':
        aircraft_message += f"**Squawk:** {squawk}\n"

    # Create the FlightAware URL and disable preview
    flight_url = f"https://www.flightaware.com/live/flight/{flight}" if flight != 'N/A' else "N/A"
    if flight_url != 'N/A':
        aircraft_message += f"**FlightAware URL:** {flight_url}\n"

    # Add the aircraft's details to the main message, separating aircraft with a newline for clarity
    message += aircraft_message + "\n"  # Add a newline between aircraft information

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

    # Debugging: print the payload before sending
    #print(f"Payload being sent: {json.dumps(payload, indent=4)}")

    response = requests.post(webhook_url, json=payload)

    # Check the response status code and print debug information
    if response.status_code == 204:
        print("Message chunk sent successfully!")
    else:
        print(f"Error: Failed to send message. Status code: {response.status_code}")
        print(f"Response Text: {response.text}")
