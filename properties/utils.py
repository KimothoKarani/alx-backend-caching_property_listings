from django.core.cache import cache
from .models import Property
import logging

logger = logging.getLogger(__name__)

def get_all_properties():
    """
    Retrieves all Property objects, caching the queryset in Redis for 1 hour.
    """
    cache_key = 'all_properties'
    properties = cache.get(cache_key)

    if properties is None:
        logger.info("Cache miss for 'all_properties'. Fetching from database.")
        properties = Property.objects.all()
        # Cache for 1 hour (3600 seconds)
        cache.set(cache_key, properties, 3600)
        logger.info("Queryset 'all_properties' stored in cache.")
    else:
        logger.info("Cache hit for 'all_properties'. Serving from cache.")

    return properties