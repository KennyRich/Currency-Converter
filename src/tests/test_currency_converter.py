import json
import pytest
from app.api.currency_converter import Symbols, LatestRates, ConversionResult, HistoricalData


@pytest.mark.asyncio
class TestConverterRouteUnauthenticated:
    async def test_get_symbols__with_unauthenticated_user(self, client):
        response = client.get("/v1/converter/symbols/")
        assert response.status_code == 401
        assert response.json()["detail"] == "Not authenticated"

    async def test_get_latest_rates__with_unauthenticated_user(self, client):
        response = client.get("/v1/converter/rates/")
        assert response.status_code == 401
        assert response.json()["detail"] == "Not authenticated"

    async def test_convert_currency__with_unauthenticated_user(self, client):
        data = {
            "from_currency": "USD",
            "to_currency": "EUR",
            "amount": 1,
        }
        response = client.post("/v1/converter/convert", data=json.dumps(data))
        assert response.status_code == 401
        assert response.json()["detail"] == "Not authenticated"

    async def test_get_historical_rates__with_unauthenticated_user(self, client):
        data = {
            "base": "USD",
            "start_date": "2020-01-01",
            "end_date": "2020-01-02",
        }
        response = client.post("/v1/converter/historical-rates", data=json.dumps(data))
        assert response.status_code == 401
        assert response.json()["detail"] == "Not authenticated"


@pytest.mark.asyncio
@pytest.mark.usefixtures("normal_user_token_headers")
class TestConverterRouteAuthenticated:

    async def test_get_symbols__with_authenticated_user(self, client, mock_get_symbols):
        response = client.get("/v1/converter/symbols/")
        assert response.status_code == 200
        assert mock_get_symbols.called
        assert response.json() == Symbols(**mock_get_symbols.return_value).dict()

    async def test_get_latest_rates__with_authenticated_user(self, client, mock_get_latest_rates):
        response = client.get("/v1/converter/rates/")
        assert response.status_code == 200
        assert mock_get_latest_rates.called
        assert response.json() == LatestRates(**mock_get_latest_rates.return_value).dict()

    async def test_convert_currency__with_authenticated_user(self, client, mock_get_currency_conversion,
                                                             mock_get_symbols_sync):
        response = client.post("/v1/converter/convert",
                               data=json.dumps({"from_currency": "USD", "to_currency": "AUD", "amount": 1}))
        assert response.status_code == 200
        assert mock_get_currency_conversion.called
        assert response.json() == ConversionResult(**mock_get_currency_conversion.return_value)

    async def test_get_historical_rates__with_authenticated_user(self, client, mock_get_historical_rates,
                                                                 mock_get_symbols_sync):
        response = client.post("/v1/converter/historical-rates", data=json.dumps(
            {"base_currency": "USD", "start_date": "2021-12-21", "end_date": "2021-12-22"}))
        assert response.status_code == 200
        assert mock_get_historical_rates.called
        assert response.json() == HistoricalData(**mock_get_historical_rates.return_value).dict()
