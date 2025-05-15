import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from db.base import Base
from db.models import User, Suggestion

DATABASE_URL = os.getenv("DATABASE_URL") if os.getenv("DATABASE_URL") else "sqlite:///bot.db"
engine = create_engine(DATABASE_URL, echo=False)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

def try_register_user(user_id: int, username: str = "") -> bool:
    session = SessionLocal()
    try:
        user = session.query(User).filter_by(id=user_id).first()
        if user:
            return False
        session.add(User(id=user_id, username=username))
        session.commit()
    finally:
        session.close()
        return True

def try_register_message(message_id: int, from_user: int, text: str) -> bool:
    session = SessionLocal()
    try:
        _from_user = session.query(User).filter_by(id=from_user)
        if not _from_user:
            return False
        session.add(Suggestion(id=message_id, from_user=from_user, text=text))
        session.commit()
    finally:
        session.close()
        return True


def init_db():
    Base.metadata.create_all(bind=engine)
