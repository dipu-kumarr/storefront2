
from dataclasses import fields
from statistics import quantiles
from rest_framework import serializers
from decimal import Decimal
from store.models import Cart, Product,Collection, Review

class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model=Collection
        fields=['id', 'title','products_count']
        
    products_count = serializers.IntegerField(read_only=True)
    



class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model=Product
        fields=['id', 'title','slug','inventory','unit_price', 'price_with_tax','collection']
    # id = serializers.IntegerField()
    # title = serializers.CharField(max_length=255)
    # price = serializers.DecimalField(max_digits=6, decimal_places=2 , source='unit_price')
    price_with_tax = serializers.SerializerMethodField(method_name='calculate_tax')
    # collection = serializers.HyperlinkedRelatedField(queryset=Collection.objects.all(),view_name='collection-detail')



    def calculate_tax(self, product:Product):
        return product.unit_price * Decimal(1.1)
    

    def create(self,validated_data):
        product = Product.objects.create(**validated_data)
        product.save()
        return product
    
class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields =['id','date','name','description']

    def create(self,validated_data):
        product_id = self.context['product_id']
        return Review.objects.create(product_id=product_id,**validated_data)
    
class CartSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only = True)
    class Meta:
        model = Cart
        fields = ['id']
    
