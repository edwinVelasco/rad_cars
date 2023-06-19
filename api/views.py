from django.db.models import ProtectedError
from django.shortcuts import render

# Create your views here.
from django.http import Http404

from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Provider, Product, Quotation
from .serializer import ProviderSerializer, ProductSerializer, QuotationSerializer, QuotationSerializerCreate


class ProviderView(APIView):

    def get(self, request):
        providers = Provider.objects.all()
        provider_json = ProviderSerializer(providers, many=True)
        return Response(provider_json.data)

    def post(self, request):
        provider_json = ProviderSerializer(data=request.data) #UnMarshall
        if provider_json.is_valid():
            provider_json.save()
            return Response(provider_json.data, status=201)
        return Response(provider_json.errors, status=400)


class DetailProviderView(APIView):
    def get_object(self, pk):
        try:
            return Provider.objects.get(id=pk)
        except Provider.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        provider = self.get_object(pk)
        provider_json = ProviderSerializer(provider)
        return Response(provider_json.data, status=200)

    def put(self, request, pk):
        provider = self.get_object(pk)
        provider_json = ProviderSerializer(provider, data=request.data)
        if provider_json.is_valid():
            provider_json.save()
            return Response(provider_json.data, status=200)

        return Response(provider_json.errors, status=400)

    def delete(self, request, pk):
        provider = self.get_object(pk)
        provider.delete()
        return Response(status=204)


class ProductView(APIView):

    def get(self, request):
        if 'name' in request.query_params:
            products = Product.objects.filter(name__contains=request.query_params['name'])
        else:
            products = Product.objects.all()
        product_json = ProductSerializer(products, many=True)
        return Response(product_json.data)

    def post(self, request):
        product_json = ProductSerializer(data=request.data) #UnMarshall
        if product_json.is_valid():
            product_json.save()
            return Response(product_json.data, status=201)
        return Response(product_json.errors, status=400)


class DetailProductView(APIView):
    def get_object(self, pk):
        try:
            return Product.objects.get(id=pk)
        except Product.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        product = self.get_object(pk)
        product_json = ProductSerializer(product)
        return Response(product_json.data, status=200)

    def put(self, request, pk):
        product = self.get_object(pk)
        product_json = ProductSerializer(product, data=request.data)
        if product_json.is_valid():
            product_json.save()
            return Response(product_json.data, status=200)

        return Response(product_json.errors, status=400)

    def delete(self, request, pk):
        try:
            product = self.get_object(pk)
            product.delete()
            return Response(status=204)
        except ProtectedError:
            return Response({'message': 'El producto tiene cotizaciones'}, status=409)


class QuotationView(APIView):

    def get(self, request, pk):
        quotations = Quotation.objects.filter(product__id=pk)
        quotations_json = QuotationSerializer(quotations, many=True)
        return Response(quotations_json.data)

    def post(self, request, pk):
        try:
            quotation_json = QuotationSerializerCreate(data=request.data)  # UnMarshall
            if quotation_json.is_valid():
                quotation_json.save()
                return Response(quotation_json.data, status=201)
            return Response(quotation_json.errors, status=400)
        except Exception as e:
            print(e)


class DetailQuotationView(APIView):
    def get_object(self, pk):
        try:
            return Quotation.objects.get(id=pk)
        except Quotation.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        quotation = self.get_object(pk)
        quotation_json = QuotationSerializer(quotation)
        return Response(quotation_json.data, status=200)

    def put(self, request, pk):
        quotation = self.get_object(pk)
        quotation_json = QuotationSerializer(quotation, data=request.data)
        if quotation_json.is_valid():
            quotation_json.save()
            return Response(quotation_json.data, status=200)

        return Response(quotation_json.errors, status=400)

    def delete(self, request, pk, pk2):
        quotation = self.get_object(pk2)
        if quotation.product_id == pk:
            quotation.delete()
            return Response(status=204)
        return Response({"error": "La cotización no se puede eliminar"}, status=400)