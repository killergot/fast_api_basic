from app.core.config import load_config
from app.utils.jwt import encode_jwt, decode_jwt

config = load_config()

SECRET_KEY = config.secret_keys.secret_key_jwt
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_SECONDS = 3600  # час


def create_access_token(user_id: int,
                        user_email: str,
                        user_role: int):
    payload = {'id': user_id,
               'email': user_email,
               'role': user_role}
    return encode_jwt(payload,
            SECRET_KEY,
            ALGORITHM,
            ACCESS_TOKEN_EXPIRE_SECONDS)

def decode_access_token(token: str) -> dict:
    return decode_jwt(token, secret=SECRET_KEY)


if __name__ == '__main__':
    a = create_access_token(1,'test',1)
    print(a)
    print(decode_access_token(a['access_token']))



