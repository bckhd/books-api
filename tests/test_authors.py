import pytest


@pytest.mark.asyncio
async def test_get_authors(ac):
    response = await ac.get("/authors/")

    assert response.status_code == 200

    data = response.json()

    assert len(data) != 0
