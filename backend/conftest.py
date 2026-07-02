import pytest
from django.core.cache import cache


@pytest.fixture(autouse=True)
def _clear_cache():
    """The cache now holds cross-request state — throttle counters
    (apps/users/views.py) and anonymous response caches (apps/common/cache.py).
    Clear it before every test so one test's requests can't throttle or serve
    stale cached responses to another."""
    cache.clear()
    yield
