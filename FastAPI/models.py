from typing import Any

from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import declarative_base
# from sqlalchemy.ext.declarative import declarative_base
# from database import Base
Base: Any  = declarative_base()

class Recipe(Base):
    __tablename__ = 'Recipe'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String)
    cooking_time = Column(Integer, default=0)
    ingredients_list = Column(String)
    description = Column(String)
    count_view = Column(Integer, default=0)
