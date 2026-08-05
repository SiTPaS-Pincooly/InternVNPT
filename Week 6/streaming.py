import time
from pyspark.sql import SparkSession
from pyspark.sql.types import *
from pyspark.sql import functions as F

spark = SparkSession.builder.appName("Streaming").getOrCreate()
spark.sparkContext.setLogLevel("ERROR")

# Khai báo schema trước
schema = StructType()\
    .add("show_id", StringType()).add("type", StringType()).add("title", StringType()) \
    .add("director", StringType()).add("cast", StringType()).add("country", StringType()) \
    .add("date_added", StringType()).add("release_year", IntegerType()) \
    .add("rating", StringType()).add("duration", StringType()) \
    .add("listed_in", StringType()).add("description", StringType())

stream_df = spark.readStream.option("header", "true")\
    .option("multiLine", "true").option("escape", '"').option("quote", '"')\
    .schema(schema).csv("stream-input")

result = stream_df.groupBy("type").count()

query = result.writeStream.outputMode("complete").format("console").start()

while query.isActive:
    time.sleep(2)
    progress = query.lastProgress
    if progress:
        print(f"Batch {progress['batchId']}: {progress['numInputRows']} rows, "
              f"{progress['inputRowsPerSecond']:.1f} rows/sec in, "
              f"{progress['processedRowsPerSecond']:.1f} rows/sec processed")
        
query.awaitTermination()