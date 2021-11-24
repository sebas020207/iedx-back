from rest_framework import serializers

from .models import Quote, Registry
from products.serializers import ProductNameSerializer, ProductIDSerializer


class QuoteSerializer(serializers.ModelSerializer):
    product = ProductNameSerializer(read_only=True, many=True)

    class Meta:
        model = Quote
        fields = ['id', 'first_name', 'last_name', 'email', 'address',
                  'mobile_phone', 'phone', 'company', 'area', 'priority', 'date', 'product']


class RegistrySerializer(serializers.ModelSerializer):

    class Meta:
        model = Registry
        fields = ['id', 'name', 'email', 'address',
                  'messagereg', 'phone', 'subject']


class CreateQuoteSerializer(serializers.ModelSerializer):
    product = ProductIDSerializer(many=True)

    class Meta:
        model = Quote
        fields = ['id', 'first_name', 'last_name', 'email', 'address',
                  'mobile_phone', 'phone', 'company', 'area', 'priority', 'product']

    def create(self, validated_data):
        product_ids = validated_data.pop('product')
        ids_list = [id['id'] for id in product_ids]
        quote = Quote(**validated_data)
        quote.save()
        quote.product.add(*ids_list)
        return quote
