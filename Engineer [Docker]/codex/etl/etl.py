SPARK_SUBMIT_CMD = """
spark-submit \\
--packages com.hortonworks:shc-core:1.1.1-2.1-s_2.11 \\
/opt/airflow/scripts/etl/pyspark_etl_job.py
"""
import sys
import os
sys.path.append("/opt/airflow")
import time
from pyspark.sql import SparkSession, DataFrame
from pyspark.sql import functions as F
from pyspark.sql.types import LongType, StructType, StructField, StringType, DoubleType
from typing import Dict, Any
import happybase
from scripts.utils.data_connection import connect_to_hbase



# --- Configuration  ---
T1_READINGS = 'sensor_readings'
T3_DEVICE = 'device'
T4_FACILITY = 'facility'
T5_SUMMARY = 'hourly_summary'
T6_ALERTS = 'alert_history'
T2_AUDIT = 'audit_log' 
ETL_SERVICE_NAME = 'PySpark_ETL_Job'

# HBase Connection Hostnames 
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

# Mapping for T4: facility 
T4_FACILITY_MAPPING = {
    "rowkey": "facility_id,string",
    "cfs": [
        {"cf": "rules", "qualifiers": ["temp_max_c", "alert_recipient"]},
        {"cf": "meta", "qualifiers": ["city"]}
    ]
}

# Mapping for T3: device 
T3_DEVICE_MAPPING = {
    "rowkey": "device_id,string",
    "cfs": [
        {"cf": "info", "qualifiers": ["model_number"]},
        {"cf": "loc", "qualifiers": ["facility_id"]}
    ]
}
# Mapping for T5: hourly_summary
T5_SUMMARY_MAPPING = {
    "rowkey": "row_key,string", 
    "cfs": [
        {"cf": "temp", "qualifiers": ["temp_avg_c", "temp_max_obs", "temp_min_obs"]},
        {"cf": "humid", "qualifiers": ["humid_avg_pct", "humid_max_obs", "reading_count"]},
        {"cf": "alert", "qualifiers": ["message"]}
    ]
}

# Mapping for T6: alert_history
T6_ALERTS_MAPPING = {
    "rowkey": "row_key,string",
    "cfs": [
        {"cf": "alert", "qualifiers": ["alert_type", "threshold_value", "actual_value", "manager_name"]}, # Manager name is denormalized
        {"cf": "ref", "qualifiers": ["device_id", "reading_ts", "status"]}
    ]
}
# Mapping for T2: audit_log
T2_AUDIT_MAPPING = {
    "rowkey": "row_key,string",
    "cfs": [
        {"cf": "log", "qualifiers": ["event_level", "message", "service_name"]},
        {"cf": "user", "qualifiers": ["device_id"]}
    ]
}

