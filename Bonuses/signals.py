from django.conf import settings
from django.core.cache import cache
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from Bonuses.models import Coupon, Coin


@receiver(post_delete, sender=Coupon)
def invalidate_cache_on_delete(sender, instance, **kwargs):
    cache.delete(settings.COUPONS_CACHE_NAME)


@receiver(post_save, sender=Coupon)
def invalidate_cache_on_save(sender, instance, **kwargs):
    cache.delete(settings.COUPONS_CACHE_NAME)


@receiver(post_save, sender=Coin)
def invalidate_cache_on_save(sender, instance, **kwargs):
    cache.delete(settings.USER_PROFILE_CACHE_NAME)
