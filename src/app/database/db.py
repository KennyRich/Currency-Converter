import os
import databases
from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import settings


if settings.USE_SQLITE_DB == "True":
    DATABASE_URL = "sqlite:///./sql_app.db"
    engine = create_engine(
        DATABASE_URL, connect_args={"check_same_thread": False}
    )
else:
    DATABASE_URL = settings.DATABASE_URL
    engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db() -> Generator:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


async def check_db_connected():
    try:
        if not str(DATABASE_URL).__contains__("sqlite"):
            database = databases.Database(DATABASE_URL)
            if not database.is_connected:
                await database.connect()
                await database.execute("SELECT 1")
        print("Database is connected (^_^)")
    except Exception as e:
        print(
            "Looks like db is missing or is there is some problem in connection,see below traceback"
        )
        raise e


async def check_db_disconnected():
    try:
        if not str(DATABASE_URL).__contains__("sqlite"):
            database = databases.Database(DATABASE_URL)
            if database.is_connected:
                await database.disconnect()
        print("Database is Disconnected (-_-) zZZ")
    except Exception as e:
        raise e
