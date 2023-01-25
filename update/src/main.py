import pandas as pd
import numpy as np
from services import Component, Database, Verhoeff
from config import Config


class Main:
    def __init__(self) -> None:
        self.__config = Config()
        self.__component = Component(self.__config)
        self.__database = Database(self.__config)
        self.__verhoeff = Verhoeff()
        self.__empty_values = [None, np.nan, ""]

    def __get_tables(self):
        excel = self.__component.get_excel()
        database = self.__database.get()
        return excel, database

    def __get_update_types(self, excel: 'pd.DataFrame'):
        new_rows = self.__component.get_new_rows(excel)
        updated_rows = self.__component.get_edit_rows(excel)
        activated_rows = self.__component.get_activated_rows(excel)
        inactivated_rows = self.__component.get_inactivated_rows(excel)

        return new_rows, updated_rows, activated_rows, inactivated_rows

    def __check_lang_conceptid(self, bundle: 'pd.DataFrame', database: 'pd.DataFrame'):
        en_row = self.__component.get_en_row(bundle).iloc[0]
        lang_rows = self.__component.get_lang_rows(bundle)
        for index, _ in lang_rows.iterrows():
            database.at[index, "sct_conceptid"] = en_row["sct_conceptid"]
            database.at[index, "legacy_conceptid"] = en_row["legacy_conceptid"]
        return database

    def __check_lang_termid(self, bundle: 'pd.DataFrame', database: 'pd.DataFrame'):
        en_row = self.__component.get_en_row(bundle).iloc[0]
        lang_rows = self.__component.get_lang_rows(bundle)
        if en_row.empty:
            raise Exception('English row is empty')
        for index, lang_row in lang_rows.iterrows():
            if lang_row["sct_term"] == en_row["sct_term"]:
                database.at[index, "sct_termid"] = en_row["sct_termid"]
                database.at[index, "legacy_termid"] = en_row["legacy_termid"]
            database.at[index, "sct_termid_en"] = en_row["sct_termid"]
        database.at[en_row.name, "sct_termid_en"] = en_row["sct_termid"]
        return database

    def __handle_conceptid(self, table, row: 'pd.DataFrame', index: int, sn2: str, sctid: str):
        if row["sct_conceptid"] in self.__empty_values and sctid in self.__empty_values and row["status"] in ["edit", "new"]:
            next_id = self.__component.next_fin_extension_id(
                table, "sct_conceptid")
            new_conceptid = self.__verhoeff.generateVerhoeff(
                next_id, "10")
            table.at[index, "sct_conceptid"] = new_conceptid
            table.at[index, "legacy_conceptid"] = f"{sn2}-{new_conceptid}"
        return table

    def __handle_termid(self, table: 'pd.DataFrame', row: 'pd.DataFrame', index: int, sn2: str, sctid: str):
        if row["sct_termid"] in self.__empty_values and sctid in self.__empty_values and row["status"] in ["edit", "new"]:
            next_id = self.__component.next_fin_extension_id(
                table, "sct_termid")
            new_termid = self.__verhoeff.generateVerhoeff(
                next_id, "10")
            table.at[index, "sct_termid"] = new_termid
            table.at[index, "legacy_termid"] = f"{sn2}-{new_termid}"
        return table

    def __handle_national_id(self, index: int, database: 'pd.DataFrame'):
        row = self.__component.get_row_by_index(database, index)
        if self.__component.is_en_row(row):
            sn2, sctid = self.__component.get_legacyid(row, "legacy_conceptid")
            database = self.__handle_conceptid(
                database, row, index, sn2, sctid)
        sn2, sctid = self.__component.get_legacyid(row, "legacy_termid")
        database = self.__handle_termid(database, row, index, sn2, sctid)
        return database

    def __handle_edit_row(self, rows: 'pd.DataFrame', database: 'pd.DataFrame'):
        old_row = self.__component.get_old_row(rows)
        old_row_index = self.__component.get_index_by_codeid(
            database, old_row["lineid"])

        new_row = self.__component.get_new_row(rows)
        new_codeid = self.__component.get_next_codeid(database)

        database = self.__component.handle_new_row(
            database, new_row, new_codeid)
        new_row_index = self.__component.get_index_by_codeid(
            database, new_codeid)
        database = self.__handle_national_id(new_row_index, database)
        return self.__component.handle_old_row(database, old_row, old_row_index, new_codeid), new_codeid

    def __handle_new_row(self, row: 'pd.DataFrame', database: 'pd.DataFrame'):
        new_codeid = self.__component.get_next_codeid(database)
        database = self.__component.handle_new_row(database, row, new_codeid)
        new_row_index = self.__component.get_index_by_codeid(
            database, new_codeid)
        database = self.__handle_national_id(new_row_index, database)
        return database, new_codeid

    def __handle_edit_bundle(self, bundle: 'pd.DataFrame', database: 'pd.DataFrame'):
        codeids = set(bundle['lineid'])
        new_lines = []
        for codeid in codeids:
            rows = bundle[bundle['lineid'] == codeid]
            database, new_id = self.__handle_edit_row(rows, database)
            new_lines.append(new_id)
        bundle = database[database['lineid'].isin(new_lines)]
        if self.__component.bundle_has_en_row(bundle):
            database = self.__check_lang_conceptid(bundle, database)
            database = self.__check_lang_termid(bundle, database)
        else:
            raise Exception("Bundle does not have an english row")
        return database

    def __handle_new_bundle(self, bundle: 'pd.DataFrame', database: 'pd.DataFrame'):
        new_lines = []
        for _, row in bundle.iterrows():
            database, new_id = self.__handle_new_row(row, database)
            new_lines.append(new_id)
        bundle = database[database['lineid'].isin(new_lines)]
        if self.__component.bundle_has_en_row(bundle):
            database = self.__check_lang_conceptid(bundle, database)
            database = self.__check_lang_termid(bundle, database)
        else:
            raise Exception("Bundle does not have an english row")
        return database

    def __handle_updated_rows(self, updated_rows: 'pd.DataFrame', database: 'pd.DataFrame'):
        bundles = self.__component.create_bundles(updated_rows)
        for bundle in bundles:
            database = self.__handle_edit_bundle(bundle, database)
        return database

    def __handle_inactivated_rows(self, inactivated_rows: 'pd.DataFrame', database: 'pd.DataFrame'):
        for index, row in inactivated_rows.iterrows():
            index = self.__component.get_index_by_codeid(
                database, row["lineid"])
            database = self.__component.handle_inactivated_row(
                database, row, index)
        return database

    def __handle_new_rows(self, new_rows: 'pd.DataFrame', database: 'pd.DataFrame'):
        bundles = self.__component.create_bundles(new_rows)
        for bundle in bundles:
            database = self.__handle_new_bundle(
                bundle, database)
        return database

    def run(self):
        excel, database = self.__get_tables()
        new_rows, updated_rows, activated_rows, inactivated_rows = self.__get_update_types(
            excel)
        table = self.__handle_updated_rows(updated_rows, database)
        table = self.__handle_inactivated_rows(inactivated_rows, table)
        table = self.__handle_new_rows(new_rows, table)
        self.__component.to_excel(table)
