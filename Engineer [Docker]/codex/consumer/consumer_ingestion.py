import json
import time
from kafka import KafkaConsumer, TopicPartition
from typing import Dict, Any, List
import sys
import os
import happybase
import traceback

sys.path.append("/opt/airflow")

# --- Import Utility ---
try:
    from scripts.utils.data_connection import connect_to_hbase
except ImportError:
    print("FATAL: Could not import connect_to_hbase. Ensure scripts/utils/data_connection.py exists.")
    sys.exit(1)

# --- Configuration Constants ---
KAFKA_TOPIC = "iot_readings"

# Inside Docker use kafka:29092, from host use localhost:9092
# Env var will override default, but we also print what we actually use
KAFKA_BROKER = os.environ.get("KAFKA_BROKER", "kafka:29092")

TABLES_NEEDED: List[str] = ["sensor_readings", "device", "facility"]
CONSUMER_GROUP = f"{KAFKA_TOPIC}_ingest_group_stage1_debug"

HBASE_CONNECTION = None
TABLES: Dict[str, Any] = {}


# --- Row Key Generation Utilities ---

def generate_row_key_t1(device_id: str, timestamp_ms: int) -> bytes:
    """Creates the Row Key for sensor_readings (T1): Salt + Device ID + Reversed TS."""
    reversed_ts = str(sys.maxsize - timestamp_ms)
    salt = device_id[-1]
    return f"{salt}_{device_id}_{reversed_ts}".encode("utf-8")


def map_and_ingest(data: Dict[str, Any]):
    global TABLES
    message_type = data.get("type")

    try:
        if message_type == "SENSOR_READING":
            T1_READINGS = TABLES["sensor_readings"]
            row_key = generate_row_key_t1(data["device_id"], data["timestamp"])
            print(f"[T1] RK={row_key.decode()} - {data['temp_c']}C")

            T1_READINGS.put(row_key, {
                b"m:temp_val": str(data["temp_c"]).encode("utf-8"),
                b"m:humid_val": str(data["humid_pct"]).encode("utf-8"),
                b"m:vibration_val": str(data["vibration_mms"]).encode("utf-8"),
                b"c:reading_ts": str(data["timestamp"]).encode("utf-8"),
                b"c:sensor_status": data["sensor_status"].encode("utf-8"),
                b"c:facility_id": data["facility_id"].encode("utf-8"),
            })
            print(f"✅ Ingested T1 Reading from {data['device_id']}")

        elif message_type == "DEVICE_METADATA_UPDATE":
            T3_DEVICE = TABLES["device"]
            row_key = data["device_id"].encode("utf-8")

            T3_DEVICE.put(row_key, {
                b"info:model_number": data["model_number"].encode("utf-8"),
                b"info:firmware_version": data["firmware_version"].encode("utf-8"),
                b"info:installation_date": data["installation_date"].encode("utf-8"),
                b"loc:facility_id": data["facility_id"].encode("utf-8"),
                b"loc:aisle": data["aisle"].encode("utf-8"),
                b"loc:loc_latitude": str(data["loc_latitude"]).encode("utf-8"),
            })
            print(f"🔄 Updated T3 Metadata for {data['device_id']}")

        elif message_type == "FACILITY_CONFIG_UPDATE":
            T4_FACILITY = TABLES["facility"]
            row_key = data["facility_id"].encode("utf-8")

            T4_FACILITY.put(row_key, {
                b"rules:temp_max_c": str(data["temp_max_c"]).encode("utf-8"),
                b"rules:alert_recipient": data["alert_recipient"].encode("utf-8"),
                b"meta:city": data["city"].encode("utf-8"),
                b"meta:manager_name": data["manager_name"].encode("utf-8"),
            })
            print(f"⚙️ Updated T4 Config for {data['facility_id']}")

        else:
            # Ignore other types in Stage 1
            pass

    except KeyError as ke:
        print(f"\n🔴 SCHEMA ERROR: Missing key in payload: {ke} for type {message_type} Full Data: {data}")
    except Exception as e:
        print(f"\n🔴 CRITICAL RUNTIME ERROR: {e}")
        traceback.print_exc(file=sys.stdout)


