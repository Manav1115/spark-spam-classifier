from pyspark.sql import SparkSession
from pyspark.sql.functions import udf
from pyspark.sql.types import FloatType
from textblob import TextBlob

def run_sentiment(texts):
    # Initialize SparkSession
    spark = SparkSession.builder.appName("DistributedSentimentAnalysis").getOrCreate()

    # Create DataFrame
    df = spark.createDataFrame([(t,) for t in texts], ["text"])

    # Define UDF
    def analyze(t):
        return float(TextBlob(t).sentiment.polarity)

    sentiment_udf = udf(analyze, FloatType())

    # Apply UDF and trigger action
    df_result = df.withColumn("polarity", sentiment_udf(df.text))
    df_result.show()  # This is the Spark ACTION

    # Collect results if needed
    results = [row["polarity"] for row in df_result.collect()]

    spark.stop()
    return results

if __name__ == "__main__":
    texts = ["I love Spark", "This is bad", "Spark is amazing!"]
    scores = run_sentiment(texts)
    print("Sentiment scores:", scores)
