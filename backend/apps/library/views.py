import re
import unicodedata
from datetime import datetime, timezone

from mongoengine.errors import DoesNotExist
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.common.permissions import IsAuthorOrAdmin

from .models import Book
from .serializers import BookDetailSerializer, BookListSerializer


def _slugify(text):
    text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('ascii')
    text = re.sub(r'[^\w\s-]', '', text.lower())
    return re.sub(r'[-\s]+', '-', text).strip('-')


# ── Public ─────────────────────────────────────────────────────────────────

class BookListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        qs = Book.objects(is_published=True).order_by('order', 'title')
        category = request.query_params.get('category', '').strip()
        language = request.query_params.get('language', '').strip()
        search   = request.query_params.get('q', '').strip()
        if category:
            qs = qs.filter(category=category)
        if language:
            qs = qs.filter(language=language)
        if search:
            qs = qs.filter(title__icontains=search)
        return Response(BookListSerializer(qs, many=True).data)


class BookDetailView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, slug):
        try:
            book = Book.objects.get(slug=slug, is_published=True)
        except DoesNotExist:
            return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)
        return Response(BookDetailSerializer(book).data)


class CategoryListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        cats = Book.objects(is_published=True).distinct('category')
        return Response(sorted(c for c in cats if c))


# ── Admin ──────────────────────────────────────────────────────────────────

class AdminBookListView(APIView):
    permission_classes = [IsAuthorOrAdmin]

    def get(self, request):
        books = Book.objects.order_by('order', 'title')
        return Response(BookListSerializer(books, many=True).data)

    def post(self, request):
        d = request.data
        title = (d.get('title') or '').strip()
        if not title:
            return Response({'detail': 'title is required.'}, status=status.HTTP_400_BAD_REQUEST)

        slug = _slugify(title)
        base, n = slug, 1
        while Book.objects(slug=slug).count():
            slug = f'{base}-{n}'
            n += 1

        book = Book(
            title=title,
            slug=slug,
            author=d.get('author', ''),
            description=d.get('description', ''),
            category=d.get('category', ''),
            language=d.get('language', 'en'),
            cover_key=d.get('cover_key', ''),
            pdf_key=d.get('pdf_key', ''),
            audio_key=d.get('audio_key', ''),
            file_size_mb=float(d.get('file_size_mb', 0)),
            page_count=int(d.get('page_count', 0)),
            tags=d.get('tags', []),
            order=int(d.get('order', 0)),
            is_published=bool(d.get('is_published', False)),
        )
        book.save()
        return Response(BookDetailSerializer(book).data, status=status.HTTP_201_CREATED)


class AdminBookDetailView(APIView):
    permission_classes = [IsAuthorOrAdmin]

    def _get_book(self, slug):
        try:
            return Book.objects.get(slug=slug)
        except DoesNotExist:
            return None

    def patch(self, request, slug):
        book = self._get_book(slug)
        if not book:
            return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)

        updatable = (
            'title', 'author', 'description', 'category', 'language',
            'cover_key', 'pdf_key', 'audio_key', 'file_size_mb',
            'page_count', 'tags', 'order', 'is_published',
        )
        for field in updatable:
            if field in request.data:
                setattr(book, field, request.data[field])

        book.updated_at = datetime.now(timezone.utc)
        book.save()
        return Response(BookDetailSerializer(book).data)

    def delete(self, request, slug):
        book = self._get_book(slug)
        if not book:
            return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)
        book.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
