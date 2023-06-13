from rest_framework import viewsets, status
from rest_framework.response import Response

import permissions as gp
from .models import AppUser as User
from .serializers import (ChangePasswordSerializer, UserSerializer)
import utilities as gu
from store.models import Cart


class ChangePasswordViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = ChangePasswordSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [gp.GbmAdmin, gp.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        if message := gu.validate_required_fields({'email': request.data.get('email'),
                                                   'password': request.data.get('password'),
                                                   'first_name': request.data.get('first_name'),
                                                   'last_name': request.data.get('last_name')}):
            return Response(message, status=status.HTTP_400_BAD_REQUEST)

        if self.queryset.filter(email__iexact=request.data.get('email')).exists():
            return Response({'message': 'User with this email already exists'},
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            print(e)
            return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request, *args, **kwargs):
        try:
            user = self.queryset.get(email=request.user.email)
            if not user.is_admin:
                return Response({'message': 'You are not authorized to view this page'},
                                status=status.HTTP_401_UNAUTHORIZED)
            queryset = self.filter_queryset(self.get_queryset())
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        except User.DoesNotExist:
            return Response({'message': 'No users found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print(e)
            return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def retrieve(self, request, *args, **kwargs):
        try:
            user = self.queryset.get(email=request.user.email)
            if not user.is_admin:
                return Response({'message': 'You are not authorized to view this page'},
                                status=status.HTTP_401_UNAUTHORIZED)
            queryset = self.queryset.get(id=kwargs.get('pk'))
            serializer = self.get_serializer(queryset)
            return Response(serializer.data)
        except User.DoesNotExist:
            return Response({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def update(self, request, *args, **kwargs):
        try:
            user = self.queryset.get(email=request.user.email)
            if not user.is_admin:
                return Response({'message': 'You are not authorized to view this page'},
                                status=status.HTTP_401_UNAUTHORIZED)
            queryset = self.queryset.get(id=kwargs.get('pk'))
            serializer = self.get_serializer(queryset, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        except User.DoesNotExist:
            return Response({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def destroy(self, request, *args, **kwargs):
        try:
            user = self.queryset.get(email=request.user.email)
            if not user.is_admin:
                return Response({'message': 'You are not authorized to view this page'},
                                status=status.HTTP_401_UNAUTHORIZED)

            queryset = self.queryset.get(id=kwargs.get('pk'))
            queryset.delete()
            return Response({'message': 'User deleted successfully'}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
