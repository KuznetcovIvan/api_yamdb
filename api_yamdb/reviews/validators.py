import re

from django.conf import settings
from django.utils.timezone import now
from rest_framework.exceptions import ValidationError


def username_validator(username):
    if username == settings.PROFILE_URL_SEGMENT:
        raise ValidationError(
            f'Логин "{settings.PROFILE_URL_SEGMENT}" запрещен.')
    invalid_chars = re.findall(r'[^\w.@+-]', username)
    if invalid_chars:
        raise ValidationError(
            'Недопустимые символы в логине: {} '
            'Разрешены только буквы, цифры и @/./+/-/_'.format(
                ''.join(set(invalid_chars))))
    return username


def validate_year(year):
    """Проверка года."""
    current_year = now().year
    if year > current_year:
        raise ValidationError(
            f'Указанный год ({year}) '
            f'не может быть больше текущего ({current_year}).')
    return year
