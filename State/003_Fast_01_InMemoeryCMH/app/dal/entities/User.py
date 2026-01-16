# app/models/user.py
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String

class Base(DeclarativeBase):
    pass

class UserEntity(Base):
    __tablename__ = "UserEntity"

    Id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    UserId: Mapped[int | None] = mapped_column(Integer, nullable=True)
    Name: Mapped[str | None] = mapped_column(String(50), nullable=True) 
 