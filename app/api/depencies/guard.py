from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials


from app.api.depencies.services import get_user_service
from app.core.security import decode_access_token
from app.services.user_service import UserService
from app.shemas.user import UserOut

security = HTTPBearer()

async def get_token_payload(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> dict:
    token = credentials.credentials
    payload = decode_access_token(token)
    if not payload or "id" not in payload:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Invalid token payload")

    return payload

async def get_current_user(
    payload: dict = Depends(get_token_payload),
    service: UserService = Depends(get_user_service)
) -> UserOut:
    user: UserOut = await service.get_user_by_id(payload["id"])
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="User not found")

    return user

def require_role(req_role: int):
    async def role_checker(payload: dict = Depends(get_token_payload)):
        if not payload["role"] & req_role:
            raise HTTPException(status_code=403,
                                detail="Not enough permissions")
        return payload
    return role_checker