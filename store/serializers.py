from rest_framework import serializers

from store.models import Product, Cart, CartItem


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = '__all__'


class CartSerializer(serializers.ModelSerializer):
    cart_item = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ('id', 'user', 'cart_item')

    def get_cart_item(self, obj):
        cart_items = CartItem.objects.filter(cart=obj)
        return CartItemSerializer(cart_items, many=True).data
