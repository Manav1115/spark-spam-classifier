#!/usr/bin/env python3
"""
High-Accuracy Spark ML NaiveBayes Spam Classifier
"""

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, lower, regexp_replace
from pyspark.ml import Pipeline
from pyspark.ml.feature import (
    RegexTokenizer,
    StopWordsRemover,
    CountVectorizer,
    IDF
)
from pyspark.ml.classification import NaiveBayes
from pyspark.ml.evaluation import BinaryClassificationEvaluator
import argparse
import os
import shutil


def build_spark(master_url):
    return (
        SparkSession.builder
        .appName("SpamClassifier_NaiveBayes")
        .master(master_url)
        .config("spark.executor.memory", "4g")
        .config("spark.driver.memory", "4g")
        .config("spark.executor.cores", "2")
        .getOrCreate()
    )


def main(args):
    master_url = args.master
    data_path = args.data_path
    model_out = args.model_out

    spark = build_spark(master_url)
    print("SparkSession created:", spark.sparkContext.appName)

    # ---------------------------------------------------------
    # 1) LOAD DATA
    # ---------------------------------------------------------
    df = spark.read.csv(data_path, header=True, inferSchema=True)

    df = (
        df.withColumn("label", col("label").cast("double"))
          .withColumn("text", lower(col("text")))
          .withColumn("text", regexp_replace("text", "[^a-zA-Z0-9 ]", " "))
    )

    print("Schema:")
    df.printSchema()
    print("Total rows:", df.count())

    # ---------------------------------------------------------
    # 2) Define Pipeline Stages
    # ---------------------------------------------------------

    tokenizer = RegexTokenizer(
        inputCol="text",
        outputCol="tokens",
        pattern="\\W+"
    )

    remover = StopWordsRemover(
        inputCol="tokens",
        outputCol="filtered"
    )

    vectorizer = CountVectorizer(
        inputCol="filtered",
        outputCol="rawFeatures",
        vocabSize=30000,
        minDF=3        # prevents overfitting
    )

    idf = IDF(
        inputCol="rawFeatures",
        outputCol="features"
    )

    # ✨ BETTER NAIVE BAYES PARAMETERS
    nb = NaiveBayes(
        modelType="multinomial",
        smoothing=1.0,
        featuresCol="features",
        labelCol="label"
    )

    pipeline = Pipeline(stages=[tokenizer, remover, vectorizer, idf, nb])

    # ---------------------------------------------------------
    # Train/Test Split
    # ---------------------------------------------------------
    train_df, test_df = df.randomSplit([0.8, 0.2], seed=42)
    print("Train:", train_df.count(), "Test:", test_df.count())

    # ---------------------------------------------------------
    # Train Model
    # ---------------------------------------------------------
    model = pipeline.fit(train_df)
    preds = model.transform(test_df)

    # ---------------------------------------------------------
    # Evaluate
    # ---------------------------------------------------------
    evaluator = BinaryClassificationEvaluator(
        labelCol="label",
        rawPredictionCol="prediction",   # NB supports prediction column too
        metricName="areaUnderROC"
    )

    auc = evaluator.evaluate(preds)
    print(f"\n🔥 AUC = {auc:.4f}")

    # CONFUSION MATRIX
    stats = preds.groupBy("label", "prediction").count().collect()
    print("\nConfusion Matrix:")
    for row in stats:
        print(f"Label={row['label']}  Prediction={row['prediction']}  Count={row['count']}")

    # Compute F1, Precision, Recall manually
    preds.createOrReplaceTempView("preds")
    pr = spark.sql("""
      SELECT
        SUM(CASE WHEN label = 1 AND prediction = 1 THEN 1 ELSE 0 END) AS TP,
        SUM(CASE WHEN label = 0 AND prediction = 1 THEN 1 ELSE 0 END) AS FP,
        SUM(CASE WHEN label = 1 AND prediction = 0 THEN 1 ELSE 0 END) AS FN
      FROM preds
    """).collect()[0]

    tp, fp, fn = pr["TP"], pr["FP"], pr["FN"]
    precision = tp / (tp + fp + 1e-9)
    recall = tp / (tp + fn + 1e-9)
    f1 = 2 * precision * recall / (precision + recall + 1e-9)

    print(f"\nPrecision = {precision:.4f}")
    print(f"Recall    = {recall:.4f}")
    print(f"F1 Score  = {f1:.4f}")

    # ---------------------------------------------------------
    # Save Model
    # ---------------------------------------------------------
    if os.path.exists(model_out):
        shutil.rmtree(model_out)

    model.write().overwrite().save(model_out)
    print("\n✅ Model successfully saved to:", model_out)

    spark.stop()


# ---------------------------------------------------------
# MAIN
# ---------------------------------------------------------
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--master", default="spark://10.10.31.111:7077")
    parser.add_argument("--data-path", default="\\wsl.localhost\Ubuntu\home\manav_anand\projects\spam_classifier\spark_ml\data\emails.csv")
    parser.add_argument("--model-out", default="\\wsl.localhost\Ubuntu\home\manav_anand\projects\spam_classifier\spark_ml\model_spam_nb")
    args = parser.parse_args()
    main(args)

