import sys

from awsglue.context import GlueContext
from awsglue.job import Job
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from pyspark.sql.functions import col


args = getResolvedOptions(
    sys.argv,
    ["JOB_NAME", "SOURCE_PATH", "DESTINATION_PATH"]
)

sc = SparkContext()
glue_context = GlueContext(sc)
spark = glue_context.spark_session

job = Job(glue_context)
job.init(args["JOB_NAME"], args)


raw_df = spark.read.option("multiline", "true").json(
    args["SOURCE_PATH"]
)


processed_df = raw_df.select(
    col("latitude"),
    col("longitude"),
    col("timezone"),
    col("current.time").alias("observation_time"),
    col("current.temperature_2m").alias("temperature_c"),
    col("current.relative_humidity_2m").alias("humidity_pct"),
    col("current.wind_speed_10m").alias("wind_speed_kmh"),
)


processed_df.write.mode("append").parquet(
    args["DESTINATION_PATH"]
)


job.commit()
