from dotenv import load_dotenv
import os
import urllib
from sqlalchemy import create_engine
import pyodbc

load_dotenv()

SERVER = os.getenv("DB_SERVER")
DATABASE = os.getenv("DB_DATABASE")
DRIVER = os.getenv("DB_DRIVER")
AUTH_METHOD = os.getenv("DB_AUTH_METHOD")


def get_pyodbc_conn_string():
    if AUTH_METHOD == "TRUSTED":
        return (
            f'DRIVER={DRIVER};'
            f'SERVER={SERVER};'
            f'DATABASE={DATABASE};'
            'Trusted_Connection=yes;'
            'Encrypt=yes;'
            'TrustServerCertificate=yes;'
        )
    else:
        raise ValueError("Unsupported DB_AUTH_METHOD. Set DB_AUTH_METHOD=TRUSTED in .env")


def get_sqlalchemy_engine():
    # 1. Get the raw connection string
    conn_str = get_pyodbc_conn_string()

    # 2. URL-encode the connection string for SQLAlchemy
    quoted_conn_string = urllib.parse.quote_plus(conn_str)

    # 3. Create the SQLAlchemy engine using the mssql+pyodbc dialect
    engine = create_engine(f'mssql+pyodbc:///?odbc_connect={quoted_conn_string}')
    return engine

