from django.contrib import admin
# MongoEngine models cannot be registered with Django admin directly.
# Use the Django admin panel for Django ORM models only (superuser management).
# Manage MongoEngine documents (User, Track, Lesson, etc.) via the API or the
# Vue.js admin panel built in Phase F.
