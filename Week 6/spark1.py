from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql.types import *

spark = SparkSession.builder.appName("Practice").getOrCreate()

df = spark.read.csv("netflix_titles.csv", header=True, inferSchema=True,
                    multiLine=True, escape='"', quote='"')

print("\ndf.show()")
df.show()
print("\ndf.show(3)")
df.show(3)
print("\ndf.show(3, truncate=False)")
df.show(3, truncate=False)
print("\ndf.printSchema()")
df.printSchema()
print("\ndf.columns")
print(df.columns)
print("\ndf.dtypes")
print(df.dtypes)
print("\ndf.count()")
print(df.count())
print("\ndf.describe().show()")
df.describe().show()
print("\ndf.summary().show()")
df.summary().show()
print("\ndf.first()")
print(df.first())
print("\ndf.head(2)")
print(df.head(2))
print("\ndf.take(2)")
print(df.take(2))

spark.stop()