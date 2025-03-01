# API для YaMDb

![Python](https://img.shields.io/badge/Python-3.8+-3776AB?logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-3.2-092E20?logo=django&logoColor=white)
![Django REST Framework](https://img.shields.io/badge/Django_REST_Framework-3.12-A30000?logo=django&logoColor=white)
![Simple JWT](https://img.shields.io/badge/Simple_JWT-4.7-000000?logo=json-web-tokens&logoColor=white)


Проект **API для YaMDb** — это REST API для платформы YaMDb.Платформа позволяет пользователям взаимодействовать с произведениями (фильмами, книгами, музыкой), оставлять отзывы и комментарии, выставлять оценки, а также управлять категориями и жанрами.

---

## Особенности
- **Аутентификация**: JWT-токены, выдаваемые после ввода кода подтверждения, отправленного на email.
- **Роли пользователей**:
  - **Аноним**: только чтение данных.
  - **User**: создание отзывов и комментариев.
  - **Moderator**: модерация отзывов и комментариев.
  - **Admin**: полный доступ ко всем ресурсам.
- **Пагинация**: Применяется для списков пользователей, произведений, отзывов и комментариев (10 элементов на страницу).
- **Фильтрация**: Поиск и фильтрация произведений по жанру, категории, названию и году выпуска.
- **Рейтинг**: Автоматический расчет среднего рейтинга произведения на основе отзывов.
- **Импорт данных**: Поддержка загрузки данных из CSV-файлов.

---

### Установка и запуск проекта

1. Клонируйте проект с репозитория `git clone https://github.com/KuznetcovIvan/api_yamdb.git`
2. Перейдите в директорию с проектом `api_yamdb`
3. Создайте виртуальное окружение в директории проекта:
   `python -m venv venv`,
   и активируйте его:
   `venv\Scripts\activate` (для Linux/macOS: `source venv/bin/activate`)
4. Установите зависимости:
   `pip install -r requirements.txt`
5. Создайте файл `.env` в корне проекта и задайте переменные окружения.
   Пример содержимого указан в файле `.env.example`.
6. Перейдите в директорию `cd api_yamdb`
7. Выполните миграции `python manage.py migrate`
8. Для импорта CSV-файлов в проект YaMDb выполните следующие шаги:
- Подготовьте CSV-файлы. Убедитесь, что файлы (users.csv, category.csv, genre.csv, titles.csv, review.csv, comments.csv, genre_title.csv) находятся в директории `static/data/`.
Файлы должны соответствовать структуре, ожидаемой моделями.
- Выполните команду импорта `python manage.py import_csv`.
9. Запустите проект `python manage.py runserver`

Проект будет доступен по адресу: [http://127.0.0.1:8000/](http://127.0.0.1:8000/).

---

## Спецификация API

После запуска проекта документация API доступна по адресу: [http://127.0.0.1:8000/redoc/](http://127.0.0.1:8000/redoc/).

Основные эндпоинты:
- **Регистрация и аутентификация**: `/api/v1/auth/signup/`, `/api/v1/auth/token/`.
- **Пользователи**: `/api/v1/users/`, `/api/v1/users/me/`.
- **Произведения**: `/api/v1/titles/`.
- **Категории и жанры**: `/api/v1/categories/`, `/api/v1/genres/`.
- **Отзывы и комментарии**: `/api/v1/titles/{title_id}/reviews/`, `/api/v1/titles/{title_id}/reviews/{review_id}/comments/`.

---

## Технологический стек

- Python
- Django
- Django REST Framework
- Simple JWT
- SQLite

---

## Авторы

- **[Иван Кузнецов](https://github.com/KuznetcovIvan)** — регистрация, аутентификация, управление пользователями.
- **[Анастасия Харькова](https://github.com/AVKharkova)** — категории, жанры, произведения, импорт данных.
- **[Данила Агапов](https://github.com/Dan3278)** — отзывы, комментарии, рейтинг.
