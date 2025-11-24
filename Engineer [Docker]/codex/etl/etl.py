import sys
import os
from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql.types import LongType, StructType, StructField, StringType, DoubleType
from typing import Dict, Any

# --- CRITICAL FIX: Ensure Python can find 'scripts' package for utilities ---
sys.path.append("/opt/airflow") 

# --- Configuration Constants ---
T1_READINGS = 'sensor_readings'
T3_DEVICE = 'device'
T4_FACILITY = 'facility'
T5_SUMMARY = 'hourly_summary'
T6_ALERTS = 'alert_history'
T2_AUDIT = 'audit_log' 

# HBase Connection Hostnames (used for Spark configuration)
HBASE_ZOOKEEPER_QUORUM = "zookeeper" 
HDFS_ROOT_DIR = "hdfs://namenode:8020/hbase" 

# Mapping for T1: sensor_readings
T1_READINGS_MAPPING = {
    "rowkey": "row_key,string", 
    "cfs": [
        {"cf": "m", "qualifiers": ["temp_val", "humid_val", "vibration_mms"]},
        {"cf": "c", "qualifiers": ["reading_ts", "sensor_status", "facility_id"]}
    ]
}

# Mapping for T4: facility (Rules Lookup)
T4_FACILITY_MAPPING = {
    "rowkey": "facility_id,string",
    "cfs": [
        {"cf": "rules", "qualifiers": ["temp_max_c", "alert_recipient"]},
        {"cf": "meta", "qualifiers": ["city"]}
    ]
}

# Mapping for T3: device (Metadata Lookup) - Reading PK (device_id)
T3_DEVICE_MAPPING = {
    "rowkey": "device_id,string",
    "cfs": [
        {"cf": "info", "qualifiers": ["model_number"]},
        {"cf": "loc", "qualifiers": ["facility_id"]}
    ]
}

HBASE_SCHEMA_MAPPINGS = {
    T1_READINGS: T1_READINGS_MAPPING,
    T4_FACILITY: T4_FACILITY_MAPPING,
    T3_DEVICE: T3_DEVICE_MAPPING,
}

def create_spark_session(app_name: str) -> SparkSession:
    return SparkSession.builder \
        .appName(app_name) \
        .config("hbase.zookeeper.quorum", HBASE_ZOOKEEPER_QUORUM) \
        .config("hbase.rootdir", HDFS_ROOT_DIR) \
        .getOrCreate()

def generate_hbase_column_string(mapping: Dict[str, Any]) -> str:
    column_parts = []
    rk_name, rk_type = mapping["rowkey"].split(',')
    column_parts.append(f'{rk_name} :key {rk_type}')

    for cf_data in mapping["cfs"]:
        cf = cf_data["cf"]
        for qualifier in cf_data["qualifiers"]:
            column_parts.append(f'{qualifier} {cf}:{qualifier} string') 
            
    return ", ".join(column_parts)

def read_hbase_table(spark: SparkSession, table_name: str) -> SparkSession.DataFrame:
    mapping = HBASE_SCHEMA_MAPPINGS.get(table_name)
    if not mapping:
        print(f"ERROR: Mapping not defined for table {table_name}")
        return spark.createDataFrame([], StructType([]))
        
    mapping_string = generate_hbase_column_string(mapping)
    print(f"--- Reading LIVE data from HBase table: {table_name} ---")
    
    try:
        df = spark.read.format("org.apache.hadoop.hbase.spark") \
            .option("hbase.columns.mapping", mapping_string) \
            .option("hbase.table", table_name) \
            .option("hbase.mapreduce.scan.cachedrows", "20000") \
            .load()
            
        if table_name == T1_READINGS:
            df = df.withColumn("reading_ts_long", df["reading_ts"].cast(LongType()))
            df = df.withColumn("timestamp", (df["reading_ts_long"] / 1000).cast("timestamp"))
            df = df.withColumn("temp_c", df["temp_val"].cast(DoubleType()))
            df = df.withColumn("humid_pct_num", df["humid_val"].cast(DoubleType()))
            
        if table_name == T4_FACILITY:
             df = df.withColumn("temp_max_c_num", df["temp_max_c"].cast(DoubleType()))
            
        print(f"Loaded {df.count()} live records from table {table_name}.")
        return df

    except Exception as e:
        print(f"🔴 CRITICAL ERROR: Failed to read from HBase table {table_name}. Check Spark-HBase JAR path.")
        return spark.createDataFrame([], StructType([]))