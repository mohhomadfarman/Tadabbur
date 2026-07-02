import pytest
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.test import APIRequestFactory
from rest_framework.views import APIView

from .cache import bump_content_generation, cache_anonymous_get


class _ProbeView(APIView):
    """Minimal endpoint so the decorator can be exercised without Mongo."""
    authentication_classes = []
    permission_classes = [AllowAny]
    calls = 0
    status_to_return = 200

    @cache_anonymous_get(timeout=60)
    def get(self, request):
        _ProbeView.calls += 1
        return Response({'call': _ProbeView.calls}, status=_ProbeView.status_to_return)


@pytest.fixture
def probe():
    _ProbeView.calls = 0
    _ProbeView.status_to_return = 200
    factory = APIRequestFactory()
    view = _ProbeView.as_view()

    def hit(**extra):
        return view(factory.get('/probe/', **extra))

    return hit


class TestCacheAnonymousGet:

    def test_second_anonymous_get_is_served_from_cache(self, probe):
        first = probe()
        second = probe()
        assert first['X-Cache'] == 'MISS'
        assert second['X-Cache'] == 'HIT'
        assert second.data == first.data
        assert _ProbeView.calls == 1  # view body ran only once

    def test_authorization_header_bypasses_cache_both_ways(self, probe):
        probe()  # prime the anonymous cache
        authed = probe(HTTP_AUTHORIZATION='Bearer whatever')
        # Bypassed: the view ran again and no cache header was attached.
        assert _ProbeView.calls == 2
        assert not authed.has_header('X-Cache')
        # And the authenticated response was not written into the anon cache.
        assert probe()['X-Cache'] == 'HIT'
        assert probe().data == {'call': 1}

    def test_bump_content_generation_invalidates(self, probe):
        probe()
        assert probe()['X-Cache'] == 'HIT'
        bump_content_generation()
        refreshed = probe()
        assert refreshed['X-Cache'] == 'MISS'
        assert refreshed.data == {'call': 2}

    def test_non_200_responses_are_not_cached(self, probe):
        _ProbeView.status_to_return = 404
        assert probe()['X-Cache'] == 'MISS'
        assert probe()['X-Cache'] == 'MISS'
        assert _ProbeView.calls == 2


@pytest.mark.django_db
class TestSitemapCache:

    def test_sitemap_served_from_cache_on_second_hit(self, client):
        first = client.get('/sitemap.xml')
        second = client.get('/sitemap.xml')
        assert first.status_code == 200
        assert first['X-Cache'] == 'MISS'
        assert second['X-Cache'] == 'HIT'
        assert second.content == first.content

    def test_content_change_refreshes_sitemap(self, client):
        client.get('/sitemap.xml')
        bump_content_generation()
        assert client.get('/sitemap.xml')['X-Cache'] == 'MISS'
