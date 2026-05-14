from django.urls import path
from . import views

urlpatterns = [
    path('set-language/', views.set_language_api, name='set_language'),
    path('posts/<str:slug>/view/', views.increment_view, name='increment_view'),
]
