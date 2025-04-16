from fastapi import Depends, status
from fastapi.routing import APIRouter

from app.api.depencies.guard import get_current_user, require_role
from app.api.depencies.services import get_bank_account_service
from app.services.bank_account_service import BankAccountService
from app.services.role_service import ADMIN_ROLE
from app.shemas.user import UserOut
from app.shemas.bank_account import BankAccountOut, BankAccountIn, BankAccountUserIn

router = APIRouter(prefix="/bank_account", tags=["bank_account"])

@router.post("/", status_code=status.HTTP_201_CREATED,
             response_model=BankAccountOut,
             summary="Create new bank account for current user",
             description="Create new bank account for current user")
async def create_account(account: BankAccountIn,
                         user:UserOut =  Depends(get_current_user),
                         service:BankAccountService =  Depends(get_bank_account_service)):
    account = BankAccountUserIn(account_id = account.account_id, user_id= user.id)
    return await service.create_account(account)


@router.get("/all", status_code=status.HTTP_201_CREATED,
            summary="Get all bank accounts for current user",
            description="Get all bank accounts for current user")
async def create_account(user:UserOut =  Depends(get_current_user),
                         service:BankAccountService =  Depends(get_bank_account_service)):
    return await service.get_all_by_user(user.id)

@router.get("/all_by_user", status_code=status.HTTP_200_OK,
            dependencies=[Depends(require_role(ADMIN_ROLE))],
            summary="Get all bank accounts for user",
            description="Get all bank accounts for user\n"
                    "- Only administrators use this endpoint\n")
async def create_account(user_id: int,
                         service:BankAccountService =  Depends(get_bank_account_service)):
    return await service.get_all_by_user(user_id)

@router.get("/{account_id}", status_code=status.HTTP_200_OK,
            summary="Get bank account by id",
            description="Get bank account by id\n"
                        "- This dont work if this account is not yours")
async def create_account(account_id: int,
                         user:UserOut =  Depends(get_current_user),
                         service:BankAccountService =  Depends(get_bank_account_service)):
    account = BankAccountUserIn.model_validate({'account': account_id, 'user': user.id})

    return await service.get_account(account)

@router.delete("/{account_id}", status_code=status.HTTP_200_OK,
               summary="Delete bank account by id",
               description="Delete bank account by id\n"
               "- This dont work if this account is not yours")
async def create_account(account_id: int,
                         user:UserOut =  Depends(get_current_user),
                         service:BankAccountService =  Depends(get_bank_account_service)):
    account = BankAccountUserIn.model_validate({'account': account_id, 'user': user.id})
    return await service.delete_account(account)



