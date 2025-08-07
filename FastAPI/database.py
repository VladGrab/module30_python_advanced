from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, AsyncEngine, async_sessionmaker


DATABASE_URL = "sqlite+aiosqlite:///./app.py.db"

engine: AsyncEngine = create_async_engine(DATABASE_URL, echo=True)
async_session = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)
session = async_session()

