from django.db.models.signals import post_save
from django.dispatch import receiver

from Payment.models import ProductStripe
from Payment.tasks import create_product


@receiver(post_save, sender=ProductStripe)
def create_stripe_product(sender, instance, created, **kwargs):
    if created:
        create_product.delay(name=instance.name, description=instance.description, id=instance.id)
    else:
        if not instance.product_id:
            create_product.delay(name=instance.name, description=instance.description, id=instance.id)
