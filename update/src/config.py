import os
from dotenv import load_dotenv
from sqlalchemy import create_engine


class Config:
    def __init__(self):
        self.__database_connection = None
        self.__database_schema = None
        self.__table_name = None
        self.__excel_path = None
        self.__excel_sheet = None
        self.__output_file = None
        self.__output_table = None
        self.__initialize()

    @property
    def connection(self):
        return self.__database_connection

    @property
    def schema(self):
        return self.__database_schema

    @property
    def table(self):
        return self.__table_name

    @property
    def excel_path(self):
        return self.__excel_path

    @property
    def excel_sheet(self):
        return self.__excel_sheet

    @property
    def output_file(self):
        return self.__output_file

    @property
    def output_table(self):
        return self.__output_table

    def __initialize(self):
        dirname = os.path.dirname(__file__)
        try:
            load_dotenv(dotenv_path=os.path.join(dirname, "..", ".env"))
        except FileNotFoundError:
            print("No .env file found\nWrite .env file with the following variables:\n")
            print(r"\nCONNECTION = <username;password@connection_address/database>\n")
            print(r"SCHEMA = <schema_name>\n")

        self.__database_connection = create_engine(os.getenv("CONNECTION"))
        self.__database_schema = os.getenv("SCHEMA")
        self.__table_name = os.getenv("TABLE")
        file_name = os.getenv("EXCEL_FILE")
        self.__excel_path = os.path.join(dirname, "..", file_name)
        self.__excel_sheet = os.getenv("EXCEL_SHEET")
        output_file_name = os.getenv("OUTPUT_FILE")
        self.__output_file = os.path.join(dirname, "..", output_file_name)
        self.__output_table = os.getenv("OUTPUT_TABLE")
