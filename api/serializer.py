from rest_framework import serializers

from .models import Provider, Product, Quotation, Mark, Model, Category


class ProviderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Provider
        fields = ('id', 'nit', 'name', 'contact', 'email', 'created_at', 'updated_at')


class MarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mark
        fields = ('id', 'name')


class ModelSerializer(serializers.ModelSerializer):
    mark = MarkSerializer(read_only=True)

    class Meta:
        model = Model
        fields = ('id', 'name', 'mark')


class ModelSerializerCreate(serializers.ModelSerializer):
    class Meta:
        model = Model
        fields = ('id', 'name', 'mark')


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name',)


class ProductSerializer(serializers.ModelSerializer):
    mark_model = ModelSerializer(read_only=True)
    category = CategorySerializer(read_only=True)

    class Meta:
        model = Product
        fields = ('id', 'code', 'name', 'description', 'price', 'stock', 'profit',
                  'net_price', 'mark_model', 'category', 'images', 'transmission',
                  'created_at', 'updated_at')


class ProductSerializerCreate (serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'code', 'name', 'description', 'price', 'stock', 'profit',
                  'net_price', 'mark_model', 'category', 'images', 'transmission',
                  'created_at', 'updated_at')


class QuotationSerializer(serializers.ModelSerializer):
    provider = ProviderSerializer(read_only=True)

    class Meta:
        model = Quotation
        fields = ('id', 'product', 'provider', 'price', 'created_at', 'updated_at')


class QuotationSerializerCreate(serializers.ModelSerializer):

    class Meta:
        model = Quotation
        fields = ('id', 'product', 'provider', 'price', 'created_at', 'updated_at')
