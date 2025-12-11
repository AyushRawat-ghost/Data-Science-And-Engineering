import time
import random
from scripts.utils.producer_base import get_producer, send_message
from itertools import cycle

KAFKA_TOPIC = 'iot_readings'
MASTER_FACILITIES = ['Minerva', 'Aether', 'Poseidon', 'Demeter', 'Apollo', 'Hades', 'Eleuthia', 'Artemis', 'Hephaestus']
ALPHAS = ['Ayush', 'Sanskruti', 'Namisha']

FACILITY_ITERATOR = cycle(MASTER_FACILITIES)
ALPHAS_ITERATOR = cycle(ALPHAS)
def generate_t4_data():
    facility = next(FACILITY_ITERATOR)
    
    temp_max_c = round(random.uniform(38.0, 42.0), 1) 
    manager_alpha = next(ALPHAS_ITERATOR)
    
    return {
        'type': 'FACILITY_CONFIG_UPDATE', 
        'facility_id': facility,
        'timestamp': int(time.time() * 1000),
        
        # Rules column Family
        'temp_max_c': temp_max_c,
        'pressure_min_hpa': round(random.uniform(975.0, 990.0), 1),
        'alert_recipient': f"alerts_{facility.lower()}@domain.com",
        
        # Meta column Family 
        'manager_name': manager_alpha,
        'city': random.choice(['Berlin', 'Mumbai', 'LA','Moscow'])
    }

def run_t4_producer():
    producer = get_producer()
    print("T4 Producer (Facility Config) streaming - CYCLIC MODE...")
    for i in range(1,10):
        data = generate_t4_data()
        send_message(producer, KAFKA_TOPIC, data['facility_id'], data)
        print(f"Sent config update for: {data['facility_id']}", end='\r')
        time.sleep(5)
        