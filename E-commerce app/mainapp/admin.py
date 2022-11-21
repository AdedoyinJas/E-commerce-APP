from django.contrib import admin
#from .models import Product , Customer , Order , Collection , 
from . import models
from django.contrib.contenttypes.admin import GenericTabularInline



@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title' , 'unit_price' , 'collection_title']
    list_ediitable = ['unit_price']
    list_filter = ['collection']
    list_per_page = 10

    def collection_title(self , product):
        return product.collection.title


@admin.register(models.Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ['title' , 'products_count']
    search_fields = ['title']

    @admin.display(ordering='products_count')
    def products_count(self , collection):
        return collection.products_count

    def get_queryet(self , request):
        return super().get_queryset(request).annotate(products_count=Count('product'))

@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name' , 'email' ]
    list_select_related = ['user']
    ordering = ['user__first_name' , 'user__last_name']


@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id' , 'placed_at' , 'customer']