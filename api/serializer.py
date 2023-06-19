from rest_framework import serializers

from .models import Provider, Product, Quotation


class ProviderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Provider
        fields = ('id', 'nit', 'name', 'contact', 'email', 'created_at', 'updated_at')


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'code', 'name', 'description', 'price', 'stock',
                  'created_at', 'updated_at')


class QuotationSerializer(serializers.ModelSerializer):
    provider = ProviderSerializer(read_only=True)

    #def create(self, validated_data):
    #    print(**validated_data)
    #    return Quotation.objects.create(**validated_data)

    class Meta:
        model = Quotation
        fields = ('id', 'product', 'provider', 'price', 'created_at', 'updated_at')


class QuotationSerializerCreate(serializers.ModelSerializer):

    class Meta:
        model = Quotation
        fields = ('id', 'product', 'provider', 'price', 'created_at', 'updated_at')

