from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:entry>", views.entry, name="entry"),
    path("random_entry", views.random_entry, name="random_entry"),
    path("search", views.search, name="search"),
    path("new_entry", views.new, name="new"),
    path("save_entry", views.save_entry, name="save_entry"),
    path("wiki/edit/<str:entry>", views.edit_entry, name="edit_entry"),
    path("wiki/edit/save/<str:entry>", views.save_edit_entry, name="save_edit_entry")
]
