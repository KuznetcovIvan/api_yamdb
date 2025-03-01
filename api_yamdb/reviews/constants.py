MAX_LENGTH_NAME = 256
MAX_LENGTH_SLUG = 50
MAX_LENGTH_STR = 50

ROLES = (
    ('user', 'Аутентифицированный пользователь'),
    ('moderator', 'Модератор'),
    ('admin', 'Администратор'),
)
ROLE_MAX_LENGTH = max(len(role[0]) for role in ROLES)
EMAIL_MAX_LENGTH = 254
USERNAME_MAX_LENGTH = 150
