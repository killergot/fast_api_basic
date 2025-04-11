import asyncio

from fastapi import Depends, status
from fastapi.routing import APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db, create_db

router = APIRouter(prefix="/dev", tags=["dev"])

@router.post("/create_db", status_code=status.HTTP_201_CREATED)
async def create_user():
    await create_db()
