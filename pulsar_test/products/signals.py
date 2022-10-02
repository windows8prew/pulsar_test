from io import BytesIO

from django.core.files.base import ContentFile
from django.db.models.signals import post_save
from django.dispatch import receiver

from PIL import Image

from pulsar_test.products.models import ProductImage


@receiver(post_save, sender=ProductImage)
def convert_product_image(sender, instance, **kwargs):
    if instance.image.name and instance.extension != 'webp':
        image = Image.open(instance.image.file)
        image_io = BytesIO()
        image.save(image_io, format='WEBP')
        ProductImage.objects.create(
            product=instance.product,
            image=ContentFile(image_io.getvalue(), instance.filename+'.webp')
        )
