# AWS Weather Data Pipeline

A weather data pipeline built with Python and AWS. It pulls current weather data from the Open-Meteo API, stores the raw response in Amazon S3, transforms it with AWS Glue and PySpark, and queries the processed data with Amazon Athena.

## Architecture

```text
Open-Meteo API
      |
      v
Python Ingestion Script
      |
      v
Amazon S3
raw JSON
      |
      v
AWS Glue + PySpark
      |
      v
Amazon S3
processed Parquet
      |
      v
Amazon Athena
      |
      v
SQL Queries
```

## Technologies

- Python
- REST APIs
- Amazon S3
- AWS Glue
- Apache Spark
- PySpark
- Amazon Athena
- SQL
- Parquet
- Boto3

## Pipeline

### 1. Extract

The Python ingestion script gets current weather data from the Open-Meteo API.

The response is saved locally as a timestamped JSON file.

### 2. Load Raw Data

Boto3 uploads the raw JSON file to:

```text
s3://rafmoran-weather-data-pipeline-2026/raw/
```

The raw API response is kept in S3 before any transformations are applied.

### 3. Transform

An AWS Glue job runs the PySpark transformation.

The job reads the raw JSON files from S3, flattens the nested weather data, and keeps these fields:

- latitude
- longitude
- timezone
- observation_time
- temperature_c
- humidity_pct
- wind_speed_kmh

The transformed data is written back to S3 as Parquet files.

```text
s3://rafmoran-weather-data-pipeline-2026/processed/
```

### 4. Query

Amazon Athena uses an external table that points to the processed Parquet files in S3.

This makes it possible to query the processed weather data with SQL.

Example:

```sql
SELECT AVG(temperature_c) AS avg_temperature_c
FROM weather_pipeline.weather_data;
```

## Project Structure

```text
aws-weather-data-pipeline/
├── data/
├── glue/
│   └── transform_weather.py
├── queries/
│   ├── all_weather.sql
│   ├── average_temperature.sql
│   ├── create_table.sql
│   └── max_wind_speed.sql
├── src/
│   └── ingest_weather.py
├── .gitignore
├── LICENSE
├── README.md
└── requirements.txt
```

## Data Flow

Raw and processed data are stored separately in S3.

```text
raw/
    weather_<timestamp>.json

processed/
    part-*.snappy.parquet
```

The raw folder keeps the original API response.

The processed folder stores the transformed Parquet data used for Athena queries.

## Running the Ingestion Script

Create and activate a Python virtual environment.

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the ingestion script:

```bash
python src/ingest_weather.py
```

The script:

1. Gets current weather data from Open-Meteo
2. Saves it as a JSON file
3. Uploads the file to the S3 `raw/` folder

## Glue Transformation

The Glue job uses these paths:

```text
SOURCE_PATH=s3://rafmoran-weather-data-pipeline-2026/raw/
DESTINATION_PATH=s3://rafmoran-weather-data-pipeline-2026/processed/
```

The PySpark job reads the raw data, selects and renames the fields, and writes the result as compressed Parquet files.

## Athena Queries

The `queries/` folder contains SQL for:

- Creating the Athena external table
- Viewing all processed weather records
- Calculating average temperature
- Finding maximum wind speed

## Current Status

The main pipeline is working:

- [x] Weather API ingestion
- [x] Raw JSON storage in Amazon S3
- [x] AWS Glue PySpark transformation
- [x] Processed Parquet storage in Amazon S3
- [x] Amazon Athena SQL queries
- [ ] Automated scheduled ingestion with AWS Lambda and EventBridge

## Future Improvements

- Automate ingestion with AWS Lambda and EventBridge
- Collect weather data from multiple locations
- Partition processed data by date or location
- Add data validation
- Add pipeline monitoring
- Improve IAM permissions for a production setup

## Purpose

Built to practice AWS data engineering with API ingestion, S3 storage, PySpark transformations, Parquet, and SQL.
