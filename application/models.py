from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP, text, ForeignKey
from .database import Base
from sqlalchemy.orm import relationship

class Cards(Base):
    __tablename__ = "cards"

    card_id = Column(String, primary_key=True, nullable=False)
    card_name = Column(String, nullable = False)
    set_name = Column(String, nullable = False)
    card_number = Column(String, nullable = False)
    pokemon_name = Column(String, nullable = False)

class Users(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, nullable=False)
    password = Column(String, nullable = False)
    email = Column(String, nullable = False)

class Collections(Base):
    __tablename__ = "collections"

    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"), primary_key=True, nullable=False)
    card_id = Column(String, ForeignKey("cards.card_id", ondelete="CASCADE"), primary_key=True, nullable=False)
    card_count = Column(Integer, nullable = False, default=0)