
# from typing import Collection
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from rest_framework.decorators import api_view  
from rest_framework.response import Response
from rest_framework import status
from .models import Product,OrderItem,Collection
from .serializers import CollectionSerializer, ProductSerializer
from django.db.models import Value,Count
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView
# Create your views here.


class ProductList(ListCreateAPIView):
    queryset = Product.objects.select_related('collection').all()
    serializer_class = ProductSerializer
    
    def get_serializer_context(self):
        return {'request': self.request}
    # def get(self,request):
    #     queryset = Product.objects.select_related('collection').all()
    #     serializer = ProductSerializer(queryset, many=True, context={'request': request})
    #     return Response(serializer.data)
    # def post(self,request):
    #     serializer = ProductSerializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     print(serializer.validated_data)
    #     serializer.save()
    #     return Response(serializer.data,status=status.HTTP_201_CREATED)
        
class ProductDetail(APIView):
    def get(self, request,id):
        product = get_object_or_404(Product, pk=id)
        serializer = ProductSerializer(product)
        return Response(serializer.data)
    def post(self, request,id):
        product = get_object_or_404(Product, pk=id)
        serializer = ProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        print(serializer.validated_data)
        serializer.save()
        return Response(serializer.data,status=status.HTTP_200_OK)

    def delete(self, request,id):
        product = get_object_or_404(Product, pk=id)
        if product.orderitems.count() > 0:  # type: ignore
            return Response({'error':'Product cannot be deleted becauseit is  associated with order item'},status=status.HTTP_405_METHOD_NOT_ALLOWED)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class CollectionList(ListCreateAPIView):
    queryset = Collection.objects.annotate(
        products_count=Count('products')).all()
    serializer_class = CollectionSerializer

# @api_view(['GET','POST'])
# def collection_list(request):
#     if request.method =='GET':
#             queryset = Collection.objects.annotate(products_count=Count('products')).all()
#             serializer = CollectionSerializer(queryset, many=True)
#             return Response(serializer.data)
#     elif request.method =='POST':                                                
#         serializer = CollectionSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         # print(serializer.validated_data)
#         serializer.save()
#         return Response(serializer.data,status=status.HTTP_201_CREATED)

@api_view(['GET','PUT','DELETE'])
def collection_detail(request,pk):
    collections=get_object_or_404(
        Collection.objects.annotate(products_count=Count('products')),pk=pk)
    if request.method =='GET':
        serializer = CollectionSerializer(collections)
        return Response(serializer.data)
    elif request.method =='PUT':
        serializer = CollectionSerializer(collections,data=request.data)
        serializer.is_valid(raise_exception=True)
        # print(serializer.validated_data)
        serializer.save()
        return Response(serializer.data,status=status.HTTP_200_OK)
    elif request.method =='DELETE':
        if collections.products.count() > 0:  # type: ignore
            return Response({'error':'Collection cannot be deleted becauseit is  associated with product'},status=status.HTTP_405_METHOD_NOT_ALLOWED)
        collections.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    