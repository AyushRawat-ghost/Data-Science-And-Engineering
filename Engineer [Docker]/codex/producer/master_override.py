import threading
import time

try:
    from sensor_readings import run_t1_producer
    from device import run_t3_producer
    from facility import run_t4_producer
except ImportError as e:
    print(f"Error importing producer scripts: {e}")
    print("Please ensure producer_t1.py, producer_t3.py, and producer_t4.py are in the correct path.")
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