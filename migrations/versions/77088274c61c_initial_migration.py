"""Initial migration

Revision ID: 77088274c61c
Revises: 
Create Date: 2025-04-11 20:48:51.261918

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

from app.config.config import load_config

config = load_config()
# revision identifiers, used by Alembic.
revision: str = '77088274c61c'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

ACCOUNT_BALANCE_TRIGGER = """
CREATE OR REPLACE FUNCTION update_account_balance()
RETURNS TRIGGER AS $$
BEGIN
    UPDATE bank_account
    SET balance = balance + NEW.amount
    WHERE id = NEW.account_id;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;
"""

ACCOUNT_BALANCE_TRIGGER2 = """
CREATE TRIGGER trigger_update_balance
    AFTER INSERT ON bank_transaction
    FOR EACH ROW
    EXECUTE FUNCTION update_account_balance();
"""

CREATE_ADMIN_USER = f"""
INSERT INTO public.users(
    full_name, email, password, is_admin, created_at, updated_at)
    VALUES ('admin', '{config.credentials.admin_username}', '{config.credentials.admin_password}', TRUE,NOW(),NOW());
"""

CREATE_TEST_USER=f"""
INSERT INTO public.users(
    full_name, email, password, is_admin, created_at, updated_at)
    VALUES ('test', '{config.credentials.test_username}', '{config.credentials.test_password}', FALSE,NOW(),NOW());
"""

CREATE_ACCOUNT_TEST_USER="""
INSERT INTO public.bank_account(
	id, user_id, balance)
	VALUES (1, 2, 0);
"""


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('full_name', sa.String(length=255), nullable=False),
    sa.Column('email', sa.String(length=255), nullable=False),
    sa.Column('password', sa.Text(), nullable=False),
    sa.Column('is_admin', sa.Boolean(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_table('bank_account',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('balance', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id', 'user_id')
    )
    op.create_table('bank_transaction',
    sa.Column('transaction_id', sa.UUID(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('account_id', sa.Integer(), nullable=False),
    sa.Column('amount', sa.Integer(), nullable=False),
    sa.Column('signature', sa.Text(), nullable=False),
    sa.ForeignKeyConstraint(['account_id', 'user_id'], ['bank_account.id', 'bank_account.user_id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('transaction_id')
    )

    op.execute(ACCOUNT_BALANCE_TRIGGER)
    op.execute(ACCOUNT_BALANCE_TRIGGER2)
    op.execute(CREATE_ADMIN_USER)
    op.execute(CREATE_TEST_USER)
    op.execute(CREATE_ACCOUNT_TEST_USER)
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.execute("DROP TRIGGER IF EXISTS trigger_update_balance ON bank_transaction")
    op.execute("DROP FUNCTION IF EXISTS update_account_balance()")
    op.drop_table('bank_transaction')
    op.drop_table('bank_account')
    op.drop_table('users')
    # ### end Alembic commands ###
