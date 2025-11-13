# Start from the official Airflow image
FROM apache/airflow:2.8.1-python3.11

# Install required system dependencies (for PySpark/Java)
USER root
RUN apt-get update \
    && apt-get install -y --no-install-recommends openjdk-17-jdk-headless \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Switch back to the Airflow user
USER airflow

# Install Python packages, including PySpark and Kafka clients
RUN pip install --no-cache-dir \
    pyspark==4.0.1 \
    pandas \
    kafka-python
    happybase \
    weaviate-client \
    langchain-weaviate \
    langchain