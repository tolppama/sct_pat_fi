import re
import pandas as pd


class Component:
    def __init__(self, config) -> None:
        self.__config = config

    def get_excel(self):
        return pd.read_excel(self.__config.excel_path, engine="openpyxl", dtype=str, sheet_name=self.__config.excel_sheet)

    def to_excel(self, table: 'pd.DataFrame'):
        table[["lineid", "sct_conceptid", "sct_termid", "sct_termid_en"]] = table[[
            "lineid", "sct_conceptid", "sct_termid", "sct_termid_en"]].astype(str)
        table = table.sort_values(
            by=["legacy_conceptid", "sct_termid_en", "lang"])
        table.to_excel(self.__config.output_file, index=False)

    def get_edit_rows(self, table: 'pd.DataFrame'):
        table = table[table['status'] != 'new']
        return table[(table['lineid'].duplicated(keep=False))].copy()

    def get_new_rows(self, table: 'pd.DataFrame'):
        return table[table['status'] == 'new'].copy()

    def get_activated_rows(self, table: 'pd.DataFrame'):
        return table[table['status'] == 'activated'].copy()

    def get_inactivated_rows(self, table: 'pd.DataFrame'):
        return table[table['status'] == 'inactivated'].copy()

    def get_en_row(self, table: 'pd.DataFrame'):
        return table[table['lang'] == 'en'].copy()

    def get_lang_rows(self, table: 'pd.DataFrame'):
        return table[table['lang'] != 'en'].copy()

    def get_lang_rows_by_en(self, table: 'pd.DataFrame', en_row: 'pd.DataFrame'):
        return table[table['sct_termid_en'] == en_row['sct_termid_en']].copy()

    def get_old_row(self, table: 'pd.DataFrame'):
        return table[table['status'] != 'edit'].iloc[0]

    def get_table_index(self, table: 'pd.DataFrame', row: 'pd.DataFrame'):
        return table.loc[table['lineid'] ==
                         row['lineid']].index[0]

    def get_new_row(self, table: 'pd.DataFrame'):
        return table[table['status'] == 'edit'].iloc[0]

    def is_en_row(self, row: 'pd.Series'):
        return row["lang"] == 'en'

    def bundle_has_en_row(self, bundle: 'pd.DataFrame'):
        return not bundle[bundle["lang"] == 'en'].empty

    def get_index_by_codeid(self, table: 'pd.DataFrame', lineid: int):
        return table.loc[table['lineid'] == int(lineid)].index.values[0]

    def get_row_by_codeid(self, table: 'pd.DataFrame', lineid: int):
        return table[table['lineid'] == lineid].copy()

    def get_row_by_index(self, table: 'pd.DataFrame', index: int):
        return table.iloc[index].copy()

    def create_bundles(self, rows: 'pd.DataFrame'):
        bundles = []
        for i in set(rows['sct_termid_en']):
            bundles.append(rows[rows['sct_termid_en'] == i])
        return bundles

    def get_next_codeid(self, table: 'pd.DataFrame'):
        return int(table['lineid'].astype(int).max() + 1)

    def create_new_codeids(self, next_lineid: int, how_many: int):
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

    def get_legacyid(self, row: 'pd.DataFrame', column: str):
        legacyid = row[column]
        if not re.fullmatch(r".+-\d*", legacyid):
            return None
        sn2, sct_id = legacyid.split('-')
        return sn2 or None, sct_id or None

    def check_component_parentid(self, en_row: 'pd.Series', lang_rows: 'pd.DataFrame', table: 'pd.DataFrame'):
        parentid = en_row['lineid']
        table.at[en_row.index, 'sct_termid_en'] = parentid
        for lang_row in lang_rows.itertuples():
            table.at[lang_row.Index, 'sct_termid_en'] = parentid
        return table

    def handle_old_row(self, table: 'pd.DataFrame', old_row: 'pd.Series', index: int, new_lineid: int):
        table.loc[index, :] = old_row[:]
        table.loc[index, 'in_use'] = 'N'
        table.loc[index, 'superseded_by'] = new_lineid
        return table

    def handle_new_row(self, table: 'pd.DataFrame', new_row: int, new_lineid: int):
        new_row['lineid'] = new_lineid
        new_row['in_use'] = 'Y'
        new_row = new_row.to_frame().T
        return pd.concat([table, new_row], ignore_index=True)

    def handle_inactivated_row(self, table: 'pd.DataFrame', inactivated_row: 'pd.Series', index: int):
        table.loc[index, :] = inactivated_row[:]
        table.loc[index, 'in_use'] = 'N'
        return table
