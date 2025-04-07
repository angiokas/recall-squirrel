from sqlalchemy.orm import Mapped, declarative_base
from sqlalchemy.orm import relationship, mapped_column
from sqlalchemy import Column, ForeignKey, String, Integer, DateTime
import uuid, datetime


Base = declarative_base()


def generate_uuid():
    return uuid.uuid4().int >> 64


class Difficulty(Base):
    __tablename__ = "difficulties"

    id: Mapped[int] = mapped_column(primary_key=True)


class Flashcard(Base):
    __tablename__ = "flashcards"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, unique=True, default=generate_uuid
    )
    title: Mapped[str] = mapped_column(default=f"Flashcard {id}")
    question: Mapped[str] = mapped_column(String, nullable=False)
    answer: Mapped[str] = mapped_column(nullable=False)


class Studyset(Base):
    __tablename__ = "studysets"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(Integer, nullable=False)
    flashcards: Mapped[list[Flashcard]] = relationship(
        "FlashcardStudyset", back_populates="studysets"
    )


class FlashcardStudyset(Base):
    __tablename__ = "flashcard_study_session"

    id: Mapped[int] = mapped_column(primary_key=True)
    flashcard_id: Mapped[int] = mapped_column(
        ForeignKey("flashcards.id"), nullable=False
    )
    studyset_id: Mapped[int] = mapped_column(ForeignKey("studysets.id"), nullable=False)

    # Relationships
    flashcard: Mapped[Flashcard] = relationship(back_populates="studysets")
    studyset: Mapped[Studyset] = relationship(back_populates="flashcards")

    session_id = Column(Integer, ForeignKey("studysets.id"), nullable=False)
    # added_at = Column(DateTime, default=datetime.datetime.)
