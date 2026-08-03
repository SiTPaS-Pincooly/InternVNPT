from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql.types import *

spark = SparkSession.builder.appName("Practice").getOrCreate()

df = spark.read.csv("netflix_titles.csv", header=True, inferSchema=True,
                    multiLine=True, escape='"', quote='"')

movies_after_2015 = df.filter((df.release_year > 2015) & (df.type == "Movie")).cache()
print(movies_after_2015.count())
movies_after_2015.groupBy("rating").count().orderBy(F.col("count").desc()).show(5)
movies_after_2015.agg(F.avg("release_year")).show()

spark.stop()