import re

from api.constants import BAD_USERNAME
from rest_framework.exceptions import ValidationError


def username_validator(username):
    if username == BAD_USERNAME:
        raise ValidationError(f'Имя "{BAD_USERNAME}" запрещено.')

    bad_chars = {char for char in username if not re.match(r"[\w.@+-]", char)}
    if bad_chars:
        raise ValidationError(
            f'Недопустимые символы в имени пользователя: '
            f'{", ".join(bad_chars)}. '
            'Разрешены только буквы, цифры и @/./+/-/_.')
    return username
