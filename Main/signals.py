from django.conf import settings
from django.core.cache import cache
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from Main.models import InfAboutCafe, Address


@receiver(post_delete, sender=InfAboutCafe)
def invalidate_cache_on_delete(sender, instance, **kwargs):
    cache.delete(settings.MAIN_INFORMATION_CACHE_NAME)


@receiver(post_save, sender=InfAboutCafe)
def invalidate_cache_on_save(sender, instance, **kwargs):
    cache.delete(settings.MAIN_INFORMATION_CACHE_NAME)


@receiver(post_save, sender=Address)
def invalidate_cache_on_save(sender, instance, **kwargs):
    cache.delete(settings.MAIN_INFORMATION_CACHE_NAME)
