from django.contrib import admin
from .models import Customer, Product, Order


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    class Meta:
        model = Customer


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    class Meta:
        model = Product


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    class Meta:
        model = Order
