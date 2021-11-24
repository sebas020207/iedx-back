from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.http import Http404, HttpResponse
from django.forms.models import model_to_dict

from .models import Product, Subcategory, Category, Supplier
from historical.models import History
from .serializers import ProductSerializer, ImageSerialiser, CategorySerializer, SubcategorySerializer, SupplierSerializer

import mimetypes
from base64 import b64decode, b64encode


class AddProductView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, format=None):
        if 'name' in request.data:
            request.data['name'] = request.data['name'].title()

        serializer = ProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        action = 'ADDED: '+request.data['name']
        history = History.objects.create(name=request.user.name, action=action)
        history.save()
        return Response(serializer.data)


class ProductView(APIView):
    permission_classes = (IsAuthenticated,)

    def update_action(self, object_before, object_after):
        object_difference = {
            key: 'Before: '+str(object_before[key])+' After: '+str(object_after[key])+'. ' for key in object_before if object_before[key] != object_after[key]
        }
        if object_difference:
            action = 'UPDATE:'
            for key in object_difference:
                action += key.capitalize()+' '+object_difference[key]
            return action
        else:
            return False

    def get_object(self, pk):
        try:
            return Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            raise Http404

    def put(self, request, pk, format=None):
        product = self.get_object(pk)
        object_before = model_to_dict(product)

        serializer = ProductSerializer(
            product, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            object_after = model_to_dict(product)
            action = self.update_action(object_before, object_after)
            if action:
                history = History.objects.create(
                    name=request.user.name, action=action)
                history.save()

            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, pk, format=None):
        product = self.get_object(pk)

        serializer = ProductSerializer(product)
        return Response(serializer.data)


class AllProductsView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        search_item = request.query_params.items()

        filters = {
            ('name__icontains' if key == 'search_item' else 'is_archived'): (not int(value) if key == 'is_active' else value)
            for (key, value) in search_item
        }

        products = Product.objects.filter(**filters)

        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)


class ProductCountView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        active = Product.objects.filter(is_archived=False)
        inactive = Product.objects.filter(is_archived=True)
        categories = Category.objects.all()

        counts = {
            "active": len(active),
            "inactive": len(
                inactive),
            "categories": len(categories)
        }

        response = Response()

        response.data = {
            "active": len(active),
            "inactive": len(
                inactive),
            "categories": len(categories)
        }
        return response


class ProductImages(APIView):
    # permission_classes = (IsAuthenticated,)

    def get_object(self, pk):
        try:
            return Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        product = self.get_object(pk)
        try:
            image = product.photo
            return HttpResponse(image, content_type="image/png")
        except:
            raise Http404

    # def get(self, request, pk, format=None):
    #     product = self.get_object(pk)
    #     try:
    #         value = product.photo
    #         mime_type, encoding = mimetypes.guess_type(str(value))
    #         if not mime_type:
    #             mime_type = 'image/png'
    #         data = value.file.read()
    #         image_data = bytes(
    #             'data:' + mime_type + ';base64,', encoding='UTF-8') + b64encode(data)
    #         return HttpResponse(image_data)
    #     except:
    #         raise Http404


class CategoryView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        category = Category.objects.all()
        serializer = CategorySerializer(category, many=True)
        return Response(serializer.data)


class SubcategoryView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, pk, format=None):
        subcategory = Subcategory.objects.filter(category_id=pk)
        serializer = SubcategorySerializer(subcategory, many=True)
        return Response(serializer.data)


class AddSupplierView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, format=None):
        serializer = SupplierSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        action = 'ADDED: '+request.data['name']
        history = History.objects.create(name=request.user.name, action=action)
        history.save()
        return Response(serializer.data)


class SupplierView(APIView):
    permission_classes = (IsAuthenticated,)

    def update_action(self, object_before, object_after):
        object_difference = {
            key: 'Before: '+str(object_before[key])+' After: '+str(object_after[key])+'. ' for key in object_before if object_before[key] != object_after[key]
        }
        if object_difference:
            action = 'UPDATE: '
            for key in object_difference:
                action += key.capitalize()+' '+object_difference[key]
            return action
        else:
            return False

    def get_object(self, pk):
        try:
            return Supplier.objects.get(pk=pk)
        except Supplier.DoesNotExist:
            raise Http404

    def put(self, request, pk, format=None):
        supplier = self.get_object(pk)
        object_before = model_to_dict(supplier)
        serializer = SupplierSerializer(
            supplier, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            object_after = model_to_dict(supplier)
            action = self.update_action(object_before, object_after)
            if action:
                history = History.objects.create(
                    name=request.user.name, action=action)
                history.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, pk, format=None):
        supplier = self.get_object(pk)

        serializer = SupplierSerializer(supplier)
        return Response(serializer.data)


class AllSuppliersView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        suppliers = Supplier.objects.all()

        serializer = SupplierSerializer(suppliers, many=True)
        return Response(serializer.data)


class PublicProductView(APIView):
    def get(self, request, format=None):
        query_params = request.query_params
        a_to_z = 'name'

        filters = {}
        if('search_item' in query_params):
            filters['name__contains'] = query_params['search_item']

        if ('supplier_id' in query_params):
                filters['supplier_id'] = query_params['supplier_id']
        if ('category_id' in query_params):
            filters['category_id'] = query_params['category_id']
        if ('subcategory_id' in query_params):
            filters['subcategory_id'] = query_params['subcategory_id']
        filters['is_archived'] = 0

        if 'order_by' in query_params:
            if query_params['order_by'] == 'z_a':
                a_to_z = '-'+a_to_z

        products = Product.objects.filter(**filters).order_by(a_to_z)

        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)


class PublicSubcategoryView(APIView):
    def get(self, request, pk, format=None):
        subcategory = Subcategory.objects.get(pk=pk)

        serializer = SubcategorySerializer(subcategory)
        return Response(serializer.data)


class PublicSubcategoriesView(APIView):
    def get(self, request, format=None):
        search_item = request.query_params.items()
        filters = {
            ('name__icontains' if key == 'name' else key): value
            for (key, value) in search_item
        }
        subcategory = Subcategory.objects.filter(**filters)
        serializer = SubcategorySerializer(subcategory, many=True)
        return Response(serializer.data)


class PublicSupplierView(APIView):
    def get(self, request, format=None):
        search_item = request.query_params.items()
        a_to_z = 'name'

        filters = {
            ('name__icontains' if key == 'name' else key): value
            for (key, value) in search_item
        }

        if 'order_by' in filters:
            if filters['order_by'] == '0':
                a_to_z = '-'+a_to_z
            del filters['order_by']

        suppliers = Supplier.objects.filter(**filters).order_by(a_to_z)

        serializer = SupplierSerializer(suppliers, many=True)
        return Response(serializer.data)

# class ListProducts(APIView):
#     def get(self, request):
#         token = request.COOKIES.get('jwt')

#         if not token:
#             raise AuthenticationFailed('Unauthenticated!')

#         try:
#             payload = jwt.decode(token, 'secret', algorithms=['HS256'])
#         except jwt.ExpiredSignatureError:
#             raise AuthenticationFailed('Unauthenticated!')

#         product = Product.objects.all()
#         serializer = ProductSerializer(product, many=True)
#         return Response(serializer.data)
