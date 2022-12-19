import pandas as pd
from services import Component, Database
from config import Config


class Main:
    def __init__(self) -> None:
        self.__config = Config()
        self.__component = Component(self.__config)
        self.__database = Database(self.__config)

    def __get_tables(self):
        excel = self.__component.get_excel()
        database = self.__database.get()
        return excel, database

    def __get_update_types(self, excel: 'pd.DataFrame'):
        new_rows = self.__component.get_new_rows(excel)
        updated_rows = self.__component.get_edit_rows(excel)
        inactivated_rows = self.__component.get_inactivated_rows(excel)

        return new_rows, updated_rows, inactivated_rows

    def __handle_row(self, rows: 'pd.DataFrame', database: 'pd.DataFrame'):
        old_row = self.__component.get_old_row(rows)
        new_row = self.__component.get_new_row(rows)
        if new_row.empty or len(new_row) > 1:
            raise Exception('New row is empty or more than one')
        new_lineid = self.__component.get_next_codeid(database)
        table = self.__component.handle_new_row(database, new_row, new_lineid)
        return self.__component.handle_old_row(table, old_row, new_lineid)

    def __handle_bundle(self, bundle: 'pd.DataFrame', database: 'pd.DataFrame'):
        lineids = set(bundle['lineid'])
        for lineid in lineids:
            rows = bundle[bundle['lineid'] == lineid]
            database = self.__handle_row(rows, database)
        return database

    def __handle_updated_rows(self, updated_rows: 'pd.DataFrame', database: 'pd.DataFrame'):
        bundles = self.__component.create_bundles(updated_rows)
        for bundle in bundles:
            database = self.__handle_bundle(bundle, database)
            print(database[database['lineid'].isin(bundle['lineid'])])
            # database = self.__handle_new_national_id(bundle, database)
        # old_rows = self.__component.get_old_rows(database)
        # en_rows = self.__component.get_en_rows(updated_rows)

    def run(self):
        excel, database = self.__get_tables()
        new_rows, updated_rows, inactivated_rows = self.__get_update_types(
            excel)
        table = self.__handle_updated_rows(updated_rows, database)
