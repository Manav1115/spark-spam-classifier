from flask import Flask, request, jsonify
from flask_cors import CORS
from pyspark.sql import SparkSession, Row
from pyspark.ml.pipeline import PipelineModel
import os

print("Starting Backend + Spark (WSL version)...")

# ----------------------------
# Spark configuration in WSL
# ----------------------------

os.environ["SPARK_HOME"] = "/home/kalp/spark/spark"
os.environ["HADOOP_HOME"] = "/home/kalp/spark/spark"
os.environ["PYSPARK_PYTHON"] = "/home/kalp/bigdata_project/backend/venv/bin/python"
os.environ["PYSPARK_DRIVER_PYTHON"] = "/home/kalp/bigdata_project/backend/venv/bin/python"


# Spark master (inside WSL)
SPARK_MASTER = "spark://172.23.202.231:7077"

# Model path inside WSL
MODEL_PATH = "/home/kalp/spam_project/model_spam_nb"

# ----------------------------
# Spark Session
# ----------------------------

spark = SparkSession.builder \
    .appName("SpamPredictionAPI") \
    .master(SPARK_MASTER) \
    .getOrCreate()

print("SparkSession connected.")

# Load trained model
model = PipelineModel.load(MODEL_PATH)
print("Model loaded successfully.")

# ----------------------------
# Flask App
# ----------------------------

app = Flask(__name__)
CORS(app)

@app.route("/", methods=["GET"])
def home():
    return "Backend + Spark (WSL) is running!"

@app.route("/predict", methods=["POST"])
def predict():
    data = request.json
    text = data.get("text", "")

    if not text.strip():
        return jsonify({"error": "Text is empty"}), 400

    df = spark.createDataFrame([Row(text=text)])
    result = model.transform(df).select("prediction", "probability").collect()[0]

    return jsonify({
        "prediction": int(result.prediction),
        "spam_probability": float(result.probability[1])
    })

if __name__ == "__main__":
    print("Running Flask on http://localhost:5000")
    app.run(host="0.0.0.0", port=5000, debug=True, use_reloader=False)
