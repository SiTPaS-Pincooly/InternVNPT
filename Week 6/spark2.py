from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql.types import *

spark = SparkSession.builder.appName("Practice").getOrCreate()

df = spark.read.csv("netflix_titles.csv", header=True, inferSchema=True,
                    multiLine=True, escape='"', quote='"')

#Group 2 - Select và Mani(fest)pulate bảng

print("\ndf.select(\"title\", \"release_year\").show()")
df.select("title", "release_year").show()
print("\ndf.select(F.col(\"title\"), F.col(\"rating\")).show()") # F.col() tái sử dụng đc trong nhiều bảng
df.select(F.col("title"), F.col("rating")).show()
print("\ndf.select(df.title, df.country).show()")
df.select(df.title, df.country).show()

print("\ndf.select(\"*\").show()")
df.select("*").show()
print("\ndf.select(df.columns[:4]).show()")
df.select(df.columns[:4]).show()

print("\ndf.withColumn(\"is_recent\", df.release_year >= 2020).show()")
df.withColumn("is_recent", df.release_year >= 2020).show()
print("\ndf.withColumn(\"release_year\", df.release_year + 0).show()")  # thay số khác vào 0 là overwrite ăn l đấy
df.withColumn("release_year", df.release_year + 0).show()
print("\ndf.withColumnRenamed(\"listed_in\", \"genres\").show()")
df.withColumnRenamed("listed_in", "genres").show()

print("\ndf.drop(\"description\").show()")
df.drop("description").show()
print("\ndf.drop(\"description\", \"cast\").show()")
df.drop("description", "cast").show()

spark.stop()