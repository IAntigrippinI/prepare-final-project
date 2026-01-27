from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config import settings

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

engine = create_engine(
    settings.DB_URL,
    echo=True,
)
session_maker = sessionmaker(
    bind=engine,
    expire_on_commit=False
)
#
# # Классическая декларативная база
Base = declarative_base()