from fastapi import FastAPI
import uvicorn
import logging

from app.middleware.cors import get_cors_middleware
from app.api.routers import api_router

from app.core.logger import init_log


init_log(logging.DEBUG)
app = FastAPI()
app.include_router(api_router)
get_cors_middleware(app)

if __name__ == "__main__":
    # Для докера
    # uvicorn.run("main:app",host="0.0.0.0", reload=True)
    uvicorn.run("main:app", reload=True)