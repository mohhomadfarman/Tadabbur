"""Anonymous response caching for public read endpoints.

Public GET responses are identical for every logged-out visitor, so they're
cached in Redis and served without touching MongoDB. Logged-in responses are
NEVER cached or served from cache — track audience restrictions and feature
cohorts personalize them per user (`is_visible_to()` etc.), and leaking one
user's view of the catalog to another would be a data exposure.

Invalidation is generation-based: every key embeds a content-generation
counter, and `bump_content_generation()` (called from config/rebuild.py on
every Track/Subject/Lesson/Book save/delete) orphans all existing keys at
once. Orphans simply expire via TTL — no key scanning needed, which Django's
built-in Redis backend doesn't support anyway. The TTL also bounds staleness
for content that doesn't bump the counter (e.g. Category edits).
"""
from functools import wraps

from django.core.cache import cache
from rest_framework.response import Response

_GENERATION_KEY = 'content-gen'


def content_generation():
    return cache.get(_GENERATION_KEY, 0)


def bump_content_generation():
    try:
        cache.incr(_GENERATION_KEY)
    except ValueError:  # key doesn't exist yet
        cache.set(_GENERATION_KEY, 1, None)


def cache_anonymous_get(timeout=180):
    """Decorator for `APIView.get` methods on public (AllowAny) endpoints.

    Caches only unauthenticated 200 responses, keyed by full path + query
    string + content generation. Requests carrying an Authorization header
    bypass the cache entirely, in both directions. Adds an `X-Cache`
    (HIT/MISS) header to cacheable responses for observability.
    """
    def decorator(get_method):
        @wraps(get_method)
        def wrapper(self, request, *args, **kwargs):
            if request.method != 'GET' or request.META.get('HTTP_AUTHORIZATION'):
                return get_method(self, request, *args, **kwargs)

            key = f'anon:{content_generation()}:{request.get_full_path()}'
            cached = cache.get(key)
            if cached is not None:
                response = Response(cached)
                response['X-Cache'] = 'HIT'
                return response

            response = get_method(self, request, *args, **kwargs)
            if response.status_code == 200:
                cache.set(key, response.data, timeout)
            response['X-Cache'] = 'MISS'
            return response
        return wrapper
    return decorator
