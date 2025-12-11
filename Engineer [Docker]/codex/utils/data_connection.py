import happybase
import time
import os
import socket
from typing import Dict, Any, List, Tuple

# --- Configuration Constants  ---
HBASE_HOST = os.environ.get('HBASE_HOST', 'hbase-master')
HBASE_PORT = int(os.environ.get('HBASE_PORT', 9090)) # HBase Thrift Server
KAFKA_BROKER = os.environ.get('KAFKA_BROKER', 'kafka:29092')
WEAVIATE_URL = os.environ.get('WEAVIATE_HOST', 'http://weaviate:8080')

def connect_to_hbase(table_names: List[str]) -> Tuple[Any, Dict[str, Any]]:
    print(f"Attempting to connect to HBase at {HBASE_HOST}:{HBASE_PORT}...")
    
    max_retries = 10
    for attempt in range(max_retries):
        try:
            connection = happybase.Connection(HBASE_HOST, HBASE_PORT, timeout=60000)
            connection.open()
            
            table_objects = {}
            for name in table_names:
                table_objects[name] = connection.table(name)
            
            print(f"✅ HBase connection successful. Tables linked: {', '.join(table_names)}")
            return connection, table_objects

        except (socket.error, Exception) as e:
            print(f"Connection failed (Attempt {attempt + 1}/{max_retries}). Retrying in 5 seconds...")
            if "has no attribute 'hbase'" in str(e):
                 print("FATAL DEPENDENCY ERROR: HappyBase internal structure is broken. Please check Python/Thrift versions.")
                 return None, {}
            time.sleep(5)

    print("🔴 Failed to connect to HBase after multiple retries. Check hbase-master service.")
    return None, {}