from recall_squirrel.config import DATABASE_URL, DATABASE_PATH
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
from recall_squirrel.db.models import *

def setup_database():
    """Initializes the database, creating tables if they don't exist."""
    engine = create_engine(DATABASE_URL, echo=True)
    if not database_exists(engine.url):
        print("Database does not exist, creating it now...")
        create_database(engine.url)
        print("Database successfully created at ", DATABASE_PATH )

        print("Creating tables...")
        Base.metadata.create_all(engine)
        print("Setup complete!")
    
if __name__ == "__main__":
    setup_database()