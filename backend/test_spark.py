import os
import sys

# Set Python executable path for Spark workers
os.environ['PYSPARK_PYTHON'] = sys.executable
os.environ['PYSPARK_DRIVER_PYTHON'] = sys.executable

from pyspark import SparkContext

sc = SparkContext("local[4]", "test")
rdd = sc.parallelize([1, 2, 3, 4, 5])
print(rdd.map(lambda x: x*x).collect())
sc.stop()
