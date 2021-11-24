from rest_framework import serializers

from .models import Product, Category, Subcategory, Supplier


class ImageSerialiser(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['photo']


class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = ['id', 'name', 'email', 'phone', 'address']


class SubcategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Subcategory
        fields = ['id', 'name', 'category_id', 'photo']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'photo']


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'is_archived',
                  'photo', 'supplier_id', 'category_id', 'subcategory_id']


class ProductNameSerializer(serializers.ModelSerializer):
    supplier_id = serializers.SlugRelatedField(
        read_only=True, slug_field='name')

    class Meta:
        model = Product
        fields = ['id', 'name', 'description',
                  'photo', 'supplier_id', 'category_id', 'subcategory_id']


class ProductIDSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=True)
