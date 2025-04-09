from fastapi import Depends, status, HTTPException
from fastapi.routing import APIRouter
from sqlalchemy.orm import Session

from app.database import get_db
from app.services.jwt import get_current_user
from app.shemas.auth import UserOut, UserIn, UserLogin, UserSessionOut
from app.crud.auth import UserCRUD

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/signup", response_model=UserOut, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserIn, db: Session = Depends(get_db)):
    return UserCRUD.create_user(db, user)

@router.post("/login", response_model=UserSessionOut, status_code=status.HTTP_201_CREATED)
async def login(user: UserLogin, db: Session = Depends(get_db)):
    return UserCRUD.login_user(db, user.email, user.password)

@router.get("/get_me", response_model=UserOut, status_code=status.HTTP_200_OK,
            dependencies=[Depends(get_current_user)])
def get_info_about_me(user = Depends(get_current_user), db: Session = Depends(get_db)):
    user = UserCRUD.get_user_if_user_exist(db, user['email'])
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_UNAUTHORIZED)
    return UserOut.model_validate(user)

