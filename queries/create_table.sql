CREATE DATABASE IF NOT EXISTS weather_pipeline;

CREATE EXTERNAL TABLE IF NOT EXISTS weather_pipeline.weather_data (
    latitude DOUBLE,
    longitude DOUBLE,
    timezone STRING,
    observation_time STRING,
    temperature_c DOUBLE,
    humidity_pct BIGINT,
    wind_speed_kmh DOUBLE
)
STORED AS PARQUET
LOCATION 's3://rafmoran-weather-data-pipeline-2026/processed/';
