import re


def validate_user_phone(value):
    """Валидация phone"""
    pattern = r'^\d{10}$'
    if re.match(pattern, str(value)):
        return value
