# SPARK  EMAIL SPAM CLASSIFIER

## PySpark + Streamlit + Pandas + Seaborn

This project performs **distributed spam classification** using **PySpark** and visualizes results in a beautiful **Streamlit dashboard**.  
It also includes a complete guide for running a **Spark Master–Worker cluster on Windows 11**.


The project also includes detailed instructions for setting up an Apache Spark Master–Worker cluster on Windows 11 machines.

----------

## 🚀 Features

- Distributed text preprocessing using PySpark  
- Spam/Nospam prediction using Naive Bayes ML pipeline  
- Streamlit interactive dashboard  
- TF-IDF + CountVectorizer NLP pipeline  
- Dataset statistics, charts & visualizations  
- Spam probability bar & keyword analysis  
- Complete Spark cluster setup (Master + Workers)

---

## DATA FILES

Place these files in the project directory or appropriate data folder:

- `emails.csv` (training dataset in CSV format)  
- SpamAssassin raw datasets (easy_ham, hard_ham, spam folders)  


## 📁 Dataset
spam_ml/data/emails.csv
```
Format: 
label,text
1,"WIN MONEY NOW!!!"
0,"Hi, are you free tomorrow?"

Where:

1 → Spam

0 → Ham
```
----------

## REQUIREMENTS

### Python Libraries

Install required packages:

```
pip install streamlit pandas numpy seaborn matplotlib pyspark flask flask-cors
```

### Apache Spark & Hadoop (winutils)

Download and extract Spark to:

```
C:\spark\
```

Download and extract Hadoop (winutils) to:

```
C:\hadoop\bin
```

Set environment variables:

```
SPARK_HOME = C:\spark
HADOOP_HOME = C:\spark\hadoop
PATH += C:\spark\bin; C:\spark\sbin
```

----------

# SETTING UP SPARK CLUSTER (WINDOWS 11)

You can run Spark on multiple laptops:

- Laptop 1 → Master  
- Laptop 2/3 → Worker nodes  

### Step 1: Verify Java 

```
java -version
```

![Java Version](https://github.com/user-attachments/assets/87da6825-036e-4c9f-9b2f-d53b7331adff)

### Step 2: Start Spark Master (Laptop 1)

Run:

```
spark-shell
```

If spark is properly installed, you'll see something like this

![01_spark-shell](https://github.com/user-attachments/assets/d3d7c324-0dd4-4053-8ed0-ebe5faa91d33)



Then start the master node by running:

```
spark-class org.apache.spark.deploy.master.Master
```

Terminal will show the confirmation like this:-

![02-Spark-Master-Deploy](https://github.com/user-attachments/assets/4d2a760f-12a5-4c9d-afaa-fdf643e7813f)


Important : 
Note down the Master URL (something like spark://192.168.43.59:7077)
### Step 3: Start Spark Worker (Laptop 2 / Laptop 3)

Run:

```
spark-class org.apache.spark.deploy.worker.Worker spark://192.168.43.59:7077

```
Terminal will look like this:
![03-Spark-Worker-Deploy](https://github.com/user-attachments/assets/15ed485b-6d42-41b6-94de-6fc5a080bcab)


### Step 4: Verify Spark UI

Open:

```
http://localhost:8080

```

![SparkUI-running_job](https://github.com/user-attachments/assets/59c53a1a-6d92-4169-8a11-00d039ebaff2)

You should see:

-   Master node
    
-   Connected workers
    
-   CPU & memory resources
    

----------

# SIMPLE PYSPARK TEST (OPTIONAL)

Create a file `test.py` with the following:

```python
from pyspark import SparkContext
sc = SparkContext("spark://192.168.43.59:7077", "TestApp")
data = sc.parallelize([1,2,3,4,5])
print(data.map(lambda x: x*x).collect())
sc.stop()
```

Run:

```
python test.py
```

This confirms your cluster is working correctly.

----------

# RUNNING THE STREAMLIT DASHBOARD

Start your interactive dashboard using:

```
streamlit run spark_ml/train_spam_ml.py
```

Open the dashboard at:

```
http://localhost:8501
```

----------

# IMPORTANT: UPDATE MASTER URL IN CODE

In your Python training and application scripts, set the Spark master URL:

```python
MASTER_URL = "spark://192.168.43.59:7077"
sc = SparkContext(MASTER_URL, "SpamClassifierApp")
```

For local testing without a cluster:

```python
MASTER_URL = "local[*]"
sc = SparkContext(MASTER_URL, "SpamClassifierApp")
```



# MODEL TRAINING

The training pipeline uses five stages:

1. RegexTokenizer: Tokenizes text input  
2. StopWordsRemover: Removes common stop words  
3. CountVectorizer: Converts tokens to feature vectors  
4. IDF: Applies inverse document frequency weighting  
5. Naive Bayes: Multinomial Naive Bayes classifier  

Training and test split:

- 80% training data  
- 20% test data  
- Random seed 42 for reproducibility  

Sample command to train:

```bash
python train_spam_ml.py --master spark://YOUR_MASTER_IP:7077 --data-path ./spark_ml/data/emails.csv --model-out ./spark_ml/model_spam_nb
```

----------

# API DOCUMENTATION

## Prediction Endpoint

POST http://localhost:5000/predict  
Content-Type: application/json

Example request payload:

```json
{
  "text": "Get rich quick! Click here now!!!"
}
```

Example response:

```json
{
  "prediction": 1,
  "spam_probability": 0.87
}
```

- `prediction`: 1 = Spam, 0 = Ham  
- `spam_probability`: Confidence score from 0.0 to 1.0  

## Health Check Endpoint

GET http://localhost:5000/  
Response: `Backend + Spark (WSL) is running!`

----------

# TROUBLESHOOTING

- Backend Spark connection errors: Use local mode `"local[*]"` in app.py if cluster unavailable  
- Frontend CORS errors: Ensure Flask-CORS is installed and enabled  
- Model file not found: Run training script to generate model  
- Port conflicts: Kill processes occupying ports 5000 (backend) or 8501 (dashboard)  
- Java environment issues: Verify `java -version` and set JAVA_HOME properly  

----------

# SUPPORT

For issues or questions:

- Check logs in the `spark/logs/` folder  
- Verify environment variables and paths in `app.py`  
- Review troubleshooting section above  

----------

# LICENSE

This project is licensed under the terms of your choice.

----------

# CONTRIBUTING

Contributions welcome via pull requests. Please fork and create a feature branch before submitting changes.

----------

