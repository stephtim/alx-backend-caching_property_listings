import logging
from django.core.cache import cache
from django_redis import get_redis_connection
from .models import Property

logger = logging.getLogger(__name__)


def get_all_properties():
    """Return all properties, using Redis cache key 'all_properties'.

    The function first attempts to read the value from the cache. If the
    value is missing, it fetches the queryset from the database, evaluates
    it into a list to make it safe to cache, stores it in the cache for
    3600 seconds (1 hour) and returns the list.
    """
    cached = cache.get('all_properties')
    if cached is not None:
        return cached

    qs = list(Property.objects.all().order_by('-created_at'))
    cache.set('all_properties', qs, 3600)
    return qs


def get_redis_cache_metrics():
    """Return Redis cache metrics (keyspace_hits, keyspace_misses, hit_rate).

    Attempts to connect to the redis instance used by Django cache backend
    (django-redis). On success returns a dict with integers for
    'keyspace_hits' and 'keyspace_misses' and a float 'hit_rate' computed as
    hits/(hits+misses) or 0 when there are no requests.

    On error returns None and logs the exception via logger.error.
    """
    try:
        conn = get_redis_connection('default')
        info = conn.info()
        hits = int(info.get('keyspace_hits', 0))
        misses = int(info.get('keyspace_misses', 0))
        total_requests = hits + misses
        hit_rate = (hits / total_requests) if total_requests > 0 else 0
        return {
            'keyspace_hits': hits,
            'keyspace_misses': misses,
            'hit_rate': hit_rate,
        }
    except Exception as e:
        logger.error('Failed to get redis metrics: %s', e)
        return None
