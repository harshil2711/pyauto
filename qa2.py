import json

# Load the JSON file
with open('adb_events_2025-06-02.json') as f:
    data = json.load(f)

# Extract and print only event names
for i in data:
    if 'event' in i:  # Check if current dictionary has an 'event' key
        print(i['event'])  # If it exists, print the value of the 'event' key
