# Start from the official Airflow image
FROM apache/airflow:2.8.1-python3.11

# --- Constants for Installation ---
ENV SHC_VERSION=1.1.1-2.1-s_2.11
ENV SHC_JAR=shc-core-$SHC_VERSION.jar
ENV SPARK_JARS_PATH=/usr/local/spark/jars/

# Install required system dependencies
USER root
RUN apt-get update \
    && apt-get install -y --no-install-recommends openjdk-17-jdk-headless \
    && apt-get install -y curl wget \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

    # Ensure Spark knows where to find the libraries
ENV SPARK_CONF_DIR=/usr/local/spark/conf 

# Switch back to the Airflow user
USER airflow

# Install Python packages, including PySpark and Kafka clients
RUN pip install --no-cache-dir \
    pyspark==4.0.1 \
    pandas \
    kafka-python \
    happybase \
    thrift \
    weaviate-client \
    langchain-weaviate \
    langchain