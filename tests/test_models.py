from recall_squirrel.session_management import start_engine
from recall_squirrel.models import (
    Base,
    Flashcard,
    Studyset,
    FlashcardStudyset,
    Difficulty,
)
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEST_BASE_DIR = os.path.abspath(os.path.join(BASE_DIR, "..", "tests"))
TEST_DB_PATH = os.path.join(TEST_BASE_DIR, "test_data.db")

engine = start_engine(TEST_DB_PATH)
Session = sessionmaker(bind=engine)


class TestModels:
    def setup_class(self):
        Base.metadata.create_all(engine)
        self.session = Session()
        self.valid_flashcard = Flashcard(
            question="What is 2+2?",
            answer="4",
        )

    def teardown_class(self):
        self.session.rollback()
        self.session.close()

    def test_flashcard_valid(self):
        self.session.add(self.valid_flashcard)
        self.session.commit()
        my_flashcard = self.session.query(Flashcard).filter_by()
