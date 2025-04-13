from .auth import router as auth_router
from .users import router as users_router
from .bank_account import router as bank_account_router
from .transaction import router as transaction_router
from fastapi.routing import APIRouter


api_router = APIRouter()
api_router.include_router(auth_router)
api_router.include_router(users_router)
api_router.include_router(bank_account_router)
api_router.include_router(transaction_router)
