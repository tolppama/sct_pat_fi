import os
from dotenv import load_dotenv

dirname = os.path.dirname(__file__)

try:
    load_dotenv(dotenv_path=os.path.join(dirname, "..", ".env"))
except FileNotFoundError:
    print("No .env file found\nWrite .env file with the following variables:\n")
    print(r"\nCONNECTION = <username;password@connection_address/database>\n")
    print(r"SCHEMA = <schema_name>\n")

CONNECTION = os.getenv("CONNECTION")
SCHEMA = os.getenv("SCHEMA")