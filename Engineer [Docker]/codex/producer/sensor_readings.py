import time
import random
from utils.producer_base import get_producer, send_message
from itertools import cycle
from typing import Dict, Any, List, Tuple

KAFKA_TOPIC = 'iot_readings'

MASTER_DEVICES: List[str] = [f'DEV_{i:04}' for i in range(1, 21)]
SENSOR_PROFILES: List[Dict[str, Any]] = [
    {
        'name': 'temperature', 
        'unit': 'C', 
        'baseline': 35.0, 
        'stddev': 0.8, 
        'alert_threshold': 40.0,
        'alert_max': 45.0
    },
    {
        'name': 'vibration_hz', 
        'unit': 'Hz', 
        'baseline': 50.0, 
        'stddev': 1.5, 
        'alert_threshold': 60.0,
        'alert_max': 70.0
    },
    {
        'name': 'pressure', 
        'unit': 'hPa', 
        'baseline': 995.0, 
        'stddev': 2.0, 
        'alert_threshold': 975.0,
        'alert_max': 960.0
    },
    {
        'name': 'humidity', 
        'unit': '%', 
        'baseline': 55.0, 
        'stddev': 3.0, 
        'alert_threshold': 75.0,
        'alert_max': 90.0
    }
]

SENSOR_ITERATOR = cycle(SENSOR_PROFILES)

def generate_t1_data() -> Dict[str, Any]:
    device_id = random.choice(MASTER_DEVICES)
    sensor_profile = next(SENSOR_ITERATOR)
    
    name = sensor_profile['name']
    unit = sensor_profile['unit']
    baseline = sensor_profile['baseline']
    stddev = sensor_profile['stddev']
    threshold = sensor_profile['alert_threshold']
    alert_max = sensor_profile['alert_max']
    
    reading_value: float = 0.0
    
    # 98% of the time, generate a normal reading 
    if random.random() > 0.02: 
        reading_value = random.gauss(baseline, stddev)
    else:
        if threshold > baseline: # High value alert
            reading_value = random.uniform(threshold, alert_max)
        else:
            reading_value = random.uniform(alert_max, threshold)

    reading_value = round(reading_value, 2)

    return {
        'type': 'DEVICE_READING', 
        'device_id': device_id,
        'timestamp': int(time.time() * 1000),
    
        'reading_name': name,
        'value': reading_value,
        'unit': unit,
    }

def run_t1_producer():
    producer = get_producer()
    print("T1 Producer (Core Telemetry) streaming - HIGH VOLUME...")
    
    try:
        while True:
            data = generate_t1_data()
            send_message(producer, KAFKA_TOPIC, data['device_id'], data)
            
            print(f"Sent Reading: {data['device_id']} - {data['reading_name']}: {data['value']} {data['unit']}", end='\r')
            
            time.sleep(0.2) 
            
    except KeyboardInterrupt:
        print("\nProducer Group T1 stopped.")
    except Exception as e:
        print(f"Producer Group T1 encountered an error: {e}")
    finally:
        producer.close()
        print("\nT1 Producer FINISHED and STOPPED.")
