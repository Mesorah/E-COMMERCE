from django.contrib import admin
from home.models import Products


@admin.register(Products)
class ProductsAdmin(admin.ModelAdmin):
    pass
