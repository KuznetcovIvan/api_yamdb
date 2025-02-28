ROLES = (
    ('user', 'Аутентифицированный пользователь'),
    ('moderator', 'Модератор'),
    ('admin', 'Администратор'),
)
ROLE_MAX_LENGTH = max(len(role[0]) for role in ROLES)
EMAIL_MAX_LENGTH = 254
USERNAME_MAX_LENGTH = 150
BAD_USERNAME = 'me'
