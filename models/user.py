
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from core.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(255), unique=True, index=True, nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)

    works = relationship(
        "Work",
        back_populates="artist",
        cascade="all, delete-orphan",
    )

    supports = relationship(
        "Support",
        back_populates="supporter",
    )
