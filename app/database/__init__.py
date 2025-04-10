from .psql import get_db, create_db, engine
from .models.auth import User
from .models.transaction import BankTransaction
from .models.bank_account import BankAccount
from .triggers import *
import asyncio



# asyncio.run(create_db())


