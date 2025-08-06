from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, AsyncEngine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite+aiosqlite:///./app.py.db"

engine: AsyncEngine = create_async_engine(DATABASE_URL, echo=True)
async_session: AsyncSession = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)
session = async_session()
Base = declarative_base()
