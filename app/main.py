from fastapi import FastAPI
import uvicorn

from app.middleware.cors import get_cors_middleware
from app.config.config import load_config
from app.api import api_router

config = load_config()

app = FastAPI()
app.include_router(api_router)
get_cors_middleware(app)

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)