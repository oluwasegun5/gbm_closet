from django.core.exceptions import ValidationError
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

import permissions as gp
from store.models import Product, Cart, CartItem
from store.serializers import ProductSerializer, CartSerializer, CartItemSerializer
import utilities as gu
from gbm_auth.models import AppUser as User


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permissions = [gp.GbmAdmin, gp.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        if message := gu.validate_required_fields({'name': request.data.get('name'),
                                                   'price': request.data.get('price'),
                                                   'quantity': request.data.get('quantity'),
                                                   'category': request.data.get('category'),
                                                   'images': request.data.get('images'),
                                                   'color': request.data.get('color'),
                                                   'size': request.data.get('size'),
                                                   'availability': request.data.get('availability')}):
            return Response(message, status=status.HTTP_400_BAD_REQUEST)

        try:
            if not User.objects.get(email=request.user.email).is_admin:
                return Response({'message': 'You are not authorized to perform this action'},
                                status=status.HTTP_401_UNAUTHORIZED)

            if self.queryset.filter(name=request.data.get('name')).exists():
                return Response({'message': 'Product with this name already exists'},
                                status=status.HTTP_400_BAD_REQUEST)

            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as e:
            return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, *args, **kwargs):
        product_id = kwargs.get('pk')
        if not product_id:
            return Response({'message': 'Product id is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            if not self.queryset.filter(id=product_id).exists():
                return Response({'message': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)
            product = self.queryset.get(id=product_id)
            serializer = self.get_serializer(product)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ValidationError as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        product_id = kwargs.get('pk')
        if not product_id:
            return Response({'message': 'Product id is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            if not self.queryset.filter(id=product_id).exists():
                return Response({'message': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)
            product = self.queryset.get(id=product_id)
            product.delete()
            return Response({'message': 'Product deleted successfully'}, status=status.HTTP_200_OK)
        except ValidationError as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['post'], detail=False, url_name='add_item_to_cart', permission_classes=[gp.IsAuthenticated])
    def add_item_to_cart(self, request, *args, **kwargs):
        data = request.data
        product_id = data.get('product_id')
        if message := gu.validate_required_fields({'quantity': data.get('quantity'),
                                                   'product_id': product_id}):
            return Response(message, status=status.HTTP_400_BAD_REQUEST)
        try:
            user = User.objects.get(email=request.user.email)
            if not self.queryset.filter(id=product_id).exists():
                return Response({'message': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)
            product = self.queryset.get(id=product_id)
            if not Cart.objects.filter(user=user).exists():
                Cart.objects.create(user=request.user)

            cart = Cart.objects.get(user=user)
            quantity = int(data.get('quantity'))
            if CartItem.objects.filter(cart=cart, product=product).exists():
                cart_item = CartItem.objects.get(cart=cart, product=product)
                cart_item.quantity += quantity
                cart_item.total = cart_item.quantity * product.price
                cart_item.save()
                return Response({'message': 'Product added to cart successfully'}, status=status.HTTP_200_OK)

            total_price = quantity * product.price
            CartItem.objects.create(cart=cart, product=product, quantity=quantity, total_price=total_price)
            return Response({'message': 'Product added to cart successfully'}, status=status.HTTP_200_OK)

        except ValidationError as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['get'], detail=False, url_name='get_cart', permission_classes=[gp.IsAuthenticated])
    def get_cart(self, request, *args, **kwargs):
        try:
            user = User.objects.get(email=request.user.email)
            if not Cart.objects.filter(user=user).exists():
                return Response({'message': 'Cart is empty'}, status=status.HTTP_200_OK)
            cart = Cart.objects.get(user=user)
            serializer = CartSerializer(cart)

            return Response(serializer.data, status=status.HTTP_200_OK)
        except Cart.DoesNotExist:
            return Response({'message': 'Cart is empty'}, status=status.HTTP_200_OK)
        except ValidationError as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)
