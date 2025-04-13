from sqlalchemy import DDL, event

from app.db.models.transaction import BankTransaction



# 1. Сначала создаем функцию
create_function = DDL("""
CREATE OR REPLACE FUNCTION update_account_balance()
RETURNS TRIGGER AS $$
BEGIN
    UPDATE bank_account
    SET balance = balance + NEW.amount
    WHERE id = NEW.account_id;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;
""")

# 2. Затем создаем триггер
create_trigger = DDL("""
CREATE TRIGGER trigger_update_balance
AFTER INSERT ON bank_transaction
FOR EACH ROW
EXECUTE FUNCTION update_account_balance();
""")

# Применяем в правильном порядке
event.listen(BankTransaction.__table__, 'after_create', create_function)
event.listen(BankTransaction.__table__, 'after_create', create_trigger)