from django.contrib import admin
from mainapp.admin import ProductAdmin
from likes.models import LikedItem
from mainapp.models import Product
from django.contrib.contenttypes.admin import GenericTabularInline
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    add_fieldsets = ((None, {'classes': ('wide',),'fields': ('username', 'password1', 'password2', 'email', 'first_name', 'last_name'),}),)


class LikeInline(GenericTabularInline):
    autocomplete_fields = ['like']
    model = LikedItem


class CustomProductAdmin(ProductAdmin):
    inlines = [LikeInline]


'''admin.site.unregister(Product)
admin.site.register(Product , CustomProductAdmin)'''