## Проект API для YaMDb

Проект API для YaMDb в рамках обучения в Яндекс Практикуме - это реализация REST API для платформы YaMDb, которая позволяет пользователям взаимодействовать с произведениями (фильмами, книгами, песнями) посредством создания отзывов и комментариев, выставления оценок, а также управления категориями и жанрами.

### Информация о стеке технологий, которые использовались для реализации проекта

- Python 3.9
- Django
- Django REST Framework
- Библиотеки для работы с JWT

### Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/KuznetcovIvan/api_yamdb/tree/develop
```

```
cd api_yamdb
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv env
```

```
source env/bin/activate
```

Установить зависимости из файла requirements.txt:

```
python3 -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

Выполнить миграции:

```
python3 manage.py migrate
```

Запустить проект:

```
python3 manage.py runserver
```

### Спецификация API

После запуска проекта спецификация API доступна по адресу:
```
http://127.0.0.1:8000/redoc/
```

### Авторы
[Ivan Kuznetcov](https://github.com/KuznetcovIvan)
[Anastasiya Kharkova](https://github.com/AVKharkova)