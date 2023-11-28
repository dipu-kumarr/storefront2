
from dataclasses import fields
from itertools import product
from statistics import quantiles
from rest_framework import serializers
from decimal import Decimal
from store.models import Cart, Product, Collection, Review, CartItem

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
    
class SimpleProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id','title','unit_price']
    
class CartItemSerializer(serializers.ModelSerializer):
    product= SimpleProductSerializer(many=False)  
    total_price = serializers.SerializerMethodField()
    def get_total_price(self, cart_item:CartItem):
        return cart_item.quantity * cart_item.product.unit_price
    class Meta:
        model = CartItem
        fields = ['id','cart','product','quantity','total_price']

class CartSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    items = CartItemSerializer(many=True,read_only = True)
    total_price = serializers.SerializerMethodField()
    
    def get_total_price(self,cart):
        return sum([item.quantity * item.product.unit_price for item in cart.items.all()])
    class Meta:
        model = Cart
        fields = ['id','items','total_price']
    
