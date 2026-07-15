from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncAttrs
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import inspect, text
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./inline.db")

engine = create_async_engine(DATABASE_URL, echo=False)
async_session = async_sessionmaker(engine, expire_on_commit=False)


class Base(AsyncAttrs, DeclarativeBase):
    pass


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        await conn.run_sync(_migrate_sqlite)


def _migrate_sqlite(sync_conn):
    inspector = inspect(sync_conn)
    columns = [c["name"] for c in inspector.get_columns("queues")]
    if "use_time_slots" not in columns:
        sync_conn.execute(text("ALTER TABLE queues ADD COLUMN use_time_slots BOOLEAN DEFAULT 1"))


async def get_db():
    async with async_session() as session:
        yield session
