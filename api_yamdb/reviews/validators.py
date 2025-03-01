import re

from django.utils.timezone import now
from rest_framework.exceptions import ValidationError

from api_yamdb.settings import RESERVED_USERNAME


def reserved_username_validator(username):
    if username == RESERVED_USERNAME:
        raise ValidationError(f'Имя "{RESERVED_USERNAME}" запрещено.')
    return username


def username_validator(username):
    reserved_username_validator(username)
    invalid_chars = sorted(set(re.findall(r'[^\w.@+-]', username)))
    if invalid_chars:
        raise ValidationError(
            f'Недопустимые символы в имени пользователя: '
            f'{" ".join(invalid_chars)} '
            'Разрешены только буквы, цифры и @/./+/-/_')
    return username


def validate_year(year):
    """Проверка года."""
    current_year = now().year
    if year > current_year:
        raise ValidationError(
            f'Указанный год ({year}) '
            f'не может быть больше текущего ({current_year}).')
    return year
