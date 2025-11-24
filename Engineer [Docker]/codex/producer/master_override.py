import threading
import time
import os
import sys

AIRFLOW_MOUNT_ROOT = "/opt/airflow"
if AIRFLOW_MOUNT_ROOT not in sys.path:
    sys.path.append(AIRFLOW_MOUNT_ROOT)

try:
    from scripts.producer.sensor_readings import run_t1_producer
    from scripts.producer.device import run_t3_producer
    from scripts.producer.facility import run_t4_producer
except ImportError as e:
    print(f"Error importing producer scripts: {e}")
    print("Please ensure facility.py, sensor_readings.py, and device.py are in the correct path.")
    exit()

def main():
    print("--- 🚀 Starting All IoT Producers Concurrently ---")

    t1_thread = threading.Thread(target=run_t1_producer, name="T1_Telemetry_Producer")
    t3_thread = threading.Thread(target=run_t3_producer, name="T3_Metadata_Producer")
    t4_thread = threading.Thread(target=run_t4_producer, name="T4_Config_Producer")

    t1_thread.start()
    t3_thread.start()
    t4_thread.start()
    
    print("\nProducers T1 (Readings), T3 (Metadata), and T4 (Config) are now running...")
    print("Press Ctrl+C to stop all producers.")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n--- 🛑 Stopping Producers ---")
        print("Producers stopped. Check Kafka topic 'iot_readings' for verification.")

if __name__ == '__main__':
    main()