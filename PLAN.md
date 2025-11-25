# Project Plan for Spam Classifier using Spark MLlib with Docker and UI Interface

## Information Gathered

- Scala Spark code "SpamClassifier.scala" is provided. It loads training and testing spam/nospam text datasets, builds a text classification pipeline with LinearSVC, uses regex tokenizers, stop word remover, count vectorizer, IDF, vector assembler, and string indexer.
- CrossValidator with param tuning is used.
- The data files are simple labeled plain text lines split into spam and non-spam files.
- The requirement includes a distributed Spark cluster with one master node and at least two worker nodes.
- The setup should use Docker for containerized clustering.
- The system should also have a UI frontend interface built using any frontend framework or language.
- User wants explanations of Spark usage commands and basic usage.
- User needs to share the GitHub repository link for evaluation.
- The environment currently contains no visible UI files or Docker setup.

## Plan

### 1. Spark Usage and Commands

- Explain how to build and run the Spark Scala application locally using `spark-submit`.
- Provide commands for running the application on a local Spark cluster for testing.
- Specify how to run the application on a standalone Spark cluster.

### 2. Dockerized Spark Cluster Setup

- Create Dockerfiles for Spark Master and Spark Worker(s).
- Create a `docker-compose.yml` file that defines:
  - Spark Master container
  - At least two Spark Worker containers connecting to the master
- Configure networking and environment variables for Spark cluster.
- Include instructions for building and starting the Spark cluster using Docker Compose.

### 3. UI Interface

- Develop a simple UI that allows a user to input a text message.
- The UI sends the input text to the Spark backend (could be a REST API endpoint or batch job submission).
- The UI displays spam or not spam prediction results.
- Use a simple frontend framework like React or vanilla HTML/JavaScript for the interface.
- Include instructions to run the frontend locally or containerize the UI in Docker for easier deployment with Spark cluster.

### 4. Integration

- Depending on implementation choices:
  - Extend Spark Scala app to expose a simple REST API or batch prediction service, or
  - Create an additional microservice that queries the Spark cluster and provides prediction API for the UI.
- Make sure the UI and Spark backend can communicate either via HTTP or shared files.
- Provide examples of usage flow.

### 5. GitHub Repository Setup

- Organize repository with subfolders:
  - `spark/` for Scala and Spark related files
  - `docker/` for Dockerfiles and docker-compose.yml
  - `ui/` for frontend interface code
  - README.md to include project overview, setup instructions, commands, and demo steps.
- Instructions for cloning, building, running cluster, running UI, and testing.

## Dependent Files to be Edited/Created

- `docker/Dockerfile-master` - Spark Master node Dockerfile
- `docker/Dockerfile-worker` - Spark Worker node Dockerfile
- `docker/docker-compose.yml` - Compose config for multi-node Spark cluster
- `ui/` folder - frontend files (e.g. `index.html`, `app.js`, or React files)
- `README.md` - Project documentation with explanations and instructions
- Enhancement of `SpamClassifier.scala` if needed to fit cluster mode and possible REST integration

## Followup Steps

- Develop and test Docker setup to launch multi-node Spark cluster.
- Prepare Spark scala app for clustered environment.
- Build and test UI interface.
- Write clear README with instructions, explain commands and usage.
- Validate end-to-end system.
- Push code to GitHub repository and provide link.

---

Please confirm if this plan meets your expectations or if you want me to modify/add anything before I proceed with the implementation steps.
