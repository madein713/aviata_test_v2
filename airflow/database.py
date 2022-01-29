
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base

from config.settings import settings


engine = create_async_engine(settings.DB_URL_AIRFLOW)
Base = declarative_base()
SessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
