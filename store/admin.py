from django.contrib import admin
from .models import Product, Cart


class ProductAdmin(admin.ModelAdmin):
    pass


class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'product')


admin.site.register(Product, ProductAdmin)
admin.site.register(Cart, CartAdmin)
