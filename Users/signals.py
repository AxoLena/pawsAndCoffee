from django.core.cache import cache
from django.db import transaction
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from Users.models import CustomUser
from Bonuses.models import Coin, History


@receiver(post_save, sender=CustomUser)
def create_user_coins(sender, instance, created, **kwargs):
    if created:
        with transaction.atomic():
            coin = Coin.objects.create(count=100)
            History.objects.create(description='Подарок за создания аккаунта', count=100, coin=coin)
            instance.coins = coin
            instance.save(update_fields=['coins'])


@receiver(post_save, sender=CustomUser)
def invalidate_cache_on_delete(sender, instance, **kwargs):
    cache.delete(f'user_profile_cache_{instance.id}')


@receiver(post_delete, sender=CustomUser)
def invalidate_cache_on_delete(sender, instance, **kwargs):
    cache.delete(f'user_profile_cache_{instance.id}')
