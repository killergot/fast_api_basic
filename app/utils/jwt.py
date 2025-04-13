from datetime import datetime, timezone

from authlib.jose import jwt
import time


def get_key(secret: str):
    return {'k': secret, 'kty': 'oct'}

def encode_jwt(payload: dict,
            secret: str,
            algorithm: str,
            expire_at: int):
    header = {'alg': algorithm, 'typ': 'JWT'}
    expire_at = time.time() + expire_at
    payload['exp'] = expire_at
    token = jwt.encode(header, payload, get_key(secret)).decode('utf-8')
    return {'access_token': token, 'expires_at': datetime.fromtimestamp(expire_at,
                                                                tz=timezone.utc)}

def decode_jwt(token: str,
               secret: str):
    try:
        claims = jwt.decode(token, get_key(secret))
        claims.validate()
        return claims
    except:
        return False

