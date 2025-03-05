from django.contrib import admin

from home.models import (  # noqa E501
    CartItem,
    Category,
    CustomerQuestion,
    Ordered,
    Products,
)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(Products)
class ProductsAdmin(admin.ModelAdmin):
    prepopulated_fields = {
        "slug": ('name',)
    }


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    search_fields = 'id', 'quantity',


@admin.register(Ordered)
class OrderedAdmin(admin.ModelAdmin):
    autocomplete_fields = 'products',


@admin.register(CustomerQuestion)
class CustomerQuestionAdmin(admin.ModelAdmin):
    pass
