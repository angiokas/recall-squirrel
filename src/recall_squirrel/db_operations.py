from .models import Base, Flashcard, Studyset, FlashcardStudyset, Difficulty
from .session_management import get_session
from sqlalchemy import inspect

Session = get_session()

def create_flashcard(
    Session, f_question: str, f_answer: str, studyset_name: str = None
):
    """Creates a Flashcard object and saves it to the database"""
    session = Session()

    try:
        flashcard = Flashcard(question=f_question, answer=f_answer)
        session.add(flashcard)
        session.commit()
        print("Flashcard added to database!")

        if studyset_name:
            print("this should be added to studyset called ", studyset_name)
            # add_to_studyset()`
    except Exception as e:
        print(f"Error occured: {e}")
        session.rollback()
    finally:
        session.close()


def get_all_flashcards(Session):
    """Returns a list of all Flashcards from the database."""
    session = Session()
    try:
        # Query the database for all Flashcards
        flashcards = session.query(Flashcard).all()
        return flashcards
    except Exception as e:
        print(f"Error occurred: {e}")
        return []
    finally:
        session.close()


def add_to_studyset(Session, flashcard, studyset):
    """Adds this Flashcard to the specified StudySet."""
    session = Session()
    try:
        if studyset not in flashcard.study_sets:
            flashcard.study_sets.append(studyset)
            session.commit()
            print(f"Flashcard added to StudySet: {studyset.name}")
        else:
            print("Flashcard is already in this StudySet.")
    except Exception as e:
        print(f"Error occurred: {e}")
        session.rollback()
    finally:
        session.close()
