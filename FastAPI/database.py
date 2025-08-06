from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, AsyncEngine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite+aiosqlite:///./app.py.db"

engine = create_async_engine(DATABASE_URL, echo=True)
# expire_on_commit=False will prevent attributes from being expired
# after commit.
async_session = sessionmaker(AsyncEngine=engine, expire_on_commit=False, class_=type[AsyncSession], autoflush=False)
session = async_session()
Base = declarative_base()
