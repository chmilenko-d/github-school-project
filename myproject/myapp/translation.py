# my_app/translation.py
from modeltranslation.translator import register, TranslationOptions
from .models import (
    Section, Post, TranslationKey, Description,
    Teacher, StaticPage, DocumentCategory, Document,
    ContactInfo, Announcement, GalleryAlbum, GalleryPhoto, MenuItem,
)


@register(Section)
class SectionTranslationOptions(TranslationOptions):
    fields = ('title', 'subtitle', 'body')


@register(Post)
class PostTranslationOptions(TranslationOptions):
    fields = ('title', 'subtitle', 'small_description', 'body')


@register(TranslationKey)
class TranslationKeyTranslationOptions(TranslationOptions):
    fields = ('value',)


@register(Description)
class DescriptionTranslationOptions(TranslationOptions):
    fields = ('title', 'subtitle', 'body', 'small_description')


# ─────────────────────────────────────────────
# Школьные модели
# ─────────────────────────────────────────────

@register(Teacher)
class TeacherTranslationOptions(TranslationOptions):
    fields = ('full_name', 'position', 'subject', 'bio')


@register(StaticPage)
class StaticPageTranslationOptions(TranslationOptions):
    fields = ('title', 'body')


@register(DocumentCategory)
class DocumentCategoryTranslationOptions(TranslationOptions):
    fields = ('name',)


@register(Document)
class DocumentTranslationOptions(TranslationOptions):
    fields = ('title', 'description')


@register(ContactInfo)
class ContactInfoTranslationOptions(TranslationOptions):
    fields = ('school_name', 'short_name', 'address', 'work_hours')


@register(Announcement)
class AnnouncementTranslationOptions(TranslationOptions):
    fields = ('title', 'body')


@register(GalleryAlbum)
class GalleryAlbumTranslationOptions(TranslationOptions):
    fields = ('title', 'description')


@register(GalleryPhoto)
class GalleryPhotoTranslationOptions(TranslationOptions):
    fields = ('caption',)


@register(MenuItem)
class MenuItemTranslationOptions(TranslationOptions):
    fields = ('title',)

