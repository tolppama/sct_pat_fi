import pandas as pd
import sqlalchemy as db
from datetime import datetime
from database_connection import get_database_connection, get_database_schema


class Database:
    def __init__(self) -> None:
        self.__engine = get_database_connection()
        self.__schema = get_database_schema()

    def get(self, table_name: str) -> 'pd.DataFrame':
        try:
            with self.__engine.connect() as connection:
                metadata = db.MetaData(schema=self.__schema)
                sct = db.Table(table_name, metadata,
                               autoload=True, autoload_with=self.__engine)
                query = db.select([sct])
                df = pd.read_sql(query, connection, index_col='lineid')
                df.index = df.index.map(int)
                return df
        except Exception as e:
            print(e)

    def post(self, df: 'pd.DataFrame', table_name: str) -> None:
        eng = self.engine
        with eng.connect() as connection:
            try:
                df.to_sql(table_name, con=connection, schema=self.__schema)
            except Exception:
                date = datetime.now()
                date = date.strftime('%Y%m%d_%H%M')
                table_name = f'sct_pat_fi_kanta_{date}'
                df.to_sql(table_name, con=connection, schema=self.__schema)
