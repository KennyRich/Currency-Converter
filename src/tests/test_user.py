import json
import pytest


@pytest.mark.asyncio
class TestCreatUser:
    async def test_create_user(self, client):
        data = {
            "name": "testuser",
            "email": "testuser@nofoobar.com",
            "password": "testing",
        }

        response = client.post("/v1/user/signup", data=json.dumps(data))
        assert response.status_code == 200
        assert response.json()["email"] == "testuser@nofoobar.com"

    async def test_create_user__error(self, client):
        data = {
            "username": "testuser",
            "email": "testuser@gmail.com",
            "password": "testing",
        }

        response = client.post("/v1/user/signup", data=json.dumps(data))
        assert response.status_code == 422

    async def test_create_user_with_invalid_email(self, client):
        data = {
            "name": "testuser",
            "email": "testuser@nofoobar",
            "password": "testing",
        }

        response = client.post("/v1/user/signup", data=json.dumps(data))
        assert response.status_code == 422
        assert response.json()["detail"] == [
            {'loc': ['body', 'email'], 'msg': 'value is not a valid email address', 'type': 'value_error.email'}]
