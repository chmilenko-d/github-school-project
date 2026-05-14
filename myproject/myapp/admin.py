from django.contrib import admin
from .models import (
    Post, Profile, Tag, Section, TranslationKey, Description,
    Teacher, StaticPage, DocumentCategory, Document,
    ContactInfo, Announcement, GalleryAlbum, GalleryPhoto, MenuItem,
)
from modeltranslation.admin import TranslationAdmin


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    model = Profile


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    model = Tag


@admin.register(Section)
class SectionAdmin(TranslationAdmin):
    model = Section

    list_display = (
        "id",
        "number",
        "title",
        "subtitle",
        "slug",
        "link",
        "publish_date",
        "published",
        "image",
        "background_image",
        "custom_css_class",
    )
    list_filter = (
        "published",
        "publish_date",
    )
    list_editable = (
        "number",
        "title",
        "subtitle",
        "slug",
        "link",
        "publish_date",
        "published",
        "image",
        "background_image",
        "custom_css_class",
    )
    search_fields = (
        "title",
        "subtitle",
        "slug",
        "body",
    )
    prepopulated_fields = {
        "slug": (
            "title",
            "subtitle",
        )
    }
    date_hierarchy = "publish_date"
    save_on_top = True


@admin.register(Description)
class DescriptionAdmin(TranslationAdmin):
    model = Description

    list_display = (
        "id",
        "number",
        "title",
        "small_description",
        "subtitle",
        "slug",
        "publish_date",
        "published",
        "image",
        "background_image",
        "custom_css_class",
    )
    list_filter = (
        "published",
        "publish_date",
    )
    list_editable = (
        "number",
        "title",
        "small_description",
        "subtitle",
        "slug",
        "publish_date",
        "published",
        "image",
        "background_image",
        "custom_css_class",
    )
    search_fields = (
        "title",
        "subtitle",
        "slug",
        "body",
    )
    prepopulated_fields = {
        "slug": (
            "title",
            "subtitle",
        )
    }
    date_hierarchy = "publish_date"
    save_on_top = True


@admin.register(Post)
class PostAdmin(TranslationAdmin):
    model = Post

    list_display = (
        "id",
        "title",
        "subtitle",
        "slug",
        "small_description",
        "publish_date",
        "published",
        "image",
    )
    list_filter = (
        "published",
        "publish_date",
    )
    list_editable = (
        "title",
        "subtitle",
        "slug",
        "publish_date",
        "published",
        "image",
    )
    search_fields = (
        "title",
        "subtitle",
        "slug",
        "body",
    )
    prepopulated_fields = {
        "slug": (
            "title",
            "subtitle",
        )
    }
    date_hierarchy = "publish_date"
    save_on_top = True

    # class Media:
    #     css = {
    #         'all': ('css/admin_custom.css',)
    #     }


@admin.register(TranslationKey)
class TranslationKeyAdmin(TranslationAdmin):
    list_display = (
        'key',
        'value',
    )
    list_editable = (
        'value',
    )
    search_fields = ['key']


# ─────────────────────────────────────────────
# Школьные модели
# ─────────────────────────────────────────────

@admin.register(Teacher)
class TeacherAdmin(TranslationAdmin):
    list_display = ('id', 'number', 'full_name', 'position', 'subject', 'published')
    list_editable = ('number', 'full_name', 'position', 'subject', 'published')
    list_filter = ('published', 'position')
    search_fields = ('full_name', 'position', 'subject')
    prepopulated_fields = {'slug': ('full_name',)}
    save_on_top = True


@admin.register(StaticPage)
class StaticPageAdmin(TranslationAdmin):
    list_display = ('id', 'number', 'title', 'slug', 'parent', 'published', 'date_modified')
    list_editable = ('number', 'title', 'slug', 'published')
    list_filter = ('published', 'parent')
    search_fields = ('title', 'body')
    prepopulated_fields = {'slug': ('title',)}
    save_on_top = True


@admin.register(DocumentCategory)
class DocumentCategoryAdmin(TranslationAdmin):
    list_display = ('id', 'number', 'name', 'slug')
    list_editable = ('number', 'name', 'slug')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Document)
class DocumentAdmin(TranslationAdmin):
    list_display = ('id', 'number', 'title', 'category', 'file', 'publish_date', 'published')
    list_editable = ('number', 'title', 'published')
    list_filter = ('published', 'category')
    search_fields = ('title', 'description')
    save_on_top = True


@admin.register(ContactInfo)
class ContactInfoAdmin(TranslationAdmin):
    list_display = ('school_name', 'phone', 'email')

    def has_add_permission(self, request):
        # Singleton: запретить создание если запись уже есть
        if ContactInfo.objects.exists():
            return False
        return super().has_add_permission(request)


@admin.register(Announcement)
class AnnouncementAdmin(TranslationAdmin):
    list_display = ('id', 'title', 'priority', 'start_date', 'end_date', 'published')
    list_editable = ('title', 'priority', 'published')
    list_filter = ('published', 'priority')
    search_fields = ('title', 'body')
    save_on_top = True


class GalleryPhotoInline(admin.TabularInline):
    model = GalleryPhoto
    extra = 1
    fields = ('number', 'image', 'caption')


@admin.register(GalleryAlbum)
class GalleryAlbumAdmin(TranslationAdmin):
    list_display = ('id', 'number', 'title', 'slug', 'date', 'published')
    list_editable = ('number', 'title', 'slug', 'published')
    list_filter = ('published',)
    search_fields = ('title', 'description')
    prepopulated_fields = {'slug': ('title',)}
    inlines = [GalleryPhotoInline]
    save_on_top = True


@admin.register(MenuItem)
class MenuItemAdmin(TranslationAdmin):
    list_display = ('id', 'number', 'title', 'url', 'page', 'parent', 'is_active')
    list_editable = ('number', 'title', 'is_active')
    list_filter = ('is_active', 'parent')
    search_fields = ('title',)
    save_on_top = True