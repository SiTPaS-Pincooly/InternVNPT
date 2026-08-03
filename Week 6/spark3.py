from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql.types import *

spark = SparkSession.builder.appName("Practice").getOrCreate()

df = spark.read.csv("netflix_titles.csv", header=True, inferSchema=True,
                    multiLine=True, escape='"', quote='"')

# Group 3 - Máy lọc nước

print("\ndf.filter(df.release_year > 2015).show()")
df.filter(df.release_year > 2015).show()
print("\ndf.filter(\"release_year > 2015\").show()")
df.filter("release_year > 2015").show()
print("\ndf.where(df.type == \"Movie\").show()")
df.where(df.type == "Movie").show()

print("\ndf.filter((df.type == \"Movie\") & (df.release_year > 2018)).show()")
df.filter((df.type == "Movie") & (df.release_year > 2018)).show()
print("\ndf.filter((df.rating == \"PG-13\") | (df.rating == \"R\")).show()")
df.filter((df.rating == "PG-13") | (df.rating == "R")).show()
print("\ndf.filter(~(df.type == \"Movie\")).show()")
df.filter(~(df.type == "Movie")).show()

print("\ndf.filter(df.director.isNull()).show()")
df.filter(df.director.isNull()).show()
print("\ndf.filter(df.director.isNotNull()).show()")
df.filter(df.director.isNotNull()).show()

print("\ndf.filter(df.title.like(\"The%\")).show()")
df.filter(df.title.like("The%")).show()
print("\ndf.filter(df.country.isin(\"United States\", \"India\")).show()")
df.filter(df.country.isin("United States", "India")).show()

spark.stop()