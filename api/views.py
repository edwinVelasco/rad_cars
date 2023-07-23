from django.db.models import ProtectedError
from django.db.models import Q

# Create your views here.
from django.http import Http404

from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Provider, Product, Quotation, Mark, Model, Category
from .serializer import ProviderSerializer, ProductSerializer, \
    QuotationSerializer, QuotationSerializerCreate, MarkSerializer, \
    ModelSerializer, CategorySerializer, ModelSerializerCreate, ProductSerializerCreate

from .schemas import ProductSchemas


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
        if 'search' in request.query_params:
            # products = Product.objects.filter(
            #     Q(name__icontains=request.query_params['search']) |
            #     Q(description__icontains=request.query_params['search']) |
            #     Q(mark_model__name__icontains=request.query_params['search']) |
            #     Q(mark_model__mark__name__icontains=request.query_params['search']) |
            #     Q(category__name__icontains=request.query_params['search'])
            # )
            q = Q()
            for name in request.query_params['search'].split(' '):
                q |= Q(name__icontains=name)
                q |= Q(description__icontains=name)
                q |= Q(mark_model__name__icontains=name)
                q |= Q(mark_model__mark__name__icontains=name)
                q |= Q(category__name__icontains=name)
            products = Product.objects.filter(q)

        elif request.query_params:
            # filter
            filters = dict()

            if 'category' in request.query_params:
                filters['category'] = request.query_params['category']

            if 'mark' in request.query_params:
                filters['mark_model__mark'] = request.query_params['mark']

            if 'model' in request.query_params:
                filters['mark_model'] = request.query_params['model']

            if 'name' in request.query_params:
                names = request.query_params['name'].split(' ')
                if len(names) == 1:
                    filters['name__icontains'] = request.query_params['name']
                    products = Product.objects.filter(**filters)
                else:
                    q = Q()
                    for name in names:
                        q |= Q(name__icontains=name)
                    products = Product.objects.filter(**filters)
                    products = products.filter(q)
            else:
                products = Product.objects.filter(**filters)

        else:
            products = Product.objects.all()

        if 'exclude' in request.query_params:
            products = products.exclude(Q(stock=0) | Q(stock=None))

        product_json = ProductSerializer(products, many=True)
        return Response(product_json.data)

    def post(self, request):
        product = ProductSchemas(**request.data).dict()
        product_json = ProductSerializerCreate(data=product) #UnMarshall
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


class MarkView(APIView):

    def get(self, request):
        marks = Mark.objects.all()
        mark_json = MarkSerializer(marks, many=True)
        return Response(mark_json.data)

    def post(self, request):
        mark_json = MarkSerializer(data=request.data) #UnMarshall
        if mark_json.is_valid():
            mark_json.save()
            return Response(mark_json.data, status=201)
        return Response(mark_json.errors, status=400)


class DetailMarkView(APIView):
    def get_object(self, pk):
        try:
            return Mark.objects.get(id=pk)
        except Mark.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        product = self.get_object(pk)
        product_json = MarkSerializer(product)
        return Response(product_json.data, status=200)

    def put(self, request, pk):
        mark = self.get_object(pk)
        mark_json = MarkSerializer(mark, data=request.data)
        if mark_json.is_valid():
            mark_json.save()
            return Response(mark_json.data, status=200)

        return Response(mark_json.errors, status=400)

    def delete(self, request, pk):
        try:
            mark = self.get_object(pk)
            mark.delete()
            return Response(status=204)
        except ProtectedError:
            return Response({'message': 'La marca tiene modelos'}, status=409)


class ModelView(APIView):

    def get(self, request):
        models = Model.objects.all()
        models_json = ModelSerializer(models, many=True)
        return Response(models_json.data)

    def post(self, request):
        model_json = ModelSerializerCreate(data=request.data) #UnMarshall
        if model_json.is_valid():
            model_json.save()
            return Response(model_json.data, status=201)
        return Response(model_json.errors, status=400)


class DetailModelView(APIView):
    def get_object(self, pk):
        try:
            return Model.objects.get(id=pk)
        except Model.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        model = self.get_object(pk)
        model_json = ModelSerializer(model)
        return Response(model_json.data, status=200)

    def put(self, request, pk):
        model = self.get_object(pk)
        model_json = ModelSerializer(model, data=request.data)
        if model_json.is_valid():
            model_json.save()
            return Response(model_json.data, status=200)

        return Response(model_json.errors, status=400)

    def delete(self, request, pk):
        try:
            model = self.get_object(pk)
            model.delete()
            return Response(status=204)
        except ProtectedError:
            return Response({'message': 'El modelo esta asignado a un producto'}, status=409)


class CategoryView(APIView):

    def get(self, request):
        categories = Category.objects.all()
        categories_json = CategorySerializer(categories, many=True)
        return Response(categories_json.data)

    def post(self, request):
        category_json = CategorySerializer(data=request.data) #UnMarshall
        if category_json.is_valid():
            category_json.save()
            return Response(category_json.data, status=201)
        return Response(category_json.errors, status=400)


class DetailCategoryView(APIView):
    def get_object(self, pk):
        try:
            return Category.objects.get(id=pk)
        except Model.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        category = self.get_object(pk)
        category_json = CategorySerializer(category)
        return Response(category.data, status=200)

    def put(self, request, pk):
        category = self.get_object(pk)
        category_json = ModelSerializer(category, data=request.data)
        if category_json.is_valid():
            category_json.save()
            return Response(category_json.data, status=200)

        return Response(category_json.errors, status=400)

    def delete(self, request, pk):
        try:
            category = self.get_object(pk)
            category.delete()
            return Response(status=204)
        except ProtectedError:
            return Response({'message': 'La Categoría esta asignada a un producto'}, status=409)

