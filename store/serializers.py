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
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ('id', 'user', 'cart_item', "total_price")

    @staticmethod
    def get_cart_item(obj):
        cart_items = CartItem.objects.filter(cart=obj)
        return CartItemSerializer(cart_items, many=True).data

    @staticmethod
    def get_total_price(obj):
        cart_items = CartItem.objects.filter(cart=obj)
        total_price = 0
        for item in cart_items:
            total_price += item.price
        return total_price
