from httpx import AsyncClient


async def test_chat_returns_service_response(client: AsyncClient) -> None:
    response = await client.post("/chat", json={"message": "Hello"})

    assert response.status_code == 200
    assert response.json() == {"response": "Hello from LangChain service!"}


async def test_chat_rejects_empty_message(client: AsyncClient) -> None:
    response = await client.post("/chat", json={"message": ""})

    assert response.status_code == 422


async def test_chat_rejects_missing_message(client: AsyncClient) -> None:
    response = await client.post("/chat", json={})

    assert response.status_code == 422
