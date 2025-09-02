import pytest
from fastapi.testclient import TestClient
from httpx import ASGITransport, AsyncClient
from main import app

client = TestClient(app)


@pytest.fixture
def anyio_backend():
    return "asyncio"


# @pytest.fixture(scope="session")
@pytest.mark.anyio
async def test_get_all_recipes():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://127.0.0.1:8000"
    ) as ac:
        response = await ac.get("/recipes/")
    assert response.status_code == 200


@pytest.mark.anyio
# @pytest.fixture(scope="session")
async def test_add_recipe():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://127.0.0.1:8000"
    ) as ac:
        response = await ac.post(
            "/recipes/",
            headers={"Content-Type": "application/json"},
            json={
                "name": "test",
                "cooking_time": 40,
                "ingredients_list": "test, test_2",
                "description": "just test",
                "count_view": 0,
            },
        )
        assert response.status_code == 200
        assert response.json() == {
            "name": "test",
            "cooking_time": 40,
            "ingredients_list": "test, test_2",
            "description": "just test",
            "count_view": 0,
        }
