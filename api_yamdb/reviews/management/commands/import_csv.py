import csv
import os

from django.conf import settings
from django.core.management.base import BaseCommand
from django.db.utils import IntegrityError
from reviews.models import Category, Comment, Genre, Review, Title, User

DATA_PATH = os.path.join(settings.BASE_DIR, 'static', 'data')


class Command(BaseCommand):
    help = 'Импорт данных из CSV'

    def add_arguments(self, parser):
        parser.add_argument('--path', type=str, default=DATA_PATH)

    def handle(self, *args, **options):
        path = options['path']
        self.stdout.write(f'Импорт данных из {path}')

        self.import_data(
            User, 'users.csv',
            ['id', 'username', 'email', 'role',
             'bio', 'first_name', 'last_name']
        )
        self.import_data(
            Category, 'category.csv',
            ['id', 'name', 'slug']
        )
        self.import_data(
            Genre, 'genre.csv',
            ['id', 'name', 'slug']
        )
        self.import_data(
            Title, 'titles.csv',
            ['id', 'name', 'year', 'description', 'category'],
            foreign_keys={'category': (Category, 'id')}
        )
        self.import_data(
            Review, 'review.csv',
            ['id', 'title_id', 'text', 'author', 'score', 'pub_date'],
            foreign_keys={'author': (User, 'id'), 'title_id': (Title, 'id')}
        )
        self.import_data(
            Comment, 'comments.csv',
            ['id', 'review_id', 'text', 'author', 'pub_date'],
            foreign_keys={'author': (User, 'id'), 'review_id': (Review, 'id')}
        )
        self.import_genre_title('genre_title.csv')

        self.stdout.write(self.style.SUCCESS('Импорт данных завершен'))

    def open_csv_file(self, file_name):
        file_path = os.path.join(DATA_PATH, file_name)
        if not os.path.exists(file_path):
            self.stdout.write(self.style.WARNING(
                f'Файл {file_name} не найден'))
            return
        try:
            return open(file_path, encoding='utf-8')
        except Exception as e:
            self.stdout.write(self.style.ERROR(
                f'Ошибка при чтении {file_name}: {e}'))
            return

    def process_row(self, row, fields, foreign_keys=None):
        try:
            data = {key: row[key] for key in fields if key in row}
            if foreign_keys:
                for field, (fk_model, fk_field) in foreign_keys.items():
                    fk_value = row[field]
                    fk_object = fk_model.objects.filter(
                        **{fk_field: fk_value}).first()
                    actual_field = (field[:- 3] if field.endswith('_id')
                                    else field)
                    data[actual_field] = fk_object
                    if actual_field != field:
                        data.pop(field, None)
            if 'id' in data:
                data['id'] = int(data['id'])
            if 'score' in data:
                data['score'] = int(data['score'])
            if 'year' in data:
                data['year'] = int(data['year'])
            return data
        except IntegrityError:
            return
        except Exception as e:
            self.stdout.write(self.style.WARNING(f'Ошибка в строке: {e}'))
            return

    def import_data(self, model, file_name, fields, foreign_keys=None):
        file = self.open_csv_file(file_name)
        if file is None:
            return
        with file:
            reader = csv.DictReader(file)
            objects = []
            for row in reader:
                data = self.process_row(row, fields, foreign_keys)
                if data:
                    objects.append(model(**data))
            if objects:
                model.objects.bulk_create(objects, ignore_conflicts=True)
                self.stdout.write(self.style.SUCCESS(
                    f'{model.__name__} импортированы'))

    def import_genre_title(self, file_name):
        file_path = os.path.join(DATA_PATH, file_name)
        if not os.path.exists(file_path):
            self.stdout.write(self.style.WARNING(
                f'Файл {file_name} не найден'))
            return
        try:
            with open(file_path, encoding='utf-8') as f:
                reader = csv.DictReader(f)
                title_genres = []
                for row in reader:
                    try:
                        title = Title.objects.filter(
                            id=row['title_id']).first()
                        genre = Genre.objects.filter(
                            id=row['genre_id']).first()
                        if title and genre:
                            title_genres.append((title, genre))
                    except Exception:
                        continue

            for title, genre in title_genres:
                title.genre.add(genre)

            self.stdout.write(self.style.SUCCESS(
                'Связи произведений и жанров импортированы'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(
                f'Ошибка при чтении {file_name}: {e}'))
