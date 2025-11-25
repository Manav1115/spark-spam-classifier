# Email Spam Classification System

## Table of Contents
- [Project Overview](#project-overview)
- [Features](#features)
- [Technology Stack & Installation](#technology-stack--installation)
- [Project Structure](#project-structure)
- [Setup Instructions](#setup-instructions)
  - [Backend Setup (Flask)](#backend-setup-flask)
  - [Frontend Setup (React)](#frontend-setup-react)
  - [Spark Setup](#spark-setup)
- [Running the Application](#running-the-application)
- [ML Model Details](#ml-model-details)
  - [Model Architecture](#model-architecture)
  - [Data Preprocessing](#data-preprocessing)
  - [Training the Model](#training-the-model)
  - [Model Performance](#model-performance)
- [API Documentation](#api-documentation)
- [Troubleshooting](#troubleshooting)

---

## Project Overview

The **Email Spam Classification System** is a comprehensive big data solution designed to classify emails as spam or legitimate (ham) using Apache Spark and machine learning. The system leverages a **Naive Bayes classifier** trained on the SpamAssassin dataset to achieve high accuracy in spam detection.

### What This Project Does:
- Analyzes email content to determine if it's spam or legitimate
- Provides real-time predictions through a REST API
- Offers a user-friendly web interface for testing classifications
- Uses distributed computing (Apache Spark) for scalable data processing
- Implements advanced NLP techniques for text preprocessing and feature extraction

---

## Features

✅ **Real-time Email Classification** - Predict whether an email is spam with high accuracy  
✅ **Spark-based ML Pipeline** - Scalable machine learning using Apache Spark  
✅ **Naive Bayes Classifier** - Advanced probabilistic classification model  
✅ **REST API Backend** - Flask-based API for predictions  
✅ **React Frontend** - Modern, responsive UI for user interaction  
✅ **Advanced NLP Processing** - Tokenization, stop-word removal, TF-IDF vectorization  
✅ **Real-time Probability Scores** - Confidence scores for spam predictions  
✅ **CORS Support** - Secure cross-origin requests  

---

## Technology Stack & Installation

### Required Tools

| Tool | Version | Purpose |
|------|---------|---------|
| **Python** | 3.8+ | Backend and ML training |
| **Node.js** | 16+ | Frontend development |
| **Apache Spark** | 3.5.7 | Distributed ML framework |
| **Java/JDK** | 11+ | Required for Spark |
| **Flask** | 3.1.2 | Web framework for API |
| **React** | 19.2.0 | Frontend framework |
| **PySpark** | 3.5.7 | Python Spark bindings |

### Installation Steps

#### 1. Install Python (if not installed)
```bash
# Windows
# Download from https://www.python.org/downloads/

# Verify installation
python --version
pip --version
```

#### 2. Install Node.js (if not installed)
```bash
# Download from https://nodejs.org/
# Verify installation
node --version
npm --version
```

#### 3. Install Apache Spark
```bash
# Download Spark 3.5.7 from https://spark.apache.org/downloads.html
# Extract to preferred location (e.g., C:\spark or ~/spark)

# Set SPARK_HOME environment variable
# Windows: setx SPARK_HOME "C:\path\to\spark"
# Linux/Mac: export SPARK_HOME="/path/to/spark"

# Verify installation
spark-submit --version
```

#### 4. Install Java/JDK
```bash
# Download from https://www.oracle.com/java/technologies/downloads/
# Or use OpenJDK

# Verify installation
java -version
```

#### 5. Install Python Dependencies
```bash
# Navigate to backend directory
cd bigdata_project/backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate

# Install requirements
pip install -r requirements.txt
```

#### 6. Install Node.js Dependencies
```bash
# Navigate to frontend directory
cd bigdata_project/Email-classifier

# Install dependencies
npm install
```

#### 7. Build Tailwind CSS
```bash
# The frontend is already configured with Tailwind CSS
# It will build automatically during npm run dev or npm run build
```

---

## Project Structure

```
Email Spam Classification/
├── bigdata_project/
│   ├── backend/
│   │   ├── app.py                 # Flask API server
│   │   ├── requirements.txt       # Python dependencies
│   │   └── venv/                  # Virtual environment
│   │
│   └── Email-classifier/          # React frontend
│       ├── src/
│       │   ├── App.jsx            # Main React component
│       │   ├── App.css            # Component styles
│       │   ├── api.js             # API client functions
│       │   ├── main.jsx           # React entry point
│       │   ├── index.css          # Global styles
│       │   └── assets/            # Images and assets
│       ├── package.json           # Node dependencies
│       ├── vite.config.js         # Vite config
│       ├── tailwind.config.js     # Tailwind CSS config
│       ├── index.html             # HTML template
│       └── public/                # Public assets
│
├── spark_ml/
│   ├── train_spam_ml.py           # Model training script
│   ├── prepare_data.py            # Data preprocessing
│   ├── prepare_spamassassin.py    # SpamAssassin data loader
│   ├── data/
│   │   └── emails.csv             # Training dataset
│   ├── model_spam_nb/             # Trained model (Naive Bayes)
│   │   ├── metadata/
│   │   └── stages/                # Pipeline stages
│   └── raw/
│       ├── easy_ham/              # Legitimate emails
│       ├── hard_ham/              # Hard-to-classify ham
│       └── spam/                  # Spam emails
│
└── spark/
    ├── spark/                     # Apache Spark installation
    ├── start-worker1.sh           # Worker node startup
    └── start-worker2.sh           # Worker node startup
```

---

## Setup Instructions

### Backend Setup (Flask)

#### Step 1: Create Python Virtual Environment
```bash
cd bigdata_project/backend
python -m venv venv
```

#### Step 2: Activate Virtual Environment
```bash
# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

#### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

The `requirements.txt` includes:
- **flask==3.1.2** - Web framework
- **flask-cors==6.0.1** - Enable CORS for frontend
- **pyspark==3.5.7** - Spark ML library
- **py4j==0.10.9.7** - Java integration
- **numpy==2.2.6** - Numerical computing

#### Step 4: Configure Spark Connection
Edit `app.py` and set the following environment variables:

```python
os.environ["SPARK_HOME"] = "/path/to/spark"
os.environ["HADOOP_HOME"] = "/path/to/spark"
SPARK_MASTER = "spark://YOUR_MASTER_IP:7077"
MODEL_PATH = "/path/to/model_spam_nb"
```

**For Local Testing (without Spark cluster):**
```python
SPARK_MASTER = "local[*]"  # Uses local machine cores
```

#### Step 5: Ensure Model is Available
The trained Naive Bayes model should be at the path specified in `MODEL_PATH`. If not available, train it using the instructions in [Training the Model](#training-the-model) section.

---

### Frontend Setup (React)

#### Step 1: Navigate to Frontend Directory
```bash
cd bigdata_project/Email-classifier
```

#### Step 2: Install Node Dependencies
```bash
npm install
```

This installs:
- **react==19.2.0** - UI framework
- **vite==7.2.4** - Build tool and dev server
- **tailwindcss==2.2.19** - CSS framework
- **lucide-react** - Icon library
- **eslint** - Code linting

#### Step 3: Verify Configuration
The frontend is configured to connect to the backend API at `http://localhost:5000`. This is defined in `src/api.js`:

```javascript
const res = await fetch("http://localhost:5000/predict", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({ text }),
});
```

If your backend runs on a different URL, update this in `src/api.js` and `src/App.jsx`.

---

### Spark Setup

#### Step 1: Install Spark
```bash
# Download Spark 3.5.7
# https://spark.apache.org/downloads.html

# Extract to desired location
# Example: C:\spark or ~/spark
```

#### Step 2: Set Environment Variables
```bash
# Windows (PowerShell)
$env:SPARK_HOME = "C:\path\to\spark"
$env:HADOOP_HOME = "C:\path\to\spark"
$env:JAVA_HOME = "C:\path\to\java"

# Linux/Mac
export SPARK_HOME="/path/to/spark"
export HADOOP_HOME="/path/to/spark"
export JAVA_HOME="/path/to/java"
```

#### Step 3: Verify Spark Installation
```bash
spark-submit --version
spark-shell --version
```

#### Step 4: Configure Master Node (for distributed setup)
Edit `$SPARK_HOME/conf/spark-env.sh`:

```bash
SPARK_MASTER_HOST=YOUR_MASTER_IP
SPARK_MASTER_PORT=7077
SPARK_MASTER_WEBUI_PORT=8080
```

---

## Running the Application

### Option 1: Local Mode (Single Machine)

#### Terminal 1: Start Backend
```bash
cd bigdata_project/backend

# Activate virtual environment
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate

# Run Flask server
python app.py
```

Backend will start at: `http://localhost:5000`

#### Terminal 2: Start Frontend
```bash
cd bigdata_project/Email-classifier

# Start development server
npm run dev
```

Frontend will start at: `http://localhost:5173` (or another port shown)

#### Access the Application
Open your browser and go to: `http://localhost:5173`

---

### Option 2: Distributed Mode (with Spark Cluster)

#### Step 1: Start Spark Master
```bash
$SPARK_HOME/sbin/start-master.sh
```

Master will run at: `spark://YOUR_IP:7077`
Web UI at: `http://YOUR_IP:8080`

#### Step 2: Start Spark Workers
```bash
# Start multiple workers
$SPARK_HOME/sbin/start-slave.sh spark://MASTER_IP:7077
$SPARK_HOME/sbin/start-slave.sh spark://MASTER_IP:7077
```

#### Step 3: Update Backend Configuration
In `bigdata_project/backend/app.py`, change:
```python
SPARK_MASTER = "spark://YOUR_MASTER_IP:7077"
```

#### Step 4: Start Backend and Frontend (same as Option 1)

---

### Full Startup Sequence

```bash
# Terminal 1: Spark Master
cd spark
./sbin/start-master.sh

# Terminal 2: Spark Worker 1
cd spark
./sbin/start-slave.sh spark://YOUR_IP:7077

# Terminal 3: Spark Worker 2
cd spark
./sbin/start-slave.sh spark://YOUR_IP:7077

# Terminal 4: Backend
cd bigdata_project/backend
source venv/bin/activate
python app.py

# Terminal 5: Frontend
cd bigdata_project/Email-classifier
npm run dev
```

---

## ML Model Details

### Model Architecture

The classification pipeline consists of 5 stages:

#### Stage 1: RegexTokenizer
- **Purpose**: Converts text into tokens (words)
- **Configuration**: 
  - Pattern: `\\W+` (splits on non-word characters)
  - Input Column: `text`
  - Output Column: `tokens`

#### Stage 2: StopWordsRemover
- **Purpose**: Removes common words that don't add value
- **Configuration**:
  - Input Column: `tokens`
  - Output Column: `filtered`
  - Removes words like: "the", "a", "and", "is", etc.

#### Stage 3: CountVectorizer
- **Purpose**: Converts words to numerical feature vectors
- **Configuration**:
  - Vocabulary Size: 30,000 words
  - Minimum Document Frequency: 3 (prevents rare words)
  - Input Column: `filtered`
  - Output Column: `rawFeatures`

#### Stage 4: IDF (Inverse Document Frequency)
- **Purpose**: Weights words based on their importance
- **How it works**:
  - Words appearing in many documents get lower weight
  - Rare but distinctive words get higher weight
  - Input Column: `rawFeatures`
  - Output Column: `features`

#### Stage 5: Naive Bayes Classifier
- **Algorithm**: Multinomial Naive Bayes
- **Type**: Binary Classification (Spam vs. Ham)
- **Smoothing**: 1.0 (Laplace smoothing to prevent zero probabilities)
- **Input Column**: `features`
- **Output Columns**: `prediction`, `probability`

### Data Preprocessing

#### Data Source
- **SpamAssassin Dataset**: Public benchmark dataset for spam classification
- **Distribution**:
  - Easy Ham: Legitimate emails
  - Hard Ham: Difficult-to-classify legitimate emails
  - Spam: Known spam emails

#### Preprocessing Steps

```python
# 1. Load CSV data
df = spark.read.csv(data_path, header=True, inferSchema=True)

# 2. Convert label to double (required for ML)
df = df.withColumn("label", col("label").cast("double"))

# 3. Convert text to lowercase
df = df.withColumn("text", lower(col("text")))

# 4. Remove special characters (keep only alphanumeric and spaces)
df = df.withColumn("text", regexp_replace("text", "[^a-zA-Z0-9 ]", " "))
```

#### Data Format
The training CSV should have two columns:
```
label,text
1,"GET FREE MONEY NOW!!!"
0,"Hi, I wanted to check if you're available for coffee tomorrow?"
```

- **label=1**: Spam
- **label=0**: Ham (Legitimate)

#### Train/Test Split
- **Training Set**: 80% of data
- **Test Set**: 20% of data
- **Random Seed**: 42 (for reproducibility)

---

### Training the Model

#### Step 1: Prepare Data
Ensure your email data is in CSV format at: `spark_ml/data/emails.csv`

Format:
```csv
label,text
1,SPAM EMAIL CONTENT...
0,LEGITIMATE EMAIL CONTENT...
```

#### Step 2: Start Spark (if using cluster)
```bash
# From spark directory
./sbin/start-master.sh
./sbin/start-slave.sh spark://YOUR_IP:7077
```

#### Step 3: Run Training Script
```bash
cd spark_ml

# Activate Python virtual environment
source ../bigdata_project/backend/venv/bin/activate

# Train model locally
python train_spam_ml.py \
  --master local[*] \
  --data-path ./data/emails.csv \
  --model-out ./model_spam_nb

# OR train on Spark cluster
python train_spam_ml.py \
  --master spark://YOUR_IP:7077 \
  --data-path ./data/emails.csv \
  --model-out ./model_spam_nb
```

#### Step 4: Model Training Output
The script will output:
```
SparkSession created: SpamClassifier_NaiveBayes
Schema:
 |-- label: double
 |-- text: string
Total rows: 5172

Train: 4137 Test: 1035

🔥 AUC = 0.9876
Precision = 0.9512
Recall    = 0.9234
F1 Score  = 0.9371

✅ Model successfully saved to: ./model_spam_nb
```

---

### Model Performance

#### Metrics Explanation

| Metric | Formula | Meaning |
|--------|---------|---------|
| **AUC (Area Under ROC)** | - | Overall classification quality (0.5-1.0, 1.0 is perfect) |
| **Precision** | TP/(TP+FP) | Of emails marked as spam, how many actually are spam? |
| **Recall** | TP/(TP+FN) | Of all spam emails, how many did we catch? |
| **F1 Score** | 2×(P×R)/(P+R) | Harmonic mean of Precision and Recall |

Where:
- **TP** (True Positives): Correctly identified spam
- **FP** (False Positives): Legitimate emails marked as spam
- **FN** (False Negatives): Spam emails marked as legitimate

#### Expected Performance
- **AUC**: 0.95-0.99
- **Precision**: 0.92-0.96 (avoid false positives)
- **Recall**: 0.90-0.95 (catch most spam)
- **F1 Score**: 0.91-0.95

---

## API Documentation

### Prediction Endpoint

#### Request
```
POST http://localhost:5000/predict
Content-Type: application/json

{
  "text": "Get rich quick! Click here now!!!"
}
```

#### Response
```json
{
  "prediction": 1,
  "spam_probability": 0.87
}
```

#### Response Fields
- **prediction**: 
  - `1` = Spam detected
  - `0` = Legitimate email
- **spam_probability**: 
  - Confidence score (0.0 to 1.0)
  - Higher value = more likely to be spam

#### Example Requests

**Spam Example:**
```bash
curl -X POST http://localhost:5000/predict \
  -H "Content-Type: application/json" \
  -d '{"text":"BUY NOW! LIMITED TIME OFFER! CLICK HERE!"}'
```

Response:
```json
{
  "prediction": 1,
  "spam_probability": 0.92
}
```

**Ham Example:**
```bash
curl -X POST http://localhost:5000/predict \
  -H "Content-Type: application/json" \
  -d '{"text":"Hi, just wanted to check on the project status. When can we meet?"}'
```

Response:
```json
{
  "prediction": 0,
  "spam_probability": 0.05
}
```

#### Health Check Endpoint
```
GET http://localhost:5000/
```

Response: `Backend + Spark (WSL) is running!`

---

## Troubleshooting

### Issue: Backend won't start - Spark connection error

**Solution:**
```bash
# Check if Spark master is running
# If not running Spark cluster, use local mode in app.py:
SPARK_MASTER = "local[*]"

# Restart backend
python app.py
```

### Issue: Frontend can't connect to backend - CORS error

**Solution:**
1. Verify backend is running on port 5000
2. Check if Flask-CORS is installed:
   ```bash
   pip install flask-cors
   ```
3. Verify `app.py` has CORS enabled:
   ```python
   CORS(app)
   ```

### Issue: Model not found - FileNotFoundError

**Solution:**
```bash
# Train the model first
cd spark_ml
python train_spam_ml.py --master local[*] --data-path ./data/emails.csv --model-out ./model_spam_nb

# Verify model exists
ls -la ./model_spam_nb
```

### Issue: Frontend won't load on localhost:5173

**Solution:**
```bash
# Kill any process on port 5173
# Windows PowerShell
Stop-Process -Name node -Force

# Linux/Mac
lsof -ti:5173 | xargs kill

# Restart frontend
cd bigdata_project/Email-classifier
npm run dev
```

### Issue: Python module not found errors

**Solution:**
```bash
# Verify virtual environment is activated
# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt

# Verify installation
python -c "import pyspark; print(pyspark.__version__)"
```

### Issue: Spark job fails with Java errors

**Solution:**
```bash
# Verify Java is installed and JAVA_HOME is set
java -version

# Set JAVA_HOME environment variable
# Windows PowerShell
$env:JAVA_HOME = "C:\path\to\java"

# Linux/Mac
export JAVA_HOME=/path/to/java

# Restart Spark
./sbin/stop-all.sh
./sbin/start-master.sh
```

### Issue: Port already in use (5000 or 5173)

**Solution:**
```bash
# Find and kill process on port 5000
# Windows PowerShell
Get-Process -Id (Get-NetTCPConnection -LocalPort 5000).OwningProcess | Stop-Process

# Linux/Mac
lsof -ti:5000 | xargs kill

# Start backend on different port
# Edit app.py: app.run(port=5001)
```

---

## Performance Optimization Tips

1. **Increase Spark Memory** (for large datasets):
   ```python
   .config("spark.executor.memory", "8g")
   .config("spark.driver.memory", "8g")
   ```

2. **Add More Workers** (for distributed processing):
   ```bash
   ./sbin/start-slave.sh spark://MASTER_IP:7077
   ```

3. **Cache Model in Memory**:
   ```python
   model = PipelineModel.load(MODEL_PATH)
   model.cache()  # Pre-cache model for faster predictions
   ```

4. **Batch Predictions** (instead of single predictions):
   - Send multiple emails in one request for better throughput

---

## Contributing

Contributions are welcome! To contribute:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

---

## License

This project is part of the Email Spam Classification system.

---

## Support

For issues or questions:
- Check the [Troubleshooting](#troubleshooting) section
- Review the [API Documentation](#api-documentation)
- Check Spark logs in `spark/logs/`
- Verify configuration in `app.py`

---

## Summary

This Email Spam Classification System combines modern web technologies (React, Flask) with big data processing (Apache Spark) and machine learning (Naive Bayes) to provide accurate, scalable spam detection. Follow the setup instructions to get started in minutes!

