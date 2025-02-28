ROLES = (
    ('user', 'Аутентифицированный пользователь'),
    ('moderator', 'Модератор'),
    ('admin', 'Администратор'),
)
ROLE_MAX_LENGTH = max(len(role[0]) for role in ROLES)
