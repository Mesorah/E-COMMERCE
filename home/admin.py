from django.contrib import admin

from home.models import Cart, CartItem, CustomerQuestion, Ordered, Products


@admin.register(Products)
class ProductsAdmin(admin.ModelAdmin):
    pass


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    pass


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    pass


@admin.register(Ordered)
class OrderedAdmin(admin.ModelAdmin):
    pass


@admin.register(CustomerQuestion)
class CustomerQuestionAdmin(admin.ModelAdmin):
    pass
