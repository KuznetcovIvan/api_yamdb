import re

from rest_framework.exceptions import ValidationError

from api_yamdb.settings import RESERVED_USERNAME


def username_validator(username):
    if username == RESERVED_USERNAME:
        raise ValidationError(f'Имя "{RESERVED_USERNAME}" запрещено.')

    invalid_chars = sorted(set(re.findall(r'[^\w.@+-]', username)))
    if invalid_chars:
        raise ValidationError(
            f'Недопустимые символы в имени пользователя: '
            f'{" ".join(invalid_chars)} '
            'Разрешены только буквы, цифры и @/./+/-/_')
    return username
