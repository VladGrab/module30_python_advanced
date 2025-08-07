from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


class Recipe(Base):
    __tablename__ = "Recipe"
    id: Column[int] = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name: Column[str] = Column(String)
    cooking_time: Column[int] = Column(Integer, default=0)
    ingredients_list: Column[str] = Column(String)
    description: Column[str] = Column(String)
    count_view: Column[int] = Column(Integer, default=0)
