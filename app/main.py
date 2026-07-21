from fastapi import FastAPI

from app.api.routes import router

app = FastAPI(title="azure-test")
app.include_router(router)
