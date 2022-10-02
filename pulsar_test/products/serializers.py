from rest_framework import serializers

from pulsar_test.products.models import Product


class ProductImageSerializer(serializers.Serializer):
    path = serializers.CharField(max_length=100)
    formats = serializers.ListField(
        child=serializers.CharField(max_length=4)
    )


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = (
            'name',
            'article',
            'price',
            'status_code',
            'status_text',
            'image',
        )

    status_code = serializers.CharField(source='status')
    status_text = serializers.CharField(source='get_status_display')
    image = serializers.SerializerMethodField('get_image')

    def get_image(self, obj):
        images = obj.images.all()
        if images:
            images_serializer = ProductImageSerializer(data={
                'path': images[0].url,
                'formats': [image.extension for image in images]
            })
            if images_serializer.is_valid():
                return images_serializer.data
