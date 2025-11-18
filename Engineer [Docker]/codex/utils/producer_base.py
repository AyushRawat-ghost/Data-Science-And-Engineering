import time
import json
import os
from kafka import KafkaProducer
from typing import Dict,Any

KAFKA_Broker=os.environ.get('KAFKA_Broker','kafka:9092')
def get_producer():
    return KafkaProducer(
        bootstrap_servers=KAFKA_Broker.split(','),
        value_serializer=lambda v:json.dumps(v).encode('utf-8'),
        key_serializer=lambda k:str(k).encode('utf-8')
    )

def send_message(producer:KafkaProducer,topic:str,key:str,data:Dict[str,Any]):
    producer.send(topic,key=key,value=data)
    time.sleep(0.01)
    
