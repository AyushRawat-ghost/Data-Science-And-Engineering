from sqlalchemy import create_engine
from urllib.parse import quote_plus

# --- SQL Server Connection Configuration ---
SERVER_NAME = 'LAPTOP-LFBT0G3K'
DATABASE_NAME = 'FlightDelayDB'
ODBC_DRIVER = '{ODBC Driver 17 for SQL Server}'

PYODBC_CONNECTION_STRING = (
    f'DRIVER={ODBC_DRIVER};'
    f'SERVER={SERVER_NAME};'
    f'DATABASE={DATABASE_NAME};'
    'Trusted_Connection=yes;'
    'Encrypt=yes;'
    'TrustServerCertificate=yes'
)


# SQLAlchemy Engine Creator
def get_sqlalchemy_engine():
    quoted_conn_str = quote_plus(PYODBC_CONNECTION_STRING)

    # Use the mssql+pyodbc dialect
    engine = create_engine(
        f"mssql+pyodbc:///?odbc_connect={quoted_conn_str}",
        fast_executemany=True
    )
    return engine