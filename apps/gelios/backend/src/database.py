from src.config import get_settings
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine


engine = create_async_engine(
    get_settings().db_host_uri,
    echo=False,
)
async_session = async_sessionmaker(engine, expire_on_commit=False)

Base = declarative_base()
