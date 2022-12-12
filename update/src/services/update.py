import pandas as pd
from .database import Database


class Update:
    @staticmethod
    def get_excel(path: str):
        return pd.read_excel(path, engine="openpyxl", dtype=str)

    @staticmethod
    def get_database(table_name: str):
        return Database().get(table_name)

    @staticmethod
    def get_new_lines(table: 'pd.DataFrame'):
        return table[table['CodeID'].isnull()]

    @staticmethod
    def get_updated_lines(table: 'pd.DataFrame'):
        return table[table.status == 'edit']

    @staticmethod
    def get_inactivated_lines(table: 'pd.DataFrame'):
        return table[table.status == 'inactivate']

    @staticmethod
    def get_lang_rows(table: 'pd.DataFrame', codeid: int):
        return table[table.parentid == codeid]

    @staticmethod
    def set_new_parentid_to_lang_rows(table: 'pd.DataFrame', parentid: int):
        table['parentid'] = parentid
        return table

    @staticmethod
    def set_lineid_as_index(table: 'pd.DataFrame'):
        table['CodeID'] = table['CodeID'].astype(float).astype(int)
        table.set_index('CodeID', inplace=True)
        return table

    @staticmethod
    def drop_lineid_column(table: 'pd.DataFrame'):
        table.drop(columns='CodeID')
        return table

    @staticmethod
    def get_next_lineid(table: 'pd.DataFrame'):
        return table.index.max() + 1

    @staticmethod
    def create_new_lineids(next_lineid: int, how_many: int):
        return [i for i in range(next_lineid, next_lineid + how_many)]

    @staticmethod
    def insert_new_lineids(table: 'pd.DataFrame', new_lineids: list):
        table['CodeID'] = new_lineids
        table['status'] = 'edit'
        return table

    @staticmethod
    def concat_new_lines(table: 'pd.DataFrame', new_lines: 'pd.DataFrame'):
        return pd.concat([table, new_lines])

    @staticmethod
    def inactivate_old_line(lineid: int, table: 'pd.DataFrame', superseding_lineid=None, reason=12):
        table.loc[lineid, 'status'] = 'ei'
        table.loc[lineid, 'expiringdate'] = pd.Timestamp.now().strftime(
            "%Y-%m-%d")
        table.loc[lineid, 'supersededby'] = int(superseding_lineid)
        table.loc[lineid, 'reason_for_inactivation'] = str(reason)
        return table

    @staticmethod
    def activate_new_line(row: 'pd.DataFrame', table: 'pd.DataFrame'):
        new_lineid = Update.get_next_lineid(table)
        row = Update.drop_lineid_column(row)
        row['CodeID'] = new_lineid
        row = Update.set_lineid_as_index(row)
        table = Update.concat_new_lines(table, row)
        return table

    @staticmethod
    def check_new_table(table: 'pd.DataFrame'):
        pass

    @staticmethod
    def to_excel(table: 'pd.DataFrame', path: str):
        table.to_excel(path, index=False)
