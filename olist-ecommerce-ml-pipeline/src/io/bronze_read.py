from src.utils.db_connector import get_pyodbc_conn_string
import pandas as pd
import pyodbc


def read_from_bronze(table_names: list) -> dict:
    print("\n--- Reading Data from Bronze Schema into Pandas Memory ---")

    # 1. Get the secure connection string
    conn_str = get_pyodbc_conn_string()

    # 2. Establish connection using pyodbc
    cnxn = pyodbc.connect(conn_str)

    dataframes = {}
    for table_name in table_names:
        print(f"Reading table: {table_name}...")
        sql_query = f"SELECT * FROM bronze.{table_name}"

        # 3. Use pandas.read_sql to execute the query and return a DataFrame
        dataframes[table_name] = pd.read_sql(sql_query, cnxn)
        print(f"Loaded {len(dataframes[table_name]):,} rows from bronze.{table_name}")

    # 4. Close the database connection
    cnxn.close()
    return dataframes
# if __name__ == "__main__":
#     print("--- Orchestrating Bronze Layer Load ---")
#     read_from_bronze(['orders_raw'])
#     print("--- ETL Module Execution Finished ---")
