from pydantic import BaseModel, Field, PositiveInt, root_validator
from typing import Dict, Union, List, Optional
from http import HTTPStatus
from .APILayer import FixerCurrencyConverter
from datetime import date


class Response(BaseModel):
    status: HTTPStatus = Field(default=HTTPStatus.OK, description="Status code")


class LatestRates(Response):
    base: str = Field(..., description="The base currency")
    date: str = Field(..., description="The date of the rates")
    rates: Dict[str, float] = Field(..., description="TThe dictionary containing rates against the base")


class Symbols(Response):
    symbols: Dict[str, str] = Field(..., description="The dictionary containing symbols against the base")


api_layer = FixerCurrencyConverter()
result = api_layer.get_symbols_sync()


class ConversionQuery(BaseModel):
    from_currency: str = Field(..., description="The currency to convert from")
    to_currency: str = Field(..., description="The currency to convert to")
    amount: Union[int, float] = Field(..., description="The amount to convert")

    @root_validator(allow_reuse=True)
    def validate_amount(cls, values):
        from_cur = values.get('from_currency')
        to_cur = values.get('to_currency')
        if not result['symbols'].get(from_cur):
            raise ValueError(f"{from_cur} is not a valid currency")
        if not result['symbols'].get(to_cur):
            raise ValueError(f"{to_cur} is not a valid currency")
        return values


class ConversionResult(Response):
    date: str = Field(..., description="The date of the rates")
    info: Dict[str, Union[PositiveInt, float]] = Field(..., description="The dictionary rate and timestamp")
    query: Dict[str, Union[str, PositiveInt]] = Field(..., description="The dictionary containing query")
    result: Union[PositiveInt, float] = Field(..., description="The result of the conversion")


class HistoricalData(Response):
    base: str = Field(..., description="The base currency")
    end_date: str = Field(..., description="The end date of the historical rates")
    rates: Dict[str, Dict[str, float]] = Field(..., description="The dictionary containing rates against the base")


class HistoricalQuery(BaseModel):
    base_currency: str = Field(..., description="The base currency")
    start_date: date = Field(..., description="The start date of the historical rates")
    end_date: date = Field(..., description="The end date of the historical rates")
    symbols: Optional[List[str]] = Field(None, description="The list of symbols to include in the historical rates")

    @root_validator(allow_reuse=True)
    def validate_dates(cls, values):
        if values.get('start_date') > values.get('end_date'):
            raise ValueError("Start date cannot be after end date")

        base_cur = values.get('base_currency')
        if not result['symbols'].get(base_cur):
            raise ValueError(f"{base_cur} is not a valid currency")
        sym = values.get('symbols')
        if sym:
            for s in sym:
                if not result['symbols'].get(s):
                    raise ValueError(f"{s} is not a valid currency")
        return values

