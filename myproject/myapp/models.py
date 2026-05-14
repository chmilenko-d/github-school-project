from django.db import models
from django.conf import settings
from django.utils import timezone
from ckeditor.fields import RichTextField
# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
    )
    website = models.URLField(blank=True)
    bio = models.CharField(max_length=240, blank=True)

    def __str__(self):
        return self.user.get_username()


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=255, unique=True)
    subtitle = models.CharField(max_length=255, blank=True)
    slug = models.SlugField(max_length=255, unique=True)
    small_description = RichTextField(blank=True, null=True)
    body = RichTextField()
    meta_description = models.CharField(max_length=150, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    publish_date = models.DateTimeField(blank=True, null=True)
    published = models.BooleanField(default=False)

    author = models.ForeignKey(Profile, on_delete=models.PROTECT)
    tags = models.ManyToManyField(Tag, blank=True)
    image = models.ImageField(upload_to='post_images/', blank=True, null=True)
    views = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["-publish_date"]


class Section(models.Model):
    title = models.CharField(max_length=255, unique=True)
    subtitle = models.CharField(max_length=255, blank=True)
    slug = models.SlugField(max_length=255, unique=True)
    link = models.CharField(max_length=255, blank=True, null=True)
    body = models.TextField()
    meta_description = models.CharField(max_length=150, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    publish_date = models.DateTimeField(blank=True, null=True)
    published = models.BooleanField(default=False)

    author = models.ForeignKey(Profile, on_delete=models.PROTECT)
    tags = models.ManyToManyField(Tag, blank=True)
    image = models.ImageField(upload_to='section_images/', blank=True, null=True)
    background_image = models.ImageField(upload_to='section_images/', blank=True, null=True)
    custom_css_class = models.CharField(max_length=255, unique=True, blank=True, null=True)

    number = models.PositiveIntegerField(default=0, help_text="Порядок отображения")

    class Meta:
        ordering = ['number']


class Description(models.Model):
    title = models.CharField(max_length=255, unique=True)
    subtitle = models.CharField(max_length=255, blank=True)
    slug = models.SlugField(max_length=255, unique=True)
    small_description = models.CharField(max_length=255, blank=True)
    body = RichTextField()
    meta_description = models.CharField(max_length=150, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    publish_date = models.DateTimeField(blank=True, null=True)
    published = models.BooleanField(default=False)

    author = models.ForeignKey(Profile, on_delete=models.PROTECT)
    tags = models.ManyToManyField(Tag, blank=True)
    image = models.ImageField(upload_to='description_images/', blank=True, null=True)
    background_image = models.ImageField(upload_to='description_images/', blank=True, null=True)
    custom_css_class = models.CharField(max_length=255, unique=True, blank=True, null=True)

    number = models.PositiveIntegerField(default=0, help_text="Порядок отображения")

    class Meta:
        ordering = ['number']


class TranslationKey(models.Model):
    key = models.CharField(max_length=100, unique=True, help_text="'button.read_more', 'title.home'")

    value = models.TextField(blank=True)

    def __str__(self):
        return self.key


# ─────────────────────────────────────────────
# Школьные модели
# ─────────────────────────────────────────────

class Teacher(models.Model):
    full_name = models.CharField(max_length=255, verbose_name="ФИО")
    slug = models.SlugField(max_length=255, unique=True)
    position = models.CharField(max_length=255, blank=True, verbose_name="Должность")
    subject = models.CharField(max_length=255, blank=True, verbose_name="Предмет")
    education = models.CharField(max_length=500, blank=True, verbose_name="Образование")
    qualification = models.CharField(max_length=255, blank=True, verbose_name="Квалификация/категория")
    experience_years = models.PositiveIntegerField(default=0, verbose_name="Стаж (лет)")
    bio = RichTextField(blank=True, verbose_name="Биография")
    photo = models.ImageField(upload_to='teacher_photos/', blank=True, null=True, verbose_name="Фото")
    email = models.EmailField(blank=True, verbose_name="Email")
    number = models.PositiveIntegerField(default=0, help_text="Порядок отображения")
    published = models.BooleanField(default=False, verbose_name="Опубликован")

    class Meta:
        ordering = ['number']
        verbose_name = "Педагог"
        verbose_name_plural = "Педагоги"

    def __str__(self):
        return self.full_name


class StaticPage(models.Model):
    title = models.CharField(max_length=255, verbose_name="Заголовок")
    slug = models.SlugField(max_length=255, unique=True)
    body = RichTextField(verbose_name="Содержание")
    meta_description = models.CharField(max_length=150, blank=True, verbose_name="SEO описание")
    parent = models.ForeignKey(
        'self', on_delete=models.SET_NULL, null=True, blank=True,
        related_name='children', verbose_name="Родительская страница"
    )
    number = models.PositiveIntegerField(default=0, help_text="Порядок отображения")
    published = models.BooleanField(default=False, verbose_name="Опубликована")
    date_modified = models.DateTimeField(auto_now=True, verbose_name="Дата изменения")

    class Meta:
        ordering = ['number']
        verbose_name = "Статическая страница"
        verbose_name_plural = "Статические страницы"

    def __str__(self):
        return self.title


class DocumentCategory(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название")
    slug = models.SlugField(max_length=255, unique=True)
    number = models.PositiveIntegerField(default=0, help_text="Порядок отображения")

    class Meta:
        ordering = ['number']
        verbose_name = "Категория документов"
        verbose_name_plural = "Категории документов"

    def __str__(self):
        return self.name


class Document(models.Model):
    title = models.CharField(max_length=255, verbose_name="Название")
    category = models.ForeignKey(
        DocumentCategory, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='documents', verbose_name="Категория"
    )
    file = models.FileField(upload_to='documents/', verbose_name="Файл")
    description = models.TextField(blank=True, verbose_name="Описание")
    publish_date = models.DateTimeField(blank=True, null=True, verbose_name="Дата публикации")
    published = models.BooleanField(default=False, verbose_name="Опубликован")
    number = models.PositiveIntegerField(default=0, help_text="Порядок отображения")

    class Meta:
        ordering = ['number']
        verbose_name = "Документ"
        verbose_name_plural = "Документы"

    def __str__(self):
        return self.title


class ContactInfo(models.Model):
    school_name = models.CharField(max_length=500, verbose_name="Полное название школы")
    short_name = models.CharField(max_length=255, blank=True, verbose_name="Сокращённое название")
    address = models.TextField(blank=True, verbose_name="Адрес")
    phone = models.CharField(max_length=50, blank=True, verbose_name="Телефон")
    email = models.EmailField(blank=True, verbose_name="Email")
    director_name = models.CharField(max_length=255, blank=True, verbose_name="ФИО директора")
    work_hours = models.CharField(max_length=255, blank=True, verbose_name="Режим работы")
    map_embed_url = models.URLField(blank=True, verbose_name="URL для iframe карты")
    telegram_url = models.URLField(blank=True, verbose_name="Telegram")
    vk_url = models.URLField(blank=True, verbose_name="ВКонтакте")
    logo = models.ImageField(upload_to='school/', blank=True, null=True, verbose_name="Логотип")
    hero_image = models.ImageField(upload_to='school/', blank=True, null=True, verbose_name="Фото школы")

    class Meta:
        verbose_name = "Контактная информация"
        verbose_name_plural = "Контактная информация"

    def __str__(self):
        return self.short_name or self.school_name

    def save(self, *args, **kwargs):
        # Singleton: разрешаем только одну запись
        if not self.pk and ContactInfo.objects.exists():
            raise ValueError("Можно создать только одну запись контактной информации.")
        super().save(*args, **kwargs)


class Announcement(models.Model):
    class Priority(models.TextChoices):
        NORMAL = 'normal', 'Обычное'
        IMPORTANT = 'important', 'Важное'
        URGENT = 'urgent', 'Срочное'

    title = models.CharField(max_length=255, verbose_name="Заголовок")
    body = RichTextField(verbose_name="Текст")
    priority = models.CharField(
        max_length=10, choices=Priority.choices,
        default=Priority.NORMAL, verbose_name="Приоритет"
    )
    start_date = models.DateTimeField(verbose_name="Дата начала показа")
    end_date = models.DateTimeField(verbose_name="Дата окончания показа")
    published = models.BooleanField(default=False, verbose_name="Опубликовано")

    class Meta:
        ordering = ['-priority', '-start_date']
        verbose_name = "Объявление"
        verbose_name_plural = "Объявления"

    def __str__(self):
        return self.title

    @property
    def is_active(self):
        now = timezone.now()
        return self.published and self.start_date <= now <= self.end_date


class GalleryAlbum(models.Model):
    title = models.CharField(max_length=255, verbose_name="Название")
    slug = models.SlugField(max_length=255, unique=True)
    description = models.TextField(blank=True, verbose_name="Описание")
    cover_image = models.ImageField(upload_to='gallery/', blank=True, null=True, verbose_name="Обложка")
    date = models.DateField(blank=True, null=True, verbose_name="Дата события")
    published = models.BooleanField(default=False, verbose_name="Опубликован")
    number = models.PositiveIntegerField(default=0, help_text="Порядок отображения")

    class Meta:
        ordering = ['number']
        verbose_name = "Фотоальбом"
        verbose_name_plural = "Фотоальбомы"

    def __str__(self):
        return self.title


class GalleryPhoto(models.Model):
    album = models.ForeignKey(
        GalleryAlbum, on_delete=models.CASCADE,
        related_name='photos', verbose_name="Альбом"
    )
    image = models.ImageField(upload_to='gallery/', verbose_name="Фото")
    caption = models.CharField(max_length=255, blank=True, verbose_name="Подпись")
    number = models.PositiveIntegerField(default=0, help_text="Порядок отображения")

    class Meta:
        ordering = ['number']
        verbose_name = "Фотография"
        verbose_name_plural = "Фотографии"

    def __str__(self):
        return self.caption or f"Фото #{self.pk}"


class MenuItem(models.Model):
    title = models.CharField(max_length=255, verbose_name="Текст пункта")
    url = models.CharField(max_length=500, blank=True, verbose_name="Внешняя ссылка")
    page = models.ForeignKey(
        StaticPage, on_delete=models.SET_NULL, null=True, blank=True,
        verbose_name="Статическая страница"
    )
    parent = models.ForeignKey(
        'self', on_delete=models.CASCADE, null=True, blank=True,
        related_name='children', verbose_name="Родительский пункт"
    )
    number = models.PositiveIntegerField(default=0, help_text="Порядок отображения")
    is_active = models.BooleanField(default=True, verbose_name="Активен")

    class Meta:
        ordering = ['number']
        verbose_name = "Пункт меню"
        verbose_name_plural = "Пункты меню"

    def __str__(self):
        return self.title