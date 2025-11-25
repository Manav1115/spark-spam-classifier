# Spam Classifier Project using Spark MLlib, Docker, and Frontend UI

## Overview

This project implements a spam classifier using Apache Spark MLlib in Scala. It includes:

- A Spark multi-node cluster setup with one Master node and two Worker nodes, containerized using Docker.
- A simple frontend UI to input text and see a spam/not spam prediction (currently simulated).
- The Spark application leverages text datasets and a LinearSVC model pipeline for classification.

## Project Structure

- `SpamClassifier.scala` - Spark MLlib Scala code for training and testing spam classifier.
- `data/` - Contains training and testing spam/nospam text files.
- `docker/` - Dockerfiles and docker-compose.yml for Spark cluster setup.
- `ui/` - Frontend interface files.

## Prerequisites

- Docker and Docker Compose installed on your machine.
- Java 11 installed (for building/running Spark code outside containers if needed).
- sbt (Scala Build Tool) installed if you plan to build/run Spark app locally.

## Running Spark Cluster with Docker

1. Build and start the Spark cluster:

```bash
cd docker
docker-compose build
docker-compose up -d
```

2. Verify Spark Master Web UI at [http://localhost:8080](http://localhost:8080).

3. The Spark workers Web UIs are available at:

- Worker 1: http://localhost:8081
- Worker 2: http://localhost:8082


## Running Spark Application

You can run the Spark Scala application inside the cluster or locally.

- To run locally:

```bash
spark-submit \
  --class SpamClassifier \
  --master local[*] \
  SpamClassifier.jar
```

- To run on the Spark cluster:

You can submit the pre-built `SpamClassifier.jar` to the Spark master in cluster mode. Example:

```bash
spark-submit \
  --class SpamClassifier \
  --master spark://localhost:7077 \
  --deploy-mode client \
  --executor-memory 1G \
  SpamClassifier.jar
```

Replace `localhost` with the hostname or IP of your Spark master node if running on separate machines.

  SpamClassifier.jar
  SpamClassifier.jar

## Running Frontend UI

To run the frontend UI:

- Open `ui/index.html` directly in your browser (easiest for demo).

- Or serve it via a simple HTTP server, e.g., using Python:

```bash
cd ui
python3 -m http.server 8000
```

Then open [http://localhost:8000](http://localhost:8000) in your browser.

Currently, the frontend uses a simple keyword-based spam detection simulation.

## Next Steps

- Integrate the frontend with the Spark backend via a REST API or microservice for real-time classification.
- Enhance the Spark application to expose a prediction API.
- Improve UI/UX for better user interaction.

## GitHub Repository

Please push this project to your GitHub repository for evaluation.

## License

MIT License

---


