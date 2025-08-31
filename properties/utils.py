# alx-backend-caching_property_listings/properties/utils.py
from django.core.cache import cache
from .models import Property
import logging
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

def get_redis_cache_metrics():
    """
    Retrieves and analyzes Redis cache hit/miss metrics.
    Connects to Redis, gets keyspace_hits and keyspace_misses from INFO,
    calculates hit ratio, logs metrics, and returns a dictionary.
    """
    try:
        # Get the low-level Redis client instance from django_redis
        # The cache.client._client is the actual redis-py client object
        redis_client = cache.get_client(None) # Pass None to get default client
        # If using multiple clients, it might return a list, take the first one
        if isinstance(redis_client, list):
            redis_client = redis_client[0]


        # Get Redis INFO statistics
        info = redis_client.info('Keyspace') # 'Keyspace' section contains hit/miss stats

        keyspace_hits = info.get('keyspace_hits', 0)
        keyspace_misses = info.get('keyspace_misses', 0)

        total_requests = keyspace_hits + keyspace_misses
        hit_ratio = 0.0
        if total_requests > 0:
            hit_ratio = (keyspace_hits / total_requests) * 100

        metrics = {
            'keyspace_hits': keyspace_hits,
            'keyspace_misses': keyspace_misses,
            'total_requests': total_requests,
            'hit_ratio': f"{hit_ratio:.2f}%"
        }

        logger.info(f"Redis Cache Metrics: {json.dumps(metrics)}") # Log metrics
        return metrics

    except Exception as e:
        logger.error(f"Error retrieving Redis cache metrics: {e}")
        return {
            'keyspace_hits': 'N/A',
            'keyspace_misses': 'N/A',
            'total_requests': 'N/A',
            'hit_ratio': 'N/A',
            'error': str(e)
        }