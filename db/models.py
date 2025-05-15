from sqlalchemy import Column, Integer, BigInteger, Boolean, String, ForeignKey
from sqlalchemy.orm import relationship

from db.base import Base

class User(Base):
    __tablename__ = "users"

    id = Column(BigInteger, primary_key=True)
    username = Column(String)
    admin = Column(Boolean, default=False)

    suggestions = relationship("Suggestion", back_populates="user")

class Suggestion(Base):
    __tablename__ = "messages"

    id = Column(BigInteger, primary_key=True)
    from_user = Column(BigInteger, ForeignKey("users.id"), nullable=False) # it should relate to user who sent it, to it's id
    text = Column(String)

    user = relationship("User", back_populates="suggestions")
