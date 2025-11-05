from django.core.cache import cache
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Property


@receiver(post_save, sender=Property)
def clear_all_properties_cache_on_save(sender, instance, **kwargs):
    """Clear the 'all_properties' cache key when a Property is saved."""
    cache.delete('all_properties')


@receiver(post_delete, sender=Property)
def clear_all_properties_cache_on_delete(sender, instance, **kwargs):
    """Clear the 'all_properties' cache key when a Property is deleted."""
    cache.delete('all_properties')
