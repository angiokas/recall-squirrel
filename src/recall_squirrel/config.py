from platformdirs import user_data_path
import os

APP_NAME = "recall-squirrel"
DATABASE_NAME = "recall_squirrel.db"
DATA_PATH = user_data_path(appname=APP_NAME)
DATABASE_PATH = DATA_PATH / DATABASE_NAME
DATABASE_URL = f"sqlite:///{DATABASE_PATH}"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEST_BASE_DIR = os.path.abspath(os.path.join(BASE_DIR, "..", "tests"))
TEST_DATABASE_PATH = os.path.join(TEST_BASE_DIR, "test_data")
TEST_DATABASE_URL = f"sqlite:///{os.path.join(TEST_DATABASE_PATH, 'test_flashcards.db')}"


