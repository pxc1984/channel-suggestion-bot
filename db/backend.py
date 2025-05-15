import os

from sqlalchemy import create_engine
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import sessionmaker

from db.base import Base
from db.models import User, SuggestionOriginalMessage, SuggestionForwardedMessage

DATABASE_URL = os.getenv("DATABASE_URL") if os.getenv("DATABASE_URL") else "sqlite:///bot.db"
engine = create_engine(DATABASE_URL, echo=False)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

def try_register_user(user_id: int, username: str = "") -> bool:
    """
    Попытаться зарегистрировать нового пользователя в базу данных
    :param user_id: Уникальный tg идентификатор пользователя
    :param username: (опционально) Юзернейм пользователя
    :return: True если пользователь был только что зарегистрирован и False если пользователь уже был до этого в базе данных
    """
    session = SessionLocal()
    try:
        user = session.get(User, user_id)
        if user:
            return False
        session.add(User(id=user_id, username=username))
        session.commit()
        return True
    finally:
        session.close()


# noinspection PyCompatibility
def register_original_message(message_id: int, from_user: int, text: str) -> bool | int:
    """
    Зарегистрировать в базу данных оригинальное сообщение с обращением
    :param message_id: Номер сообщения в чате (по сути бесполезная хуета...)
    :param from_user: От кого было получено сообщение. Это буквально уникальный айди пользователя
    :param text: (Опционально) текст, с которым шло сообщение
    :return: Уникальный айди сообщения если регистрация прошла успешно и False если такое сообщение уже есть в бд или же такого пользователя нет
    """
    session = SessionLocal()
    try:
        _from_user = session.get(User, from_user)
        if not _from_user:
            return False
        obj = SuggestionOriginalMessage(message_id=message_id, from_user=from_user, text=text)
        session.add(obj)
        session.commit()
        return obj.id
    finally:
        session.close()

def register_forwarded_message(message_id: int, chat_id: int, original_suggestion: int) -> bool:
    """
    Зарегистрировать в базу данных пересланное сообщение с обращением
    :param message_id: Номер сообщения в чате
    :param chat_id: Уникальный айди пользователя куда было отправлено сообщение
    :param original_suggestion: Уникальный внутрибазный идентификатор оригинального сообщения
    :return: Получилось зарегистрировать или нет
    """
    session = SessionLocal()
    try:
        if not get_original_message(original_suggestion):
            return False
        session.add(SuggestionForwardedMessage(message_id=message_id, chat_id=chat_id, original_suggestion=original_suggestion))
        session.commit()
        return True
    finally:
        session.close()

def get_original_message_from_forwarded(chat_id: int, message_id: int):
    """
    Вспомогательная функция, позволяющая получить внутрибазный идентификатор зная где было написано сообщение и какой номер этого
    сообщения в чате
    :param chat_id: В каком чате
    :param message_id: Номер сообщения в чате
    :return: False если оригинала сообщения не найдено и original_suggestion iD если оригинал найдер
    """
    session = SessionLocal()
    try:
        fwd_entry = session.query(SuggestionForwardedMessage).filter_by(chat_id=chat_id, message_id=message_id).first()
        if not fwd_entry:
            return False
        return get_original_message(fwd_entry.original_suggestion)
    finally:
        session.close()

def get_original_message(original_suggestion: int):
    """
    Уточняет существование уникального айди сообщения в базе данных
    :param original_suggestion: Уникальный айди оригинального обращения
    :return: Возвращает False если такого не найдено и original_suggestion если и правда такое существует
    """
    session = SessionLocal()
    try:
        msg = session.get(SuggestionOriginalMessage, original_suggestion)
        return msg.serialize() if msg is not None else False
    finally:
        session.close()

def is_admin(user_id: int) -> bool:
    """
    Узнать, является ли пользователем администратором бота
    :param user_id: Айди пользователя
    :return: Является или нет администратором бота
    """
    session = SessionLocal()
    try:
        try:
            user = session.get_one(User, user_id)
        except NoResultFound:
            return None
        return user.admin
    finally:
        session.close()

def is_admin_by_username(username: str) -> bool:
    session = SessionLocal()
    try:
        user = session.query(User).filter_by(username=username).first()
        if user is None:
            return False
        return user.admin
    finally:
        session.close()

def set_admin(user_id: int, status: bool) -> bool:
    """
    Устанавливает админ статус у пользователя на требуемый
    :param user_id: Айди пользователя, которому ставить
    :param status:
    :return:
    """
    session = SessionLocal()
    try:
        is_admin_status = is_admin(user_id)
        if is_admin_status is None:
            return False
        elif is_admin(user_id) == status:
            return True
        else:
            user = session.get(User, user_id)
            if user is None:
                return False
            user.admin = status
            session.commit()
            return True
    finally:
        session.close()

def set_admin_by_username(username: str, status: bool) -> bool:
    session = SessionLocal()
    try:
        _user = session.query(User).filter_by(username=username).first()
        if not _user:
            return False
        return set_admin(_user.id, status)
    finally:
        session.close()

def init_db():
    """
    Вспомогательная функция. Вызывается 1 раз в main.py и больше НИГДЕ НЕ ВЫЗЫВАТЬ!!
    :return:
    """
    Base.metadata.create_all(bind=engine)
