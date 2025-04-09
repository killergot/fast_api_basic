from .auth import router as auth_router
from fastapi.routing import APIRouter

api_router = APIRouter()
api_router.include_router(auth_router)
