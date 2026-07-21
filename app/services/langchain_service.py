class LangChainService:
    """Service abstraction over LangChain.

    Intentionally trivial for now: it returns a static string. The async
    signature and service boundary are what matter — the internals can be
    swapped for a real LangChain chain (OpenAI, RAG, etc.) without touching
    the API layer.
    """

    async def invoke(self, message: str) -> str:
        return "Hello from LangChain service!"
