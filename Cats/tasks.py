import stripe
from celery import shared_task
from django.core.exceptions import ValidationError

from Payment.models import ProductStripe


@shared_task()
def create_product(name, description, id):
    product = ProductStripe.objects.get(id=id)
    stripe_products = stripe.Product.list()
    for stripe_product in stripe_products.data:
        if stripe_product.name != name:
            try:
                new_product = stripe.Product.create(
                    name=name,
                    description=description,
                )
                product.product_id = new_product.id
            except Exception as e:
                raise ValidationError(str(e))
        else:
            product.product_id = product.id
    product.save()
