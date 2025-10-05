
import pandas as pd
import pyodbc
from sqlalchemy.exc import SQLAlchemyError
import sys

from pipelines.db_config import (
    PYODBC_CONNECTION_STRING,
    SERVER_NAME,
    DATABASE_NAME,
    get_sqlalchemy_engine
)


def check_db_and_pandas_connection():
    print("--- Starting SQL Server / Pandas Connection Test ---")
    cnxn = None

    try:
        print(f"1. Attempting PyODBC connection to {SERVER_NAME}/{DATABASE_NAME}...")
        cnxn = pyodbc.connect(PYODBC_CONNECTION_STRING)
        cursor = cnxn.cursor()
        cursor.execute("SELECT 1 AS ConnectionTest")
        if cursor.fetchone()[0] == 1:
            print("✅ PyODBC SUCCESS: Low-level connection and test query successful.")
        else:
            raise Exception("Test query failed.")
    except pyodbc.Error as ex:
        print(f"\n❌ PyODBC FAILED: Connection error: {ex}")
        sys.exit(1)
    finally:
        if cnxn:
            cnxn.close()

    try:
        print("\n2. Attempting SQLAlchemy Engine creation...")
        engine = get_sqlalchemy_engine()
        df_test = pd.read_sql("SELECT 'Success' AS Status", engine)

        if df_test.iloc[0]['Status'] == 'Success':
            print("✅ SQLAlchemy/Pandas SUCCESS: Engine created and data read confirmed.")

    except SQLAlchemyError as e:
        print(f"\n❌ SQLAlchemy FAILED: Could not create or use engine. Details: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ UNEXPECTED ERROR: {e}")
        sys.exit(1)

    print("\n--- All Connection Checks Complete. Ready for Ingestion! ---")


if __name__ == '__main__':
    check_db_and_pandas_connection()