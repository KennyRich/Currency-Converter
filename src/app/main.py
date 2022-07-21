from app.config import settings
from app.database.db import Base, engine, check_db_connected, check_db_disconnected
from fastapi import FastAPI
from app.api.login import login
from app.api.user import user
from app.api.currency_converter import currency_converter
from app.api.exception_handler import *
from httpx._exceptions import TimeoutException


def create_tables():
    Base.metadata.create_all(bind=engine)


def start_application():
    app = FastAPI(title=settings.PROJECT_NAME, version=settings.PROJECT_VERSION)
    app.include_router(login.router)
    app.include_router(user.router)
    app.include_router(currency_converter.router)
    app.add_exception_handler(TimeoutException, timeout_exception_handler)
    app.add_exception_handler(Exception, global_exception_handler)
    create_tables()
    return app


app = start_application()


@app.on_event("startup")
async def app_startup():
    await check_db_connected()


@app.on_event("shutdown")
async def app_shutdown():
    await check_db_disconnected()
