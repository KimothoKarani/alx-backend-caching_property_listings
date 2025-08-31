# alx-backend-caching_property_listings/properties/utils.py
from django.core.cache import cache
from .models import Property
import logging
from django_redis import get_redis_connection
import json # Import json for cleaner logging if needed, though dict is fine

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

import logging
from django_redis import get_redis_connection

logger = logging.getLogger(__name__)

def get_redis_cache_metrics():
    """
    Retrieves Redis cache hit/miss statistics and calculates hit ratio.
    """
    try:
        conn = get_redis_connection("default")
        info = conn.info("stats")

        keyspace_hits = info.get("keyspace_hits", 0)
        keyspace_misses = info.get("keyspace_misses", 0)

        total_requests = keyspace_hits + keyspace_misses
        hit_ratio = (keyspace_hits / total_requests) if total_requests > 0 else 0

        metrics = {
            "keyspace_hits": keyspace_hits,
            "keyspace_misses": keyspace_misses,
            "total_requests": total_requests,
            "hit_ratio": round(hit_ratio, 2),
        }

        logger.info(f"Redis Cache Metrics: {metrics}")
        return metrics

    except Exception as e:
        logger.error(f"Error retrieving Redis cache metrics: {e}")
        return {
            "keyspace_hits": "N/A",
            "keyspace_misses": "N/A",
            "total_requests": "N/A",
            "hit_ratio": "N/A",
            "error": str(e),
        }
