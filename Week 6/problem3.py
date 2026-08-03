from pyspark.sql import SparkSession
from pyspark.sql import functions as F

spark = SparkSession.builder.appName("Practice").getOrCreate()

df = spark.read.csv("netflix_titles.csv", header=True, inferSchema=True,
                    multiLine=True, escape='"', quote='"')

top_countries = df.filter(F.col("release_year") > 2015).groupBy("country").agg(
    F.avg("release_year").alias("avg_year"),
    F.count("*").alias("num_title")
).sort(F.col("num_title").desc()).cache()
print("Top 10 countries titles count:")
top_countries.select("country", "num_title").show(10)
print("Average release year of the top country:")
top_countries.select("country", "avg_year").show(1)