import pandas as pd
from services import update


def get_tables():
    excel = update.get_excel('<excel_file_path>')
    database = update.get_database('<table_name>')

    return excel, database


def get_update_types(excel: 'pd.DataFrame'):
    new_lines = update.get_new_lines(excel)
    updated_lines = update.get_updated_lines(excel)
    inactivated_lines = update.get_inactivated_lines(excel)

    return new_lines, updated_lines, inactivated_lines


def main():
    excel, database = get_tables()
    new_lines, updated_lines, inactivated_lines = get_update_types(excel)
