from django.db import models
from django.core.validators import MinValueValidator
from uuid import uuid4
from django.contrib import admin
from django.conf import settings


class Collection(models.Model):
    title = models.CharField(max_length=255)
    #featured_product = models.ForeignKey('Product' , on_delete=models.SET_NULL, null = True ,related_name = '+' , blank=True)

    def __str__(self) -> str:
        return self.title

    class Meta:
        ordering = ['title']


class Product(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    unit_price = models.DecimalField(max_digits=6,decimal_places=2 ,validators=[MinValueValidator(1)])
    collection = models.ForeignKey(Collection, on_delete=models.PROTECT, related_name='products')

    def __str__(self) -> str:
        return self.title

    class Meta:
        ordering = ['title']


class Customer(models.Model):
    #first_name = models.CharField(max_length=255 , default = 'DEFAULT VALUE')
    #last_name = models.CharField(max_length=255 ,  default = 'DEFAULT VALUE')
    phone = models.CharField(max_length=255 , default = 'DEFAULT VALUE')
    email = models.EmailField(unique=True ,  default = 'DEFAULT VALUE')
    user = models.OneToOneField(settings.AUTH_USER_MODEL , on_delete = models.CASCADE)


    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'

    @admin.display(ordering='user__first__name')
    def first_name(self):
        return self.user.first_name

    @admin.display(ordering='user__last__name')
    def last_name(self):
        return self.user.last_name

    class Meta:
        ordering = ['user__first_name' , 'user__last_name']


class Order(models.Model):
    PAYMENT_STATUS_PENDING = 'P'
    PAYMENT_STATUS_COMPLETE = 'C'
    PAYMENT_STATUS_FAILED = 'F'
    PAYMENT_STATUS_CHOICES = [
        (PAYMENT_STATUS_PENDING, 'Pending'),
        (PAYMENT_STATUS_COMPLETE, 'Complete'),
        (PAYMENT_STATUS_FAILED, 'Failed')]

    placed_at = models.DateTimeField(auto_now_add=True , null = True)
    payment_status = models.CharField(max_length=1 , choices=PAYMENT_STATUS_CHOICES , default=PAYMENT_STATUS_PENDING)
    customer = models.ForeignKey(Customer , on_delete = models.PROTECT)

    '''class Meta:
        permission = [
            ('cancel_order' , 'Can cancel order')
        ]'''

class OrderItem(models.Model):
    order = models.ForeignKey(Order , on_delete=models.PROTECT , related_name='items')
    name = models.CharField(max_length=255)
    unit_price = models.DecimalField(max_digits=6 , decimal_places=2)

class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    name = models.CharField(max_length=255)
    description = models.TextField()
    date = models.DateField(auto_now_add=True)


class Cart(models.Model):
    id = models.UUIDField(primary_key= True , default= uuid4)
    created_at = models.DateTimeField(auto_now_add=True)

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(validators=[MinValueValidator(1)])

    class Meta:
        unique_together = [['cart', 'product']]
