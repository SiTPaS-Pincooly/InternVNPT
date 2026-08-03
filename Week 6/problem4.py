from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql.window import Window

spark = SparkSession.builder.appName("Practice").getOrCreate()
spark.sparkContext.setLogLevel("ERROR")

df = spark.read.csv("netflix_titles.csv", header=True, inferSchema=True,
                    multiLine=True, escape='"', quote='"')

w = Window.partitionBy("rating").orderBy(F.col("date_added").desc())
df.withColumn("rank", F.row_number().over(w)).select("title", "rating", "date_added")\
    .filter(F.col("rank") == 1).show(truncate=False)
spark.stop()