import re

from datab import Database

db = Database("hospital.db")


def check_good(text: str):
    flag = True
    for row in text.split():
        if not row.isalpha():
            flag = False
    return flag


def validate_phone_number(phone_number: str) -> bool:
    pattern = r'^\+7 \(\d{5}\) \d-\d{2}-\d{2}$'
    if re.match(pattern, phone_number):
        return True
    return False


def check_user(id: int):
    return db.user_exists(id)
