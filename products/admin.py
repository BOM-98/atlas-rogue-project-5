from django.contrib import admin
from .models import Product, Category


class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "sku",
        "name",
        "designer",
        "price",
        "rrp",
        "size",
        "colour",
        "length",
        "image_url",
        "image",
    )
    ordering = ("name",)

class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        "friendly_name",
        "name",
    )

# Register your models here.
admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)