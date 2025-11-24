from airflow.models.dag import DAG
from airflow.operators.bash import BashOperator
from airflow.utils.dates import days_ago
from datetime import timedelta

FINITE_SETUP_SCRIPTS = [
    'device.py', 
    'facility.py',
]
INFINITE_PRODUCER_SCRIPT = 'sensor_readings.py' 

with DAG(
    dag_id='iot_automated_stream_pipeline',
    start_date=days_ago(1),
    schedule_interval=None, # Run manually once for setup
    catchup=False,
    tags=['iot', 'stream', 'hbase', 'rag'],
    default_args={
        'owner': 'airflow',
        'retries': 0, 
    }
) as dag:
    
    # 1. Setup Task: Create all HBase tables
    create_hbase_schema = BashOperator(
        task_id='create_hbase_schema',
        bash_command='Get-Content -Raw ./codex/ddl.hbase | docker exec -i hbase-master hbase shell',
    )
    populate_metadata = BashOperator(
        task_id='populate_initial_metadata',
        bash_command='python3 /opt/airflow/scripts/hbase/metadata_setup.py',
    )
    
    finite_producer_tasks = []
    for script_name in FINITE_SETUP_SCRIPTS:
        task = BashOperator(
            task_id=f'produce_finite_{script_name[:-3]}', 
            bash_command=f'python3 ./codex/producer/{script_name}',
            execution_timeout=timedelta(minutes=2) 
        )
        finite_producer_tasks.append(task)

    start_continuous_producer = BashOperator(
        task_id='start_t1_sensor_stream',
        bash_command=f'python3 ./codex/producer/{INFINITE_PRODUCER_SCRIPT} &',
        execution_timeout=timedelta(hours=24),
    )

    # start_hbase_ingestion_consumer = BashOperator(
    #     task_id='start_hbase_ingestion_consumer',
    #     bash_command='python3 ./consumer/consumer_ingestion.py &',
    #     execution_timeout=timedelta(hours=24), # Expects to run indefinitely
    # )

    # run_pyspark_etl = BashOperator(
    #     task_id='run_pyspark_etl_transform',
    #     bash_command='echo "PySpark ETL Job triggered..."', # Placeholder for spark-submit
    # )

    create_hbase_schema >> populate_metadata
    
    populate_metadata >> finite_producer_tasks
    
    # finite_producer_tasks >> [start_continuous_producer, start_hbase_ingestion_consumer]
    
    # start_continuous_producer >> run_pyspark_etl
    # start_hbase_ingestion_consumer >> run_pyspark_etl