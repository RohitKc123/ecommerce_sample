from django.db import models
from django.contrib.auth import get_user_model

from common.constant import CATEGORY_CHOICES, COMPANY, ITEM_STOCK, IN_STOCK, METHOD

USER = get_user_model()

ORDER_STATUS = (
    ("Order Received", "Order Received"),
    ("Order Processing", "Order Processing"),
    ("On the way", "On the way"),
    ("Order Completed", "Order Completed"),
    ("Order Canceled", "Order Canceled"),
)

WISHLIST_STATUS = (
    ("Pending", "Pending"),
    ("In Review", "In Review"),
    ("Canceled", "Canceled"),
    ("Completed", "Completed"),
)


# Create your models here.
class Product(models.Model):
    user = models.ForeignKey(USER, on_delete=models.CASCADE, related_name='user_product', blank=True, null=True)
    name = models.CharField(max_length=100, blank=False, null=False)
    price = models.FloatField(default=0)
    quantity = models.IntegerField(default=0)
    image = models.ImageField(upload_to='product', null=True, blank=True, )
    description = models.TextField()
    category = models.CharField(max_length=30, choices=CATEGORY_CHOICES)
    company = models.CharField(max_length=30, choices=COMPANY, null=True, blank=True)
    generation = models.CharField(max_length=20, blank=True, null=True)
    status = models.CharField(max_length=10, choices=ITEM_STOCK, default=IN_STOCK)
    added_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    featured = models.BooleanField(default=False, blank=True, null=True)


class WishList(models.Model):
    user = models.ForeignKey(USER, on_delete=models.CASCADE, related_name='wishlist')
    wished_item = models.ForeignKey(Product, on_delete=models.CASCADE)
    product_qty = models.IntegerField(null=True, blank=True, default=0)
    price = models.IntegerField(null=True, blank=True)
    status = models.CharField(choices=WISHLIST_STATUS, default="Pending", max_length=15)
    added_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.first_name}-->{self.wished_item.name}"


class Order(models.Model):
    user = models.ForeignKey(USER, on_delete=models.CASCADE)
    ordered_item = models.ManyToManyField(WishList, null=True, blank=True)
    shipping_address = models.CharField(max_length=100)
    order_by = models.CharField(max_length=50)
    mobile = models.IntegerField()
    email = models.EmailField(max_length=100)
    total = models.PositiveIntegerField()
    order_status = models.CharField(max_length=50, choices=ORDER_STATUS, default='Order Processing')
    created_at = models.DateTimeField(auto_now_add=True)
    payment_method = models.CharField(max_length=20, choices=METHOD)
    payment_completed = models.BooleanField(default=False, null=True, blank=True)
