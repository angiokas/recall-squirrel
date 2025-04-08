from sqlalchemy import create_engine, inspect

from .models import Base

from platformdirs import user_data_path
from pathvalidate import ValidationError, validate_filepath
import weakref
import pprint
import os


APP_NAME = "recall-squirrel"
DB_NAME = "recall_squirrel.db"
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))

DEV_DB_PATH = os.path.join(BASE_DIR, "data", DB_NAME)

PROD_DATA_PATH = user_data_path(appname=APP_NAME)
PROD_DB_PATH = os.path.join(PROD_DATA_PATH, DB_NAME)

DEFAULT_DB_PATH = DEV_DB_PATH

sqlite_configs = {
    "default": {
        "drivername": "sqlite",
        "database": os.environ.get("DB_PATH", DB_NAME),
        "DB_PATH": os.environ.get("DB_PATH", DEFAULT_DB_PATH),
    },
    "dev": {
        "drivername": "sqlite",
        "database": os.environ.get("DB_PATH", DB_NAME),
        "DB_PATH": os.environ.get("DB_PATH", DEV_DB_PATH),
    },
}

database_configs = {
    "postgresql": {
        "drivername": "postgresql+psycopg2",
        "username": os.environ.get("DB_USER", "prod_user"),
        "password": os.environ.get("DB_PASSWORD", "prod_password"),
        "host": os.environ.get("DB_HOST", "prod_host"),
        "port": os.environ.get("DB_PORT", "5432"),
        "database": os.environ.get("DB_NAME", "prod_db"),
        "query": {
            "sslmode": "require",
        },
    },
    "mysql": {
        "drivername": "mysql+pymysql",
        "username": os.environ.get("DB_USER", "mysql_user"),
        "password": os.environ.get("DB_PASSWORD", "mysql_password"),
        "host": os.environ.get("DB_HOST", "localhost"),
        "port": os.environ.get("DB_PORT", "3306"),
        "database": os.environ.get("DB_NAME", "mysql_db"),
        "query": {
            "charset": "utf8mb4",
        },
    },
    "mongodb": {
        "drivername": "mongodb",
        "username": os.environ.get("DB_USER", "mongo_user"),
        "password": os.environ.get("DB_PASSWORD", "mongo_password"),
        "host": os.environ.get("DB_HOST", "localhost"),
        "port": os.environ.get("DB_PORT", "27017"),
        "database": os.environ.get("DB_NAME", "mongodb_db"),
        "query": {
            "authSource": "admin",
            "replicaSet": "rs0",
        },
    },
}


class DatabaseEngineFactory:
    _instances = weakref.WeakValueDictionary()

    def __init__(self, environment="dev", configs=sqlite_configs, base=Base):
        self.db_environment = environment
        self.db_configs = configs[self.db_environment]
        self.base = base
        self.engine = None
        self.name = environment + self.db_configs["drivername"]
        DatabaseEngineFactory._instances[self.name] = self

    @staticmethod
    def get_instance(name):
        return DatabaseEngineFactory._instances.get(name, None)

    @staticmethod
    def get_instances():
        for instance in DatabaseEngineFactory._instances.values():
            print(f"Instance: {instance}")

    def create_engine(self):
        if not self.engine:
            try:
                db_url = self.generate_url()
                self.engine = create_engine(db_url)
                self.ensure_tables()
            except Exception as e:
                print(f"Error creating engine: {e}")
                raise
        return self.engine

    def get_environment(self):
        return self.db_environment

    def get_db_configs(self):
        return self.db_configs

    def get_db_path(self):
        db_path = self.db_configs["DB_PATH"]
        if not os.path.exists(db_path):
            try:
                validate_filepath(db_path, platform="auto")
            except ValidationError as e:
                raise e

            db_dir = os.path.dirname(db_path)

            if not os.path.exists(db_dir):
                try:
                    os.makedirs(db_dir)
                    print(f"Successfully created directory {db_dir}")
                except Exception as e:
                    print(f"Error while creating directories: {e}")

        return db_path

    def generate_url(self):
        return f"sqlite:///{self.get_db_path()}"

    def ensure_tables(self):
        print("Ensuring tables")
        if self.engine is None:
            raise ValueError("Engine has not been created yet!")

        engine = self.engine
        base = self.base

        inspector = inspect(engine)
        existing_tables = inspector.get_table_names()
        model_tables = base.metadata.tables.keys()
        missing_tables = [
            table for table in model_tables if table not in existing_tables
        ]

        if missing_tables:
            print("Missing tables:", missing_tables)
            print("Creating tables now...")
            try:
                base.metadata.create_all(engine)
                print("Successfully created tables!")
            except Exception as e:
                print(f"Error while creating tables: {e}")

    def __repr__(self):
        if self.engine is None:
            raise ValueError("Engine has not been created yet!")

        instance_info = {
            "Instance Name": self.name,
            "Environment": self._db_environment,
            "Driver name": self.db_configs.get("drivername"),
            "Database Path": self.db_configs.get("DB_PATH"),
        }

        inspector = inspect(self.engine)
        tables = inspector.get_table_names()

        db_info = {}
        db_info["Tables in the database"] = tables

        for table_name in tables:
            table_info = {}
            columns = inspector.get_columns(table_name)
            table_info["Columns"] = [
                {"name": col["name"], "type": str(col["type"])} for col in columns
            ]
            indexes = inspector.get_indexes(table_name)
            table_info["Indexes"] = indexes

            foreign_keys = inspector.get_foreign_keys(table_name)
            table_info["Foreign Keys"] = foreign_keys

            primary_key = inspector.get_pk_constraint(table_name)
            table_info["Primary Key"] = primary_key

            db_info[table_name] = table_info

        full_info = {
            "Engine Instance Info": instance_info,
            "Database Info": db_info,
        }

        return pprint.pformat(full_info, indent=4)