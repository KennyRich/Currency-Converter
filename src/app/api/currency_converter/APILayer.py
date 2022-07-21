from abc import ABC
from .BaseApILayer import BaseCurrencyConverterAPI
from typing import NoReturn, Final, Dict
from app.config import settings
import httpx
from functools import lru_cache
from datetime import date
from fastapi import HTTPException


class FixerCurrencyConverter(BaseCurrencyConverterAPI, ABC):
    def __init__(self) -> NoReturn:
        self.base_url: Final[str] = settings.API_BASE_URL
        self.headers: Dict = {"apikey": settings.APILAYER_API_KEY}
        self.timeout = None

    async def get_latest_rates(self):
        url = self.base_url + '/latest'
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=self.headers)
            if response.status_code == 200:
                return response.json()
            raise HTTPException(status_code=response.status_code, detail=response.json())

    @lru_cache(None)
    async def get_symbols(self):
        url = self.base_url + '/symbols'
        async with httpx.AsyncClient(timeout=None) as client:
            response = await client.get(url, headers=self.headers)
            if response.status_code == 200:
                return response.json()
            raise HTTPException(status_code=response.status_code, detail=response.json())

    async def get_currency_conversion(self, from_currency, to_currency, amount):
        url = self.base_url + '/convert'
        params = {
            "from": from_currency,
            "to": to_currency,
            "amount": amount
        }
        async with httpx.AsyncClient(timeout=None) as client:
            response = await client.get(url, headers=self.headers, params=params)
            if response.status_code == 200:
                return response.json()
            raise HTTPException(status_code=response.status_code, detail=response.json())

    async def get_historical_rates(self, currency: str, start_date: date, end_date: date, symbols: list[str]):
        if symbols:
            symbols = ','.join(symbols)
            url = self.base_url + f'/timeseries?start_date={start_date}&end_date={end_date}&base={currency}&symbols={symbols}'
        else:
            url = self.base_url + f'/timeseries?start_date={start_date}&end_date={end_date}&base={currency}'

        async with httpx.AsyncClient(timeout=None) as client:
            response = await client.get(url, headers=self.headers)
            if response.status_code == 200:
                return response.json()
            raise HTTPException(status_code=response.status_code, detail=response.json())

    @lru_cache(None)
    def get_symbols_sync(self):
        url = self.base_url + '/symbols'
        response = httpx.get(url, headers=self.headers, timeout=None)
        return response.json()
