import re
import pandas as pd


class Component:
    def __init__(self, config) -> None:
        self.__config = config

    def get_excel(self):
        return pd.read_excel(self.__config.excel_path, engine="openpyxl", dtype=str, sheet_name=self.__config.excel_sheet)

    def to_excel(self, table: 'pd.DataFrame'):
        table.to_excel(self.__config.excel_path, index=False)

    def get_edit_rows(self, table: 'pd.DataFrame'):
        return table[(table['lineid'].duplicated(keep=False))]

    def get_new_rows(self, table: 'pd.DataFrame'):
        return table[table['status'] == 'new']

    def get_inactivated_rows(self, table: 'pd.DataFrame'):
        return table[table['status'] == 'inactivated']

    def get_en_rows(self, table: 'pd.DataFrame'):
        return table[table['lang'] == 'en']

    def get_lang_rows(self, table: 'pd.DataFrame'):
        return table[table['lang'] != 'en']

    def get_old_row(self, table: 'pd.DataFrame'):
        return table[table['status'] != 'edit']

    def get_new_row(self, table: 'pd.DataFrame'):
        return table[table['status'] == 'edit']

    def create_bundles(self, rows: 'pd.DataFrame'):
        bundles = []
        for i in set(rows['sct_termid_en']):
            bundles.append(rows[rows['sct_termid_en'] == i])
        return bundles

    def get_next_codeid(self, table: 'pd.DataFrame'):
        return int(table['lineid'].astype(int).max() + 1)

    def create_new_lineids(self, next_lineid: int, how_many: int):
        return [i for i in range(next_lineid, next_lineid + how_many)]

    def next_fin_extension_id(self, table: 'pd.DataFrame', column: str) -> int:
        fin_id_series = table[column][table[column].str.fullmatch(
            r"^\d+1000288(10|11)\d$") == True]
        fin_id_max = 0

        if not fin_id_series.empty:
            fin_id_series = fin_id_series.apply(lambda x: x[:len(x)-10])
            fin_id_series = fin_id_series.astype(int)
            fin_id_max = fin_id_series.max()
        fin_id_max += 1
        return fin_id_max

    def check_legacyid(self, row: 'pd.Series', column: str, sn2: bool = False):
        legacyid = row[column]
        if not re.fullmatch(r".+-\d+", legacyid):
            return None
        if sn2:
            return legacyid.split('-')[0]
        return legacyid.split('-')[1]

    def check_component_parentid(self, en_row: 'pd.Series', lang_rows: 'pd.DataFrame', table: 'pd.DataFrame'):
        parentid = en_row['lineid']
        table.at[en_row.index, 'sct_termid_en'] = parentid
        for lang_row in lang_rows.itertuples():
            table.at[lang_row.Index, 'sct_termid_en'] = parentid
        return table

    def handle_new_line(self, table: 'pd.DataFrame', old_row: 'pd.Series', new_row: 'pd.Series', new_lineid: int):
        table.at[new_row.index.values[0], 'lineid'] = new_lineid
        table.at[old_row.index.values[0], 'superseded_by'] = new_lineid
        table.at[old_row.index.values[0], 'in_use'] = 'N'
        table.at[new_row.index.values[0], 'in_use'] = 'Y'
        return table
