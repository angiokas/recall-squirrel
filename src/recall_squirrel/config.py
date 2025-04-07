from platformdirs import user_data_path
import os

APP_NAME = "recall-squirrel"
DB_NAME = "recall_squirrel.db"
DATA_PATH = user_data_path(appname=APP_NAME)
DB_PATH = os.environ.get("DB_PATH", DATA_PATH / DB_NAME)
