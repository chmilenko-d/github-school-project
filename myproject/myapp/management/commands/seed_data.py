"""
Management command: заполнение БД тестовыми данными для школьного сайта.

Данные читаются из seed_data.json (рядом с этим файлом).
Чтобы адаптировать под свою школу — просто отредактируй seed_data.json.

Запуск:
    python manage.py seed_data           # создать данные
    python manage.py seed_data --clear   # очистить и создать заново
"""
import json
from pathlib import Path
from datetime import timedelta

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone

from myapp.models import (
    Profile, Tag, Post, Section, Description, TranslationKey,
    Teacher, StaticPage, DocumentCategory, Document,
    ContactInfo, Announcement, GalleryAlbum, GalleryPhoto, MenuItem,
)

DATA_FILE = Path(__file__).parent / 'seed_data.json'


class Command(BaseCommand):
    help = 'Заполняет БД данными из seed_data.json'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear', action='store_true',
            help='Удалить все существующие данные перед заполнением',
        )
        parser.add_argument(
            '--file', type=str, default=None,
            help='Путь к JSON-файлу с данными (по умолчанию seed_data.json)',
        )

    def handle(self, *args, **options):
        json_path = Path(options['file']) if options['file'] else DATA_FILE
        if not json_path.exists():
            self.stderr.write(self.style.ERROR(f'Файл не найден: {json_path}'))
            return

        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        if options['clear']:
            self.stdout.write('Очистка данных...')
            self._clear_data()

        self.stdout.write(f'Загрузка данных из {json_path.name}...')

        now = timezone.now()
        user, profile = self._create_user()
        tags = self._create_tags(data.get('tags', []))
        self._create_contact_info(data.get('contact_info', {}))
        self._create_sections(data.get('sections', []), profile, tags, now)
        self._create_posts(data.get('posts', []), profile, tags, now)
        self._create_descriptions(data.get('descriptions', []), profile, now)
        self._create_teachers(data.get('teachers', []))
        categories = self._create_document_categories(data.get('document_categories', []))
        self._create_documents(data.get('documents', []), categories, now)
        self._create_static_pages(data.get('static_pages', []))
        self._create_announcements(data.get('announcements', []), now)
        self._create_gallery(data.get('gallery_albums', []))
        self._create_menu_items(data.get('menu_items', []))
        self._create_translation_keys(data.get('translation_keys', {}))

        self.stdout.write(self.style.SUCCESS('✅ Тестовые данные успешно созданы!'))

    # ── Очистка ──

    def _clear_data(self):
        for model in [MenuItem, GalleryPhoto, GalleryAlbum, Announcement,
                       Document, DocumentCategory, StaticPage, Teacher,
                       TranslationKey, Description, Section, Post, Tag,
                       ContactInfo, Profile]:
            model.objects.all().delete()
        User.objects.filter(is_superuser=False).delete()
        self.stdout.write('  Данные очищены.')

    # ── Пользователь ──

    def _create_user(self):
        user, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'first_name': 'Администратор',
                'last_name': '',
                'email': 'admin@school.edu',
                'is_staff': True,
                'is_superuser': True,
            },
        )
        if created:
            user.set_password('admin123')
            user.save()
            self.stdout.write('  Создан пользователь admin / admin123')

        profile, _ = Profile.objects.get_or_create(
            user=user,
            defaults={'bio': 'Администратор сайта', 'website': ''},
        )
        return user, profile

    # ── Теги ──

    def _create_tags(self, tag_names):
        tags = {}
        for name in tag_names:
            tag, _ = Tag.objects.get_or_create(name=name)
            tags[name] = tag
        self.stdout.write(f'  Тегов: {len(tags)}')
        return tags

    # ── Контакты ──

    def _create_contact_info(self, info):
        if not info or ContactInfo.objects.exists():
            self.stdout.write('  ContactInfo уже существует, пропускаю.')
            return
        ContactInfo.objects.create(**info)
        self.stdout.write('  Создана контактная информация.')

    # ── Секции ──

    def _create_sections(self, sections, profile, tags, now):
        for item in sections:
            tag_names = item.pop('tag_names', [])
            section, created = Section.objects.get_or_create(
                slug=item['slug'],
                defaults={**item, 'published': True, 'publish_date': now, 'author': profile},
            )
            if created:
                for tn in tag_names:
                    if tn in tags:
                        section.tags.add(tags[tn])
            item['tag_names'] = tag_names  # restore for potential re-run
        self.stdout.write(f'  Секций: {len(sections)}')

    # ── Посты ──

    def _create_posts(self, posts, profile, tags, now):
        for item in posts:
            tag_names = item.pop('tag_names', [])
            days_ago = item.pop('days_ago', 0)
            post, created = Post.objects.get_or_create(
                slug=item['slug'],
                defaults={
                    **item,
                    'published': True,
                    'publish_date': now - timedelta(days=days_ago),
                    'author': profile,
                },
            )
            if created:
                for tn in tag_names:
                    if tn in tags:
                        post.tags.add(tags[tn])
            item['tag_names'] = tag_names
            item['days_ago'] = days_ago
        self.stdout.write(f'  Постов: {len(posts)}')

    # ── Описания ──

    def _create_descriptions(self, descriptions, profile, now):
        for item in descriptions:
            Description.objects.get_or_create(
                slug=item['slug'],
                defaults={**item, 'published': True, 'publish_date': now, 'author': profile},
            )
        self.stdout.write(f'  Описаний: {len(descriptions)}')

    # ── Учителя ──

    def _create_teachers(self, teachers):
        for item in teachers:
            Teacher.objects.get_or_create(
                slug=item['slug'],
                defaults={**item, 'published': True},
            )
        self.stdout.write(f'  Учителей: {len(teachers)}')

    # ── Категории документов ──

    def _create_document_categories(self, categories):
        cats = {}
        for item in categories:
            cat, _ = DocumentCategory.objects.get_or_create(
                slug=item['slug'], defaults=item,
            )
            cats[item['slug']] = cat
        self.stdout.write(f'  Категорий документов: {len(cats)}')
        return cats

    # ── Документы ──

    def _create_documents(self, documents, categories, now):
        count = 0
        for item in documents:
            cat_slug = item.pop('category_slug', None)
            cat = categories.get(cat_slug)
            if not Document.objects.filter(title=item['title']).exists():
                doc = Document(**item, category=cat, published=True, publish_date=now)
                doc.file = ''
                doc.save()
                count += 1
            item['category_slug'] = cat_slug  # restore
        self.stdout.write(f'  Документов: {count} (⚠️ файлы — через Admin)')

    # ── Статические страницы ──

    def _create_static_pages(self, pages):
        for item in pages:
            StaticPage.objects.get_or_create(
                slug=item['slug'], defaults={**item, 'published': True},
            )
        self.stdout.write(f'  Статических страниц: {len(pages)}')

    # ── Объявления ──

    def _create_announcements(self, announcements, now):
        for item in announcements:
            start_days = item.pop('start_days_ago', 0)
            end_days = item.pop('end_days_ahead', 30)
            Announcement.objects.get_or_create(
                title=item['title'],
                defaults={
                    **item,
                    'start_date': now - timedelta(days=start_days),
                    'end_date': now + timedelta(days=end_days),
                    'published': True,
                },
            )
            item['start_days_ago'] = start_days
            item['end_days_ahead'] = end_days
        self.stdout.write(f'  Объявлений: {len(announcements)}')

    # ── Галерея ──

    def _create_gallery(self, albums):
        for item in albums:
            GalleryAlbum.objects.get_or_create(
                slug=item['slug'], defaults={**item, 'published': True},
            )
        self.stdout.write(f'  Альбомов: {len(albums)} (⚠️ фото — через Admin)')

    # ── Меню ──

    def _create_menu_items(self, items):
        for item in items:
            MenuItem.objects.get_or_create(
                title=item['title'], defaults={**item, 'is_active': True},
            )
        self.stdout.write(f'  Пунктов меню: {len(items)}')

    # ── Переводы ──

    def _create_translation_keys(self, keys):
        for key, values in keys.items():
            if isinstance(values, list) and len(values) == 2:
                value_ru, value_en = values
            else:
                value_ru, value_en = str(values), str(values)
            TranslationKey.objects.get_or_create(
                key=key, defaults={'value': value_ru, 'value_en': value_en},
            )
        self.stdout.write(f'  Ключей переводов: {len(keys)}')
