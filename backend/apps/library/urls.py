from django.urls import path

from .views import (
    AdminBookDetailView,
    AdminBookListView,
    BookDetailView,
    BookListView,
    CategoryListView,
)

urlpatterns = [
    # Public
    path('books/',                   BookListView.as_view(),       name='book-list'),
    path('books/<slug:slug>/',       BookDetailView.as_view(),     name='book-detail'),
    path('categories/',              CategoryListView.as_view(),   name='category-list'),

    # Admin (IsAuthorOrAdmin enforced in each view)
    path('admin/books/',             AdminBookListView.as_view(),  name='admin-book-list'),
    path('admin/books/<slug:slug>/', AdminBookDetailView.as_view(), name='admin-book-detail'),
]
