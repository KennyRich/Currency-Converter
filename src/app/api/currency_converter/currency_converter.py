from fastapi import APIRouter, Depends
from . import LatestRates, Symbols, ConversionResult, HistoricalData, ConversionQuery, HistoricalQuery
from app.database.models.user import User
from app.api.security import get_current_user_from_token
from .APILayer import FixerCurrencyConverter

router = APIRouter(
    tags=['converter'],
    prefix='/v1/converter',
    responses={404: {'description': 'Not found'}},
)


@router.get(
    "/symbols",
    description="Get all symbols for available currencies",
    response_model=Symbols,
    status_code=200,
)
async def get_symbols(user: User = Depends(get_current_user_from_token), api_layer=Depends(FixerCurrencyConverter)):
    symbols = await api_layer.get_symbols()
    return Symbols(**symbols)


@router.get(
    '/rates',
    description="Get all the latest rates",
    response_model=LatestRates,
    status_code=200,
)
async def get_latest_rates(user: User = Depends(get_current_user_from_token),
                           api_layer=Depends(FixerCurrencyConverter)):
    rates = await api_layer.get_latest_rates()
    return LatestRates(**rates)


@router.post(
    '/convert',
    description="Convert all the available currencies using this route",
    response_model=ConversionResult,
    status_code=200,
)
async def convert_currency(conversion_query: ConversionQuery, user: User = Depends(get_current_user_from_token),
                           api_layer=Depends(FixerCurrencyConverter)):
    conversion_result = await api_layer.get_currency_conversion(
        from_currency=conversion_query.from_currency,
        to_currency=conversion_query.to_currency,
        amount=conversion_query.amount,
    )
    print(f"This is the conversion result: {conversion_result}")
    return ConversionResult(**conversion_result)


@router.post(
    '/historical-rates',
    description="Get historical rates for a currency within a start date and end date",
    response_model=HistoricalData,
    status_code=200,
)
async def get_historical_rates(historical_query: HistoricalQuery, user: User = Depends(get_current_user_from_token),
                               api_layer=Depends(FixerCurrencyConverter)):
    historical_data = await api_layer.get_historical_rates(
        currency=historical_query.base_currency,
        start_date=historical_query.start_date,
        end_date=historical_query.end_date,
        symbols=historical_query.symbols,
    )
    return historical_data