HBASE_SCHEMA_MAPPINGS = {
    T1_READINGS: T1_READINGS_MAPPING,
    T2_AUDIT:T2_AUDIT_MAPPING,
    T4_FACILITY: T4_FACILITY_MAPPING,
    T3_DEVICE: T3_DEVICE_MAPPING,
    T6_ALERTS : T6_ALERTS_MAPPING,
    T5_SUMMARY:T5_SUMMARY_MAPPING
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

def read_hbase_table(spark: SparkSession, table_name: str) -> DataFrame:
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

def calculate_hourly_summary(readings_df: DataFrame) -> DataFrame:
    hourly_df = readings_df.groupBy(
        "facility_id", 
        F.window(readings_df.timestamp, "1 hour").alias("hour_key")
    ).agg(
        # Temperature Aggregates
        F.avg("temp_c").alias("temp_avg_c"),
        F.max("temp_c").alias("temp_max_obs"),
        F.min("temp_c").alias("temp_min_obs"),
        
        # Humidity Aggregates
        F.avg("humid_pct_num").alias("humid_avg_pct"),
        F.max("humid_pct_num").alias("humid_max_obs"),

        F.count("*").alias("reading_count")
    )
    
    # Message Generation: Check if high temp was observed
    hourly_df = hourly_df.withColumn("alert_message",
        F.when(F.col("temp_max_obs") > 40, 
            F.lit("High Temperature Warning Observed")
        ).otherwise(
            F.lit("Normal Operating Conditions")
        )
    )
    
    # Structure the output for HBase
    summary_df = hourly_df.withColumn("row_key",
        F.concat_ws("_", 
            F.col("facility_id"), 
            F.date_format(F.col("hour_key").start, "yyyyMMddHH")
        )
    ).select(
        "row_key", 
        F.col("facility_id").alias("facility_id"), # FK
        F.col("temp_avg_c").alias("temp:temp_avg_c"),
        F.col("temp_max_obs").alias("temp:temp_max_obs"),
        F.col("temp_min_obs").alias("temp:temp_min_obs"),
        F.col("humid_avg_pct").alias("humid:humid_avg_pct"),
        F.col("humid_max_obs").alias("humid:humid_max_obs"),
        F.col("reading_count").alias("humid:reading_count"),
        F.col("alert_message").alias("alert:message")
    )
    
    print(f"Calculated {summary_df.count()} hourly summary records for T5.")
    return summary_df

def identify_alerts(readings_df: DataFrame, facility_df: DataFrame) -> DataFrame:
    enriched_readings = readings_df.join(
        facility_df.select("facility_id", "temp_max_c_num", "alert_recipient", "manager_name"), 
        on="facility_id", 
        how="inner"
    )
    
    # Filter: Actual temperature > Max allowed temperature (Rule Check)
    alert_df = enriched_readings.filter(enriched_readings.temp_c > enriched_readings.temp_max_c_num)
    
    # Construct the Row Key (PK/FK) for T6: Facility ID + Reversed TS
    alert_df = alert_df.withColumn("alert_row_key", 
        F.concat_ws("_", 
            F.col("facility_id"), 
            F.lit(sys.maxsize).cast(LongType()) - F.col("reading_ts_long") 
        )
    ).withColumn("alert_type", F.lit("TEMP_EXCEEDED"))
    
    print(f"Identified {alert_df.count()} alert events exceeding thresholds for T6.")

    # Select and rename columns to match the T6 schema (alert, ref CFs)
    return alert_df.select(
        F.col("alert_row_key").alias("row_key"),
        F.col("alert_type").alias("alert:alert_type"),
        F.col("temp_max_c_num").alias("alert:threshold_value"),
        F.col("temp_c").alias("alert:actual_value"),
        F.col("manager_name").alias("alert:manager_name"),
        
        # Reference CF
        F.col("device_id").alias("ref:device_id"), # FK
        F.col("reading_ts_long").alias("ref:reading_ts"),
        F.lit("OPEN").alias("ref:status")
    )

def generate_row_key_t2(event_type: str, timestamp_ms: int) -> bytes:
    reversed_ts = str(sys.maxsize - timestamp_ms)
    return f"{event_type}_{reversed_ts}".encode('utf-8')

def write_audit_log(message: str, event_level: str, connection: happybase.Connection):
    T2_AUDIT_TABLE = connection.table(T2_AUDIT)
    current_ts_ms = int(time.time() * 1000)
    
    row_key_t2 = generate_row_key_t2(event_level, current_ts_ms)
    
    try:
        T2_AUDIT_TABLE.put(row_key_t2, {
            # CF 'log'
            b'log:event_level': event_level.encode('utf-8'),
            b'log:message': message.encode('utf-8'),
            b'log:service_name': ETL_SERVICE_NAME.encode('utf-8'),
            # CF 'user'
            b'user:device_id': b'SYSTEM_WIDE', 
        })
        print(f"--- Audited ETL Event [{event_level}]: {message} ---")
    except Exception as e:
        print(f"🔴 CRITICAL AUDIT WRITE FAILURE: Failed to write audit log to T2: {e}")


def run_etl():
    hbase_conn, audit_tables = connect_to_hbase([T2_AUDIT])
    if not hbase_conn:
        print("EXITING ETL: Audit connection failed during startup.")
        return
    spark = create_spark_session("IoTPipelineETL")
    write_audit_log( "ETL Job Started Successfully.", "INFO",hbase_conn)
    
    # 1. Extract LIVE Data from HBase (T1, T4 needed for processing)
    readings_df = read_hbase_table(spark, T1_READINGS)
    facility_df = read_hbase_table(spark, T4_FACILITY)
    
    # --- Check for minimum data integrity before proceeding ---
    if readings_df.count() == 0 or facility_df.count() == 0:
        write_audit_log("Insufficient data in T1/T4 tables. Exiting ETL run.", "WARN",hbase_conn)
        spark.stop()
        return

    # 2. Process T5: Calculate Hourly Aggregations (Gold Data)
    hourly_summary_df = calculate_hourly_summary(readings_df)
    
    # 3. Process T6: Identify and Structure Alerts (Gold Data)
    alert_history_df = identify_alerts(readings_df, facility_df)

    # 4. Write Back to HBase (T5 & T6)
    print("\n--- Writing Gold Layer Results to HBase ---")
    
    #  writing T5: Hourly Summary
    hourly_summary_df.write.format("org.apache.hadoop.hbase.spark") \
        .option("hbase.columns.mapping", generate_hbase_column_string(T5_SUMMARY_MAPPING)) \
        .option("hbase.table", 'hourly_summary') \
        .option("hbase.mapreduce.bulkload.enabled", "true") \
        .mode("append") \
        .save()
    print(f"✅ Successfully wrote {hourly_summary_df.count()} rows to T5 ({T5_SUMMARY}).")

    # writing T6: Alert History
    alert_history_df.write.format("org.apache.hadoop.hbase.spark") \
        .option("hbase.columns.mapping", generate_hbase_column_string(T6_ALERTS_MAPPING)) \
        .option("hbase.table", 'alert_history') \
        .option("hbase.mapreduce.bulkload.enabled", "true") \
        .mode("append") \
        .save()
    print(f"✅ Successfully wrote {alert_history_df.count()} rows to T6 ({T6_ALERTS}).")
    
    write_audit_log("ETL Job Completed Successfully.", "INFO",hbase_conn)
    spark.stop()


if __name__ == "__main__":
    try:
        from scripts.utils.data_connection import connect_to_hbase
    except ImportError:
        print("FATAL: Utility module scripts/utils/data_connections not found.")
        sys.exit(1)
    run_etl()