import pandas as pd
import sqlalchemy as db


class Database:
    def __init__(self) -> None:
        self.__engine = db.create_engine("postgresql://${USERNAME}:${PASSWORD}@${CONNECTION_ADDRESS}:${PORT}/${DATABASE}")
        self.__schema = "snomedct"
        self.__table_name = "sct_pat_fi_kanta_20221101"
        self.__output_table = "test_table"

    def get(self) -> 'pd.DataFrame':
        try:
            with self.__engine.connect() as connection:
                metadata = db.MetaData(schema=self.__schema)
                sct = db.Table(self.__table_name, metadata,
                               autoload=True, autoload_with=self.__engine)
                query = db.select([sct])
                df = pd.read_sql(query, connection)
                # df['lineid'] = df['lineid'].astype(int)
                return df
        except Exception as e:
            print(e)

    def post(self, df: 'pd.DataFrame') -> None:
        with self.__engine.connect() as connection:
            try:
                df.to_sql(self.__output_table, con=connection,
                          schema=self.__schema)
            except Exception as e:
                print(e)
