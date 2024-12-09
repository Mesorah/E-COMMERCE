from django.contrib import admin
from home.models import Products, Cart


@admin.register(Products)
class ProductsAdmin(admin.ModelAdmin):
    pass


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    pass


# @admin.register(CartItem)
# class CartItemAdmin(admin.ModelAdmin):
#     pass
