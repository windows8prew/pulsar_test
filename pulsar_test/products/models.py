from io import BytesIO
from os.path import join, basename

from django.db import models
from django.utils.translation import gettext_lazy as _


class Product(models.Model):
    class Meta:
        verbose_name = _('Товар')
        verbose_name_plural = _('Товары')

        ordering = ('created_at',)

    class Status(models.IntegerChoices):
        NO_STATUS = 0, _('Без статуса')
        IN_STOCK = 1, _('В наличии')
        ON_ORDER = 2, _('Под заказ')
        AWAITED = 3, _('Ожидается поступление')
        NOT_AVAILABLE = 4, _('Нет в наличии')
        NOT_PRODUCED = 5, _('Не производится')

    created_at = models.DateTimeField(auto_now_add=True)
    name = models.CharField(_('Название'), max_length=255)
    article = models.CharField(_('Артикул'), max_length=255, unique=True)
    price = models.DecimalField(_('Цена'),  max_digits=11, decimal_places=2, default=0)
    status = models.IntegerField(_('Статус'), choices=Status.choices, default=Status.NO_STATUS)

    def __repr__(self):
        return f"Product({self.id=}, {self.name=})"


class ProductImage(models.Model):
    ALLOWED_EXTENSIONS = ('jpg', 'jpeg', 'png', 'webp')

    class Meta:
        verbose_name = _('Изображение')
        verbose_name_plural = _('Изображение')

        ordering = ('created_at',)

    def image_dir(self, filename):
        return join('product_images', str(self.product.pk)+filename.split('.')[-1])

    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(_('Изображение'), max_length=100, upload_to=image_dir)
    product = models.ForeignKey(verbose_name=_('Товар'), to='Product', related_name='images', on_delete=models.CASCADE)

    def __repr__(self):
        return f"ProductImage({self.id=}, {self.image=})"

    @property
    def url(self):
        return ''.join(self.image.url.split('.')[0:-1])

    @property
    def filename(self):
        return basename(self.image.name).split('.')[0]

    @property
    def extension(self):
        return self.image.name.split('.')[-1].lower()

    def save(self, *args, **kwargs):
        obj = super(ProductImage, self).save(*args, **kwargs)

        # with BytesIO() as f:
        #     im.save(f, format='JPEG')
        #     return f.getvalue()