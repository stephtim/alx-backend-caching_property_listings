from django.core.cache import cache
from .models import Property


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
