from django.contrib import admin
from .models import Product, Sales

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'model', 'quantity', 'selling_price', 'category', 'user')
    search_fields = ('name', 'model', 'description')
    list_filter = ('category', 'user')

class SalesAdmin(admin.ModelAdmin):
    list_display = ('product', 'customer', 'quantity', 'total', 'status', 'date', 'user')
    search_fields = ('product__name', 'customer__name')
    list_filter = ('status', 'payment_mode', 'date', 'user')

admin.site.register(Product, ProductAdmin)
admin.site.register(Sales, SalesAdmin)
