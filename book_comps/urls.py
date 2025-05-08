from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("search_books/", views.search_books, name="search_books")
]