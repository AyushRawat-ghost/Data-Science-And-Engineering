import pandas as pd
from sqlalchemy.engine import Engine
from src.utils.db_connector import get_sqlalchemy_engine
TEMP_TABLE_NAME = 'T_TEMP_SILVER_FACT'


def load_temp_master_fact(df_silver_master: pd.DataFrame) -> str:
    ENGINE: Engine = get_sqlalchemy_engine()
    print("\n--- Loading Silver Master Fact to SQL Transient Storage ---")

    try:
        df_silver_master.to_sql(
            name=TEMP_TABLE_NAME,
            con=ENGINE,
            schema='dbo',
            if_exists='replace',
            index=False
        )
        print(f"✅ Transient Master Fact loaded successfully to dbo.{TEMP_TABLE_NAME}")
        return TEMP_TABLE_NAME

    except Exception as e:
        print(f"❌ FAILED to write temporary Silver Fact table. Error: {e}")
        raise