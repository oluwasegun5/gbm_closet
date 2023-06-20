import uuid
import enums as ge
from gbm_auth.models import AppUser as User

from django.db import models


class Product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    description = models.TextField(default="")
    price = models.DecimalField(max_digits=12, decimal_places=2)
    color = models.CharField(max_length=255)
    quantity = models.IntegerField()
    images = models.JSONField(default=list)
    size = models.IntegerField(default=0)
    category = models.CharField(max_length=8, choices=ge.ProductCategory.choices(),
                                default=ge.ProductCategory.BAG.value)
    availability = models.CharField(max_length=8, choices=ge.ProductAvailability.choices(),
                                    default=ge.ProductAvailability.IN_STOCK.value)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Cart(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # total_price = models.DecimalField(max_digits=12, decimal_places=2, default=0.00) # total price of all cart items

    def __str__(self):
        return self.user.first_name + "'s cart"


class CartItem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=12, decimal_places=2, default=0.00) # product price * quantity

    def __str__(self):
        return self.product.name + " in " + self.cart.user.first_name + "'s cart"
