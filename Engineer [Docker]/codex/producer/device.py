import time
import random
from datetime import date, timedelta
from scripts.utils.producer_base import get_producer, send_message
from typing import Dict, Any, List

KAFKA_TOPIC = 'iot_readings'

MASTER_DEVICES: List[str] = [f'DEV_{i:04}' for i in range(1, 21)]
MASTER_FACILITIES = ['Minerva', 'Aether', 'Poseidon', 'Demeter', 'Apollo', 'Hades', 'Eleuthia', 'Artemis', 'Hephaestus']
AVAILABLE_MODELS: List[str] = ['IoT-X300', 'Sensor-B450', 'Gateway-G10', 'Probe-P900']

# --- SETUP: STATIC METADATA MAPPING ---

DEVICE_MODEL_MAP: Dict[str, str] = {}
for i, device_id in enumerate(MASTER_DEVICES):
    model_index = i % len(AVAILABLE_MODELS)
    DEVICE_MODEL_MAP[device_id] = AVAILABLE_MODELS[model_index]
    
DEVICE_LOCATION_MAP: Dict[str, Dict[str, Any]] = {}
for device_id in MASTER_DEVICES:
    DEVICE_LOCATION_MAP[device_id] = {
        'facility_id': random.choice(MASTER_FACILITIES),
        'aisle': random.choice(['Aisle-01', 'Aisle-05', 'Bay-10', 'Rack-4']),
        'loc_latitude': round(random.uniform(21.0, 22.0), 4),
        'loc_longitude': round(random.uniform(77.0, 78.0), 4) # Added longitude for completeness
    }

DEVICE_INSTALLATION_DATE_MAP: Dict[str, str] = {}
for device_id in MASTER_DEVICES:
    start_date = date.today() - timedelta(days=random.randint(90, 700))
    DEVICE_INSTALLATION_DATE_MAP[device_id] = start_date.isoformat()


def generate_t3_data() -> Dict[str, Any]:

    device_id = random.choice(MASTER_DEVICES)
    static_model_number = DEVICE_MODEL_MAP[device_id]
    
    static_install_date = DEVICE_INSTALLATION_DATE_MAP[device_id]
    current_loc = DEVICE_LOCATION_MAP[device_id] 

    firmware_version = random.choice(['v1.2.1', 'v1.3.0', 'v2.0.0'])
    
    if random.random() < 0.05:
        new_facility = random.choice(MASTER_FACILITIES)
        new_aisle = random.choice(['Aisle-01', 'Aisle-05', 'Bay-10', 'Rack-4'])
        
        DEVICE_LOCATION_MAP[device_id]['facility_id'] = new_facility
        DEVICE_LOCATION_MAP[device_id]['aisle'] = new_aisle
        
    return {
        'type': 'DEVICE_METADATA_UPDATE', 
        'device_id': device_id,
        'timestamp': int(time.time() * 1000),
        
        # Data for the 'info' Column Family (Hardware Details)
        'model_number': static_model_number,
        'serial_number': f"SN-{device_id}-{static_model_number[-3:]}",
        'firmware_version': firmware_version,
        'installation_date': static_install_date,
        
        'facility_id': current_loc['facility_id'], 
        'aisle': current_loc['aisle'],
        'loc_latitude': current_loc['loc_latitude'],
        'loc_longitude': current_loc['loc_longitude']
    }

def run_t3_producer():
    producer = get_producer()
    print("T3 Producer (Device Metadata) streaming...")
    
    NUM_UPDATES = 50
    
    try:
        for i in range(NUM_UPDATES):
            data = generate_t3_data()
            send_message(producer, KAFKA_TOPIC, data['device_id'], data)
            print(f"Sent T3 Update {i+1}/{NUM_UPDATES} for {data['device_id']}", end='\r')
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\nProducer Group T3 stopped.")
    except Exception as e:
        print(f"Producer Group T3 encountered an error: {e}")
    finally:
        if 'producer' in locals() and producer:
            producer.close()
        print("\nT3 Producer FINISHED and STOPPED.")
