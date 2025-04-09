from datetime import datetime, timezone
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Depends,HTTPException, status

from authlib.jose import jwt
import time

from app.config.config import load_config


config = load_config()

SECRET_KEY = config.secret_keys.secret_key_jwt
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_SECONDS = 3600  # час

key = {'k': SECRET_KEY, 'kty': 'oct'}
header = {'alg': ALGORITHM, 'typ': 'JWT'}

security = HTTPBearer()

def get_jwt(sub: str):
    expire_at = time.time() + ACCESS_TOKEN_EXPIRE_SECONDS
    payload = { 'sub': sub, 'exp': expire_at}
    token = jwt.encode(header, payload, key).decode('utf-8')
    return {'access_token': token, 'expires_at': datetime.fromtimestamp(expire_at,
                                                                tz=timezone.utc)}

def verify_jwt(token):
    try:
        claims = jwt.decode(token, key)
        claims.validate()
        return claims
    except:
        return False

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    if not credentials or not credentials.scheme.lower() == "bearer":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authorization scheme"
        )

    token = credentials.credentials
    claims = verify_jwt(token)
    if not claims:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )
    return claims