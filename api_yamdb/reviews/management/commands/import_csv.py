import csv
import os
from django.core.management.base import BaseCommand
from django.conf import settings

from users.models import MyUser
from reviews.models import Category, Genre, Title, Review, Comment

DATA_PATH = os.path.join(settings.BASE_DIR, 'static', 'data')


class Command(BaseCommand):
    help = 'Импорт данных из CSV файлов'

    def add_arguments(self, parser):
        parser.add_argument('--path', type=str, default=DATA_PATH)

    def handle(self, *args, **options):
        path = options['path']
        self.stdout.write(f'Импорт данных из {path}')

        # Универсальная функция
        def import_data(model, file_name, fields):
            file_path = os.path.join(path, file_name)
            if not os.path.exists(file_path):
                self.stdout.write(self.style.WARNING(f'Файл {file_name} не найден'))
                return
            try:
                with open(file_path, encoding='utf-8') as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        defaults = {key: row[key] for key in fields if key in row}
                        try:
                            model.objects.get_or_create(**defaults)
                        except Exception as e:
                            self.stdout.write(self.style.WARNING(
                                f'Ошибка при импорте записи из {file_name}: {e}'
                            ))
                self.stdout.write(self.style.SUCCESS(f'{model.__name__} импортированы'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Ошибка при чтении файла {file_name}: {e}'))

        # Импорт пользователей, категорий и жанров
        import_data(MyUser, 'users.csv', ['username', 'email', 'role', 'bio', 'first_name', 'last_name'])
        import_data(Category, 'category.csv', ['name', 'slug'])
        import_data(Genre, 'genre.csv', ['name', 'slug'])

        # Импорт произведений (titles.csv)
        titles_file = os.path.join(path, 'titles.csv')
        if not os.path.exists(titles_file):
            self.stdout.write(self.style.WARNING('Файл titles.csv не найден'))
        else:
            try:
                with open(titles_file, encoding='utf-8') as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        try:
                            category = Category.objects.get(slug=row['category'])
                        except Category.DoesNotExist:
                            self.stdout.write(self.style.WARNING(
                                f'Категория с slug "{row["category"]}" не найдена. Пропускаем запись.'
                            ))
                            continue
                        try:
                            Title.objects.get_or_create(
                                name=row['name'],
                                year=row['year'],
                                defaults={'description': row.get('description', ''), 'category': category}
                            )
                        except Exception as e:
                            self.stdout.write(self.style.WARNING(
                                f'Ошибка при импорте произведения "{row.get("name")}": {e}'
                            ))
                    self.stdout.write(self.style.SUCCESS('Произведения импортированы'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Ошибка при чтении файла titles.csv: {e}'))

        # Импорт связей произведений и жанров (genre_title.csv)
        genre_title_file = os.path.join(path, 'genre_title.csv')
        if not os.path.exists(genre_title_file):
            self.stdout.write(self.style.WARNING('Файл genre_title.csv не найден'))
        else:
            try:
                with open(genre_title_file, encoding='utf-8') as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        try:
                            title = Title.objects.get(pk=row['title_id'])
                            genre = Genre.objects.get(pk=row['genre_id'])
                            title.genre.add(genre)
                        except Exception as e:
                            self.stdout.write(self.style.WARNING(
                                f'Ошибка при связывании title_id={row.get("title_id")} с genre_id={row.get("genre_id")}: {e}'
                            ))
                    self.stdout.write(self.style.SUCCESS('Связи произведений и жанров импортированы'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Ошибка при чтении файла genre_title.csv: {e}'))

        # Импорт отзывов (review.csv)
        review_file = os.path.join(path, 'review.csv')
        if not os.path.exists(review_file):
            self.stdout.write(self.style.WARNING('Файл review.csv не найден'))
        else:
            try:
                with open(review_file, encoding='utf-8') as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        try:
                            title = Title.objects.get(pk=row['title'])
                            user = MyUser.objects.get(username=row['author'])
                            Review.objects.get_or_create(
                                title=title,
                                author=user,
                                defaults={
                                    'text': row['text'],
                                    'score': row['score'],
                                    'pub_date': row.get('pub_date')
                                }
                            )
                        except Exception as e:
                            self.stdout.write(self.style.WARNING(
                                f'Ошибка при импорте отзыва для title_id={row.get("title")} автором {row.get("author")}: {e}'
                            ))
                    self.stdout.write(self.style.SUCCESS('Отзывы импортированы'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Ошибка при чтении файла review.csv: {e}'))

        # Импорт комментариев (comments.csv)
        comments_file = os.path.join(path, 'comments.csv')
        if not os.path.exists(comments_file):
            self.stdout.write(self.style.WARNING('Файл comments.csv не найден'))
        else:
            try:
                with open(comments_file, encoding='utf-8') as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        try:
                            review = Review.objects.get(pk=row['review'])
                            user = MyUser.objects.get(username=row['author'])
                            Comment.objects.get_or_create(
                                review=review,
                                author=user,
                                defaults={
                                    'text': row['text'],
                                    'pub_date': row.get('pub_date')
                                }
                            )
                        except Exception as e:
                            self.stdout.write(self.style.WARNING(
                                f'Ошибка при импорте комментария для review_id={row.get("review")} автором {row.get("author")}: {e}'
                            ))
                    self.stdout.write(self.style.SUCCESS('Комментарии импортированы'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Ошибка при чтении файла comments.csv: {e}'))

        self.stdout.write(self.style.SUCCESS('Импорт данных завершен'))
