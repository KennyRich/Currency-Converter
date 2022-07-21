from abc import ABC, abstractmethod


class BaseCurrencyConverterAPI(ABC):
    @abstractmethod
    async def get_latest_rates(self):
        ...

    @abstractmethod
    async def get_symbols(self):
        ...

    @abstractmethod
    async def get_currency_conversion(self, from_currency, to_currency, amount):
        ...

    @abstractmethod
    async def get_historical_rates(self, currency, start_date, end_date, symbols):
        ...
