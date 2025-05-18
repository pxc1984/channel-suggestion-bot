from sqlalchemy import Column, Integer, BigInteger, Boolean, String, ForeignKey

from db.base import Base

class User(Base):
    __tablename__ = "users"

    id = Column(BigInteger, primary_key=True)
    username = Column(String)
    admin = Column(Boolean, default=False)
    banned = Column(Boolean, default=False)

class SuggestionOriginalMessage(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, autoincrement=True)
    message_id = Column(BigInteger)
    from_user = Column(BigInteger, ForeignKey("users.id"), nullable=False) # it should relate to user who sent it, to it's id
    text = Column(String)

    def serialize(self):
        return {
            'id': self.id,
            'message_id': self.message_id,
            'from_user': self.from_user,
        }

class SuggestionForwardedMessage(Base):
    __tablename__ = "forwarded"

    id = Column(Integer, primary_key=True, autoincrement=True)
    message_id = Column(BigInteger)
    chat_id = Column(BigInteger)
    original_suggestion = Column(Integer, ForeignKey("messages.id"))

    def serialize(self):
        return {
            'id': self.id,
            'message_id': self.message_id,
            'chat_id': self.chat_id,
            'original_suggestion': self.original_suggestion,
        }
