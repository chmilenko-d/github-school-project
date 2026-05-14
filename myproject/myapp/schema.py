import graphene
from django.contrib.auth import get_user_model
from django.utils import timezone
from graphene_django import DjangoObjectType

from . import models


class UserType(DjangoObjectType):
    class Meta:
        model = get_user_model()


class AuthorType(DjangoObjectType):
    class Meta:
        model = models.Profile


class PostType(DjangoObjectType):
    class Meta:
        model = models.Post
        fields = '__all__'


class TranslationKeyType(DjangoObjectType):
    class Meta:
        model = models.TranslationKey
        fields = '__all__'


class TagType(DjangoObjectType):
    class Meta:
        model = models.Tag


class SectionType(DjangoObjectType):
    class Meta:
        model = models.Section
        fields = '__all__'


class DescriptionType(DjangoObjectType):
    class Meta:
        model = models.Description
        fields = '__all__'


# ─────────────────────────────────────────────
# Школьные типы
# ─────────────────────────────────────────────

class TeacherType(DjangoObjectType):
    class Meta:
        model = models.Teacher
        fields = '__all__'


class StaticPageType(DjangoObjectType):
    class Meta:
        model = models.StaticPage
        fields = '__all__'


class DocumentCategoryType(DjangoObjectType):
    class Meta:
        model = models.DocumentCategory
        fields = '__all__'


class DocumentType(DjangoObjectType):
    class Meta:
        model = models.Document
        fields = '__all__'


class ContactInfoType(DjangoObjectType):
    class Meta:
        model = models.ContactInfo
        fields = '__all__'


class AnnouncementType(DjangoObjectType):
    class Meta:
        model = models.Announcement
        fields = '__all__'


class GalleryAlbumType(DjangoObjectType):
    class Meta:
        model = models.GalleryAlbum
        fields = '__all__'


class GalleryPhotoType(DjangoObjectType):
    class Meta:
        model = models.GalleryPhoto
        fields = '__all__'


class MenuItemType(DjangoObjectType):
    class Meta:
        model = models.MenuItem
        fields = '__all__'


class Query(graphene.ObjectType):
    # Существующие запросы
    all_posts = graphene.List(
        PostType,
        offset=graphene.Int(default_value=0),
        limit=graphene.Int(default_value=5)
    )
    author_by_username = graphene.Field(AuthorType, username=graphene.String())
    post_by_slug = graphene.Field(PostType, slug=graphene.String())
    posts_by_author = graphene.List(PostType, username=graphene.String())
    posts_by_tag = graphene.List(PostType, tag=graphene.String())
    all_sections = graphene.List(SectionType)
    all_descriptions = graphene.List(DescriptionType)
    section_by_slug = graphene.Field(SectionType, slug=graphene.String(required=True))
    description_by_slug = graphene.Field(DescriptionType, slug=graphene.String())
    translation_by_key = graphene.Field(TranslationKeyType, key=graphene.String())
    all_translation_keys = graphene.List(TranslationKeyType)

    # Школьные запросы
    all_teachers = graphene.List(TeacherType)
    teacher_by_slug = graphene.Field(TeacherType, slug=graphene.String(required=True))
    static_page_by_slug = graphene.Field(StaticPageType, slug=graphene.String(required=True))
    all_documents = graphene.List(DocumentType, category=graphene.String())
    all_document_categories = graphene.List(DocumentCategoryType)
    contact_info = graphene.Field(ContactInfoType)
    active_announcements = graphene.List(AnnouncementType)
    all_gallery_albums = graphene.List(GalleryAlbumType)
    gallery_album_by_slug = graphene.Field(GalleryAlbumType, slug=graphene.String(required=True))
    all_menu_items = graphene.List(MenuItemType)

    def resolve_all_posts(root, info, offset, limit):
        return (
            models.Post.objects
            .filter(published=True)
            .select_related('author')
            .prefetch_related('tags')
            .order_by('-publish_date')
            [offset:offset + limit]
        )

    def resolve_author_by_username(root, info, username):
        return models.Profile.objects.select_related("user").get(
            user__username=username
        )

    def resolve_post_by_slug(root, info, slug):
        return (
            models.Post.objects.prefetch_related("tags")
            .select_related("author")
            .get(slug=slug)
        )

    def resolve_posts_by_author(root, info, username):
        return (
            models.Post.objects.prefetch_related("tags")
            .select_related("author")
            .filter(author__user__username=username)
        )

    def resolve_posts_by_tag(root, info, tag):
        return (
            models.Post.objects.prefetch_related("tags")
            .select_related("author")
            .filter(tags__name__iexact=tag)
        )

    def resolve_all_sections(root, info):
        return (
            models.Section.objects.all()
        )

    def resolve_all_descriptions(root, info):
        return (
            models.Description.objects.all()
        )

    def resolve_section_by_slug(self, info, slug):
        return (
            models.Section.objects.prefetch_related("tags")
            .select_related("author")
            .get(slug=slug)
        )

    def resolve_description_by_slug(self, info, slug):
        return (
            models.Description.objects.prefetch_related("tags")
            .select_related("author")
            .get(slug=slug)
        )

    def resolve_all_translation_keys(self, info):
        return (
            models.TranslationKey.objects.all()
        )

    def resolve_translation_by_key(root, info, key):
        return (
            models.TranslationKey.objects
            .get(key=key)
        )

    # ─────────────────────────────────────────────
    # Школьные resolvers
    # ─────────────────────────────────────────────

    def resolve_all_teachers(root, info):
        return models.Teacher.objects.filter(published=True)

    def resolve_teacher_by_slug(root, info, slug):
        return models.Teacher.objects.get(slug=slug, published=True)

    def resolve_static_page_by_slug(root, info, slug):
        return models.StaticPage.objects.get(slug=slug, published=True)

    def resolve_all_documents(root, info, category=None):
        qs = models.Document.objects.filter(published=True).select_related('category')
        if category:
            qs = qs.filter(category__slug=category)
        return qs

    def resolve_all_document_categories(root, info):
        return models.DocumentCategory.objects.all()

    def resolve_contact_info(root, info):
        return models.ContactInfo.objects.first()

    def resolve_active_announcements(root, info):
        now = timezone.now()
        return models.Announcement.objects.filter(
            published=True,
            start_date__lte=now,
            end_date__gte=now,
        )

    def resolve_all_gallery_albums(root, info):
        return models.GalleryAlbum.objects.filter(published=True)

    def resolve_gallery_album_by_slug(root, info, slug):
        return models.GalleryAlbum.objects.prefetch_related('photos').get(
            slug=slug, published=True
        )

    def resolve_all_menu_items(root, info):
        return models.MenuItem.objects.filter(is_active=True).select_related('page', 'parent')


schema = graphene.Schema(query=Query)
