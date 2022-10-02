from django import forms
from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.utils.html import format_html
from django.core.validators import FileExtensionValidator

from pulsar_test.products.models import Product, ProductImage


class ProductForm(forms.ModelForm):
    image = forms.ImageField(label=_("Изображение"), required=False,
                             validators=[FileExtensionValidator(allowed_extensions=ProductImage.ALLOWED_EXTENSIONS)],
                             widget=forms.FileInput(attrs={'accept': '.'+',.'.join(ProductImage.ALLOWED_EXTENSIONS)}))
    clean_image = forms.BooleanField(label=_("Очистить изображение"), required=False)

    class Meta:
        model = Product
        exclude = ()

    def save(self, *args, **kwargs):
        product = super(ProductForm, self).save(*args, **kwargs)
        product.save()
        image = self.cleaned_data['image']
        clean_image = self.cleaned_data['clean_image']
        if image or clean_image:
            ProductImage.objects.filter(product=product).delete()
        if image:
            ProductImage.objects.create(
                image=image,
                product=product,
            )
        return product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    form = ProductForm
    list_display = ('name', 'article', 'price', 'status',)
    readonly_fields = ('image_tag',)

    def image_tag(self, obj):
        image = obj.images.first()
        return format_html('<img src="{}" style="max-width: 400px;max-height: 400px;"/>'.format(image.image.url) if image else '')

    image_tag.short_description = ''

