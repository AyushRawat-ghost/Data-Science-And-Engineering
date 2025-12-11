#!/bin/bash
SPARK_PACKAGES="org.apache.hbase:hbase-client:2.1.3,org.apache.hbase:hbase-mapreduce:2.1.3,org.apache.hadoop:hadoop-client:3.2.1"
SPARK_SUBMIT_PATH="${SPARK_HOME}/bin/spark-submit"
HBASE_CONFIG_FILE="/opt/airflow/config/hbase-site.xml"
# Check if the executable exists at the expected SPARK_HOME path
if [ ! -f "$SPARK_SUBMIT_PATH" ]; then
    echo "FATAL: spark-submit not found at SPARK_HOME location. Attempting simple call..."
    SPARK_SUBMIT_PATH="spark-submit"
fi

$SPARK_SUBMIT_PATH \
    --packages "$SPARK_PACKAGES" \
    --files "$HBASE_CONFIG_FILE" \
    /opt/airflow/scripts/etl/etl.py

# Check the exit code of spark-submit
if [ $? -ne 0 ]; then
    echo "🔴 ERROR: PySpark ETL job failed. Check logs for Java/HBase exceptions."
    exit 1
fi

echo "✅ PySpark ETL job execution complete."