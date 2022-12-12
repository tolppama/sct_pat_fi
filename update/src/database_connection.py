from sqlalchemy import create_engine
from config import CONNECTION, SCHEMA

engine = create_engine(CONNECTION)


def get_database_connection():
    return engine

def get_database_schema():
    return SCHEMA