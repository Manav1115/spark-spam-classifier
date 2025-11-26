from flask import Flask, request, jsonify
from flask_cors import CORS
from spark_job import run_sentiment

app = Flask(__name__)
CORS(app)  # Allows frontend JS from another IP

# Home route (optional)
@app.route("/")
def home():
    return "Flask backend is running!"

# Sentiment analysis route
@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.json
    text = data.get("text", "")
    score = run_sentiment(text)

    sentiment = (
        "Positive" if score > 0 else
        "Negative" if score < 0 else
        "Neutral"
    )

    return jsonify({
        "score": score,
        "sentiment": sentiment
    })

if __name__ == "__main__":
    # Run on your machine's IP so other devices can access
    app.run(host="10.198.228.48", port=5000, debug=True)
