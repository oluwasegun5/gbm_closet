from rest_framework import serializers

from store.models import Product, Cart, CartItem


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class CartItemSerializer(serializers.Serializer):


    class Meta:
        model = CartItem
        fields = ('id', 'cart', 'product')

    def get_product(self, obj):
        return ProductSerializer(obj.product).data

    @staticmethod
    def get_total_price(self, obj):
        return obj.product.price * obj.quantity


class CartSerializer(serializers.Serializer):
    cart_items = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ('id', 'user', 'cart_items')

    def get_cart_items(self, obj):
        cart_items = CartItem.objects.filter(cart=obj)
        print(cart_items)
        return CartItemSerializer(cart_items, many=True).data
