from sqlalchemy import create_engine, inspect
from recall_squirrel.models import (
    Base,
    Flashcard,
    Studyset,
    FlashcardStudyset,
    Difficulty,
)
from sqlalchemy.orm import sessionmaker
from recall_squirrel.config import DB_PATH
import os


def initialize_engine(DB_PATH):
    DB_URL = f"sqlite:///{DB_PATH}"

    if not os.path.exists(DB_PATH):
        if not (os.path.isfile(DB_PATH)):
            raise Exception(f"{DB_PATH} is not a valid path.")

        print(f"{DB_PATH} does not exist. Creating DB now...")

        DB_DIR = os.path.dirname(DB_PATH)

        if not os.path.exists(DB_DIR):
            os.makedirs(DB_DIR)
            print(f"Successfully created directory {DB_DIR}")
    try:
        engine = create_engine(DB_URL, echo=True)
        Base.metadata.create_all(engine)
        print(f"Successfully created database and tables: {DB_URL}")
        return engine

    except Exception as e:
        print(f"Error while creating engine: {e}")
        raise


def check_missing_tables(engine):
    inspector = inspect(engine)
    existing_tables = inspector.get_table_names()
    model_tables = Base.metadata.tables.keys()
    missing_tables = [table for table in model_tables if table not in existing_tables]
    if missing_tables:
        print("Missing tables:", missing_tables)
        print("Creating tables now...")
        try:
            Base.metadata.create_all(engine)
            print("Successfully created tables!")
        except Exception as e:
            print(f"Error while creating tables: {e}")


def print_db_info(engine):
    inspector = inspect(engine)

    tables = inspector.get_table_names()
    print(f"Tables in the database: {tables}")

    for table_name in tables:
        print(f"\nTable: {table_name}")

        columns = inspector.get_columns(table_name)
        for column in columns:
            print(f"  Column: {column['name']} - Type: {column['type']}")

        indexes = inspector.get_indexes(table_name)
        print(f"  Indexes: {indexes}")

        foreign_keys = inspector.get_foreign_keys(table_name)
        print(f"  Foreign Keys: {foreign_keys}")

        primary_key = inspector.get_pk_constraint(table_name)
        print(f"  Primary Key: {primary_key}")


def start_engine(DB_PATH):
    engine = initialize_engine(DB_PATH)
    check_missing_tables(engine)
    print_db_info(engine)

    return engine


engine = start_engine(DB_PATH)
Session = sessionmaker(bind=engine)
