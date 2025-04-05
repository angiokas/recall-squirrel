from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from recall_squirrel.config import DATABASE_URL

engine = create_engine(DATABASE_URL, echo=True)
Session = sessionmaker(bind=engine)
def new_session():
    return Session()