import json
from datetime import datetime
from pathlib import Path
from botocore.exceptions import BotoCoreError, ClientError

import requests
import boto3


API_URL = "https://api.open-meteo.com/v1/forecast"

PARAMS = {
    "latitude": 37.7749,
    "longitude": -122.4194,
    "current": "temperature_2m,relative_humidity_2m,wind_speed_10m",
    "timezone": "auto",
}
BUCKET_NAME = "rafmoran-weather-data-pipeline-2026"

def upload_to_s3(file_path):
    s3 = boto3.client("s3")

    object_key = f"raw/{file_path.name}"

    s3.upload_file(
        str(file_path),
        BUCKET_NAME,
        object_key
    )

    return object_key

def fetch_weather():
    response = requests.get(API_URL, params=PARAMS, timeout=10)
    response.raise_for_status()
    return response.json()


def save_raw_weather(data):
    output_dir = Path("data")
    output_dir.mkdir(exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = output_dir / f"weather_{timestamp}.json"

    with open(output_path, "w") as file:
        json.dump(data, file, indent=2)

    return output_path


def main():
    try:
        weather_data = fetch_weather()
        output_path = save_raw_weather(weather_data)

        object_key = upload_to_s3(output_path)

        print(f"Weather data saved locally to {output_path}")
        print(f"Weather data uploaded to s3://{BUCKET_NAME}/{object_key}")

    except requests.RequestException as error:
        print(f"Failed to retrieve weather data: {error}")

    except (BotoCoreError, ClientError) as error:
        print(f"Failed to upload weather data to S3: {error}")


if __name__ == "__main__":
    main()
