from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache
from .models import Property
import logging

logger = logging.getLogger(__name__)

@receiver(post_save, sender=Property)
def invalidate_property_cache_on_save(sender, instance, created, **kwargs):
    """
    Invalidates the 'all_properties' cache key after a Property object is saved (created or updated).
    """
    cache_key = 'all_properties'
    if cache.delete(cache_key):
        if created:
            logger.info(f"Cache invalidated: '{cache_key}' due to new property '{instance.title}' being created.")
        else:
            logger.info(f"Cache invalidated: '{cache_key}' due to property '{instance.title}' being updated.")
    else:
        logger.info(f"Cache key '{cache_key}' not found or already invalidated on save for property '{instance.title}'.")


@receiver(post_delete, sender=Property)
def invalidate_property_cache_on_delete(sender, instance, **kwargs):
    """
    Invalidates the 'all_properties' cache key after a Property object is deleted.
    """
    cache_key = 'all_properties'
    if cache.delete(cache_key):
        logger.info(f"Cache invalidated: '{cache_key}' due to property '{instance.title}' being deleted.")
    else:
        logger.info(f"Cache key '{cache_key}' not found or already invalidated on delete for property '{instance.title}'.")