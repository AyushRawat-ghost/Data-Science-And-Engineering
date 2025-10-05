# pipelines/ingest_bronze.py

import pandas as pd
from sqlalchemy.exc import SQLAlchemyError
import os
import sys

from .db_config import get_sqlalchemy_engine

RAW_CSV_DIR = 'data/raw_csvs/'
BRONZE_TABLE_NAME = 'flights_raw'
DB_SCHEMA = 'bronze'
CHUNKSIZE = 100000
COLUMN_MAPPING = {
    'FL_DATE': 'FlightDate',
    'OP_CARRIER': 'CarrierCode',
    'ORIGIN': 'Origin',
    'DEST': 'Destination',
    'CRS_DEP_TIME': 'ScheduledDepartureTime',
    'DEP_DELAY': 'DepartureDelay',
    'ARR_DELAY': 'ArrivalDelay',
    'CANCELLED': 'CancelledFlag',
    'DISTANCE': 'Distance',
    'NAS_DELAY': 'NASDelay',
    'CARRIER_DELAY': 'CarrierDelay',
}



def ingest_data_to_bronze():
    print("\n--- Starting Bronze Layer Ingestion ---")

    # 1. Get the SQL Server Engine
    try:
        engine = get_sqlalchemy_engine()
        engine.connect()
    except SQLAlchemyError as e:
        print(f"❌ ERROR: Failed to get or connect engine: {e}")
        sys.exit(1)

    print("✅ Successfully connected to SQL Server via SQLAlchemy.")

    # 2. Iterate through all CSV files
    all_files = sorted(os.listdir(RAW_CSV_DIR))
    csv_files = [f for f in all_files if f.endswith(".csv")]

    if not csv_files:
        print(f"❌ ERROR: No CSV files found in {RAW_CSV_DIR}. Please check data path.")
        sys.exit(1)

    # 3. Process files and chunks
    total_chunks_loaded = 0

    for filename in csv_files:
        file_path = os.path.join(RAW_CSV_DIR, filename)
        source_year = filename.split('.')[0]
        print(f"\nProcessing file: {filename}")

        cols_to_read = list(COLUMN_MAPPING.keys())

        for i, chunk in enumerate(pd.read_csv(
                file_path,
                chunksize=CHUNKSIZE,
                low_memory=False,
                usecols=cols_to_read)
        ):
            try:
                chunk.rename(columns=COLUMN_MAPPING, inplace=True)
                chunk['SourceYear'] = source_year
                chunk.to_sql(
                    BRONZE_TABLE_NAME,
                    engine,
                    if_exists='append',
                    index=False,
                    schema=DB_SCHEMA
                )
                total_chunks_loaded += 1
                print(f"Loaded {total_chunks_loaded} chunks ({filename}, Chunk {i + 1})...", end='\r')

            except Exception as e:
                print(f"\n❌ FAILED to load chunk {i + 1} from {filename}. Error: {e}")
                sys.exit(1)

    print(f"\n\n✅ Bronze Layer Ingestion Complete! Total chunks loaded: {total_chunks_loaded}.")
    print(f"Data is stored in SQL Server table: {DB_SCHEMA}.{BRONZE_TABLE_NAME}")


if __name__ == '__main__':
    ingest_data_to_bronze()