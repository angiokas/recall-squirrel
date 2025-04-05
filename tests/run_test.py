import os
from recall_squirrel.config import TEST_DATABASE_PATH, TEST_DATABASE_URL
from recall_squirrel.db.db_operations import *
# Override environment variables to use the test database
os.environ["DATABASE_PATH"] = TEST_DATABASE_PATH
os.environ["DATABASE_URL"] = TEST_DATABASE_URL
