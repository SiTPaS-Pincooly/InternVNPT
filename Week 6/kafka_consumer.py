from pyspark.sql import SparkSession
from pyspark.sql.types import *
from pyspark.sql import functions as F
import time

spark = SparkSession.builder \
    .appName("KafkaStream") \
    .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.13:4.2.0") \
    .getOrCreate()
spark.sparkContext.setLogLevel("ERROR")

schema = StructType() \
    .add("show_id", StringType()).add("type", StringType()).add("title", StringType()) \
    .add("director", StringType()).add("cast", StringType()).add("country", StringType()) \
    .add("date_added", StringType()).add("release_year", IntegerType()) \
    .add("rating", StringType()).add("duration", StringType()) \
    .add("listed_in", StringType()).add("description", StringType())

raw = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "network-events") \
    .option("startingOffsets", "latest") \
    .load()

parsed = raw.selectExpr("CAST(value AS STRING) as json_str") \
    .select(F.from_json(F.col("json_str"), schema).alias("data")).select("data.*")

query = parsed.groupBy("type").count().writeStream \
    .outputMode("complete") \
    .format("console") \
    .start()

while query.isActive:
    time.sleep(1)
    progress = query.lastProgress
    if progress and progress.get("batchId", 0) > 0:
        print(f"Batch {progress['batchId']}: {progress['numInputRows']} rows, "
              f"{progress['inputRowsPerSecond']:.1f} rows/sec in, "
              f"{progress['processedRowsPerSecond']:.1f} rows/sec processed")
        print(progress['sources'])

query.awaitTermination()
