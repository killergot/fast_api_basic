from dataclasses import dataclass
from typing import Optional

from environs import Env

@dataclass
class DB:
    db_name : str
    db_host : str
    db_user : str
    db_pass : str

@dataclass
class SecretKeys:
    secret_key_jwt : str
    secret_key_signature : str

@dataclass
class Credentials:
    admin_username : str
    admin_password : str
    test_username : str
    test_password : str


@dataclass
class Config:
    database: DB
    secret_keys: SecretKeys
    credentials: Credentials



def load_config(path: Optional[str] = None) -> Config:
    env = Env()
    env.read_env(path)
    return Config(database = DB(db_name=env('DB_NAME'),
                          db_host=env('DB_HOST'),
                          db_user=env('DB_USER'),
                          db_pass=str(env('DB_PASS'))),
                  secret_keys = SecretKeys(secret_key_jwt = env('SECRET_KEY_JWT'),
                                           secret_key_signature = env('SECRET_KEY_SIGNATURE')),
                  credentials = Credentials(admin_username = env('ADMIN_MAIL'),
                                            admin_password = env('ADMIN_PASS'),
                                            test_username = env('TEST_MAIL'),
                                            test_password = str(env('TEST_PASS'))))