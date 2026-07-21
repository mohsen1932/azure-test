from app.services.langchain_service import LangChainService


async def test_invoke_returns_static_response() -> None:
    service = LangChainService()

    result = await service.invoke("anything")

    assert result == "Hello from LangChain service!"
