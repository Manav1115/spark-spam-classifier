from pyspark.sql import SparkSession

spark = SparkSession.builder.getOrCreate()

# Simple test: create a range and collect
data = spark.range(5).collect()
print("Data from Spark:", data)

spark.stop()
