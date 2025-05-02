from django.conf import settings
from django.core.cache import cache
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from Cats.models import Cats
from Payment.models import ProductStripe


@receiver(post_delete, sender=Cats)
def invalidate_cache_on_delete(sender, instance, **kwargs):
    cache.delete(settings.CATS_CACHE_NAME)


@receiver(post_save, sender=Cats)
def invalidate_cache_on_save(sender, instance, **kwargs):
    cache.delete(settings.CATS_CACHE_NAME)


@receiver(post_save, sender=Cats)
def create_my_model_product_stripe(sender, instance, **kwargs):
    name = instance.name
    product_is_exists = ProductStripe.objects.filter(name=name).exists()
    if not product_is_exists:
        description = f'Подписка на поддержание котика {name}'
        ProductStripe.objects.create(name=name, description=description)