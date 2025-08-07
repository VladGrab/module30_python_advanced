from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import declarative_base, Mapped
# from sqlalchemy.ext.declarative import declarative_base
# from database import Base
Base = declarative_base()

class Recipe(Base):
    __tablename__ = 'Recipe'
    id: Mapped[int] = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name: Mapped[str] = Column(String)
    cooking_time: Mapped[int] = Column(Integer, default=0)
    ingredients_list: Mapped[str] = Column(String)
    description: Mapped[str] = Column(String)
    count_view: Mapped[int] = Column(Integer, default=0)
