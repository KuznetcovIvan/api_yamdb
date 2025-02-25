import csv
import os

from django.conf import settings
from django.core.management.base import BaseCommand
from django.db.utils import IntegrityError

from reviews.models import Category, Comment, Genre, Review, Title 
from users.models import User

DATA_PATH = os.path.join(settings.BASE_DIR, 'static', 'data')


class Command(BaseCommand):
    help = 'Импорт из CSV файлов'

    def add_arguments(self, parser):
        parser.add_argument('--path', type=str, default=DATA_PATH)

    def handle(self, *args, **options):
        path = options['path']
        self.stdout.write(f'Импорт данных из {path}')

        def import_data(model, file_name, fields, foreign_keys=None, id_field=None):
            """Универсальная функция для импорта данных"""
            file_path = os.path.join(path, file_name)
            if not os.path.exists(file_path):
                self.stdout.write(self.style.WARNING(f'Файл {file_name} не найден'))
                return

            try:
                with open(file_path, encoding='utf-8') as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        try:
                            defaults = {key: row[key] for key in fields if key in row}
                            if foreign_keys:
                                for csv_field, (fk_model, fk_field) in foreign_keys.items():
                                    try:
                                        defaults[csv_field] = fk_model.objects.get(**{fk_field: row[csv_field]})
                                    except fk_model.DoesNotExist:
                                        self.stdout.write(self.style.WARNING(
                                            f'Ошибка: {fk_model.__name__} с {fk_field}={row[csv_field]} не найден.'
                                        ))
                                        continue

                            if id_field:
                                obj, created = model.objects.get_or_create(
                                    id=row[id_field], defaults=defaults
                                )
                            else:
                                obj, created = model.objects.get_or_create(**defaults)

                        except IntegrityError as e:
                            self.stdout.write(self.style.WARNING(
                                f'Ошибка целостности в {file_name}: {e}'
                            ))
                        except Exception as e:
                            self.stdout.write(self.style.WARNING(
                                f'Ошибка при импорте записи из {file_name}: {e}'
                            ))

                self.stdout.write(self.style.SUCCESS(f'{model.__name__} импортированы'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Ошибка при чтении файла {file_name}: {e}'))
        # Импорт пользователей
        import_data(
            User, 'users.csv',
            ['id', 'username', 'email', 'role', 'bio', 'first_name', 'last_name'],
            id_field='id'
        )

        # Импорт категорий и жанров
        import_data(Category, 'category.csv', ['id', 'name', 'slug'], id_field='id')
        import_data(Genre, 'genre.csv', ['id', 'name', 'slug'], id_field='id')

        # Импорт произведений
        import_data(
            Title, 'titles.csv', ['id', 'name', 'year', 'description', 'category'],
            foreign_keys={'category': (Category, 'id')}, id_field='id'
        )

        # Импорт связей произведений и жанров
        genre_title_file = os.path.join(path, 'genre_title.csv')
        if os.path.exists(genre_title_file):
            try:
                with open(genre_title_file, encoding='utf-8') as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        try:
                            title = Title.objects.get(id=row['title_id'])
                            genre = Genre.objects.get(id=row['genre_id'])
                            title.genre.add(genre)
                        except Exception as e:
                            self.stdout.write(self.style.WARNING(
                                f'Ошибка при связывании title_id={row["title_id"]} с genre_id={row["genre_id"]}: {e}'
                            ))
                self.stdout.write(self.style.SUCCESS('Связи произведений и жанров импортированы'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Ошибка при чтении файла genre_title.csv: {e}'))
        else:
            self.stdout.write(self.style.WARNING('Файл genre_title.csv не найден'))
        import_data(
            Review, 'review.csv', ['id', 'text', 'score', 'pub_date', 'author', 'title'],
            foreign_keys={'author': (User, 'id'), 'title': (Title, 'id')}, id_field='id'
        )

        import_data(
            Comment, 'comments.csv', ['id', 'text', 'pub_date', 'author', 'review'],
            foreign_keys={'author': (User, 'id'), 'review': (Review, 'id')}, id_field='id'
        )
        self.stdout.write(self.style.SUCCESS('Импорт завершен'))