def run_consumer():
    """Kafka consumer with direct partition assignment (no subscribe) and minimal, clear debug."""
    global HBASE_CONNECTION, TABLES

    # 1. Connect to HBase
    HBASE_CONNECTION, TABLES = connect_to_hbase(TABLES_NEEDED)
    if not HBASE_CONNECTION:
        print("Exiting consumer due to HBase connection failure.")
        return

    print(f"Starting Kafka Consumer. Env KAFKA_BROKER={os.environ.get('KAFKA_BROKER')}")
    print(f"Using broker: {KAFKA_BROKER}, Topic: {KAFKA_TOPIC}")

    # 2. Create consumer WITHOUT subscribe
    consumer = KafkaConsumer(
        bootstrap_servers=KAFKA_BROKER.split(","),
        group_id=None,                 # no consumer group (simpler debugging)
        auto_offset_reset="earliest",
        enable_auto_commit=False,
        value_deserializer=lambda x: json.loads(x.decode("utf-8")),
        session_timeout_ms=10000,
        consumer_timeout_ms=10000,
    )

    # 3. Metadata debug
    try:
        topics = consumer.topics()
        print(f"[META] Topics visible on broker {KAFKA_BROKER}: {topics}")
    except Exception as e:
        print(f"❌ Could not fetch topics from broker {KAFKA_BROKER}: {e}")
        if HBASE_CONNECTION:
            HBASE_CONNECTION.close()
        return

    if KAFKA_TOPIC not in topics:
        print(f"❌ Topic '{KAFKA_TOPIC}' NOT found on this broker.")
        if HBASE_CONNECTION:
            HBASE_CONNECTION.close()
        return

    partitions = consumer.partitions_for_topic(KAFKA_TOPIC)
    print(f"[META] partitions_for_topic('{KAFKA_TOPIC}'): {partitions}")

    if not partitions:
        print(f"❌ Topic '{KAFKA_TOPIC}' has no partitions.")
        if HBASE_CONNECTION:
            HBASE_CONNECTION.close()
        return

    # 4. DIRECT ASSIGNMENT ONLY (no subscribe)
    # For now we just read all partitions; your topic has only {0} anyway
    topic_partitions = [TopicPartition(KAFKA_TOPIC, p) for p in partitions]
    consumer.assign(topic_partitions)
    print(f"✅ Directly assigned partitions: {topic_partitions}")

    # Seek to the beginning of each partition every run (for debugging)
    consumer.seek_to_beginning()

    # Offset debug
    try:
        beginning = consumer.beginning_offsets(topic_partitions)
        end = consumer.end_offsets(topic_partitions)
        for tp in topic_partitions:
            cur = consumer.position(tp)
            print(
                f"[OFFSETS] {tp}: beginning={beginning.get(tp)}, "
                f"end={end.get(tp)}, current_after_seek={cur}"
            )
    except Exception as e:
        print(f"Warning: Could not fetch offsets: {e}")

    print("Begin the Ultimate (reading messages now)...")

    # 5. Consume loop with controlled empty polling
    empty_polls = 0
    MAX_EMPTY_POLLS = 20

    try:
        while True:
            messages = consumer.poll(timeout_ms=5000)

            if not messages:
                empty_polls += 1
                print(f"[DEBUG] No messages in this poll ({empty_polls}/{MAX_EMPTY_POLLS})")
                if empty_polls >= MAX_EMPTY_POLLS:
                    print("No messages for a while. Exiting consumer cleanly.")
                    break
                time.sleep(1)
                continue

            empty_polls = 0

            for topic_partition, records in messages.items():
                for message in records:
                    print(
                        f"[MSG] partition={topic_partition.partition}, "
                        f"offset={message.offset}, "
                        f"value={message.value}"
                    )
                    map_and_ingest(message.value)

    except KeyboardInterrupt:
        print("\nReceived Ctrl+C, shutting down consumer gracefully...")
    except Exception as e:
        print(f"\nCritical consumer loop error: {e}")
        traceback.print_exc(file=sys.stdout)
    finally:
        if HBASE_CONNECTION:
            HBASE_CONNECTION.close()
        print("Consumer process finished.")


if __name__ == "__main__":
    run_consumer()
