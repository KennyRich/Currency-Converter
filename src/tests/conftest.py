import os
import sys
from typing import Any
from typing import Generator

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.orm import sessionmaker
from app.api.login import login
from app.api.user import user
from app.api.currency_converter import currency_converter
from httpx import AsyncClient
from unittest.mock import patch, MagicMock

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database.db import Base, get_db
from app.config import settings
from tests.utils import authentication_token_from_email


def start_application():
    app = FastAPI()
    app.include_router(login.router)
    app.include_router(user.router)
    app.include_router(currency_converter.router)
    return app


SQLALCHEMY_DATABASE_URL = "sqlite:///./test_db.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
# Use connect_args parameter only with sqlite
SessionTesting = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="module")
def app() -> Generator[FastAPI, Any, None]:
    """
    Create a fresh database on each test case.
    """
    Base.metadata.create_all(engine)  # Create the tables.
    _app = start_application()
    yield _app
    Base.metadata.drop_all(engine)


@pytest.fixture(scope="module")
def db_session(app: FastAPI) -> Generator[SessionTesting, Any, None]:
    connection = engine.connect()
    transaction = connection.begin()
    session = SessionTesting(bind=connection)
    yield session  # use the session in tests.
    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture(scope="module")
def client(
        app: FastAPI, db_session: SessionTesting
) -> Generator[TestClient, Any, None]:
    """
    Create a new FastAPI TestClient that uses the `db_session` fixture to override
    the `get_db` dependency that is injected into routes.
    """

    def _get_test_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = _get_test_db
    with TestClient(app) as client:
        yield client


@pytest.fixture(scope="module")
def normal_user_token_headers(client: TestClient, db_session: Session):
    return authentication_token_from_email(
        client=client, email=settings.TEST_USER_EMAIL, db=db_session
    )


class AsyncMock(MagicMock):
    async def __call__(self, *args, **kwargs):
        return super(AsyncMock, self).__call__(*args, **kwargs)


@pytest.fixture(scope="module")
def mock_get_latest_rates(client: TestClient):
    latest_rates = {
        "timestamp": 1658335084,
        "base": "EUR",
        "date": "2022-07-20",
        "rates": {
            "AED": 3.74862,
            "AFN": 91.556446,
            "ALL": 117.008415,
            "AMD": 424.152073,
            "ANG": 1.837422,
            "AOA": 439.187184,
            "ARS": 132.048184,
            "AUD": 1.480259,
            "AWG": 1.834465,
            "AZN": 1.74221,
            "BAM": 1.95535,
            "BBD": 2.058465,
            "BDT": 95.808915,
            "BGN": 1.955083,
            "BHD": 0.384689,
            "BIF": 2099.363879,
            "BMD": 1.020565,
            "BND": 1.420217,
            "BOB": 6.998982,
            "BRL": 5.54891,
            "BSD": 1.019535,
        }
    }
    with patch("app.api.currency_converter.FixerCurrencyConverter.get_latest_rates",
               new_callable=AsyncMock) as mock_get_latest_rates:
        mock_get_latest_rates.return_value = latest_rates
        yield mock_get_latest_rates


@pytest.fixture(scope="module")
def mock_get_symbols(client: TestClient):
    symbols = {"symbols": {
        "AED": "United Arab Emirates Dirham",
        "AFN": "Afghan Afghani",
        "ALL": "Albanian Lek",
        "AMD": "Armenian Dram",
        "ANG": "Netherlands Antillean Guilder",
        "AOA": "Angolan Kwanza",
        "ARS": "Argentine Peso",
        "AUD": "Australian Dollar",
        "AWG": "Aruban Florin",
        "AZN": "Azerbaijani Manat",
        "BAM": "Bosnia-Herzegovina Convertible Mark",
        "BBD": "Barbadian Dollar",
        "BDT": "Bangladeshi Taka",
        "BGN": "Bulgarian Lev",
        "BHD": "Bahraini Dinar",
        "BIF": "Burundian Franc",
        "BMD": "Bermudan Dollar",
        "BND": "Brunei Dollar",
    }}
    with patch("app.api.currency_converter.FixerCurrencyConverter.get_symbols",
               new_callable=AsyncMock) as mock_get_symbols:
        mock_get_symbols.return_value = symbols
        yield mock_get_symbols


@pytest.fixture(scope="module")
def mock_get_symbols_sync(client: TestClient):
    symbols = {
        "symbols": {
            "AED": "United Arab Emirates Dirham",
            "AFN": "Afghan Afghani",
            "ALL": "Albanian Lek",
            "AMD": "Armenian Dram",
            "ANG": "Netherlands Antillean Guilder",
            "AOA": "Angolan Kwanza",
            "ARS": "Argentine Peso",
            "AUD": "Australian Dollar",
            "AWG": "Aruban Florin",
        }
    }
    with patch("app.api.currency_converter.schemas.result") as mock_get_symbols_sync:
        mock_get_symbols_sync.return_value = symbols
        yield mock_get_symbols_sync


@pytest.fixture(scope="module")
def mock_get_currency_conversion(client: TestClient):
    currency_conversion = {
        "success": True,
        "query": {
            "from": "EUR",
            "to": "USD",
            "amount": 1
        },
        "info": {
            "timestamp": 1658336705,
            "rate": 1.017755
        },
        "date": "2022-07-20",
        "result": 1.017755
    }
    with patch("app.api.currency_converter.FixerCurrencyConverter.get_currency_conversion",
               new_callable=AsyncMock) as mock_get_currency_conversion:
        mock_get_currency_conversion.return_value = currency_conversion
        yield mock_get_currency_conversion


@pytest.fixture(scope="module")
def mock_get_historical_rates(client: TestClient):
    historical_rates = {
        "success": True,
        "timeseries": True,
        "start_date": "2021-12-21",
        "end_date": "2022-12-22",
        "base": "EUR",
        "rates": {
            "2021-12-21": {
                "AED": 4.145594,
                "AFN": 117.37834,
                "ALL": 120.982832,
                "AMD": 555.771258,
            },
            "2021-12-22": {
                "AED": 4.160739,
                "AFN": 117.253775,
                "ALL": 120.695346,
                "AMD": 557.825548,
            },
        }
    }
    with patch("app.api.currency_converter.FixerCurrencyConverter.get_historical_rates",
               new_callable=AsyncMock) as mock_get_historical_rates:
        mock_get_historical_rates.return_value = historical_rates
        yield mock_get_historical_rates

