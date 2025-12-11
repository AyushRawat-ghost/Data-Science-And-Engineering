import time
import random
from scripts.utils.producer_base import get_producer, send_message
from typing import Dict, Any, List

KAFKA_TOPIC = 'iot_readings'

# --- Master Lists (Parent Keys) ---
MASTER_DEVICES: List[str] = [f'DEV_{i:04}' for i in range(1, 21)]
MASTER_FACILITIES: List[str] = ['Minerva', 'Aether', 'Poseidon', 'Demeter', 'Apollo', 'Hades', 'Eleuthia', 'Artemis', 'Hephastus']

# --- Unified Sensor Profiles (Used for Realistic Generation) ---
SENSOR_BASELINE = {
    'temp_c': {'baseline': 35.0, 'stddev': 0.8, 'alert_threshold': 40.0},
    'humid_pct': {'baseline': 55.0, 'stddev': 3.0, 'alert_threshold': 75.0},
    'pressure_hpa': {'baseline': 995.0, 'stddev': 2.0, 'alert_threshold': 975.0},
    'vibration_mms': {'baseline': 1.5, 'stddev': 0.5, 'alert_threshold': 4.5}
}

def generate_t1_data() -> Dict[str, Any]:
    """
    Generates a single, dense structured sensor reading payload matching the T1 schema.
    """
    
    device_id = random.choice(MASTER_DEVICES)
    facility_id = random.choice(MASTER_FACILITIES)
    
    current_readings = {}
    is_alert = False

    # Generate all four measurements simultaneously
    for key, profile in SENSOR_BASELINE.items():
        value = random.gauss(profile['baseline'], profile['stddev'])

        if random.random() < 0.02:
            if profile['alert_threshold'] > profile['baseline']: 
                value = profile['alert_threshold'] + random.uniform(1.0, 5.0) 
            else: 
                value = profile['alert_threshold'] - random.uniform(1.0, 5.0)
            is_alert = True
        
        current_readings[key] = round(value, 2)
    
    # Determine overall status
    status = 'CRITICAL' if is_alert else 'OK'

    return {
        'type': 'SENSOR_READING', # CRITICAL: Type matches consumer
        'device_id': device_id,
        'timestamp': int(time.time() * 1000), 
        
        # --- Data Fields matching Consumer/HBase T1 Schema ---
        'temp_c': current_readings['temp_c'],
        'humid_pct': current_readings['humid_pct'],
        'pressure_hpa': current_readings['pressure_hpa'],
        'vibration_mms': current_readings['vibration_mms'],
        
        # Context Fields
        'sensor_status': status,
        'facility_id': facility_id # FK
    }

def run_t1_producer():
    producer = get_producer()
    print("T1 Producer (Raw Readings) streaming - HIGH VOLUME...")
    
    try:
        while True:
            device_id = random.choice(MASTER_DEVICES)
            data = generate_t1_data()
            
            send_message(producer, KAFKA_TOPIC, data['device_id'], data)
            time.sleep(0.02)
            
    except Exception as e:
        print(f"Producer T1 encountered a critical error: {e}")
    finally:
        producer.close()
