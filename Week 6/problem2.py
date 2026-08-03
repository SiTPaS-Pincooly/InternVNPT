from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql.types import *

spark = SparkSession.builder.appName("Practice").getOrCreate()

df = spark.read.csv("netflix_titles.csv", header=True, inferSchema=True,
                    multiLine=True, escape='"', quote='"')

shows_after_2018 = df.filter((F.col("type") == "TV Show") & (F.col("release_year") > 2018))
print(shows_after_2018.count())

spark.stop()