import pandas as pd
import sklearn
import pyodbc
from dotenv import load_dotenv
import os
import datetime
from sqlalchemy import create_engine
import urllib

load_dotenv()
# SQL Server Details
SERVER = os.getenv("DB_SERVER")
DATABASE = os.getenv("DB_DATABASE")
DRIVER = os.getenv("DB_DRIVER")
TEST_TABLE_NAME = "dbo.test_table"

# Connection String for pyodbc
CONNECTION_STRING = (
    f'DRIVER={DRIVER};'
    f'SERVER={SERVER};'
    f'DATABASE={DATABASE};'
    'Trusted_Connection=yes;'
    'Encrypt=yes;'
    'TrustServerCertificate=yes;'
)

def run_health_check():
    """Performs tests on Python libraries and pyodbc SQL Server connectivity."""
    print("--- 🩺 Starting Pandas/SQL Server Health Check ---")

    try:
        print(f"✅ Pandas installed (Version: {pd.__version__})")
        print(f"✅ Scikit-learn installed (Version: {sklearn.__version__})")
    except Exception as e:
        print(f"❌ Python Library Check Failed: {e}")
        return

    # 2. Pyodbc SQL Server Connection Test
    cnxn = None
    try:
        print(f"\nAttempting to connect to {SERVER}/{DATABASE}...")
        cnxn = pyodbc.connect(CONNECTION_STRING)
        print("✅ Pyodbc SQL Server Connection Successful.")
    except Exception as e:
        print(
            f"❌ Pyodbc SQL Server Connection Failed. Check connection string, ODBC driver, and SQL Server status. Error: {e}")
        return

    # 3. Pandas Read/Write Test (Crucial for ETL logic)
    try:
        test_data = {
            'ID': [1],
            'TestStatus': ["PANDAS_OK"],
            'CheckTime': [datetime.datetime.now()]
        }
        df_test_write = pd.DataFrame(test_data)
        quoted_conn_string = urllib.parse.quote_plus(CONNECTION_STRING)
        engine = create_engine(f'mssql+pyodbc:///?odbc_connect={quoted_conn_string}')
        df_test_write.to_sql(
            name=TEST_TABLE_NAME.split('.')[-1],
            con=engine,
            schema=TEST_TABLE_NAME.split('.')[0],
            if_exists='replace',
            index=False
        )
        print(f"✅ Pandas to_sql (Write Test) Successful to {TEST_TABLE_NAME}.")

        # TEST READ
        df_test_read = pd.read_sql(f"SELECT * FROM {TEST_TABLE_NAME}", cnxn)
        print("✅ Pandas read_sql (Read Test) Successful. Data sample:")
        print(df_test_read)

    except Exception as e:
        print(f"❌ Pandas SQL I/O Test Failed. Check SQLAlchemy setup or permissions. Error: {e}")

    finally:
        if cnxn:
            cnxn.close()
            print("\n--- SQL Connection Closed ---")


if __name__ == "__main__":
    run_health_check()