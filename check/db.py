import pandas as pd
import sqlalchemy as db


class Database:

    def __init__(self):
        eng = self.__engine_init()
        self.engine = eng
        # Here you can alter the target schema
        self.schema = 'sct_pat_fi_pub'

    def __engine_init(self):
        try:
            # Here you can alter the connection string
            engine = db.create_engine(
                'postgresql://<username;password@connection_address/database>')
            return engine
        except Exception as e:
            print(e)

    # Retrieves SQL table and returns dataframe, sets lineid to index.
    def table_to_df(self, table_name) -> 'pd.DataFrame':
        eng = self.engine
        try:
            with eng.connect() as connection:
                metadata = db.MetaData(schema=self.schema)
                sct = db.Table(table_name, metadata,
                               autoload=True, autoload_with=eng)
                query = db.select([sct])
                df = pd.read_sql(query, connection)
                df.index = df.index.map(int)
                return df

        except Exception as e:
            print(e)
