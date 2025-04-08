from sqlalchemy.orm import sessionmaker
from recall_squirrel.configs import DatabaseEngineFactory

_engine = None
_Session = None


def get_engine():
    global _engine

    if _engine is None:
        factory = DatabaseEngineFactory()
        _engine = factory.create_engine()
    return _engine


def get_session():
    global _Session
    if _Session is None:
        _Session = sessionmaker(bind=get_engine(), expire_on_commit=False)
    return _Session()


