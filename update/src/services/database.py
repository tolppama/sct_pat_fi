import pandas as pd
import sqlalchemy as db
from datetime import datetime


class Database:
    def __init__(self, config) -> None:
        self.__engine = config.connection
        self.__schema = config.schema
        self.__table_name = config.table
        self.__output_table = config.output_table

    def get(self) -> 'pd.DataFrame':
        try:
            with self.__engine.connect() as connection:
                metadata = db.MetaData(schema=self.__schema)
                sct = db.Table(self.__table_name, metadata,
                               autoload=True, autoload_with=self.__engine)
                query = db.select([sct])
                df = pd.read_sql(query, connection)
                df['lineid'] = df['lineid'].astype(int)
                return df
        except Exception as e:
            print(e)

    def post(self, df: 'pd.DataFrame') -> None:
        with self.__engine.connect() as connection:
            try:
                df.to_sql(self.__output_table, con=connection,
                          schema=self.__schema)
            except Exception:
                date = datetime.now()
                date = date.strftime('%Y%m%d_%H%M')
                table_name = f'sct_pat_fi_kanta_{date}'
                df.to_sql(table_name, con=connection, schema=self.__schema)
