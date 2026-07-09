import requests
import json
import csv
from datetime import datetime


def fetch_weather_data():
    # Lagos coordinates for the Open-Meteo API
    url = "https://api.open-meteo.com/v1/forecast?latitude=6.5244&longitude=3.3792&current_weather=true"

    print(f"[{datetime.now()}] Fetching data from API...")

    try:
        # Make the GET request to the API
        response = requests.get(url)
        # This will raise an error if the website responds with a 404 or 500
        response.raise_for_status()

        # Parse the JSON response into a Python dictionary
        data = response.json()
        return data['current_weather']

    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return None


def save_to_csv(weather_data, filename="lagos_weather.csv"):
    if not weather_data:
        print("No data to save.")
        return

    print(f"[{datetime.now()}] Saving data to {filename}...")

    # Define the headers based on the API response keys
    headers = weather_data.keys()

    # Open a new CSV file in 'write' mode
    with open(filename, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=headers)

        # Write the header row
        writer.writeheader()
        # Write the data row
        writer.writerow(weather_data)

    print("Success! Data pipeline complete.")


if __name__ == "__main__":
    # This is the main execution flow of our pipeline
    raw_data = fetch_weather_data()
    save_to_csv(raw_data)
