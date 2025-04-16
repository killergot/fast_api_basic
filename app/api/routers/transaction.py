from doctest import debug_script
from uuid import UUID

from fastapi import Depends, status, HTTPException
from fastapi.routing import APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.depencies.guard import get_current_user, require_role
from app.api.depencies.services import get_bank_transaction_service
from app.db.models.user import User
from app.services.role_service import ADMIN_ROLE
from app.services.transaction_service import TransactionService
from app.shemas.transaction import TransactionIn, TransactionOut, TransactionWebhookIn

router = APIRouter(prefix="/transaction", tags=["transaction"])

@router.post("/", status_code=status.HTTP_201_CREATED,
             response_model=TransactionOut,
             summary="Creating a transaction from a user",
             description="Creating a transaction from a user\n"
                         "- Signature build automatically")
async def do_transaction(transaction: TransactionIn,
                         service: TransactionService = Depends(get_bank_transaction_service),
                         user: User = Depends(get_current_user)):
    return await service.create_from_user(transaction, user.id)

@router.post("/webhook", status_code=status.HTTP_201_CREATED,
             response_model=TransactionOut,
             summary="Creating a transaction from a webhook",
             description="Creating a transaction from a webhook"
                         "\n- Signature requre")
async def do_transaction(transaction: TransactionWebhookIn,
                         service: TransactionService = Depends(get_bank_transaction_service)):
    return await service.check_webhook(transaction)

@router.get("/all/{user_id}", status_code=status.HTTP_200_OK,
            dependencies=[Depends(require_role(ADMIN_ROLE))],
            summary="Get all transactions from a any user\n",
            description="Get all transactions from a any user\n"
                    "- Only administrator can use this endpoint")
async def get_all_transactions(user_id : int,
                               service: TransactionService = Depends(get_bank_transaction_service)):
    return await service.get_all_by_user(user_id)

@router.get("/all", status_code=status.HTTP_200_OK,
            summary="Get all transactions from current user",)
async def get_all_transactions(user: User = Depends(get_current_user),
                               service: TransactionService = Depends(get_bank_transaction_service)):
    return await service.get_all_by_user(user.id)


@router.get("/{transaction_id}", status_code=status.HTTP_200_OK,
            summary="Get a specific transaction\n",
            description="Get a specific transaction\n"
            "- This dont work if this account is not yours")
async def get_transaction(transaction_id: UUID,
                          user = Depends(get_current_user),
                          service: TransactionService = Depends(get_bank_transaction_service)):
    return await service.get_from_user(transaction_id,user.id)

@router.delete("/{transaction_id}", status_code=status.HTTP_204_NO_CONTENT,
               dependencies=[Depends(require_role(ADMIN_ROLE))],
               summary="Delete a specific transaction\n",
               description="Delete a specific transaction\n"
                           "- Only administrator can use this endpoint")
async def try_delete_transaction(transaction_id: UUID,
                                 service: TransactionService = Depends(get_bank_transaction_service)):
    if not service.delete(transaction_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Deleting transactions is not allowed by system policy"
        )




