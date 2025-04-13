from functools import reduce
from operator import concat

from app.core.config import load_config
from app.utils.hash import encode_data

SECRET_KEY = load_config().secret_keys.secret_key_signature


def get_signature(*args: any):
    data = reduce(concat, [*map(str,args),SECRET_KEY])
    return encode_data(data)